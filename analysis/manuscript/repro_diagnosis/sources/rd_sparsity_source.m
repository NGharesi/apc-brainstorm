function varargout = rd_sparsity_source(action,varargin)
% Dispatch into copied historical functions. Generator/noise prefix unchanged.
    switch action
        case 'profile'
            varargout{1}=local_get_profile(varargin{1});
        case 'generate'
            cfg=varargin{1};keepRate=varargin{2};
    t = 0:(1 / cfg.fs_hz):(cfg.duration_s - 1 / cfg.fs_hz);
    signal = local_simulate_sparse_burst_signal(t, cfg, keepRate);
    signal = local_add_mixed_noise(signal, cfg.snr_db);


            varargout{1}=signal;varargout{2}=t;
        case 'apc'
            varargout{1}=local_run_apc(varargin{:});
        otherwise
            error('repro_diagnosis:Action','Unknown action');
    end
end

function cfg = local_get_profile(profileName)
    profileName = lower(string(profileName));

    cfg = struct();
    cfg.profile_name = char(profileName);
    cfg.random_seed = 20260618;
    cfg.fs_hz = 500;
    cfg.duration_s = 8.0;
    cfg.true_fp_hz = 8.0;
    cfg.true_fa_hz = 120.0;
    cfg.phase_offset_deg = -90;
    cfg.low_amp = 1.0;
    cfg.true_high_amp = 1.30;
    cfg.base_hf_amp = 0.08;
    cfg.burst_sigma_s = 0.028;
    cfg.burst_phase_jitter_s = 0.010;
    cfg.snr_db = -3.0;
    cfg.broad_fa_band_hz = [80 150];
    cfg.phase_scan_hz = 4:1:12;
    cfg.amplitude_scan_hz = 80:8:152;
    cfg.metric = 'canolty';
    cfg.fa_tolerance_hz = 8.0;
    cfg.fp_tolerance_hz = 1.0;
    cfg.coupling_level = 0.60;
    cfg.background_burst_scale = 0.18;

    switch profileName
        case "fast"
            cfg.n_repeats = 10;
            cfg.burst_keep_rates = [1.00 0.75 0.50 0.35 0.25 0.15];
        case "full"
            cfg.n_repeats = 25;
            cfg.burst_keep_rates = [1.00 0.85 0.70 0.55 0.40 0.25 0.15];
        otherwise
            error('Unknown profileName: %s', profileName);
    end
end


function trialRows = local_run_trial(cfg, keepRate, repIdx)
    t = 0:(1 / cfg.fs_hz):(cfg.duration_s - 1 / cfg.fs_hz);
    signal = local_simulate_sparse_burst_signal(t, cfg, keepRate);
    signal = local_add_mixed_noise(signal, cfg.snr_db);

    apcResult = local_run_apc(signal, t, cfg);
    mvlScan = local_scan_standard_pac(signal, cfg, 'canolty');
    klmiScan = local_scan_standard_pac(signal, cfg, 'tort');
    glmScan = local_scan_standard_pac(signal, cfg, 'glm');

    trialRows = {
        local_pack_row("APC", keepRate, repIdx, apcResult, cfg), ...
        local_pack_row("MVL-scan", keepRate, repIdx, mvlScan, cfg), ...
        local_pack_row("KLMI-scan", keepRate, repIdx, klmiScan, cfg), ...
        local_pack_row("GLM-scan", keepRate, repIdx, glmScan, cfg)};
end


