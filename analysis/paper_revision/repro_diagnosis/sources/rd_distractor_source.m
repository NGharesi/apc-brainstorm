function varargout = rd_distractor_source(action,varargin)
% Dispatch into copied historical functions. Generator/noise prefix unchanged.
    switch action
        case 'profile'
            varargout{1}=local_get_profile(varargin{1});
        case 'generate'
            cfg=varargin{1};distractorScale=varargin{2};
    t = 0:(1 / cfg.fs_hz):(cfg.duration_s - 1 / cfg.fs_hz);
    coupledSignal = local_simulate_distractor_signal(t, cfg, distractorScale, 'coupled');
    nullSignal = local_simulate_distractor_signal(t, cfg, distractorScale, 'null');
    coupledSignal = local_add_mixed_noise(coupledSignal, cfg.snr_db);
    nullSignal = local_add_mixed_noise(nullSignal, cfg.snr_db);


            varargout{1}=coupledSignal;varargout{2}=t;
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
    cfg.duration_s = 6.0;
    cfg.true_fp_hz = 8.0;
    cfg.true_fa_hz = 120.0;
    cfg.distractor_fa_hz = 96.0;
    cfg.phase_offset_deg = -90;
    cfg.low_amp = 1.0;
    cfg.true_high_amp = 1.3;
    cfg.distractor_base_amp = 0.6;
    cfg.base_hf_amp = 0.08;
    cfg.burst_sigma_s = 0.028;
    cfg.coupling_level = 0.60;
    cfg.burst_phase_jitter_s = 0.010;
    cfg.snr_db = -3.0;
    cfg.broad_fa_band_hz = [80 150];
    cfg.phase_scan_hz = 4:1:12;
    cfg.amplitude_scan_hz = 80:8:152;
    cfg.phase_band_half_width_hz = 1.5;
    cfg.amplitude_band_half_width_hz = 6.0;
    cfg.metric = 'canolty';
    cfg.fa_tolerance_hz = 8.0;
    cfg.fp_tolerance_hz = 1.0;
    cfg.oracle_control_distractor_scale = 0.0;

    switch profileName
        case "fast"
            cfg.n_repeats = 10;
            cfg.distractor_scale_values = [0.0 0.5 1.0 1.5 2.0 2.5];
        case "full"
            cfg.n_repeats = 25;
            cfg.distractor_scale_values = [0.0 0.5 1.0 1.5 2.0 2.5 3.0];
        case "reviewer_control"
            % Full replication of the reviewer-requested fixed-pair control.
            cfg.n_repeats = 25;
            cfg.distractor_scale_values = [0.0 0.5 1.0 1.5 2.0 2.5 3.0];
        otherwise
            error('Unknown profileName: %s', profileName);
    end
end


function [trialRows, oracleRows] = local_run_trial(cfg, distractorScale, repIdx)
    t = 0:(1 / cfg.fs_hz):(cfg.duration_s - 1 / cfg.fs_hz);
    coupledSignal = local_simulate_distractor_signal(t, cfg, distractorScale, 'coupled');
    nullSignal = local_simulate_distractor_signal(t, cfg, distractorScale, 'null');
    coupledSignal = local_add_mixed_noise(coupledSignal, cfg.snr_db);
    nullSignal = local_add_mixed_noise(nullSignal, cfg.snr_db);

    apcResult = local_run_apc(coupledSignal, t, cfg);
    mvlScan = local_scan_standard_pac(coupledSignal, cfg, 'canolty');
    klmiScan = local_scan_standard_pac(coupledSignal, cfg, 'tort');
    glmScan = local_scan_standard_pac(coupledSignal, cfg, 'glm');

    trialRows = {
        local_pack_row("APC", distractorScale, repIdx, apcResult, cfg), ...
        local_pack_row("MVL-scan", distractorScale, repIdx, mvlScan, cfg), ...
        local_pack_row("KLMI-scan", distractorScale, repIdx, klmiScan, cfg), ...
        local_pack_row("GLM-scan", distractorScale, repIdx, glmScan, cfg)};

    oracleRows = {
        local_pack_oracle_row("MVL-fixed", "coupled", distractorScale, repIdx, ...
            local_fixed_standard_pac(coupledSignal, cfg, 'canolty', cfg.true_fp_hz, cfg.true_fa_hz)), ...
        local_pack_oracle_row("KLMI-fixed", "coupled", distractorScale, repIdx, ...
            local_fixed_standard_pac(coupledSignal, cfg, 'tort', cfg.true_fp_hz, cfg.true_fa_hz)), ...
        local_pack_oracle_row("GLM-fixed", "coupled", distractorScale, repIdx, ...
            local_fixed_standard_pac(coupledSignal, cfg, 'glm', cfg.true_fp_hz, cfg.true_fa_hz)), ...
        local_pack_oracle_row("MVL-fixed", "null", distractorScale, repIdx, ...
            local_fixed_standard_pac(nullSignal, cfg, 'canolty', cfg.true_fp_hz, cfg.true_fa_hz)), ...
        local_pack_oracle_row("KLMI-fixed", "null", distractorScale, repIdx, ...
            local_fixed_standard_pac(nullSignal, cfg, 'tort', cfg.true_fp_hz, cfg.true_fa_hz)), ...
        local_pack_oracle_row("GLM-fixed", "null", distractorScale, repIdx, ...
            local_fixed_standard_pac(nullSignal, cfg, 'glm', cfg.true_fp_hz, cfg.true_fa_hz))};
