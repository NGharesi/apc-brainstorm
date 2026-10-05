function results = score_apc_sleepedf_expected_modes(summaryCsv)
% SCORE_APC_SLEEPEDF_EXPECTED_MODES
% Quantify agreement between Sleep-EDF APC results and physiology-guided
% expected ranges for slow oscillations and spindle carriers.
%
% This is not a true labeled-ground-truth benchmark. Instead, it scores
% whether the recovered dominant APC mode falls into expected literature-
% guided ranges:
%   - slow phase carrier: 0.5 to 1.25 Hz
%   - frontal channel (Fpz-Cz): spindle carrier 9 to 12 Hz
%   - posterior channel (Pz-Oz): spindle carrier 12 to 16 Hz
%
% USAGE:
%   results = score_apc_sleepedf_expected_modes
%   results = score_apc_sleepedf_expected_modes( ...
%       'C:\Users\nghare\.brainstorm\process\apc_sleepedf_batch_summary.csv')

    if nargin < 1 || isempty(summaryCsv)
        summaryCsv = fullfile(fileparts(mfilename('fullpath')), 'apc_sleepedf_batch_summary.csv');
    end

    if ~exist(summaryCsv, 'file')
        error('Summary CSV not found: %s', summaryCsv);
    end

    T = readtable(summaryCsv);
    T.stage = string(T.stage);
    T.channel = string(T.channel);
    T.subject_id = string(T.subject_id);

    valid = T.status_code == 0 & isfinite(T.phase_frequency_hz) & isfinite(T.amplitude_frequency_hz) & ...
        isfinite(T.pac_strength) & T.duration_s > 0 & T.n_phase_events > 0 & T.n_bursts > 0;
    T = T(valid, :);

    T.fP_expected = T.phase_frequency_hz >= 0.5 & T.phase_frequency_hz <= 1.25;
    T.fA_expected = false(height(T), 1);

    isFrontal = T.channel == "EEGFpz_Cz";
    isPosterior = T.channel == "EEGPz_Oz";

    T.fA_expected(isFrontal) = T.amplitude_frequency_hz(isFrontal) >= 9 & T.amplitude_frequency_hz(isFrontal) <= 12;
    T.fA_expected(isPosterior) = T.amplitude_frequency_hz(isPosterior) >= 12 & T.amplitude_frequency_hz(isPosterior) <= 16;
    T.joint_expected = T.fP_expected & T.fA_expected;

    stages = ["N2","N3","N2N3"];
    channels = ["EEGFpz_Cz","EEGPz_Oz"];
    rows = cell(0, 10);

    for iChan = 1:numel(channels)
        for iStage = 1:numel(stages)
            idx = T.channel == channels(iChan) & T.stage == stages(iStage);
            sub = T(idx, :);
            if isempty(sub)
                continue;
            end

            rows(end+1, :) = { ...
                channels(iChan), ...
                stages(iStage), ...
                numel(unique(sub.subject_id)), ...
                mean(sub.fP_expected) * 100, ...
                mean(sub.fA_expected) * 100, ...
                mean(sub.joint_expected) * 100, ...
                median(sub.phase_frequency_hz, 'omitnan'), ...
                median(sub.amplitude_frequency_hz, 'omitnan'), ...
                median(sub.pac_strength, 'omitnan'), ...
                median(sub.n_bursts, 'omitnan')}; %#ok<AGROW>
        end
    end

    scoreTable = cell2table(rows, 'VariableNames', ...
        {'channel','stage','n_subjects','fP_in_expected_pct','fA_in_expected_pct', ...
         'joint_in_expected_pct','fP_median_hz','fA_median_hz','pac_median','n_bursts_median'});

    outDir = fileparts(mfilename('fullpath'));
    outCsv = fullfile(outDir, 'apc_sleepedf_expected_mode_scores.csv');
    writetable(scoreTable, outCsv);

    results = struct();
    results.summary_csv = summaryCsv;
    results.score_table = scoreTable;
    results.csv_file = outCsv;

    fprintf('Saved Sleep-EDF expected-mode agreement table:\n');
    fprintf('  %s\n', outCsv);
    disp(scoreTable);
end
