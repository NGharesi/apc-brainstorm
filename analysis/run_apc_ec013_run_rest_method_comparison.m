function results = run_apc_ec013_run_rest_method_comparison(resultsFile)
% RUN_APC_EC013_RUN_REST_METHOD_COMPARISON
% Compare APC against scanned PAC estimators on the exact same EC013 run
% and rest bouts used in the proof-of-principle rodent LFP analysis.
%
% USAGE:
%   results = run_apc_ec013_run_rest_method_comparison
%   results = run_apc_ec013_run_rest_method_comparison(resultsFile)
%
% INPUT:
%   resultsFile : MAT file created by run_apc_ec013_run_rest
%
% OUTPUT FILES:
%   apc_ec013_run_rest_method_comparison_results.mat
%   apc_ec013_run_rest_method_comparison_bouts.csv
%   apc_ec013_run_rest_method_comparison_summary.csv
%   apc_ec013_run_rest_method_comparison_variability.csv
%
% NOTES:
%   - APC is taken from the existing run_apc_ec013_run_rest output so the
%     primary analysis remains unchanged.
%   - Conventional PAC estimators are scanned over the same run/rest bouts:
%       MVL-scan  : Canolty mean-vector-length PAC
%       KLMI-scan : Tort Kullback-Leibler modulation index
%       GLM-scan  : sinusoid-regression PAC score
%   - A surrogate z-score is computed for every method on every bout by
%     circularly shifting the amplitude envelope relative to the phase
%     series while holding the recovered (fP, fA) pair fixed.

    if nargin < 1 || isempty(resultsFile)
        resultsFile = fullfile(fileparts(mfilename('fullpath')), 'apc_ec013_run_rest_results.mat');
    end

    if ~exist(resultsFile, 'file')
        error('Run/rest APC results MAT file not found: %s', resultsFile);
    end

    S = load(resultsFile, 'results');
    if ~isfield(S, 'results')
        error('MAT file does not contain a results struct: %s', resultsFile);
    end
    base = S.results;

    [signalWin, timeWin] = local_get_signal_window(base);
    fs = 1 / median(diff(timeWin));

    cfg = local_get_config(fs);
    rowStruct = repmat(local_empty_row(), 0, 1);

    stateNames = {'run', 'rest'};
    for iState = 1:numel(stateNames)
        stateName = stateNames{iState};
        bouts = base.(stateName).bouts;
        apcTbl = base.(stateName).summary_table;

        for iBout = 1:height(bouts)
            idx = bouts.start_idx(iBout):bouts.stop_idx(iBout);
            boutSignal = double(signalWin(idx));
            boutTime = double(timeWin(idx));

            apcItem = local_unpack_apc_row(apcTbl(iBout, :));
            apcItem.metric_name = "canolty";
            apcItem.method = "APC";
            apcItem = local_add_surrogate_stats(apcItem, boutSignal, fs, cfg);
            rowStruct(end + 1, 1) = local_pack_row(stateName, iBout, bouts.duration_s(iBout), apcItem); %#ok<AGROW>

            mvlItem = local_scan_standard_pac(boutSignal, fs, cfg, 'canolty');
            mvlItem.method = "MVL-scan";
            mvlItem.metric_name = "canolty";
            mvlItem = local_add_surrogate_stats(mvlItem, boutSignal, fs, cfg);
            rowStruct(end + 1, 1) = local_pack_row(stateName, iBout, bouts.duration_s(iBout), mvlItem); %#ok<AGROW>

            klmiItem = local_scan_standard_pac(boutSignal, fs, cfg, 'tort');
            klmiItem.method = "KLMI-scan";
            klmiItem.metric_name = "tort";
            klmiItem = local_add_surrogate_stats(klmiItem, boutSignal, fs, cfg);
            rowStruct(end + 1, 1) = local_pack_row(stateName, iBout, bouts.duration_s(iBout), klmiItem); %#ok<AGROW>

            glmItem = local_scan_standard_pac(boutSignal, fs, cfg, 'glm');
            glmItem.method = "GLM-scan";
            glmItem.metric_name = "glm";
            glmItem = local_add_surrogate_stats(glmItem, boutSignal, fs, cfg);
            rowStruct(end + 1, 1) = local_pack_row(stateName, iBout, bouts.duration_s(iBout), glmItem); %#ok<AGROW>
        end
    end

    boutTable = struct2table(rowStruct);
    summaryTable = local_build_summary_table(boutTable);
    variabilityTable = local_build_variability_table(boutTable);

    outDir = fileparts(mfilename('fullpath'));
    outMat = fullfile(outDir, 'apc_ec013_run_rest_method_comparison_results.mat');
    outBoutCsv = fullfile(outDir, 'apc_ec013_run_rest_method_comparison_bouts.csv');
    outSummaryCsv = fullfile(outDir, 'apc_ec013_run_rest_method_comparison_summary.csv');
    outVarCsv = fullfile(outDir, 'apc_ec013_run_rest_method_comparison_variability.csv');

    results = struct();
    results.base_results_file = resultsFile;
    results.config = cfg;
    results.bout_table = boutTable;
    results.summary_table = summaryTable;
    results.variability_table = variabilityTable;
    results.output_mat = outMat;
    results.output_bout_csv = outBoutCsv;
    results.output_summary_csv = outSummaryCsv;
    results.output_variability_csv = outVarCsv;

    save(outMat, 'results', '-v7.3');
    writetable(boutTable, outBoutCsv);
    writetable(summaryTable, outSummaryCsv);
    writetable(variabilityTable, outVarCsv);

    fprintf('\nSaved EC013 run/rest method-comparison outputs:\n');
    fprintf('  %s\n', outMat);
    fprintf('  %s\n', outBoutCsv);
    fprintf('  %s\n', outSummaryCsv);
    fprintf('  %s\n', outVarCsv);