end


function row = local_pack_row(methodName, distractorScale, repIdx, item, cfg)
    row = struct();
    row.method = string(methodName);
    row.distractor_scale = distractorScale;
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
    row.phase_abs_error_deg = local_circular_abs_error(item.preferred_phase_deg, cfg.phase_offset_deg);
end


function row = local_pack_oracle_row(methodName, signalCondition, distractorScale, repIdx, item)
    row = struct();
    row.method = string(methodName);
    row.signal_condition = string(signalCondition);
    row.distractor_scale = distractorScale;
    row.repeat_index = repIdx;
    row.valid = item.valid;
    row.status_code = item.status_code;
    row.fixed_fp_hz = item.fp_hz;
    row.fixed_fa_hz = item.fa_hz;
    row.preferred_phase_deg = item.preferred_phase_deg;
    row.score = item.score;
end


function signal = local_simulate_distractor_signal(t, cfg, distractorScale, couplingMode)
    if nargin < 4 || isempty(couplingMode)
        couplingMode = 'coupled';
    end

    fp = cfg.true_fp_hz;
    phi0 = deg2rad(cfg.phase_offset_deg);

    low = cfg.low_amp * sin(2 * pi * fp * t);

    cycleTimes = ((phi0 + pi / 2) / (2 * pi * fp)) + (0:ceil(t(end) * fp) + 2) / fp;
    cycleTimes = cycleTimes(cycleTimes >= t(1) - 1 / fp & cycleTimes <= t(end) + 1 / fp);

    if strcmpi(couplingMode, 'coupled')
        coupledTimes = cycleTimes + cfg.burst_phase_jitter_s * randn(size(cycleTimes));
    else
        coupledTimes = linspace(t(1), t(end), numel(cycleTimes) + 2);
        coupledTimes = coupledTimes(2:end-1);
        coupledTimes = coupledTimes + 0.45 / fp * (2 * rand(size(coupledTimes)) - 1);
        coupledTimes = min(max(coupledTimes, t(1)), t(end));
    end
    trueEnv = zeros(size(t));
    for iCycle = 1:numel(coupledTimes)
        trueEnv = trueEnv + exp(-0.5 * ((t - coupledTimes(iCycle)) / cfg.burst_sigma_s) .^ 2);
    end
    if max(trueEnv) > 0
        trueEnv = trueEnv ./ max(trueEnv);
    end

    randTimes = linspace(t(1), t(end), numel(cycleTimes) + 2);
    randTimes = randTimes(2:end-1);
    randTimes = randTimes + 0.45 / fp * (2 * rand(size(randTimes)) - 1);
    randTimes = min(max(randTimes, t(1)), t(end));
    distractorEnv = zeros(size(t));
    for iRand = 1:numel(randTimes)
        distractorEnv = distractorEnv + exp(-0.5 * ((t - randTimes(iRand)) / cfg.burst_sigma_s) .^ 2);
    end
    if max(distractorEnv) > 0
        distractorEnv = distractorEnv ./ max(distractorEnv);
    end

    trueHfEnvelope = cfg.base_hf_amp + cfg.true_high_amp * cfg.coupling_level * trueEnv;
    distractorEnvelope = cfg.base_hf_amp + cfg.distractor_base_amp * distractorScale * distractorEnv;

    trueHf = trueHfEnvelope .* sin(2 * pi * cfg.true_fa_hz * t);
    distractorHf = distractorEnvelope .* sin(2 * pi * cfg.distractor_fa_hz * t + 2 * pi * rand());
    signal = low + trueHf + distractorHf;
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
    noiseScaled = sqrt(noisePowerTarget) * noiseMix;
    signalOut = signalIn + noiseScaled;
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
            switch lower(metricName)
                case 'glm'
                    [scoreVal, prefDeg] = local_glm_pac_metric(phaseAngles, ampEnv);
                otherwise
                    [scoreVal, prefDeg] = calc_MI_all_methods(phaseAngles, ampEnv, metricName, false, 0, 1, false, 18);
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


