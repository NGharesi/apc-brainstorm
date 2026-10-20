function results = run_apc_full_pipeline_null_calibration_frozen(profileName)
% Fork of run_apc_full_pipeline_null_calibration.m for protocol amendment
% 2026-10-20. Only changes: function name, frozen_reviewer profile
% (original APC, frozen v1.1.0 bst_apc with minPhaseCycles = 3, same seed
% 20261005 as the earlier reviewer run so signals are paired across
% code versions), and checkpointing for every profile.
% RUN_APC_FULL_PIPELINE_NULL_CALIBRATION Calibrate APC false positives.
%
% Every replicate is a new raw signal and runs the complete APC pipeline:
% burst detection, fP selection, trough selection, fA selection, and raw
% coupling estimation. Internal APC surrogates are disabled deliberately;
% they would be computed after fP/fA selection and cannot calibrate the
% selected-pair statistic. A calibration split defines one global raw-score
% threshold; an independent holdout split estimates false-positive rates.
%
% Usage:
%   run_apc_full_pipeline_null_calibration('fast')      % 25/split/condition
%   run_apc_full_pipeline_null_calibration('reviewer')  % 100/split/condition

    if nargin < 1 || isempty(profileName), profileName = 'reviewer'; end
    cfg = local_config(profileName);
    rng(cfg.randomSeed, 'twister');

    rows = cell(2 * numel(cfg.conditions) * cfg.nRepeats, 1);
    iRow = 0;
    checkpointFile = fullfile(fileparts(mfilename('fullpath')), ...
        sprintf('apc_full_pipeline_null_calibration_checkpoint_%s.mat', lower(cfg.profileName)));
    if exist(checkpointFile, 'file')
        checkpoint = load(checkpointFile, 'rows', 'iRow', 'rngState');
        rows = checkpoint.rows;
        iRow = checkpoint.iRow;
        rng(checkpoint.rngState);
        fprintf('Resuming %s after %d completed replicates.\n', cfg.profileName, iRow);
    end
    completedRows = iRow;
    for iSplit = 1:numel(cfg.splits)
        for iCondition = 1:numel(cfg.conditions)
            for iRepeat = 1:cfg.nRepeats
                linearIndex = ((iSplit - 1) * numel(cfg.conditions) + iCondition - 1) * cfg.nRepeats + iRepeat;
                if linearIndex <= completedRows, continue; end
                fprintf('[%s] %s, %s %d/%d\n', cfg.profileName, ...
                    cfg.splits(iSplit), cfg.conditions(iCondition), iRepeat, cfg.nRepeats);
                iRow = iRow + 1;
                rawSignal = local_simulate(cfg, cfg.conditions(iCondition));
                rows{iRow} = local_run_full_pipeline(rawSignal, cfg, ...
                    cfg.splits(iSplit), cfg.conditions(iCondition), iRepeat);
                if (mod(iRow, 10) == 0 || iRow == numel(rows))
                    rngState = rng; %#ok<NASGU>
                    save(checkpointFile, 'rows', 'iRow', 'rngState', '-v7.3');
                end
            end
        end
    end
    runTable = struct2table([rows{1:iRow}]);

    % Failed runs are assigned zero score. This makes a false-positive rate
    % conditional neither on event detection nor on carrier recovery.
    calibration = runTable(runTable.split == "calibration" & runTable.condition ~= "coupled_positive", :);
    threshold = prctile(calibration.score_for_calibration, cfg.thresholdPercentile);
    holdout = runTable(runTable.split == "holdout", :);
    holdout.is_positive = holdout.score_for_calibration > threshold;
    runTable.is_positive = false(height(runTable), 1);
    runTable.is_positive(runTable.split == "holdout") = holdout.is_positive;

    summaryTable = local_summary(runTable, threshold, cfg);
    baseDir = fileparts(mfilename('fullpath'));
    tag = lower(cfg.profileName);
    files.mat = fullfile(baseDir, sprintf('apc_full_pipeline_null_calibration_%s.mat', tag));
    files.runs = fullfile(baseDir, sprintf('apc_full_pipeline_null_calibration_runs_%s.csv', tag));
    files.summary = fullfile(baseDir, sprintf('apc_full_pipeline_null_calibration_summary_%s.csv', tag));
    files.text = fullfile(baseDir, sprintf('apc_full_pipeline_null_calibration_summary_%s.txt', tag));
    files.png = fullfile(baseDir, sprintf('apc_full_pipeline_null_calibration_%s.png', tag));
    files.pdf = fullfile(baseDir, sprintf('apc_full_pipeline_null_calibration_%s.pdf', tag));
    files.fig = fullfile(baseDir, sprintf('apc_full_pipeline_null_calibration_%s.fig', tag));
    writetable(runTable, files.runs);
    writetable(summaryTable, files.summary);
    save(files.mat, 'cfg', 'runTable', 'summaryTable', 'threshold', '-v7.3');
    local_write_text(files.text, cfg, threshold, summaryTable);
    fig = local_plot(runTable, summaryTable, threshold, cfg);
    exportgraphics(fig, files.png, 'Resolution', 300);
    exportgraphics(fig, files.pdf, 'ContentType', 'vector');
    savefig(fig, files.fig); close(fig);

    fprintf('\nSaved full-pipeline null-calibration outputs:\n  %s\n  %s\n  %s\n', ...
        files.mat, files.summary, files.png);
    results = struct('config', cfg, 'threshold', threshold, 'run_table', runTable, ...
        'summary_table', summaryTable, 'files', files);