function row = local_pack_row(methodName, keepRate, repIdx, item, cfg)
    row = struct();
    row.method = string(methodName);
    row.burst_keep_rate = keepRate;
    row.repeat_index = repIdx;
    row.valid = item.valid;
    row.status_code = item.status_code;
    row.recovered_fp_hz = item.fp_hz;
    row.recovered_fa_hz = item.fa_hz;
    row.preferred_phase_deg = item.preferred_phase_deg;
    row.score = item.score;
    row.fp_abs_error_hz = abs(item.fp_hz - cfg.true_fp_hz);
    row.fa_abs_error_hz = abs(item.fa_hz - cfg.true_fa_hz);
    row.fa_correct = double(isfinite(item.fa_hz) && abs(item.fa_hz - cfg.true_fa_hz) <= cfg.fa_tolerance_hz);
    row.fp_correct = double(isfinite(item.fp_hz) && abs(item.fp_hz - cfg.true_fp_hz) <= cfg.fp_tolerance_hz);
    row.pair_correct = double(row.fa_correct == 1 && row.fp_correct == 1);
end


function signal = local_simulate_sparse_burst_signal(t, cfg, keepRate)
    fp = cfg.true_fp_hz;
    phi0 = deg2rad(cfg.phase_offset_deg);
    low = cfg.low_amp * sin(2 * pi * fp * t);

    cycleTimes = ((phi0 + pi / 2) / (2 * pi * fp)) + (0:ceil(t(end) * fp) + 2) / fp;
    cycleTimes = cycleTimes(cycleTimes >= t(1) - 1 / fp & cycleTimes <= t(end) + 1 / fp);

    keepMask = rand(size(cycleTimes)) <= keepRate;
    keptTimes = cycleTimes(keepMask) + cfg.burst_phase_jitter_s * randn(1, sum(keepMask));
    trueEnv = local_gaussian_burst_envelope(t, keptTimes, cfg.burst_sigma_s);
    if max(trueEnv) > 0
        trueEnv = trueEnv ./ max(trueEnv);
    end

    % Add weak burst-like background so scanned PAC methods may average
    % over diffuse structure when the true events become sparse.
    randTimes = linspace(t(1), t(end), numel(cycleTimes) + 2);
    randTimes = randTimes(2:end-1);
    randTimes = randTimes + (0.45 / fp) * (2 * rand(size(randTimes)) - 1);
    randTimes = min(max(randTimes, t(1)), t(end));
    bgEnv = local_gaussian_burst_envelope(t, randTimes, cfg.burst_sigma_s);
    if max(bgEnv) > 0
        bgEnv = bgEnv ./ max(bgEnv);
    end

    hfEnvelope = cfg.base_hf_amp + cfg.true_high_amp * (cfg.coupling_level * trueEnv + cfg.background_burst_scale * bgEnv);
    high = hfEnvelope .* sin(2 * pi * cfg.true_fa_hz * t);
    signal = low + high;
end


function env = local_gaussian_burst_envelope(t, eventTimes, sigmaS)
    env = zeros(size(t));
    for iEvent = 1:numel(eventTimes)
        env = env + exp(-0.5 * ((t - eventTimes(iEvent)) / sigmaS) .^ 2);
    end
end


function signalOut = local_add_mixed_noise(signalIn, snrDb)
    n = numel(signalIn);
    signalPower = mean(signalIn .^ 2);
    pink = local_powerlaw_noise(n, 1.0);
    white = randn(1, n);
    noiseMix = pink + 0.5 * white;
    noiseMix = noiseMix - mean(noiseMix);
    noiseMix = noiseMix ./ max(sqrt(mean(noiseMix .^ 2)), eps);
    noisePowerTarget = signalPower / (10 ^ (snrDb / 10));
    signalOut = signalIn + sqrt(noisePowerTarget) * noiseMix;
end


function x = local_powerlaw_noise(n, alpha)
    freqs = (0:(n - 1));
    amp = ones(1, n);
    valid = freqs > 0 & freqs <= floor(n / 2);
    amp(valid) = 1 ./ (freqs(valid) .^ (alpha / 2));
    phaseRand = 2 * pi * rand(1, n);
    spectrum = amp .* exp(1i * phaseRand);
    spectrum(1) = 0;

    if mod(n, 2) == 0
        posIdx = 2:(n / 2);
        negIdx = n:-1:(n / 2 + 2);
        spectrum(negIdx) = conj(spectrum(posIdx));
        spectrum(n / 2 + 1) = real(spectrum(n / 2 + 1));
    else
        posIdx = 2:((n + 1) / 2);
        negIdx = n:-1:((n + 3) / 2);
        spectrum(negIdx) = conj(spectrum(posIdx));
    end

    x = real(ifft(spectrum));
    x = x - mean(x);
    x = x ./ max(std(x), eps);