function out = local_fixed_standard_pac(signal, cfg, metricName, fpHz, faHz)
    fs = cfg.fs_hz;
    lowBand = [max(0.5, fpHz - cfg.phase_band_half_width_hz), fpHz + cfg.phase_band_half_width_hz];
    highBand = [max(1.0, faHz - cfg.amplitude_band_half_width_hz), ...
        min(fs / 2 - 1.0, faHz + cfg.amplitude_band_half_width_hz)];

    lowSig = local_bandpass(signal, fs, lowBand(1), lowBand(2));
    highSig = local_bandpass(signal, fs, highBand(1), highBand(2));
    phaseAngles = angle(hilbert(lowSig(:)));
    ampEnv = abs(hilbert(highSig(:)));

    switch lower(metricName)
        case 'glm'
            [scoreVal, prefDeg] = local_glm_pac_metric(phaseAngles, ampEnv);
        otherwise
            [scoreVal, prefDeg] = calc_MI_all_methods(phaseAngles, ampEnv, metricName, false, 0, 1, false, 18);
    end

    out = struct();
    out.valid = isfinite(scoreVal);
    out.status_code = double(~out.valid);
    out.fp_hz = fpHz;
    out.fa_hz = faHz;
    out.preferred_phase_deg = prefDeg;
    out.score = scoreVal;

    if ~out.valid
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


function errDeg = local_circular_abs_error(aDeg, bDeg)
    if ~isfinite(aDeg) || ~isfinite(bDeg)
        errDeg = NaN;
        return;
    end
    delta = mod(aDeg - bDeg + 180, 360) - 180;
    errDeg = abs(delta);
end


function summaryTable = local_build_summary(runTable, methods)
    rows = cell(0, 16);
    condValues = unique(runTable.distractor_scale);

    for iCond = 1:numel(condValues)
        val = condValues(iCond);
        sub = runTable(abs(runTable.distractor_scale - val) < 1e-9, :);
        for iMethod = 1:numel(methods)
            methodName = methods(iMethod);
            methodSub = sub(sub.method == methodName, :);
            n = height(methodSub);

            [pairRate, pairSem]   = local_mean_sem(methodSub.pair_correct);
            [faRate, faRateSem]   = local_mean_sem(methodSub.fa_correct);
            [fpRate, fpRateSem]   = local_mean_sem(methodSub.fp_correct);
            [faErrMean, faErrSem] = local_mean_sem(methodSub.fa_abs_error_hz);
            [fpErrMean, fpErrSem] = local_mean_sem(methodSub.fp_abs_error_hz);

            rows(end+1, :) = { ...
                val, ...
                string(methodName), ...
                n, ...
                mean(methodSub.valid, 'omitnan'), ...
                pairRate, pairSem, ...
                faRate, faRateSem, ...
                fpRate, fpRateSem, ...
                median(methodSub.fa_abs_error_hz, 'omitnan'), ...
                median(methodSub.fp_abs_error_hz, 'omitnan'), ...
                faErrMean, faErrSem, ...
                fpErrMean, fpErrSem}; %#ok<AGROW>
        end
    end

    summaryTable = cell2table(rows, 'VariableNames', { ...
        'distractor_scale', 'method', 'n_repeats', 'valid_rate', ...
        'pair_correct_rate', 'pair_correct_rate_sem', ...
        'fa_correct_rate', 'fa_correct_rate_sem', ...
        'fp_correct_rate', 'fp_correct_rate_sem', ...
        'median_fa_abs_error_hz', 'median_fp_abs_error_hz', ...
        'mean_fa_abs_error_hz', 'mean_fa_abs_error_hz_sem', ...
        'mean_fp_abs_error_hz', 'mean_fp_abs_error_hz_sem'});