end

function cfg = local_config(profileName)
    cfg.profileName = char(lower(string(profileName)));
    cfg.randomSeed = 20261005;
    cfg.fs = 500; cfg.durationSec = 12; cfg.fP = 8; cfg.fA = [80 150];
    cfg.useEventCarrier = false;
    cfg.trueFA = 120; cfg.snrDb = -3; cfg.thresholdPercentile = 95;
    cfg.splits = ["calibration", "holdout"];
    cfg.conditions = ["colored_noise", "uncoupled_bursts", "transient_artifact", ...
        "harmonic_null", "coupled_positive"];
    switch lower(string(profileName))
        case "fast", cfg.nRepeats = 25;
        case "reviewer", cfg.nRepeats = 100;
        case "hybrid_smoke"
            cfg.nRepeats = 1;
            cfg.useEventCarrier = true;
        case "hybrid_reviewer"
            cfg.nRepeats = 100;
            cfg.useEventCarrier = true;
        case "frozen_smoke"
            cfg.nRepeats = 1;        % syntax check only; never reported
        case "frozen_reviewer"
            cfg.nRepeats = 100;      % seed stays 20261005 (paired with 'reviewer')
        otherwise, error('Use frozen_smoke or frozen_reviewer (other profiles: see original script).');
    end
    if cfg.useEventCarrier
        cfg.randomSeed = 20261020;
        cfg.fA = [80 152];
        cfg.amplitudeCandidatesHz = 88:4:148;
    end
end

function row = local_run_full_pipeline(signal, cfg, split, condition, repeatIndex)
    time = (0:numel(signal)-1) ./ cfg.fs;
    opts = struct('fA', cfg.fA, 'epoch', [-0.6 0.6], ...
        'decomposition', 'fft_peak', 'metric', 'canolty', 'diagm', false, ...
        'surrogates', false, 'num_perm', 0, 'numPhaseBins', 18, ...
        'burstProminenceScale', 0.75, 'amplitudeBandWidthHz', 12);
    opts.minPhaseCycles = 3;   % frozen v1.1.0 phase rule, all profiles
    out = bst_apc(struct('data', signal, 'time', time), opts);
    status = out.status_code.Value(1);
    rawScore = out.pac_strength.Value(1);
    if cfg.useEventCarrier
        hybrid = apc_event_carrier(signal, cfg.fs, out, ...
            cfg.amplitudeCandidatesHz, 6, 1.5, 0.020);
        status = hybrid.status_code;
        rawScore = hybrid.score;
        out.amplitude_frequency_hz.Value(1) = hybrid.fa_hz;
        out.preferred_phase_deg.Value(1) = hybrid.preferred_phase_deg;
    end
    if status ~= 0 || ~isfinite(rawScore), scoreForCalibration = 0; else, scoreForCalibration = rawScore; end
    row = struct('split', string(split), 'condition', string(condition), ...
        'repeat_index', repeatIndex, 'status_code', status, ...
        'valid_pipeline_run', status == 0, 'n_bursts', out.n_bursts.Value(1), ...
        'n_phase_events', out.n_phase_events.Value(1), ...
        'raw_coupling_score', rawScore, 'score_for_calibration', scoreForCalibration, ...
        'fP_hz', out.phase_frequency_hz.Value(1), ...
        'fA_hz', out.amplitude_frequency_hz.Value(1), ...
        'preferred_phase_deg', out.preferred_phase_deg.Value(1));