end


function out = local_run_apc(signal, time, cfg)
    sMatrix = struct('data', signal, 'time', time);
    options = struct( ...
        'fA', cfg.broad_fa_band_hz, ...
        'epoch', [-0.6 0.6], ...
        'decomposition', 'fft_peak', ...
        'metric', cfg.metric, ...
        'diagm', false, ...
        'surrogates', false, ...
        'num_perm', 0, ...
        'numPhaseBins', 18);

    sApc = bst_apc(sMatrix, options);
    out = struct();
    out.valid = double(sApc.status_code.Value(1)) == 0;
    out.status_code = double(sApc.status_code.Value(1));
    out.fp_hz = double(sApc.phase_frequency_hz.Value(1));
    out.fa_hz = double(sApc.amplitude_frequency_hz.Value(1));
    out.preferred_phase_deg = double(sApc.preferred_phase_deg.Value(1));
    out.score = double(sApc.pac_strength.Value(1));
    if ~out.valid
        out.fp_hz = NaN;
        out.fa_hz = NaN;
        out.preferred_phase_deg = NaN;
        out.score = 0;
    end
end


function out = local_scan_standard_pac(signal, cfg, metricName)
    fs = cfg.fs_hz;
    fpCandidates = cfg.phase_scan_hz(:).';
    faCandidates = cfg.amplitude_scan_hz(:).';
    lowPhase = cell(size(fpCandidates));
    highEnv = cell(size(faCandidates));

    for iFp = 1:numel(fpCandidates)
        band = [max(0.5, fpCandidates(iFp) - 1.5), fpCandidates(iFp) + 1.5];
        lowPhase{iFp} = angle(hilbert(local_bandpass(signal, fs, band(1), band(2))));
    end
    for iFa = 1:numel(faCandidates)
        band = [max(1.0, faCandidates(iFa) - 6.0), min(fs / 2 - 1.0, faCandidates(iFa) + 6.0)];
        highEnv{iFa} = abs(hilbert(local_bandpass(signal, fs, band(1), band(2))));
    end

    scoreMap = nan(numel(fpCandidates), numel(faCandidates));
    prefMap = nan(numel(fpCandidates), numel(faCandidates));
    for iFp = 1:numel(fpCandidates)
        for iFa = 1:numel(faCandidates)
            switch lower(metricName)
                case 'glm'
                    [scoreVal, prefDeg] = local_glm_pac_metric(lowPhase{iFp}, highEnv{iFa});
                otherwise
                    [scoreVal, prefDeg] = calc_MI_all_methods(lowPhase{iFp}, highEnv{iFa}, metricName, false, 0, 1, false, 18);
            end
            scoreMap(iFp, iFa) = scoreVal;
            prefMap(iFp, iFa) = prefDeg;
        end
    end

    [bestScore, idx] = max(scoreMap(:), [], 'omitnan');
    [iFpBest, iFaBest] = ind2sub(size(scoreMap), idx);
    out = struct();
    out.valid = isfinite(bestScore);
    out.status_code = double(~out.valid);
    if out.valid
        out.fp_hz = fpCandidates(iFpBest);
        out.fa_hz = faCandidates(iFaBest);
        out.preferred_phase_deg = prefMap(iFpBest, iFaBest);
        out.score = bestScore;
    else
        out.fp_hz = NaN;
        out.fa_hz = NaN;
        out.preferred_phase_deg = NaN;
        out.score = 0;
    end
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