end


function [m, sem] = local_mean_sem(x)
    x = x(isfinite(x));
    n = numel(x);
    if n == 0
        m = NaN;
        sem = NaN;
        return;
    end
    m = mean(x);
    if n > 1
        sem = std(x) / sqrt(n);
    else
        sem = 0;
    end
end


function summaryTable = local_build_oracle_summary(oracleTable)
    methods = unique(oracleTable.method, 'stable');
    conds = unique(oracleTable.signal_condition, 'stable');
    scales = unique(oracleTable.distractor_scale);
    rows = cell(0, 8);

    for iScale = 1:numel(scales)
        scaleVal = scales(iScale);
        scaleSub = oracleTable(abs(oracleTable.distractor_scale - scaleVal) < 1e-9, :);
        for iMethod = 1:numel(methods)
            methodName = methods(iMethod);
            for iCond = 1:numel(conds)
                condName = conds(iCond);
                sub = scaleSub(scaleSub.method == methodName & scaleSub.signal_condition == condName, :);
                [meanScore, semScore] = local_mean_sem(sub.score);
                rows(end+1, :) = { ...
                    scaleVal, string(methodName), string(condName), height(sub), ...
                    meanScore, semScore, ...
                    median(sub.score, 'omitnan'), ...
                    local_percentile(sub.score, 75) - local_percentile(sub.score, 25)}; %#ok<AGROW>
            end
        end
    end

    summaryTable = cell2table(rows, 'VariableNames', { ...
        'distractor_scale', 'method', 'signal_condition', 'n_repeats', ...
        'mean_score', 'mean_score_sem', 'median_score', 'iqr_score'});
end


function aucTable = local_build_oracle_auc_table(oracleTable)
    methods = unique(oracleTable.method, 'stable');
    scales = unique(oracleTable.distractor_scale);
    rows = cell(0, 5);

    for iScale = 1:numel(scales)
        scaleVal = scales(iScale);
        scaleSub = oracleTable(abs(oracleTable.distractor_scale - scaleVal) < 1e-9, :);
        for iMethod = 1:numel(methods)
            methodName = methods(iMethod);
            coupled = scaleSub.score(scaleSub.method == methodName & scaleSub.signal_condition == "coupled");
            nullVals = scaleSub.score(scaleSub.method == methodName & scaleSub.signal_condition == "null");
            aucVal = local_pairwise_auc(coupled, nullVals);
            rows(end+1, :) = { ...
                scaleVal, string(methodName), numel(coupled), numel(nullVals), aucVal}; %#ok<AGROW>
        end
    end

    aucTable = cell2table(rows, 'VariableNames', { ...
        'distractor_scale', 'method', 'n_coupled', 'n_null', 'auc_coupled_vs_null'});
end


function aucVal = local_pairwise_auc(posVals, negVals)
    posVals = double(posVals(:));
    negVals = double(negVals(:));
    posVals = posVals(isfinite(posVals));
    negVals = negVals(isfinite(negVals));
    if isempty(posVals) || isempty(negVals)
        aucVal = NaN;
        return;
    end

    wins = 0;
    ties = 0;
    total = 0;
    for iPos = 1:numel(posVals)
        for iNeg = 1:numel(negVals)
            total = total + 1;
            if posVals(iPos) > negVals(iNeg)
                wins = wins + 1;
            elseif posVals(iPos) == negVals(iNeg)
                ties = ties + 1;
            end
        end
    end
    aucVal = (wins + 0.5 * ties) / total;
end