end

function signal = local_simulate(cfg, condition)
    t = 0:1/cfg.fs:(cfg.durationSec - 1/cfg.fs);
    phase = 2*pi*cfg.fP*t - pi/2;
    low = sin(phase);
    eventTimes = (0:ceil(cfg.durationSec*cfg.fP)) ./ cfg.fP + 0.75/cfg.fP;
    eventTimes = eventTimes(eventTimes > 0 & eventTimes < cfg.durationSec);
    switch condition
        case "colored_noise"
            signal = zeros(size(t));
        case "uncoupled_bursts"
            signal = low + local_bursts(t, rand(size(eventTimes))*cfg.durationSec, cfg.trueFA, 1.5);
        case "transient_artifact"
            artifactTimes = sort(rand(size(eventTimes))*cfg.durationSec);
            signal = local_bursts(t, artifactTimes, cfg.trueFA, 1.5) + 0.9*local_spikes(t, artifactTimes);
        case "harmonic_null"
            signal = low + 0.40*sin(2*phase + .4) + 0.20*sin(3*phase - .2);
        case "coupled_positive"
            signal = low + local_bursts(t, eventTimes + .010*randn(size(eventTimes)), cfg.trueFA, 1.5);
        otherwise
            error('Unknown condition: %s', condition);
    end
    signal = local_add_noise(signal, cfg.snrDb);
end

function y = local_bursts(t, centers, frequency, amplitude)
    envelope = zeros(size(t));
    for k = 1:numel(centers)
        envelope = envelope + exp(-0.5*((t-centers(k))/0.028).^2);
    end
    y = amplitude * envelope .* sin(2*pi*frequency*t);
end

function y = local_spikes(t, centers)
    y = zeros(size(t));
    for k = 1:numel(centers)
        y = y + exp(-0.5*((t-centers(k))/0.006).^2);
    end
end

function y = local_add_noise(signal, snrDb)
    pink = cumsum(randn(size(signal))); pink = (pink-mean(pink))/std(pink);
    white = randn(size(signal)); noise = pink + 0.5*white; noise = noise/std(noise);
    if any(signal)
        scale = sqrt(mean(signal.^2)/(10^(snrDb/10)));
    else
        scale = 1;
    end
    y = signal + scale*noise;
end

function summary = local_summary(runTable, threshold, cfg)
    conditions = unique(runTable.condition, 'stable'); rows = cell(numel(conditions), 1);
    for i = 1:numel(conditions)
        condition = conditions(i);
        cal = runTable(runTable.split == "calibration" & runTable.condition == condition, :);
        hold = runTable(runTable.split == "holdout" & runTable.condition == condition, :);
        positives = sum(hold.is_positive); total = height(hold);
        [lower, upper] = local_wilson(positives, total, 1.96);
        rows{i} = struct('condition', condition, 'n_calibration', height(cal), ...
            'n_holdout', total, 'threshold_raw_score', threshold, ...
            'calibration_valid_rate', mean(cal.valid_pipeline_run), ...
            'calibration_score_median', median(cal.score_for_calibration), ...
            'holdout_valid_rate', mean(hold.valid_pipeline_run), ...
            'holdout_positive_count', positives, 'holdout_positive_rate', positives/total, ...
            'holdout_wilson95_low', lower, 'holdout_wilson95_high', upper, ...
            'holdout_fP_median_hz', median(hold.fP_hz, 'omitnan'), ...
            'holdout_fA_median_hz', median(hold.fA_hz, 'omitnan'));
    end
    summary = struct2table([rows{:}]);
