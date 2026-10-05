function results = run_apc_operational_validation(profileName)
% RUN_APC_OPERATIONAL_VALIDATION Reviewer-requested APC operational checks.
%
% Runs the full APC pipeline on coupled, null, harmonic/non-sinusoidal,
% transient-artifact, and no-oscillator simulations. It also evaluates
% split-half carrier stability and sensitivity to burst threshold and
% amplitude-search range. Surrogate z scores use rank-matched spectral
% amplitude-envelope phase scrambling because circular shifts are not a
% valid magnitude null for a stationary periodic MVL signal. The default
% reviewer profile uses 25 repeats.
%
% OUTPUTS:
%   apc_operational_validation_<profile>.mat
%   apc_operational_validation_runs_<profile>.csv
%   apc_operational_validation_summary_<profile>.csv
%   apc_operational_validation_summary_<profile>.txt
%   apc_operational_validation_<profile>.png/.fig/.pdf

    if nargin < 1 || isempty(profileName)
        profileName = 'reviewer';
    end
    cfg = local_config(profileName);
    rng(cfg.random_seed, 'twister');

    rows = {};
    for iCondition = 1:numel(cfg.conditions)
        for iRepeat = 1:cfg.n_repeats
            fprintf('[%s] %s, repeat %d/%d\n', cfg.profile_name, ...
                cfg.conditions(iCondition), iRepeat, cfg.n_repeats);
            signal = local_simulate_signal(cfg, cfg.conditions(iCondition));
            rows{end + 1} = local_run_row(signal, cfg, cfg.conditions(iCondition), ...
                iRepeat, 'baseline', cfg.fA, cfg.burst_prominence_scale); %#ok<AGROW>

            % Stability is meaningful only for the coupled reference case.
            if cfg.conditions(iCondition) == "coupled"
                rows{end + 1} = local_run_row(signal, cfg, "coupled", iRepeat, ...
                    'threshold_low', cfg.fA, 0.55); %#ok<AGROW>
                rows{end + 1} = local_run_row(signal, cfg, "coupled", iRepeat, ...
                    'threshold_high', cfg.fA, 0.95); %#ok<AGROW>
                rows{end + 1} = local_run_row(signal, cfg, "coupled", iRepeat, ...
                    'band_wide', [70 160], cfg.burst_prominence_scale); %#ok<AGROW>
                rows{end + 1} = local_run_row(signal, cfg, "coupled", iRepeat, ...
                    'band_narrow', [90 140], cfg.burst_prominence_scale); %#ok<AGROW>
                [firstHalf, secondHalf] = local_split_halves(signal);
                rows{end + 1} = local_run_row(firstHalf, cfg, "coupled", iRepeat, ...
                    'split_first', cfg.fA, cfg.burst_prominence_scale); %#ok<AGROW>
                rows{end + 1} = local_run_row(secondHalf, cfg, "coupled", iRepeat, ...
                    'split_second', cfg.fA, cfg.burst_prominence_scale); %#ok<AGROW>
            end
        end
    end

    runTable = struct2table([rows{:}]);
    summaryTable = local_summary(runTable, cfg);
    splitTable = local_split_summary(runTable);

    baseDir = fileparts(mfilename('fullpath'));
    tag = lower(cfg.profile_name);
    outMat = fullfile(baseDir, sprintf('apc_operational_validation_%s.mat', tag));
    outRuns = fullfile(baseDir, sprintf('apc_operational_validation_runs_%s.csv', tag));
    outSummary = fullfile(baseDir, sprintf('apc_operational_validation_summary_%s.csv', tag));
    outText = fullfile(baseDir, sprintf('apc_operational_validation_summary_%s.txt', tag));
    writetable(runTable, outRuns);
    writetable(summaryTable, outSummary);
    save(outMat, 'cfg', 'runTable', 'summaryTable', 'splitTable', '-v7.3');
    local_write_text(outText, cfg, summaryTable, splitTable);

    fig = local_plot(summaryTable, splitTable, cfg);
    outPng = fullfile(baseDir, sprintf('apc_operational_validation_%s.png', tag));
    outPdf = fullfile(baseDir, sprintf('apc_operational_validation_%s.pdf', tag));
    outFig = fullfile(baseDir, sprintf('apc_operational_validation_%s.fig', tag));
    exportgraphics(fig, outPng, 'Resolution', 300);
    exportgraphics(fig, outPdf, 'ContentType', 'vector');
    savefig(fig, outFig);
    close(fig);

    fprintf('\nSaved operational-validation outputs:\n  %s\n  %s\n  %s\n  %s\n  %s\n', ...
        outMat, outRuns, outSummary, outText, outPng);
    results = struct('config', cfg, 'run_table', runTable, 'summary_table', summaryTable, ...
        'split_table', splitTable, 'mat_file', outMat, 'runs_csv', outRuns, ...
        'summary_csv', outSummary, 'text_file', outText, 'png_file', outPng);
end