function fig = local_make_figure(cfg, summaryTable, runTable, methods)
    fig = figure( ...
        'Color', 'w', ...
        'Units', 'normalized', ...
        'Position', [0.10 0.10 0.80 0.76], ...
        'Name', 'APC distractor benchmark', ...
        'Renderer', 'painters');

    % Main text: compact recovery and error summary only (panels A-D).
    tl = tiledlayout(fig, 2, 2, 'Padding', 'compact', 'TileSpacing', 'compact');
    tl.OuterPosition = [0.05 0.06 0.90 0.74];

    annotation(fig, 'textbox', [0.10 0.89 0.80 0.05], ...
        'String', 'Dominant-Mode Recovery with a Competing High-Frequency Distractor', ...
        'EdgeColor', 'none', ...
        'HorizontalAlignment', 'center', ...
        'VerticalAlignment', 'middle', ...
        'FontWeight', 'bold', 'FontSize', 16, 'FontName', 'Helvetica');

    ax1 = nexttile(tl, 1);
    local_plot_recovery_curve(ax1, summaryTable, methods, cfg.distractor_scale_values, ...
        'pair_correct_rate', 'Distractor amplitude scale (relative)', ...
        'Correct pair recovery rate', 'A  Joint recovery of the true coupling pair', false);
    ylim(ax1, [0 1]);
    yticks(ax1, 0:0.2:1);

    ax2 = nexttile(tl, 2);
    local_plot_recovery_curve(ax2, summaryTable, methods, cfg.distractor_scale_values, ...
        'fa_correct_rate', 'Distractor amplitude scale (relative)', ...
        'Correct f_A recovery rate', 'B  Recovery of the true burst-locked f_A band', false);
    ylim(ax2, [0 1]);
    yticks(ax2, 0:0.2:1);

    ax3 = nexttile(tl, 3);
    local_plot_summary_curve(ax3, summaryTable, methods, cfg.distractor_scale_values, ...
        'mean_fa_abs_error_hz', 'mean_fa_abs_error_hz_sem', 'Distractor amplitude scale (relative)', ...
        '|f_A error| (Hz)', 'C  High-frequency carrier recovery error', false);
    local_apply_log_error_axis(ax3);

    ax4 = nexttile(tl, 4);
    local_plot_summary_curve(ax4, summaryTable, methods, cfg.distractor_scale_values, ...
        'mean_fp_abs_error_hz', 'mean_fp_abs_error_hz_sem', 'Distractor amplitude scale (relative)', ...
        '|f_P error| (Hz)', 'D  Phase-carrier recovery error', false);
    local_apply_log_error_axis(ax4);

    % Ask the tiled layout to reserve a dedicated legend row above panels.
    lgd = legend(ax1, 'Orientation', 'horizontal', 'Box', 'off', 'FontSize', 11);
    lgd.Layout.Tile = 'north';
end


function fig = local_make_endpoint_figure(cfg, runTable, methods)
    fig = figure( ...
        'Color', 'w', ...
        'Units', 'normalized', ...
        'Position', [0.14 0.18 0.72 0.56], ...
        'Name', 'APC distractor endpoint distributions', ...
        'Renderer', 'painters');
    tl = tiledlayout(fig, 1, 2, 'Padding', 'compact', 'TileSpacing', 'compact');
    tl.OuterPosition = [0.05 0.08 0.90 0.74];
    annotation(fig, 'textbox', [0.10 0.88 0.80 0.05], ...
        'String', 'Endpoint Distributions of High-Frequency Carrier Error', ...
        'EdgeColor', 'none', 'HorizontalAlignment', 'center', ...
        'VerticalAlignment', 'middle', 'FontWeight', 'bold', ...
        'FontSize', 16, 'FontName', 'Helvetica');

    condLow = min(cfg.distractor_scale_values);
    condHigh = max(cfg.distractor_scale_values);
    style = local_method_styles();

    ax5 = nexttile(tl, 1);
    condLowSub = runTable(abs(runTable.distractor_scale - condLow) < 1e-9, :);
    local_plot_raw_point_group(ax5, condLowSub, methods, 'fa_abs_error_hz', style);
    title(ax5, sprintf('E  Per-trial |f_A error| (amplitude scale = %.1f)', condLow), ...
        'FontWeight', 'bold', 'FontSize', 13);
    ylabel(ax5, '|f_A error| (Hz)');
    xlabel(ax5, 'Method');
    set(ax5, 'FontName', 'Helvetica', 'FontSize', 12, 'LineWidth', 1.1);
    box(ax5, 'off');

    ax6 = nexttile(tl, 2);
    condHighSub = runTable(abs(runTable.distractor_scale - condHigh) < 1e-9, :);
    local_plot_raw_point_group(ax6, condHighSub, methods, 'fa_abs_error_hz', style);
    title(ax6, sprintf('F  Per-trial |f_A error| (amplitude scale = %.1f)', condHigh), ...
        'FontWeight', 'bold', 'FontSize', 13);
    ylabel(ax6, '|f_A error| (Hz)');
    xlabel(ax6, 'Method');
    set(ax6, 'FontName', 'Helvetica', 'FontSize', 12, 'LineWidth', 1.1);
    box(ax6, 'off');