function summaryTable = local_build_summary(runTable, methods)
    rows = cell(0, 22);
    condValues = unique(runTable.burst_keep_rate);
    for iCond = 1:numel(condValues)
        val = condValues(iCond);
        sub = runTable(abs(runTable.burst_keep_rate - val) < 1e-9, :);
        for iMethod = 1:numel(methods)
            methodName = methods(iMethod);
            methodSub = sub(sub.method == methodName, :);

            n = height(methodSub);
            [pairRate, pairCiLo, pairCiHi] = local_binomial_rate_ci(methodSub.pair_correct);
            [faRate, faCiLo, faCiHi]       = local_binomial_rate_ci(methodSub.fa_correct);
            [fpRate, fpCiLo, fpCiHi]       = local_binomial_rate_ci(methodSub.fp_correct);
            [faErrMean, faErrCiLo, faErrCiHi] = local_mean_ci(methodSub.fa_abs_error_hz);
            [fpErrMean, fpErrCiLo, fpErrCiHi] = local_mean_ci(methodSub.fp_abs_error_hz);

            rows(end+1, :) = { ...
                val, ...
                string(methodName), ...
                n, ...
                mean(methodSub.valid, 'omitnan'), ...
                pairRate, pairCiLo, pairCiHi, ...
                faRate, faCiLo, faCiHi, ...
                fpRate, fpCiLo, fpCiHi, ...
                median(methodSub.fa_abs_error_hz, 'omitnan'), ...
                median(methodSub.fp_abs_error_hz, 'omitnan'), ...
                faErrMean, faErrCiLo, faErrCiHi, ...
                fpErrMean, fpErrCiLo, fpErrCiHi}; %#ok<AGROW>
        end
    end

    summaryTable = cell2table(rows, 'VariableNames', { ...
        'burst_keep_rate', 'method', 'n_repeats', 'valid_rate', ...
        'pair_correct_rate', 'pair_correct_rate_ci_low', 'pair_correct_rate_ci_high', ...
        'fa_correct_rate', 'fa_correct_rate_ci_low', 'fa_correct_rate_ci_high', ...
        'fp_correct_rate', 'fp_correct_rate_ci_low', 'fp_correct_rate_ci_high', ...
        'median_fa_abs_error_hz', 'median_fp_abs_error_hz', ...
        'mean_fa_abs_error_hz', 'mean_fa_abs_error_hz_ci_low', 'mean_fa_abs_error_hz_ci_high', ...
        'mean_fp_abs_error_hz', 'mean_fp_abs_error_hz_ci_low', 'mean_fp_abs_error_hz_ci_high'});
end


function [m, ciLo, ciHi] = local_mean_ci(x)
    x = x(isfinite(x));
    n = numel(x);
    if n == 0
        m = NaN;
        ciLo = NaN;
        ciHi = NaN;
        return;
    end
    m = mean(x);
    if n > 1
        sem = std(x) / sqrt(n);
        delta = tinv(0.975, n - 1) * sem;
    else
        delta = 0;
    end
    ciLo = max(0, m - delta);
    ciHi = m + delta;
end


function [pHat, ciLo, ciHi] = local_binomial_rate_ci(x)
    x = x(isfinite(x));
    n = numel(x);
    if n == 0
        pHat = NaN;
        ciLo = NaN;
        ciHi = NaN;
        return;
    end

    k = sum(x ~= 0);
    pHat = k / n;
    z = 1.95996398454005;
    denom = 1 + (z ^ 2) / n;
    center = (pHat + (z ^ 2) / (2 * n)) / denom;
    halfWidth = (z / denom) * sqrt((pHat * (1 - pHat) / n) + ((z ^ 2) / (4 * n ^ 2)));
    ciLo = max(0, center - halfWidth);
    ciHi = min(1, center + halfWidth);
end