end

function [lower, upper] = local_wilson(successes, total, z)
    if total == 0, lower = NaN; upper = NaN; return; end
    p = successes / total; denominator = 1 + z^2/total;
    center = (p + z^2/(2*total)) / denominator;
    half = z * sqrt((p*(1-p) + z^2/(4*total))/total) / denominator;
    lower = max(0, center-half); upper = min(1, center+half);
end

function local_write_text(fileName, cfg, threshold, summary)
    fid = fopen(fileName, 'w'); cleanup = onCleanup(@() fclose(fid));
    fprintf(fid, 'Full-pipeline null calibration (%s)\n', cfg.profileName);
    fprintf(fid, 'Threshold: %.6g (pooled %dth percentile of %d independent calibration null runs).\n', ...
        threshold, cfg.thresholdPercentile, cfg.nRepeats * (numel(cfg.conditions)-1));
    fprintf(fid, 'Internal APC surrogates were disabled. Each replicate reran event detection, fP selection, fA selection, and raw coupling estimation.\n');
    fprintf(fid, 'Invalid pipeline runs count in the false-positive-rate denominator and contribute score zero during calibration.\n\n');
    fprintf(fid, '%s\n', evalc('disp(summary)'));
end

function fig = local_plot(runTable, summary, threshold, cfg)
    fig = figure('Color', 'w', 'Position', [100 100 1250 700]);
    tiledlayout(2, 2, 'Padding', 'compact', 'TileSpacing', 'compact');
    holdout = runTable(runTable.split == "holdout", :);
    conditions = categorical(summary.condition);
    nexttile; bar(conditions, summary.holdout_valid_rate, 'FaceColor', [0.12 0.42 0.70]);
    ylim([0 1]); ylabel('Rate'); title('A  Valid full-pipeline output rate'); grid off;
    nexttile; bar(conditions, summary.holdout_positive_rate, 'FaceColor', [0.85 0.33 0.10]); hold on;
    errorbar(1:height(summary), summary.holdout_positive_rate, ...
        summary.holdout_positive_rate-summary.holdout_wilson95_low, ...
        summary.holdout_wilson95_high-summary.holdout_positive_rate, 'k.', 'LineWidth', 1.2);
    ylim([0 1]); ylabel('Holdout rate above threshold'); title('B  Full-pipeline false-positive / sensitivity rate'); grid off;
    nexttile; hold on;
    for i = 1:numel(cfg.conditions)
        values = holdout.score_for_calibration(holdout.condition == cfg.conditions(i));
        scatter(i + 0.08*randn(size(values)), values, 12, 'filled', 'MarkerFaceAlpha', .45);
    end
    yline(threshold, 'k--', 'Calibration threshold'); xlim([.5 numel(cfg.conditions)+.5]);
    xticks(1:numel(cfg.conditions)); xticklabels(strrep(cfg.conditions, '_', ' ')); xtickangle(25);
    ylabel('Raw APC coupling score'); title('C  Independent holdout scores'); grid off;
    nexttile; hold on;
    for i = 1:numel(cfg.conditions)
        values = holdout.fA_hz(holdout.condition == cfg.conditions(i));
        scatter(i + 0.08*randn(size(values)), values, 12, 'filled', 'MarkerFaceAlpha', .45);
    end
    xlim([.5 numel(cfg.conditions)+.5]); xticks(1:numel(cfg.conditions)); xticklabels(strrep(cfg.conditions, '_', ' ')); xtickangle(25);
    ylabel('Selected fA (Hz)'); title('D  Carrier selection under nulls'); grid off;
    sgtitle(sprintf('Full-Pipeline APC Null Calibration (%s; n = %d per split/condition)', cfg.profileName, cfg.nRepeats), 'FontWeight', 'bold');
end