end


function fig = local_make_oracle_figure(cfg, oracleTable, aucTable)
    fig = figure( ...
        'Color', 'w', ...
        'Units', 'normalized', ...
        'Position', [0.12 0.18 0.72 0.58], ...
        'Name', 'APC distractor oracle control', ...
        'Renderer', 'painters');

    tl = tiledlayout(fig, 1, 2, 'Padding', 'compact', 'TileSpacing', 'compact');
    tl.OuterPosition = [0.05 0.07 0.90 0.73];

    annotation(fig, 'textbox', [0.08 0.88 0.84 0.06], ...
        'String', sprintf(['Fixed-Pair Positive Control at the Known Simulated Pair ' ...
        '(f_P = %.1f Hz, f_A = %.1f Hz)'], cfg.true_fp_hz, cfg.true_fa_hz), ...
        'EdgeColor', 'none', ...
        'HorizontalAlignment', 'center', ...
        'VerticalAlignment', 'middle', ...
        'FontWeight', 'bold', 'FontSize', 15, 'FontName', 'Helvetica');

    ax1 = nexttile(tl, 1);
    hold(ax1, 'on');
    style = local_method_styles();
    oracleMethods = ["MVL-fixed","KLMI-fixed","GLM-fixed"];
    conds = ["coupled","null"];
    offsets = [-0.16 0.16];
    condColors = [0.10 0.45 0.85; 0.60 0.60 0.60];
    hCoupled = gobjects(1);
    hNull = gobjects(1);

    for iMethod = 1:numel(oracleMethods)
        m = oracleMethods(iMethod);
        for iCond = 1:numel(conds)
            c = conds(iCond);
            vals = oracleTable.score(oracleTable.method == m & ...
                oracleTable.signal_condition == c & ...
                abs(oracleTable.distractor_scale - cfg.oracle_control_distractor_scale) < 1e-9);
            xCenter = iMethod + offsets(iCond);
            xJitter = xCenter + 0.045 * (rand(size(vals)) - 0.5) * 2;
            h = scatter(ax1, xJitter, vals, 22, condColors(iCond, :), 'filled', ...
                'MarkerFaceAlpha', 0.55, 'MarkerEdgeColor', 'none');
            if iMethod == 1 && iCond == 1
                hCoupled = h;
            elseif iMethod == 1 && iCond == 2
                hNull = h;
            end
            if ~isempty(vals)
                med = median(vals, 'omitnan');
                q1 = local_percentile(vals, 25);
                q3 = local_percentile(vals, 75);
                plot(ax1, [xCenter - 0.08, xCenter + 0.08], [med med], ...
                    'Color', condColors(iCond, :), 'LineWidth', 2.0, 'HandleVisibility', 'off');
                plot(ax1, [xCenter xCenter], [q1 q3], ...
                    'Color', condColors(iCond, :), 'LineWidth', 1.0, 'HandleVisibility', 'off');
            end
        end
    end

    xticks(ax1, 1:numel(oracleMethods));
    xticklabels(ax1, {'MVL-fixed','KLMI-fixed','GLM-fixed'});
    ylabel(ax1, 'PAC score at the known pair');
    xlabel(ax1, 'Comparator method');
    title(ax1, sprintf('A  Zero-distractor oracle control (scale = %.1f)', cfg.oracle_control_distractor_scale), ...
        'FontWeight', 'bold', 'FontSize', 13);
    grid(ax1, 'off');
    box(ax1, 'off');
    set(ax1, 'FontName', 'Helvetica', 'FontSize', 12, 'LineWidth', 1.1);
    legend(ax1, [hCoupled hNull], {'Coupled','Null'}, 'Location', 'northwest', 'Box', 'off');

    ax2 = nexttile(tl, 2);
    hold(ax2, 'on');
    scales = cfg.distractor_scale_values;
    for iMethod = 1:numel(oracleMethods)
        m = oracleMethods(iMethod);
        y = nan(size(scales));
        for iScale = 1:numel(scales)
            idx = find(aucTable.method == m & ...
                abs(aucTable.distractor_scale - scales(iScale)) < 1e-9, 1);
            if ~isempty(idx)
                y(iScale) = aucTable.auc_coupled_vs_null(idx);
            end
        end
        key = local_style_key(erase(m, '-fixed') + "-scan");
        plot(ax2, scales, y, 'Color', style.(key).color, 'LineWidth', 2.0, ...
            'Marker', style.(key).marker, 'MarkerSize', 7, 'DisplayName', char(m));
    end
    ylim(ax2, [0.5 1.0]);
    xlim(ax2, [min(scales) max(scales)]);
    ylabel(ax2, 'Coupled vs null AUC');
    xlabel(ax2, 'Distractor amplitude scale (relative)');
    title(ax2, 'B  Detectability when the correct pair is supplied', ...
        'FontWeight', 'bold', 'FontSize', 13);
    grid(ax2, 'off');
    box(ax2, 'off');
    set(ax2, 'FontName', 'Helvetica', 'FontSize', 12, 'LineWidth', 1.1);
    legend(ax2, 'Location', 'southwest', 'Box', 'off');
