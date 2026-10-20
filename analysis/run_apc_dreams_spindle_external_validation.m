function results = run_apc_dreams_spindle_external_validation(profile)
% RUN_APC_DREAMS_SPINDLE_EXTERNAL_VALIDATION  All-window, annotation-blinded test.
%
% Every 30-s window in DREAMS excerpts 1-6 is analyzed. Expert scorer-2
% annotations are used only after APC/PAC frequency selection. The sigma
% range is an outcome definition (11-16 Hz), never an input search range.

    if nargin < 1 || isempty(profile), profile = 'original'; end
    rng(20261013, 'twister');
    cfg = local_config(profile);
    rows = repmat(local_empty_row(), 0, 1);
    for excerpt = 1:6
        [x, fs, annotations] = local_load_excerpt(excerpt, cfg);
        starts = 0:cfg.window_s:(floor(numel(x) / fs / cfg.window_s) * cfg.window_s - cfg.window_s);
        if strcmp(cfg.profile, 'hybrid_smoke'), starts = starts(1); end
        for iWindow = 1:numel(starts)
            startTime = starts(iWindow);
            i0 = round(startTime * fs) + 1;
            i1 = i0 + round(cfg.window_s * fs) - 1;
            rows(end + 1, 1) = local_window(x(i0:i1), fs, excerpt, iWindow, startTime, annotations, cfg); %#ok<AGROW>
        end
        fprintf('[%d/6] excerpt %d: %d windows\n', excerpt, excerpt, numel(starts));
    end
    windows = struct2table(rows);
    excerptSummary = local_excerpt_summary(windows, cfg);
    inference = local_paired_inference(excerptSummary, cfg);
    files = local_write(windows, excerptSummary, inference, cfg);
    results = struct('config', cfg, 'windows', windows, 'excerpt_summary', excerptSummary, ...
        'inference', inference, 'files', files, ...
        'interpretation', ['External validation of frequency selection and event alignment against blinded expert annotations. ' ...
        'This is not a calibrated APC detection-threshold analysis.']);
    save(files.mat, 'results', '-v7.3');
    local_plot(excerptSummary, files.figure);
    local_write_summary(results, files.summary);
end

function cfg = local_config(profile)
    cfg.profile = lower(char(profile));
    if ~ismember(cfg.profile, {'original', 'hybrid', 'hybrid_smoke'})
        error('Use profile original, hybrid, or hybrid_smoke.');
    end
    cfg.useHybrid = startsWith(cfg.profile, 'hybrid');
    cfg.root = 'D:\APC_project\RealDatasets\DREAMS_Spindles\extracted';
    cfg.window_s = 30;
    cfg.amplitudeRangeHz = [4 30];
    cfg.phaseGridHz = .5:.5:4;
    cfg.amplitudeGridHz = 4:2:30;
    cfg.sigmaOutcomeHz = [11 16];
    cfg.peakProminenceZ = 1;
    cfg.minPeakSpacingS = .5;
    cfg.nShiftNull = 200;
    cfg.apcOptions = struct('fA', cfg.amplitudeRangeHz, 'epoch', [-1 1], ...
        'decomposition', 'fft_peak', 'metric', 'canolty', 'diagm', false, ...
        'surrogates', false, 'num_perm', 0, 'numPhaseBins', 18, ...
        'amplitudeBandWidthHz', 4);
end

function [x, fs, annotations] = local_load_excerpt(excerpt, cfg)
    x = readmatrix(fullfile(cfg.root, sprintf('excerpt%d.txt', excerpt)), 'FileType', 'text', 'NumHeaderLines', 1);
    x = x(isfinite(x));
    fs = local_legacy_edf_rate(fullfile(cfg.root, sprintf('excerpt%d.edf', excerpt)));
    x = x(1:fs * 30 * 60);
    annotations = readmatrix(fullfile(cfg.root, sprintf('Visual_scoring2_excerpt%d.txt', excerpt)), 'FileType', 'text', 'NumHeaderLines', 1);
    annotations = annotations(all(isfinite(annotations), 2), 1:2);
end