function cfg = local_config(profileName)
    cfg.profile_name = char(lower(string(profileName)));
    cfg.random_seed = 20261004;
    cfg.fs = 500; cfg.duration_s = 12; cfg.fP = 8; cfg.fA = [80 150]; cfg.true_fA = 120;
    cfg.true_phase_deg = -90; cfg.snr_db = -3; cfg.num_perm = 100;
    cfg.burst_prominence_scale = 0.75; cfg.min_bursts = 12; cfg.min_phase_events = 8;
    cfg.conditions = ["coupled", "null", "harmonic", "transient", "no_oscillator"];
    switch lower(string(profileName))
        case "fast", cfg.n_repeats = 10;
        case "reviewer", cfg.n_repeats = 25;
        otherwise, error('Use profileName ''fast'' or ''reviewer''.');
    end
end

function row = local_run_row(signal, cfg, condition, repeatIndex, setting, faBand, prominence)
    t = (0:numel(signal)-1) ./ cfg.fs;
    opts = struct('fA', faBand, 'epoch', [-0.6 0.6], 'decomposition', 'fft_peak', ...
        'metric', 'canolty', 'diagm', false, 'surrogates', true, 'num_perm', cfg.num_perm, ...
        'numPhaseBins', 18, 'burstProminenceScale', prominence, ...
        'amplitudeBandWidthHz', 12, 'surrogateMethod', 'phase_scramble');
    out = bst_apc(struct('data', signal, 'time', t), opts);
    status = out.status_code.Value(1);
    nBursts = out.n_bursts.Value(1);
    nPhase = out.n_phase_events.Value(1);
    row = struct('condition', string(condition), 'repeat_index', repeatIndex, ...
        'setting', string(setting), 'fa_low_hz', faBand(1), 'fa_high_hz', faBand(2), ...
        'burst_prominence_scale', prominence, 'status_code', status, ...
        'n_bursts', nBursts, 'n_phase_events', nPhase, ...
        'passes_minimum_counts', status == 0 && nBursts >= cfg.min_bursts && nPhase >= cfg.min_phase_events, ...
        'fP_hz', out.phase_frequency_hz.Value(1), 'fA_hz', out.amplitude_frequency_hz.Value(1), ...
        'preferred_phase_deg', out.preferred_phase_deg.Value(1), 'surrogate_z', out.pac_strength.Value(1), ...
        'significant_z', status == 0 && out.pac_strength.Value(1) > 1.96, ...
        'fp_error_hz', abs(out.phase_frequency_hz.Value(1) - cfg.fP), ...
        'fa_error_hz', abs(out.amplitude_frequency_hz.Value(1) - cfg.true_fA));
end

function signal = local_simulate_signal(cfg, condition)
    t = 0:1/cfg.fs:(cfg.duration_s - 1/cfg.fs);
    phase = 2*pi*cfg.fP*t + deg2rad(cfg.true_phase_deg + 90);
    low = sin(phase);
    cycleTimes = (0:ceil(cfg.duration_s*cfg.fP)) ./ cfg.fP + 0.75/cfg.fP;
    cycleTimes = cycleTimes(cycleTimes > 0 & cycleTimes < cfg.duration_s);
    switch condition
        case "coupled"
            signal = low + local_bursts(t, cycleTimes + .010*randn(size(cycleTimes)), cfg.true_fA, 1.5);
        case "null"
            signal = low + local_bursts(t, rand(size(cycleTimes))*cfg.duration_s, cfg.true_fA, 1.5);
        case "harmonic"
            nonsinusoidal = low + 0.40*sin(2*phase + .4) + 0.20*sin(3*phase - .2);
            signal = nonsinusoidal + local_bursts(t, cycleTimes + .010*randn(size(cycleTimes)), cfg.true_fA, 1.5);
        case "transient"
            transientTimes = sort(rand(size(cycleTimes))*cfg.duration_s);
            signal = local_bursts(t, transientTimes, cfg.true_fA, 1.5) + 0.9*local_spikes(t, transientTimes);
        case "no_oscillator"
            signal = local_bursts(t, rand(size(cycleTimes))*cfg.duration_s, cfg.true_fA, 1.5);
        otherwise
            error('Unknown condition.');
    end
    signal = local_add_noise(signal, cfg.snr_db);
end

function y = local_bursts(t, centers, freq, amplitude)
    envelope = zeros(size(t));
    for k = 1:numel(centers), envelope = envelope + exp(-0.5*((t-centers(k))/0.028).^2); end
    y = amplitude * envelope .* sin(2*pi*freq*t);
end

function y = local_spikes(t, centers)
    y = zeros(size(t));
    for k = 1:numel(centers), y = y + exp(-0.5*((t-centers(k))/0.006).^2); end
end

function y = local_add_noise(x, snrDb)
    pink = cumsum(randn(size(x))); pink = (pink-mean(pink))/std(pink);
    white = randn(size(x)); noise = pink + 0.5*white; noise = noise/std(noise);
    y = x + sqrt(mean(x.^2)/(10^(snrDb/10))) * noise;
end