end


function local_apply_log_error_axis(ax)
    % Log scale makes near-zero (APC) errors visible alongside much
    % larger competitor errors, which get compressed together on a
    % linear axis. Values of exactly 0 are floored to a small display
    % epsilon by local_plot_summary_curve before plotting (the floor is
    % a display-only convention -- it is not a claim of nonzero error).
    set(ax, 'YScale', 'log');
    ax.YMinorGrid = 'off';
end


function local_plot_recovery_curve(ax, summaryTable, methods, xValues, fieldName, xLabelText, yLabelText, titleText, showLegend)
    style = local_method_styles();
    hold(ax, 'on');
    for iMethod = 1:numel(methods)
        methodName = methods(iMethod);
        sub = summaryTable(summaryTable.method == methodName, :);
        y = nan(size(xValues));
        lowerError = nan(size(xValues));
        upperError = nan(size(xValues));
        for iX = 1:numel(xValues)
            idx = find(abs(sub.distractor_scale - xValues(iX)) < 1e-9, 1);
            if ~isempty(idx)
                y(iX) = sub.(fieldName)(idx);
                [ciLower, ciUpper] = local_wilson_interval(round(y(iX) * sub.n_repeats(idx)), sub.n_repeats(idx));
                lowerError(iX) = y(iX) - ciLower;
                upperError(iX) = ciUpper - y(iX);
            end
        end
        styleKey = local_style_key(methodName);
        errorbar(ax, xValues, y, lowerError, upperError, ...
            'Color', style.(styleKey).color, 'LineStyle', style.(styleKey).line, ...
            'Marker', style.(styleKey).marker, 'LineWidth', 1.6, ...
            'MarkerSize', 7, 'CapSize', 4, 'DisplayName', char(methodName));
    end
    xlabel(ax, xLabelText);
    ylabel(ax, yLabelText);
    title(ax, titleText, 'FontWeight', 'bold', 'FontSize', 13);
    xlim(ax, [min(xValues) max(xValues)]);
    if showLegend
        legend(ax, 'Location', 'southwest', 'Box', 'off', 'FontSize', 11);
    end
    set(ax, 'FontName', 'Helvetica', 'FontSize', 12, 'LineWidth', 1.1);
    grid(ax, 'off');
    box(ax, 'off');
end


function [lower, upper] = local_wilson_interval(k, n)
    z = 1.959963984540054;
    if n <= 0
        lower = NaN;
        upper = NaN;
        return;
    end
    p = k / n;
    denominator = 1 + z^2 / n;
    center = (p + z^2 / (2 * n)) / denominator;
    halfWidth = z * sqrt(p * (1 - p) / n + z^2 / (4 * n^2)) / denominator;
    lower = center - halfWidth;
    upper = center + halfWidth;
end