function fs = local_legacy_edf_rate(edfFile)
    fid = fopen(edfFile, 'r');
    if fid < 0, error('Could not open %s.', edfFile); end
    cleaner = onCleanup(@() fclose(fid)); %#ok<NASGU>
    header = char(fread(fid, 256, '*char')');
    duration = str2double(strtrim(header(245:252)));
    nSignals = str2double(strtrim(header(253:256)));
    fseek(fid, 256 + 216 * nSignals, 'bof');
    fs = str2double(strtrim(char(fread(fid, 8, '*char')))) ./ duration;
    if ~isfinite(fs) || fs <= 0 || fs ~= round(fs)
        error('Invalid sampling rate in %s.', edfFile);
    end
end

function row = local_window(x, fs, excerpt, index, startTime, annotations, cfg)
    row = local_empty_row();
    row.excerpt = excerpt; row.window = index; row.start_s = startTime;
    row.expertSpindleCount = local_overlap_count(annotations, startTime, cfg.window_s);
    t = (0:numel(x) - 1) ./ fs;
    options = cfg.apcOptions;
    options.fA(2) = min(options.fA(2), fs / 2 - 2);
    apc = bst_apc(struct('data', x(:).', 'time', t), options);
    row.apcStatus = apc.status_code.Value(1);
    row.apcFaHz = apc.amplitude_frequency_hz.Value(1);
    if cfg.useHybrid
        candidateHz = cfg.amplitudeGridHz(cfg.amplitudeGridHz + 2 < fs/2);
        hybrid = apc_event_carrier(x, fs, apc, candidateHz, 2, 1.5, 0.020);
        row.hybridStatus = hybrid.status_code;
        row.hybridFpHz = hybrid.fp_hz;
        row.hybridFaHz = hybrid.fa_hz;
        row.hybridScore = hybrid.score;
    end
    [row.pacFaHz, row.pacScore] = local_scan(x, fs, cfg, 'canolty');
    [row.normPacFaHz, row.normPacScore] = local_scan(x, fs, cfg, 'ozkurt');
    row = local_add_alignment(row, x, fs, annotations, startTime, cfg, 'apc');
    row = local_add_alignment(row, x, fs, annotations, startTime, cfg, 'pac');
    row = local_add_alignment(row, x, fs, annotations, startTime, cfg, 'normPac');
    if cfg.useHybrid
        row = local_add_alignment(row, x, fs, annotations, startTime, cfg, 'hybrid');
    end
end

function row = local_add_alignment(row, x, fs, annotations, startTime, cfg, prefix)
    frequency = row.([prefix 'FaHz']);
    if ~isfinite(frequency) || frequency - 2 <= 0 || frequency + 2 >= fs / 2
        return;
    end
    envelope = abs(hilbert(local_bandpass(x, fs, frequency - 2, frequency + 2)));
    threshold = median(envelope) + cfg.peakProminenceZ * std(envelope);
    [~, peaks] = findpeaks(envelope, 'MinPeakHeight', threshold, ...
        'MinPeakDistance', max(1, round(cfg.minPeakSpacingS * fs)));
    eventTimes = startTime + (peaks - 1) ./ fs;
    [precision, recall] = local_event_overlap(eventTimes, annotations, startTime, cfg.window_s);
    row.([prefix 'Sigma']) = frequency >= cfg.sigmaOutcomeHz(1) && frequency <= cfg.sigmaOutcomeHz(2);
    row.([prefix 'PeakCount']) = numel(eventTimes);
    row.([prefix 'Precision']) = precision;
    row.([prefix 'Recall']) = recall;
    row.([prefix 'ExcessPrecision']) = precision - local_shift_null(eventTimes, annotations, startTime, cfg);
end

function [fa, best] = local_scan(x, fs, cfg, metric)
    best = -inf; fa = NaN;
    phases = cell(numel(cfg.phaseGridHz), 1);
    amplitudes = cell(numel(cfg.amplitudeGridHz), 1);
    for i = 1:numel(phases)
        f = cfg.phaseGridHz(i);
        phases{i} = angle(hilbert(local_bandpass(x, fs, max(.1, f - .5), f + .5)));
    end
    for i = 1:numel(amplitudes)
        f = cfg.amplitudeGridHz(i);
        if f + 2 < fs / 2, amplitudes{i} = abs(hilbert(local_bandpass(x, fs, f - 2, f + 2))); end
    end
    for i = 1:numel(phases)
        for j = 1:numel(amplitudes)
            if isempty(amplitudes{j}), continue; end
            value = calc_MI_all_methods(phases{i}, amplitudes{j}, metric, 'no', 0, 1, false, 18);
            if value > best, best = value; fa = cfg.amplitudeGridHz(j); end
        end
    end
end

function value = local_shift_null(eventTimes, annotations, startTime, cfg)
    if isempty(eventTimes), value = NaN; return; end
    null = nan(cfg.nShiftNull, 1);
    relative = eventTimes - startTime;
    for i = 1:cfg.nShiftNull
        shifted = startTime + mod(relative + rand * cfg.window_s, cfg.window_s);
        null(i) = local_event_overlap(shifted, annotations, startTime, cfg.window_s);
    end
    value = mean(null, 'omitnan');
end

function [precision, recall] = local_event_overlap(eventTimes, annotations, startTime, duration)
    localEvents = annotations(annotations(:, 1) < startTime + duration & annotations(:, 1) + annotations(:, 2) > startTime, :);
    if isempty(eventTimes), precision = NaN; else
        hits = false(size(eventTimes));
        for i = 1:size(localEvents, 1)
            hits = hits | (eventTimes >= localEvents(i, 1) & eventTimes <= localEvents(i, 1) + localEvents(i, 2));
        end
        precision = mean(hits);
    end
    if isempty(localEvents), recall = NaN; else
        recalled = false(size(localEvents, 1), 1);
        for i = 1:size(localEvents, 1)
            recalled(i) = any(eventTimes >= localEvents(i, 1) & eventTimes <= localEvents(i, 1) + localEvents(i, 2));
        end
        recall = mean(recalled);
    end
end

function n = local_overlap_count(events, startTime, duration)
    n = sum(events(:, 1) < startTime + duration & events(:, 1) + events(:, 2) > startTime);
end

function y = local_bandpass(x, fs, lo, hi)
    % Second-order sections avoid numerical instability for the lowest
    % prespecified phase bands at the DREAMS sampling rates.
    [z, p, k] = butter(4, [lo hi] ./ (fs / 2), 'bandpass');
    [sos, gain] = zp2sos(z, p, k);
    y = filtfilt(sos, gain, double(x(:)));
end

function summary = local_excerpt_summary(windows, cfg)
    methods = {'apc', 'pac', 'normPac'};
    if cfg.useHybrid, methods{end + 1} = 'hybrid'; end
    entries = cell(6, 1);
    for excerpt = 1:6
        sub = windows(windows.excerpt == excerpt, :);
        entry = struct('excerpt', excerpt, 'nWindows', height(sub), 'nAnnotatedWindows', sum(sub.expertSpindleCount > 0));
        for i = 1:numel(methods)
            name = methods{i};
            entry.([name 'SigmaFraction']) = mean(sub.([name 'Sigma']), 'omitnan');
            entry.([name 'Precision']) = mean(sub.([name 'Precision']), 'omitnan');
            entry.([name 'Recall']) = mean(sub.([name 'Recall']), 'omitnan');
            entry.([name 'ExcessPrecision']) = mean(sub.([name 'ExcessPrecision']), 'omitnan');
        end
        entries{excerpt} = entry;
    end
    summary = struct2table(vertcat(entries{:}));
    summary.sigmaRangeHz = repmat(string(sprintf('%g-%g', cfg.sigmaOutcomeHz)), height(summary), 1);
end

function inference = local_paired_inference(summary, cfg)
    outcomes = {'SigmaFraction', 'Precision', 'Recall', 'ExcessPrecision'};
    comparisons = {'pac', 'normPac'};
    method = 'apc';
    if cfg.useHybrid
        method = 'hybrid';
        comparisons = {'apc', 'pac', 'normPac'};
    end
    rows = repmat(struct('outcome', "", 'comparison', "", 'meanDifference', NaN, 'ciLow', NaN, 'ciHigh', NaN, 'pSignFlip', NaN), 0, 1);
    for iOutcome = 1:numel(outcomes)
        for iComparison = 1:numel(comparisons)
            d = summary.([method outcomes{iOutcome}]) - summary.([comparisons{iComparison} outcomes{iOutcome}]);
            d = d(isfinite(d));
            [lo, hi] = local_bootstrap_ci(d);
            rows(end + 1, 1) = struct('outcome', string(outcomes{iOutcome}), 'comparison', string(comparisons{iComparison}), ...
                'meanDifference', mean(d, 'omitnan'), 'ciLow', lo, 'ciHigh', hi, 'pSignFlip', local_sign_flip(d)); %#ok<AGROW>
        end
    end
    inference = struct2table(rows);
end

function [lo, hi] = local_bootstrap_ci(d)
    if isempty(d), lo = NaN; hi = NaN; return; end
    values = zeros(5000, 1);
    for i = 1:numel(values), values(i) = mean(d(randi(numel(d), numel(d), 1))); end
    ci = prctile(values, [2.5 97.5]); lo = ci(1); hi = ci(2);
end

function p = local_sign_flip(d)
    n = numel(d);
    if n == 0, p = NaN; return; end
    observed = abs(mean(d));
    signs = dec2bin(0:2^n-1) - '0';
    values = abs((signs * 2 - 1) * d ./ n);
    p = mean(values >= observed);
end

function row = local_empty_row()
    row = struct('excerpt', NaN, 'window', NaN, 'start_s', NaN, 'expertSpindleCount', NaN, ...
        'apcStatus', NaN, 'apcFaHz', NaN, 'pacFaHz', NaN, 'pacScore', NaN, 'normPacFaHz', NaN, 'normPacScore', NaN, ...
        'hybridStatus', NaN, 'hybridFpHz', NaN, 'hybridFaHz', NaN, 'hybridScore', NaN, ...
        'apcSigma', false, 'pacSigma', false, 'normPacSigma', false, ...
        'hybridSigma', false, ...
        'apcPeakCount', NaN, 'pacPeakCount', NaN, 'normPacPeakCount', NaN, ...
        'hybridPeakCount', NaN, ...
        'apcPrecision', NaN, 'pacPrecision', NaN, 'normPacPrecision', NaN, ...
        'hybridPrecision', NaN, ...
        'apcRecall', NaN, 'pacRecall', NaN, 'normPacRecall', NaN, ...
        'hybridRecall', NaN, ...
        'apcExcessPrecision', NaN, 'pacExcessPrecision', NaN, 'normPacExcessPrecision', NaN, ...
        'hybridExcessPrecision', NaN);
end

function files = local_write(windows, excerpts, inference, cfg)
    root = fileparts(mfilename('fullpath'));
    suffix = '';
    if cfg.useHybrid, suffix = ['_' cfg.profile]; end
    files.windows = fullfile(root, ['apc_dreams_spindle_external_windows' suffix '.csv']);
    files.excerpts = fullfile(root, ['apc_dreams_spindle_external_excerpts' suffix '.csv']);
    files.inference = fullfile(root, ['apc_dreams_spindle_external_inference' suffix '.csv']);
    files.figure = fullfile(root, ['apc_dreams_spindle_external_validation' suffix '.png']);
    files.summary = fullfile(root, ['apc_dreams_spindle_external_summary' suffix '.txt']);
    files.mat = fullfile(root, ['apc_dreams_spindle_external_validation' suffix '.mat']);
    writetable(windows, files.windows); writetable(excerpts, files.excerpts); writetable(inference, files.inference);
end

function local_plot(summary, file)
    names = {'SigmaFraction', 'Precision', 'Recall', 'ExcessPrecision'};
    labels = {'Sigma-range selection', 'Peak precision', 'Spindle recall', 'Precision above shifted null'};
    methods = {'apc', 'pac', 'normPac'};
    if ismember('hybridSigmaFraction', summary.Properties.VariableNames)
        methods{end + 1} = 'hybrid';
    end
    colors = [0.85 0.35 0; 0.10 0.40 0.80; 0.15 0.60 0.35; 0.65 0.20 0.25];
    figure('Visible', 'off', 'Color', 'w', 'Position', [100 100 1180 520]);
    tiledlayout(1, 4, 'TileSpacing', 'compact', 'Padding', 'compact');
    for i = 1:numel(names)
        nexttile; hold on;
        for iMethod = 1:numel(methods)
            y = summary.([methods{iMethod} names{i}]);
            scatter(iMethod + .05 * randn(size(y)), y, 28, colors(iMethod, :), 'filled', 'MarkerFaceAlpha', .7);
            plot([iMethod-.22 iMethod+.22], [mean(y, 'omitnan') mean(y, 'omitnan')], 'Color', colors(iMethod, :), 'LineWidth', 2);
        end
        xlim([.5 numel(methods)+.5]); xticks(1:numel(methods));
        tickLabels = {'APC','PAC','Norm. PAC','APC-event'};
        xticklabels(tickLabels(1:numel(methods)));
        ylabel(labels{i}); box off; grid off;
    end
    exportgraphics(gcf, file, 'Resolution', 300); close(gcf);
end

function local_write_summary(results, file)
    S = results.excerpt_summary;
    fid = fopen(file, 'w');
    fprintf(fid, 'DREAMS all-window external spindle validation\n');
    fprintf(fid, 'Six excerpts, %d windows total; scorer-2 annotations used only for evaluation.\n', height(results.windows));
    methods = {'apc','pac','normPac'};
    if results.config.useHybrid, methods{end+1} = 'hybrid'; end
    for method = methods
        m = method{1};
        fprintf(fid, '%s: sigma fraction %.3f; precision %.3f; recall %.3f; precision above shifted null %.3f\n', ...
            m, mean(S.([m 'SigmaFraction']), 'omitnan'), mean(S.([m 'Precision']), 'omitnan'), ...
            mean(S.([m 'Recall']), 'omitnan'), mean(S.([m 'ExcessPrecision']), 'omitnan'));
    end
    fclose(fid);
end