end


function cfg = local_get_config(fs)
    cfg = struct();
    cfg.fs_hz = fs;
    cfg.phase_scan_hz = 4:0.5:12;
    cfg.amplitude_scan_hz = 80:4:150;
    cfg.phase_band_half_width_hz = 1.5;
    cfg.amplitude_band_half_width_hz = 6.0;
    cfg.n_phase_bins = 18;
    cfg.n_surrogates = 100;
    cfg.min_shift_fraction = 0.10;
    cfg.max_shift_fraction = 0.90;
end


function row = local_empty_row()
    row = struct( ...
        'state', "", ...
        'bout_index', NaN, ...
        'duration_s', NaN, ...
        'method', "", ...
        'metric_name', "", ...
        'valid', NaN, ...
        'status_code', NaN, ...
        'phase_frequency_hz', NaN, ...
        'amplitude_frequency_hz', NaN, ...
        'preferred_phase_deg', NaN, ...
        'score_raw', NaN, ...
        'score_z', NaN, ...
        'score_percentile', NaN, ...
        'null_mean', NaN, ...
        'null_std', NaN);
end


function row = local_pack_row(stateName, boutIdx, durationS, item)
    row = local_empty_row();
    row.state = string(stateName);
    row.bout_index = boutIdx;
    row.duration_s = durationS;
    row.method = string(item.method);
    row.metric_name = string(item.metric_name);
    row.valid = item.valid;
    row.status_code = item.status_code;
    row.phase_frequency_hz = item.fp_hz;
    row.amplitude_frequency_hz = item.fa_hz;
    row.preferred_phase_deg = item.preferred_phase_deg;
    row.score_raw = item.score;
    row.score_z = item.score_z;
    row.score_percentile = item.score_percentile;
    row.null_mean = item.null_mean;
    row.null_std = item.null_std;
end


function item = local_unpack_apc_row(tblRow)
    item = struct();
    item.valid = double(tblRow.status_code(1) == 0);
    item.status_code = double(tblRow.status_code(1));
    item.fp_hz = double(tblRow.phase_frequency_hz(1));
    item.fa_hz = double(tblRow.amplitude_frequency_hz(1));
    item.preferred_phase_deg = double(tblRow.preferred_phase_deg(1));
    item.score = double(tblRow.pac_strength(1));

    if ~item.valid
        item.fp_hz = NaN;
        item.fa_hz = NaN;
        item.preferred_phase_deg = NaN;
        item.score = NaN;
    end
end