function [firstHalf, secondHalf] = local_split_halves(x)
    middle = floor(numel(x)/2); firstHalf = x(1:middle); secondHalf = x(middle+1:end);
end

function summary = local_summary(runTable, cfg)
    keys = unique(runTable(:, {'condition','setting'}), 'rows'); rows = cell(height(keys), 1);
    for k = 1:height(keys)
        mask = runTable.condition == keys.condition(k) & runTable.setting == keys.setting(k);
        x = runTable(mask, :);
        rows{k} = struct('condition', keys.condition(k), 'setting', keys.setting(k), 'n', height(x), ...
            'valid_count_rate', mean(x.passes_minimum_counts), 'significant_rate', mean(x.significant_z), ...
            'median_bursts', median(x.n_bursts), 'median_phase_events', median(x.n_phase_events), ...
            'median_fP_hz', median(x.fP_hz, 'omitnan'), 'median_fA_hz', median(x.fA_hz, 'omitnan'), ...
            'median_z', median(x.surrogate_z, 'omitnan'), 'min_burst_threshold', cfg.min_bursts, ...
            'min_phase_event_threshold', cfg.min_phase_events);
    end
    summary = struct2table([rows{:}]);
end

function splitTable = local_split_summary(runTable)
    baseline = runTable(runTable.setting == "baseline" & runTable.condition == "coupled", :);
    first = runTable(runTable.setting == "split_first", :); second = runTable(runTable.setting == "split_second", :);
    ids = intersect(intersect(baseline.repeat_index, first.repeat_index), second.repeat_index);
    rows = cell(numel(ids), 1);
    for k = 1:numel(ids)
        b = baseline(baseline.repeat_index == ids(k), :); a = first(first.repeat_index == ids(k), :); c = second(second.repeat_index == ids(k), :);
        rows{k} = struct('repeat_index', ids(k), 'split_valid', a.passes_minimum_counts && c.passes_minimum_counts, ...
            'split_fp_difference_hz', abs(a.fP_hz-c.fP_hz), 'split_fa_difference_hz', abs(a.fA_hz-c.fA_hz), ...
            'full_vs_split_fp_max_error_hz', max(abs([a.fP_hz c.fP_hz]-b.fP_hz)), ...
            'full_vs_split_fa_max_error_hz', max(abs([a.fA_hz c.fA_hz]-b.fA_hz)));
    end
    splitTable = struct2table([rows{:}]);
end

function local_write_text(fileName, cfg, summary, splitTable)
    fid = fopen(fileName, 'w'); cleanup = onCleanup(@() fclose(fid));
    fprintf(fid, 'APC operational validation (%s)\n', cfg.profile_name);
    fprintf(fid, 'Operational count criterion: >= %d burst epochs and >= %d phase events.\n', cfg.min_bursts, cfg.min_phase_events);
    fprintf(fid, 'Surrogates use rank-matched amplitude-envelope Fourier phase scrambling; a full-pipeline null false-positive rate is the null/baseline significant_z rate (z > 1.96).\n\n');
    fprintf(fid, '%s\n', evalc('disp(summary)'));
    fprintf(fid, 'Split-half median fP difference: %.3f Hz; median fA difference: %.3f Hz.\n', ...
        median(splitTable.split_fp_difference_hz, 'omitnan'), median(splitTable.split_fa_difference_hz, 'omitnan'));
end

function fig = local_plot(summary, splitTable, cfg)
    fig = figure('Color','w','Position',[100 100 1250 700]); tiledlayout(2,2,'Padding','compact','TileSpacing','compact');
    baseline = summary(summary.setting == "baseline", :);
    nexttile; bar(categorical(baseline.condition), baseline.valid_count_rate, 'FaceColor',[0.12 0.42 0.70]); ylim([0 1]); ylabel('Rate'); title('A  Passing operational counts'); grid off;
    nexttile; bar(categorical(baseline.condition), baseline.significant_rate, 'FaceColor',[0.85 0.33 0.10]); ylim([0 1]); ylabel('Rate'); title('B  Surrogate-positive rate'); grid off;
    nexttile; sensitivity = summary(summary.condition == "coupled" & summary.setting ~= "baseline" & ~startsWith(summary.setting,"split"), :); bar(categorical(sensitivity.setting), sensitivity.median_fA_hz, 'FaceColor',[0.15 0.62 0.45]); ylabel('Median f_A (Hz)'); title('C  Threshold/range sensitivity'); grid off;
    nexttile; histogram(splitTable.split_fp_difference_hz, 'FaceColor',[0.25 0.25 0.25]); hold on; xline(median(splitTable.split_fp_difference_hz,'omitnan'),'r-','LineWidth',2); xlabel('|split-half f_P difference| (Hz)'); ylabel('Repeats'); title(sprintf('D  Split-half stability (n = %d)', height(splitTable))); grid off;
    sgtitle(sprintf('APC Operational Validation (%s; %d repeats)', cfg.profile_name, cfg.n_repeats), 'FontWeight','bold');
end