function fig = local_make_figure(cfg, summaryTable, runTable, methods)
    fig = figure('Color', 'w', 'Units', 'normalized', 'Position', [0.04 0.05 0.92 0.86], ...
        'Name', 'APC burst sparsity benchmark', 'Renderer', 'painters');

    tl = tiledlayout(fig, 2, 2, 'Padding', 'compact', 'TileSpacing', 'compact');
    tl.OuterPosition = [0.05 0.05 0.90 0.80];

    annotation(fig, 'textbox', [0.10 0.90 0.80 0.06], ...
        'String', 'Dominant-Mode Recovery as True Coupled Bursts Become Sparse', ...
        'EdgeColor', 'none', ...
        'HorizontalAlignment', 'center', ...
        'VerticalAlignment', 'middle', ...
        'FontWeight', 'bold', 'FontSize', 17, 'FontName', 'Helvetica');

    ax1 = nexttile(tl, 1);
    local_plot_summary_curve(ax1, summaryTable, methods, cfg.burst_keep_rates, ...
        'pair_correct_rate', 'pair_correct_rate_ci_low', 'pair_correct_rate_ci_high', ...
        'True burst keep rate', 'Correct pair recovery rate', 'A  Joint recovery of the true coupling pair', false);
    ylim(ax1, [0 1]);
    yticks(ax1, 0:0.2:1);

    ax2 = nexttile(tl, 2);
    local_plot_summary_curve(ax2, summaryTable, methods, cfg.burst_keep_rates, ...
        'fa_correct_rate', 'fa_correct_rate_ci_low', 'fa_correct_rate_ci_high', ...
        'True burst keep rate', 'Correct f_A recovery rate', 'B  Recovery of the true burst-locked f_A band', false);
    ylim(ax2, [0 1]);
    yticks(ax2, 0:0.2:1);

    ax3 = nexttile(tl, 3);
    local_plot_summary_curve(ax3, summaryTable, methods, cfg.burst_keep_rates, ...
        'mean_fa_abs_error_hz', 'mean_fa_abs_error_hz_ci_low', 'mean_fa_abs_error_hz_ci_high', ...
        'True burst keep rate', '|f_A error| (Hz)', 'C  High-frequency carrier recovery error', false);
    local_apply_log_error_axis(ax3);

    ax4 = nexttile(tl, 4);
    local_plot_summary_curve(ax4, summaryTable, methods, cfg.burst_keep_rates, ...
        'mean_fp_abs_error_hz', 'mean_fp_abs_error_hz_ci_low', 'mean_fp_abs_error_hz_ci_high', ...
        'True burst keep rate', '|f_P error| (Hz)', 'D  Phase-carrier recovery error', false);
    local_apply_log_error_axis(ax4);

    lgd = legend(ax1, 'Orientation', 'horizontal', 'Box', 'off', 'FontSize', 12);
    lgd.Units = 'normalized';
    drawnow;
    lgd.Position(1) = 0.5 - lgd.Position(3) / 2;
    lgd.Position(2) = 0.855;
end