function item = local_scan_standard_pac(signal, fs, cfg, metricName)
    fpCandidates = cfg.phase_scan_hz(:).';
    faCandidates = cfg.amplitude_scan_hz(:).';

    lowPhase = cell(size(fpCandidates));
    for iFp = 1:numel(fpCandidates)
        band = [max(0.5, fpCandidates(iFp) - cfg.phase_band_half_width_hz), ...
            fpCandidates(iFp) + cfg.phase_band_half_width_hz];
        lowSig = local_bandpass(signal, fs, band(1), band(2));
        lowPhase{iFp} = angle(hilbert(lowSig(:)));
    end

    highEnv = cell(size(faCandidates));
    for iFa = 1:numel(faCandidates)
        band = [max(1.0, faCandidates(iFa) - cfg.amplitude_band_half_width_hz), ...
            min(fs / 2 - 1.0, faCandidates(iFa) + cfg.amplitude_band_half_width_hz)];
        highSig = local_bandpass(signal, fs, band(1), band(2));
        highEnv{iFa} = abs(hilbert(highSig(:)));
    end

    scoreMap = nan(numel(fpCandidates), numel(faCandidates));
    prefMap = nan(numel(fpCandidates), numel(faCandidates));
    for iFp = 1:numel(fpCandidates)
        phaseAngles = lowPhase{iFp};
        for iFa = 1:numel(faCandidates)
            ampEnv = highEnv{iFa};
            [scoreVal, prefDeg] = local_metric_value(phaseAngles, ampEnv, metricName, cfg.n_phase_bins);
            scoreMap(iFp, iFa) = scoreVal;
            prefMap(iFp, iFa) = prefDeg;
        end
    end

    [bestScore, idx] = max(scoreMap(:), [], 'omitnan');
    item = struct();
    item.valid = isfinite(bestScore);
    item.status_code = double(~item.valid);
    item.fp_hz = NaN;
    item.fa_hz = NaN;
    item.preferred_phase_deg = NaN;
    item.score = NaN;

    if item.valid
        [iFpBest, iFaBest] = ind2sub(size(scoreMap), idx);
        item.fp_hz = fpCandidates(iFpBest);
        item.fa_hz = faCandidates(iFaBest);
        item.preferred_phase_deg = prefMap(iFpBest, iFaBest);
        item.score = bestScore;
    end
end


function item = local_add_surrogate_stats(item, signal, fs, cfg)
    item.score_z = NaN;
    item.score_percentile = NaN;
    item.null_mean = NaN;
    item.null_std = NaN;

    if ~item.valid || ~isfinite(item.fp_hz) || ~isfinite(item.fa_hz)
        return;
    end

    lowBand = [max(0.5, item.fp_hz - cfg.phase_band_half_width_hz), ...
        item.fp_hz + cfg.phase_band_half_width_hz];
    highBand = [max(1.0, item.fa_hz - cfg.amplitude_band_half_width_hz), ...
        min(fs / 2 - 1.0, item.fa_hz + cfg.amplitude_band_half_width_hz)];

    lowSig = local_bandpass(signal, fs, lowBand(1), lowBand(2));
    highSig = local_bandpass(signal, fs, highBand(1), highBand(2));
    phaseAngles = angle(hilbert(lowSig(:)));
    ampEnv = abs(hilbert(highSig(:)));

    [obsScore, ~] = local_metric_value(phaseAngles, ampEnv, char(item.metric_name), cfg.n_phase_bins);
    nullScores = nan(cfg.n_surrogates, 1);
    nSamp = numel(ampEnv);
    minShift = max(1, round(cfg.min_shift_fraction * nSamp));
    maxShift = max(minShift + 1, round(cfg.max_shift_fraction * nSamp));

    for iPerm = 1:cfg.n_surrogates
        shift = randi([minShift, maxShift], 1, 1);
        envShift = circshift(ampEnv, shift);
        nullScores(iPerm) = local_metric_value(phaseAngles, envShift, char(item.metric_name), cfg.n_phase_bins);
    end

    item.null_mean = mean(nullScores, 'omitnan');
    item.null_std = std(nullScores, 0, 'omitnan');
    if isfinite(item.null_std) && item.null_std > 0
        item.score_z = (obsScore - item.null_mean) ./ item.null_std;
    end
    item.score_percentile = mean(obsScore > nullScores, 'omitnan');
    item.score = obsScore;
end


function [scoreVal, prefDeg] = local_metric_value(phaseAngles, ampEnv, metricName, nPhaseBins)
    switch lower(metricName)
        case 'glm'
            [scoreVal, prefDeg] = local_glm_pac_metric(phaseAngles, ampEnv);
        otherwise
            [scoreVal, prefDeg] = calc_MI_all_methods(phaseAngles, ampEnv, metricName, false, 0, 1, false, nPhaseBins);
    end
end


function [score, prefDeg] = local_glm_pac_metric(phaseAngles, ampEnv)
    phaseAngles = double(phaseAngles(:));
    ampEnv = double(ampEnv(:));
    X = [ones(size(phaseAngles)), sin(phaseAngles), cos(phaseAngles)];
    beta = X \ ampEnv;
    yhat = X * beta;

    ssRes = sum((ampEnv - yhat) .^ 2);
    ssTot = sum((ampEnv - mean(ampEnv)) .^ 2);
    if ssTot <= 0
        score = 0;
    else
        score = max(0, 1 - ssRes / ssTot);
    end
    prefDeg = rad2deg(atan2(beta(2), beta(3)));
