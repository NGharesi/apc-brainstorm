function results = run_apc_sleepedf_wideband_mixed_models()
% RUN_APC_SLEEPEDF_WIDEBAND_MIXED_MODELS
% Fit prespecified repeated-night models for the Sleep-EDF wideband APC
% quality-control analysis. Valid APC score and fP observations are modeled
% as outcome ~ channel * stage + (1|participant) + (1|recording).
%
% fA is intentionally excluded: its high boundary-hit rate invalidates a
% physiological carrier-frequency interpretation. This runner uses only
% completed signal-level output; it does not recompute APC or surrogates.
%
% OUTPUTS:
%   apc_sleepedf_wideband_mixed_model_coefficients.csv
%   apc_sleepedf_wideband_mixed_model_counts.csv
%   apc_sleepedf_wideband_mixed_model_summary.txt
%   apc_sleepedf_wideband_mixed_models.mat

    baseDir = fileparts(mfilename('fullpath'));
    source = fullfile(baseDir, 'apc_sleepedf_coupling_validation_wideband_signal_level.csv');
    raw = readtable(source, 'TextType', 'string');
    valid = raw(raw.apc_status == 0, :);
    valid.participant_id = categorical(valid.participant_id);
    valid.recording_id = categorical(valid.recording_id);
    valid.channel = categorical(valid.channel, {'EEGFpz_Cz', 'EEGPz_Oz'});
    valid.stage = categorical(valid.stage, {'N2', 'N3'});

    % Retain complete cases only for each outcome, never silently impute.
    outcomes = {'apc_score_z', 'apc_fp_hz'};
    coefficientTables = cell(numel(outcomes), 1);
    modelInfo = struct();
    for iOutcome = 1:numel(outcomes)
        outcome = outcomes{iOutcome};
        sub = valid(isfinite(valid.(outcome)), :);
        formula = sprintf('%s ~ channel * stage + (1|participant_id) + (1|recording_id)', outcome);
        model = fitlme(sub, formula, 'FitMethod', 'REML');
        modelInfo.(outcome) = model;
        coefficientTables{iOutcome} = local_coefficient_table(model, outcome, sub, false);

        % Outcome-standardized estimates provide an effect-size scale while
        % retaining the raw-unit model as the primary reported analysis.
        sub.standardized_outcome = (sub.(outcome) - mean(sub.(outcome))) ./ std(sub.(outcome));
        standardized = fitlme(sub, 'standardized_outcome ~ channel * stage + (1|participant_id) + (1|recording_id)', 'FitMethod', 'REML');
        standardizedTable = local_coefficient_table(standardized, outcome, sub, true);
        coefficientTables{iOutcome} = outerjoin(coefficientTables{iOutcome}, standardizedTable, ...
            'Keys', {'outcome','term'}, 'MergeKeys', true, 'Type', 'left');
    end
    coefficients = vertcat(coefficientTables{:});

    counts = local_counts(raw, valid);
    coefficientFile = fullfile(baseDir, 'apc_sleepedf_wideband_mixed_model_coefficients.csv');
    countFile = fullfile(baseDir, 'apc_sleepedf_wideband_mixed_model_counts.csv');
    summaryFile = fullfile(baseDir, 'apc_sleepedf_wideband_mixed_model_summary.txt');
    matFile = fullfile(baseDir, 'apc_sleepedf_wideband_mixed_models.mat');
    writetable(coefficients, coefficientFile);
    writetable(counts, countFile);
    local_write_summary(summaryFile, coefficients, counts);
    save(matFile, 'modelInfo', 'coefficients', 'counts', 'raw', 'valid', '-v7.3');

    fprintf('Saved mixed-effects outputs:\n  %s\n  %s\n  %s\n  %s\n', coefficientFile, countFile, summaryFile, matFile);
    results = struct('models', modelInfo, 'coefficients', coefficients, 'counts', counts, ...
        'coefficient_file', coefficientFile, 'count_file', countFile, 'summary_file', summaryFile, 'mat_file', matFile);
end

function output = local_coefficient_table(model, outcome, sub, standardized)
    coefficients = model.Coefficients;
    confidence = coefCI(model, 'Alpha', 0.05);
    nCoefficients = size(coefficients, 1);
    if istable(coefficients)
        variableNames = coefficients.Properties.VariableNames;
    else
        % MATLAB R2022b can expose mixed-model coefficients as a dataset.
        variableNames = coefficients.Properties.VarNames;
    end
    if ismember('DF', variableNames)
        df = coefficients.DF;
    else
        df = nan(nCoefficients, 1);
    end
    prefix = 'estimate';
    if standardized, prefix = 'standardized_estimate'; end
    output = table(repmat(string(outcome), nCoefficients, 1), string(coefficients.Name), ...
        coefficients.Estimate, confidence(:,1), confidence(:,2), coefficients.SE, coefficients.tStat, df, coefficients.pValue, ...
        repmat(height(sub), nCoefficients, 1), repmat(numel(categories(sub.participant_id)), nCoefficients, 1), ...
        repmat(numel(categories(sub.recording_id)), nCoefficients, 1), ...
        'VariableNames', {'outcome','term',prefix,[prefix '_ci_low'],[prefix '_ci_high'],[prefix '_se'],'t_statistic','df','p_value','n_rows','n_participants','n_recordings'});
    if standardized
        output = output(:, {'outcome','term',prefix,[prefix '_ci_low'],[prefix '_ci_high']});
    end
end

function counts = local_counts(raw, valid)
    [groups, channel, stage] = findgroups(valid.channel, valid.stage);
    rows = strings(max(groups), 1);
    recordings = zeros(max(groups), 1); participants = zeros(max(groups), 1); validRows = zeros(max(groups), 1);
    for k = 1:max(groups)
        index = groups == k;
        rows(k) = string(channel(k)) + "_" + string(stage(k));
        recordings(k) = numel(unique(valid.recording_id(index)));
        participants(k) = numel(unique(valid.participant_id(index)));
        validRows(k) = sum(index);
    end
    base = table(rows, recordings, participants, validRows, zeros(height(rows),1), zeros(height(rows),1), ...
        'VariableNames', {'channel_stage','n_recordings','n_participants','n_valid_rows','n_one_night_participants','n_two_night_participants'});
    pairs = unique(raw(:, {'participant_id','recording_id'}));
    group = findgroups(pairs.participant_id);
    nightsPerParticipant = splitapply(@numel, pairs.recording_id, group);
    mapping = table("participant_night_mapping", height(pairs), numel(unique(pairs.participant_id)), ...
        NaN, sum(nightsPerParticipant == 1), sum(nightsPerParticipant == 2), ...
        'VariableNames', {'channel_stage','n_recordings','n_participants','n_valid_rows','n_one_night_participants','n_two_night_participants'});
    counts = [base; mapping];
end

function local_write_summary(fileName, coefficients, counts)
    fid = fopen(fileName, 'w'); cleanup = onCleanup(@() fclose(fid));
    fprintf(fid, 'Sleep-EDF shared-wideband mixed-effects analysis\n');
    fprintf(fid, 'Model: outcome ~ channel * stage + (1|participant_id) + (1|recording_id), REML.\n');
    fprintf(fid, 'Outcomes: APC surrogate-normalized score and slow-carrier fP only. fA is excluded because boundary-hit quality control failed.\n');
    fprintf(fid, 'Reference levels: channel EEGFpz_Cz; stage N2.\n\n');
    fprintf(fid, '%s\n', evalc('disp(counts)'));
    fprintf(fid, '%s\n', evalc('disp(coefficients)'));
end