function local_plot_summary_curve(ax, summaryTable, methods, xValues, fieldName, semFieldName, xLabelText, yLabelText, titleText, showLegend)
    style = local_method_styles();
    hold(ax, 'on');

    % Values at or below this floor are drawn at the floor so a log-scale
    % axis can display them; this only affects the C/D error panels,
    % where the floor is far below any meaningful recovery error.
    logFloor = 0.05;

    for iMethod = 1:numel(methods)
        methodName = methods(iMethod);
        sub = summaryTable(summaryTable.method == methodName, :);
        y = nan(size(xValues));
        ySem = nan(size(xValues));
        for iX = 1:numel(xValues)
            idx = find(abs(sub.distractor_scale - xValues(iX)) < 1e-9, 1);
            if ~isempty(idx)
                y(iX) = sub.(fieldName)(idx);
                ySem(iX) = sub.(semFieldName)(idx);
            end
        end

        yPlot = y;
        if strcmp(ax.YScale, 'log')
            yPlot(yPlot < logFloor) = logFloor;
        end

        styleKey = local_style_key(methodName);
        errorbar(ax, xValues, yPlot, ySem, ...
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
    grid(ax, 'off');
    box(ax, 'off');
end


function local_plot_raw_point_group(ax, condSub, methods, fieldName, style)
    hold(ax, 'on');
    nMethods = numel(methods);
    jitterWidth = 0.11;
    allVals = condSub.(fieldName);
    allVals = allVals(isfinite(allVals));
    for iMethod = 1:nMethods
        methodName = methods(iMethod);
        values = condSub.(fieldName)(condSub.method == methodName);
        values = values(isfinite(values));
        styleKey = local_style_key(methodName);
        color = style.(styleKey).color;
        xJitter = iMethod + jitterWidth * (rand(size(values)) - 0.5) * 2;
        scatter(ax, xJitter, values, 22, color, 'filled', ...
            'MarkerFaceAlpha', 0.60, 'MarkerEdgeColor', 'none');
        if ~isempty(values)
            medianValue = median(values);
            q1 = local_percentile(values, 25);
            q3 = local_percentile(values, 75);
            plot(ax, [iMethod - 0.16, iMethod + 0.16], [medianValue medianValue], ...
                'Color', color, 'LineWidth', 2.2);
            plot(ax, [iMethod iMethod], [q1 q3], 'Color', color, 'LineWidth', 1.0);
        end
    end
    xlim(ax, [0.4, nMethods + 0.6]);
    xticks(ax, 1:nMethods);
    xticklabels(ax, cellstr(methods));
    if ~isempty(allVals)
        ylim(ax, [min(0, min(allVals)), max(allVals) + 0.05 * max(allVals)]);
    end
    grid(ax, 'off');
end


function local_plot_violin_group(ax, condSub, methods, fieldName, style)
    hold(ax, 'on');
    nMethods = numel(methods);
    halfWidth = 0.35;
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

        if numel(vals) >= 2 && (max(vals) - min(vals)) > 0
            [yGrid, dens] = local_kde(vals, 200);
            dens = dens ./ max(dens);
            xLeft = xCenter - halfWidth * dens;
            xRight = xCenter + halfWidth * dens;
            patch(ax, [xLeft, fliplr(xRight)], [yGrid, fliplr(yGrid)], color, ...
                'FaceAlpha', 0.30, 'EdgeColor', color, 'LineWidth', 1.0);
        end

        if ~isempty(vals)
            xJitter = xCenter + jitterWidth * (rand(size(vals)) - 0.5) * 2;
            scatter(ax, xJitter, vals, 16, color, 'filled', ...
                'MarkerFaceAlpha', 0.45, 'MarkerEdgeColor', 'none');
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
    grid(ax, 'on');
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
    % Publication-safe palette with APC highlighted as the primary method.
    style.APC.color = [0.84 0.37 0.00];         % vermillion / burnt orange
    style.APC.line = '-';
    style.APC.marker = 'o';

    style.MVLscan.color = [0.00 0.45 0.70];     % blue
    style.MVLscan.line = '-';
    style.MVLscan.marker = '+';

    style.KLMIscan.color = [0.10 0.10 0.10];    % near-black
    style.KLMIscan.line = '-';
    style.KLMIscan.marker = '*';

    style.GLMscan.color = [0.00 0.62 0.45];     % bluish green
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