function fig = local_make_endpoint_rawpoint_figure(cfg, runTable, methods)
    fig = figure('Color', 'w', 'Units', 'normalized', 'Position', [0.12 0.12 0.72 0.42], ...
        'Name', 'APC burst sparsity endpoint raw points', 'Renderer', 'painters');

    tl = tiledlayout(fig, 1, 2, 'Padding', 'compact', 'TileSpacing', 'compact');
    tl.OuterPosition = [0.05 0.08 0.92 0.80];

    annotation(fig, 'textbox', [0.10 0.89 0.80 0.08], ...
        'String', 'Supplementary per-trial endpoint distributions for the burst sparsity benchmark', ...
        'EdgeColor', 'none', ...
        'HorizontalAlignment', 'center', ...
        'VerticalAlignment', 'middle', ...
        'FontWeight', 'bold', 'FontSize', 16, 'FontName', 'Helvetica');

    style = local_method_styles();
    keepLow = min(cfg.burst_keep_rates);
    keepHigh = max(cfg.burst_keep_rates);

    ax1 = nexttile(tl, 1);
    keepLowSub = runTable(abs(runTable.burst_keep_rate - keepLow) < 1e-9, :);
    local_plot_rawpoint_group(ax1, keepLowSub, methods, 'fa_abs_error_hz', style);
    title(ax1, sprintf('E  Per-trial |f_A error| distribution (keep rate = %.2f; n = %d repeats/method)', ...
        keepLow, sum(keepLowSub.method == methods(1))), 'FontWeight', 'bold', 'FontSize', 13);
    ylabel(ax1, '|f_A error| (Hz)');
    xlabel(ax1, 'Method');
    set(ax1, 'FontName', 'Helvetica', 'FontSize', 12, 'LineWidth', 1.1);
    box(ax1, 'off');

    ax2 = nexttile(tl, 2);
    keepHighSub = runTable(abs(runTable.burst_keep_rate - keepHigh) < 1e-9, :);
    local_plot_rawpoint_group(ax2, keepHighSub, methods, 'fa_abs_error_hz', style);
    title(ax2, sprintf('F  Per-trial |f_A error| distribution (keep rate = %.2f; n = %d repeats/method)', ...
        keepHigh, sum(keepHighSub.method == methods(1))), 'FontWeight', 'bold', 'FontSize', 13);
    ylabel(ax2, '|f_A error| (Hz)');
    xlabel(ax2, 'Method');
    set(ax2, 'FontName', 'Helvetica', 'FontSize', 12, 'LineWidth', 1.1);
    box(ax2, 'off');
end


function local_apply_log_error_axis(ax)
    set(ax, 'YScale', 'log');
    ax.YMinorGrid = 'on';
end


function local_plot_summary_curve(ax, summaryTable, methods, xValues, fieldName, ciLowFieldName, ciHighFieldName, xLabelText, yLabelText, titleText, showLegend)
    style = local_method_styles();
    hold(ax, 'on');

    logFloor = 0.05;
    for iMethod = 1:numel(methods)
        methodName = methods(iMethod);
        sub = summaryTable(summaryTable.method == methodName, :);
        y = nan(size(xValues));
        yErrLo = nan(size(xValues));
        yErrHi = nan(size(xValues));
        for iX = 1:numel(xValues)
            idx = find(abs(sub.burst_keep_rate - xValues(iX)) < 1e-9, 1);
            if ~isempty(idx)
                y(iX) = sub.(fieldName)(idx);
                yErrLo(iX) = sub.(fieldName)(idx) - sub.(ciLowFieldName)(idx);
                yErrHi(iX) = sub.(ciHighFieldName)(idx) - sub.(fieldName)(idx);
            end
        end

        yPlot = y;
        if strcmp(ax.YScale, 'log')
            yPlot(yPlot < logFloor) = logFloor;
            yErrLo = min(yErrLo, max(yPlot - logFloor, 0));
        end

        styleKey = local_style_key(methodName);
        errorbar(ax, xValues, yPlot, yErrLo, yErrHi, ...
            'Color', style.(styleKey).color, ...
            'LineStyle', style.(styleKey).line, ...
            'Marker', style.(styleKey).marker, ...
            'LineWidth', 1.6, ...
            'MarkerSize', 7, ...
            'CapSize', 4, ...
            'DisplayName', char(methodName));
    end
    xlabel(ax, xLabelText);
    ylabel(ax, yLabelText);
    title(ax, titleText, 'FontWeight', 'bold', 'FontSize', 13);
    xlim(ax, [min(xValues) max(xValues)]);
    if showLegend
        legend(ax, 'Location', 'southwest', 'Box', 'off', 'FontSize', 11);
    end
    set(ax, 'FontName', 'Helvetica', 'FontSize', 12, 'LineWidth', 1.1);
    grid(ax, 'on');
    box(ax, 'off');
end