end


function x = local_bandpass(signal, fs, lowHz, highHz)
    wn = [lowHz, highHz] ./ (fs / 2);
    wn(1) = max(wn(1), 1e-4);
    wn(2) = min(wn(2), 0.999);
    if wn(2) <= wn(1)
        x = zeros(size(signal));
        return;
    end
    [b, a] = butter(4, wn, 'bandpass');
    x = filtfilt(b, a, double(signal(:)));
end


function summaryTable = local_build_summary_table(boutTable)
    methods = unique(boutTable.method, 'stable');
    states = unique(boutTable.state, 'stable');
    rows = cell(0, 18);

    for iMethod = 1:numel(methods)
        for iState = 1:numel(states)
            sub = boutTable(boutTable.method == methods(iMethod) & boutTable.state == states(iState), :);
            valid = sub(sub.valid == 1, :);

            rows(end + 1, :) = { ...
                string(methods(iMethod)), ...
                string(states(iState)), ...
                height(sub), ...
                height(valid), ...
                mean(valid.duration_s, 'omitnan'), ...
                median(valid.duration_s, 'omitnan'), ...
                mean(valid.score_raw, 'omitnan'), ...
                median(valid.score_raw, 'omitnan'), ...
                mean(valid.score_z, 'omitnan'), ...
                median(valid.score_z, 'omitnan'), ...
                mean(valid.score_percentile, 'omitnan'), ...
                median(valid.score_percentile, 'omitnan'), ...
                mean(valid.phase_frequency_hz, 'omitnan'), ...
                median(valid.phase_frequency_hz, 'omitnan'), ...
                mean(valid.amplitude_frequency_hz, 'omitnan'), ...
                median(valid.amplitude_frequency_hz, 'omitnan'), ...
                iqr(valid.phase_frequency_hz), ...
                iqr(valid.amplitude_frequency_hz)}; %#ok<AGROW>
        end
    end

    summaryTable = cell2table(rows, 'VariableNames', { ...
        'method', 'state', 'n_bouts', 'n_valid', ...
        'duration_mean_s', 'duration_median_s', ...
        'score_raw_mean', 'score_raw_median', ...
        'score_z_mean', 'score_z_median', ...
        'score_percentile_mean', 'score_percentile_median', ...
        'fp_mean_hz', 'fp_median_hz', ...
        'fa_mean_hz', 'fa_median_hz', ...
        'fp_iqr_hz', 'fa_iqr_hz'});
end


function variabilityTable = local_build_variability_table(boutTable)
    methods = unique(boutTable.method, 'stable');
    states = unique(boutTable.state, 'stable');
    rows = cell(0, 10);

    for iMethod = 1:numel(methods)
        for iState = 1:numel(states)
            sub = boutTable(boutTable.method == methods(iMethod) & boutTable.state == states(iState) & boutTable.valid == 1, :);
            fpVals = sub.phase_frequency_hz;
            faVals = sub.amplitude_frequency_hz;
            zVals = sub.score_z;

            rows(end + 1, :) = { ...
                string(methods(iMethod)), ...
                string(states(iState)), ...
                height(sub), ...
                std(fpVals, 0, 'omitnan'), ...
                iqr(fpVals), ...
                mad(fpVals, 1), ...
                std(faVals, 0, 'omitnan'), ...
                iqr(faVals), ...
                mad(faVals, 1), ...
                median(zVals, 'omitnan')}; %#ok<AGROW>
        end
    end

    variabilityTable = cell2table(rows, 'VariableNames', { ...
        'method', 'state', 'n_valid', ...
        'fp_std_hz', 'fp_iqr_hz', 'fp_mad_hz', ...
        'fa_std_hz', 'fa_iqr_hz', 'fa_mad_hz', ...
        'score_z_median'});
end


function [signalWin, timeWin] = local_get_signal_window(results)
    if isfield(results, 'signal_window') && isfield(results, 'signal_time')
        signalWin = double(results.signal_window(:).');
        timeWin = double(results.signal_time(:).');
        return;
    end

    dataFile = results.input_file;
    recName = results.recording;
    D = load(dataFile, recName);
    rec = D.(recName);
    idx = results.analysis_idx(1):results.analysis_idx(2);
    signalWin = double(rec.Value(idx));
    timeWin = double(rec.Time(idx));
end