function local_plot_rawpoint_group(ax, condSub, methods, fieldName, style)
    hold(ax, 'on');
    nMethods = numel(methods);
    jitterWidth = 0.11;

    allVals = condSub.(fieldName);
    allVals = allVals(isfinite(allVals));
    if isempty(allVals)
        yPad = 1;
        yMin = 0;
    else
        yMin = min(0, min(allVals));
        yPad = 0.05 * max(1, max([yMin; allVals(:)]) - min([yMin; allVals(:)]));
    end

    for iMethod = 1:nMethods
        methodName = methods(iMethod);
        xCenter = iMethod;
        vals = condSub.(fieldName)(condSub.method == methodName);
        vals = vals(isfinite(vals));
        styleKey = local_style_key(methodName);
        color = style.(styleKey).color;

        if ~isempty(vals)
            xJitter = xCenter + jitterWidth * (rand(size(vals)) - 0.5) * 2;
            scatter(ax, xJitter, vals, 24, color, 'filled', ...
                'MarkerFaceAlpha', 0.65, 'MarkerEdgeColor', 'none');
        end

        if ~isempty(vals)
            med = median(vals);
            q1 = local_percentile(vals, 25);
            q3 = local_percentile(vals, 75);
            plot(ax, [xCenter - 0.16, xCenter + 0.16], [med med], ...
                'Color', color, 'LineWidth', 2.2);
            plot(ax, [xCenter xCenter], [q1 q3], 'Color', color, 'LineWidth', 1.0);
        end
    end

    xlim(ax, [0.4, nMethods + 0.6]);
    xticks(ax, 1:nMethods);
    xticklabels(ax, cellstr(methods));
    xtickangle(ax, 0);
    if ~isempty(allVals)
        ylim(ax, [yMin - yPad, max(allVals) + yPad]);
    end
    grid(ax, 'off');
end


function p = local_percentile(x, pct)
    x = sort(double(x(:)));
    n = numel(x);
    if n == 0
        p = NaN;
        return;
    end
    if n == 1
        p = x(1);
        return;
    end
    rank = (pct / 100) * (n - 1) + 1;
    lo = floor(rank);
    hi = ceil(rank);
    frac = rank - lo;
    p = x(lo) + frac * (x(hi) - x(lo));
end


function [xi, f] = local_kde(x, nPoints)
    x = double(x(:));
    n = numel(x);
    sigma = std(x);
    iqrVal = local_percentile(x, 75) - local_percentile(x, 25);
    spread = min(sigma, iqrVal / 1.34);
    if ~isfinite(spread) || spread <= 0
        spread = max(sigma, eps);
    end
    if ~isfinite(spread) || spread <= 0
        spread = max(max(x) - min(x), 1) / 10;
    end
    bw = 0.9 * spread * n ^ (-1 / 5);
    bw = max(bw, eps);

    pad = 3 * bw;
    xi = linspace(min(x) - pad, max(x) + pad, nPoints);
    f = zeros(1, nPoints);
    for i = 1:n
        f = f + exp(-0.5 * ((xi - x(i)) / bw) .^ 2);
    end
    f = f / (n * bw * sqrt(2 * pi));
end


function style = local_method_styles()
    style.APC.color = [0.84 0.37 0.00];
    style.APC.line = '-';
    style.APC.marker = 'o';

    style.MVLscan.color = [0.00 0.45 0.70];
    style.MVLscan.line = '-';
    style.MVLscan.marker = '+';

    style.KLMIscan.color = [0.10 0.10 0.10];
    style.KLMIscan.line = '-';
    style.KLMIscan.marker = '*';

    style.GLMscan.color = [0.00 0.62 0.45];
    style.GLMscan.line = '-';
    style.GLMscan.marker = '>';
end


function key = local_style_key(methodName)
    switch string(methodName)
        case "APC"
            key = 'APC';
        case "MVL-scan"
            key = 'MVLscan';
        case "KLMI-scan"
            key = 'KLMIscan';
        case "GLM-scan"
            key = 'GLMscan';
        otherwise
            error('Unknown method name: %s', methodName);
    end
end
