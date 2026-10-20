function results = run_apc_premise_two_rhythm_benchmark(profileName)
% RUN_APC_PREMISE_TWO_RHYTHM_BENCHMARK Prespecified test of the APC premise.
%
% Protocol amendment 2026-10-20 (APC_protocol_amendment_2026-10-20.md),
% written and frozen before any run of this file.
%
% Question: when bursts are locked to a slow rhythm that is NOT the
% dominant low-frequency spectral component, does burst-timing phase
% estimation (APC) recover the coupled rhythm better than a trivial
% spectral-peak baseline, and is the result driven by polarity flipping?
%
% Profiles:
%   'smoke'   1 repeat per cell, seed 20261019. Syntax check only; never reported.
%   'holdout' 100 repeats per cell, seed 20261021. The only reportable run.
%
% Cells (coupled rhythm amplitude 0.5, uncoupled distractor amplitude 1.0):
%   A_keep100 / A_keep040 : bursts locked to 5 Hz, distractor 11 Hz
%   B_keep100 / B_keep040 : bursts locked to 11 Hz, distractor 5 Hz
%   R_single_keep100      : single 8-Hz rhythm, coupled (reference)
%   N_uncoupled           : single 8-Hz rhythm, bursts at uniform random times
%
% Methods (identical signal per repeat):
%   APC, APC-noflip (flipTroughs=false), APC-event-carrier,
%   APC-noflip-event-carrier, Spectral-peak-event-carrier (fP = largest
%   residual peak of the Welch spectrum above a log-log linear aperiodic fit,
%   1-30 Hz; fA by the frozen apc_event_carrier rule), and matched-grid
%   MVL, Ozkurt-MVL, KLMI, GLM and event-phase scans.
%
% Primary endpoint: joint recovery (|fP - coupled rhythm| <= 1 Hz and
% |fA - 120| <= 8 Hz). Primary contrast: APC-event-carrier minus
% Spectral-peak-event-carrier, paired within repeat, percentile bootstrap
% (10,000 resamples). Decision rule (fixed in advance): the premise is
% supported only if the 95% interval of the primary contrast is above zero
% in BOTH A_keep100 and B_keep100. Every method and cell is reported.

    if nargin < 1 || isempty(profileName), profileName = 'smoke'; end
    cfg = local_get_profile(profileName);
    rng(cfg.random_seed, 'twister');

    methods = ["APC","APC-noflip","APC-event-carrier","APC-noflip-event-carrier", ...
        "Spectral-peak-event-carrier","MVL-scan","Ozkurt-MVL-scan","KLMI-scan", ...
        "GLM-scan","Event-phase-scan"];
    cells = local_cells();
    runRows = {};
    fprintf('APC premise two-rhythm benchmark (%s; %d repeats/cell)\n', cfg.profile_name, cfg.n_repeats);
    for iCell = 1:numel(cells)
        for iRep = 1:cfg.n_repeats
            fprintf('[%s] %s repeat %d/%d\n', cfg.profile_name, cells(iCell).name, iRep, cfg.n_repeats);
            rows = local_run_trial(cfg, cells(iCell), iRep);
            runRows(end+1:end+numel(rows)) = rows; %#ok<AGROW>
        end
    end
    runTable = struct2table([runRows{:}]);

    rng(cfg.random_seed + 1, 'twister');   % separate stream for resampling
    summaryTable = local_summary(runTable, methods, cells);
    contrastTable = local_contrasts(runTable, cfg);
    aucTable = local_null_auc(runTable, methods);
    decision = local_decision(contrastTable);

    baseDir = fileparts(mfilename('fullpath')); tag = lower(cfg.profile_name);
    files.mat = fullfile(baseDir, sprintf('apc_premise_two_rhythm_%s.mat', tag));
    files.runs = fullfile(baseDir, sprintf('apc_premise_two_rhythm_runs_%s.csv', tag));
    files.summary = fullfile(baseDir, sprintf('apc_premise_two_rhythm_summary_%s.csv', tag));
    files.contrasts = fullfile(baseDir, sprintf('apc_premise_two_rhythm_contrasts_%s.csv', tag));
    files.auc = fullfile(baseDir, sprintf('apc_premise_two_rhythm_null_auc_%s.csv', tag));
    files.text = fullfile(baseDir, sprintf('apc_premise_two_rhythm_summary_%s.txt', tag));
    files.png = fullfile(baseDir, sprintf('apc_premise_two_rhythm_%s.png', tag));
    files.pdf = fullfile(baseDir, sprintf('apc_premise_two_rhythm_%s.pdf', tag));
    writetable(runTable, files.runs); writetable(summaryTable, files.summary);
    writetable(contrastTable, files.contrasts); writetable(aucTable, files.auc);
    save(files.mat, 'cfg', 'cells', 'runTable', 'summaryTable', 'contrastTable', 'aucTable', 'decision', '-v7.3');
    local_write_text(files.text, cfg, summaryTable, contrastTable, aucTable, decision);
    fig = local_plot(summaryTable, methods, cells, cfg);
    exportgraphics(fig, files.png, 'Resolution', 300);
    exportgraphics(fig, files.pdf, 'ContentType', 'vector'); close(fig);
    fprintf('\nDecision: %s\nSaved outputs to %s\n', decision, files.summary);
    results = struct('config', cfg, 'run_table', runTable, 'summary_table', summaryTable, ...
        'contrast_table', contrastTable, 'auc_table', aucTable, 'decision', decision, 'files', files);
end


function cfg = local_get_profile(profileName)
    cfg = struct();
    cfg.profile_name = char(lower(string(profileName)));
    cfg.fs_hz = 500; cfg.duration_s = 8.0; cfg.true_fa_hz = 120.0;
    cfg.phase_offset_deg = -90; cfg.true_high_amp = 1.30; cfg.base_hf_amp = 0.08;
    cfg.burst_sigma_s = 0.028; cfg.burst_phase_jitter_s = 0.010; cfg.snr_db = -3.0;
    cfg.coupling_level = 0.60; cfg.background_burst_scale = 0.18;
    cfg.broad_fa_band_hz = [80 152]; cfg.phase_scan_hz = 1:1:30;
    cfg.amplitude_scan_hz = 88:4:148; cfg.metric = 'canolty';
    cfg.fa_tolerance_hz = 8.0; cfg.fp_tolerance_hz = 1.0; cfg.min_phase_cycles = 3;
    cfg.welch_window_s = 2; cfg.welch_nfft = 4096; cfg.spectral_range_hz = [1 30];
    cfg.n_boot = 10000;
    switch lower(string(profileName))
        case "smoke",   cfg.n_repeats = 1;   cfg.random_seed = 20261019;
        case "holdout", cfg.n_repeats = 100; cfg.random_seed = 20261021;
        otherwise, error('Use profile ''smoke'' or ''holdout''.');
    end
end


function cells = local_cells()
    mk = @(name, fr, ar, fd, ad, keep, coupled) struct('name', string(name), ...
        'rhythm_hz', fr, 'rhythm_amp', ar, 'distractor_hz', fd, 'distractor_amp', ad, ...
        'keep_rate', keep, 'is_coupled', coupled);
    cells = [ ...
        mk("A_keep100", 5, 0.5, 11, 1.0, 1.00, true), ...
        mk("A_keep040", 5, 0.5, 11, 1.0, 0.40, true), ...
        mk("B_keep100", 11, 0.5, 5, 1.0, 1.00, true), ...
        mk("B_keep040", 11, 0.5, 5, 1.0, 0.40, true), ...
        mk("R_single_keep100", 8, 1.0, NaN, 0.0, 1.00, true), ...
        mk("N_uncoupled", 8, 1.0, NaN, 0.0, 1.00, false)];
end


function trialRows = local_run_trial(cfg, c, repIdx)
    t = 0:(1 / cfg.fs_hz):(cfg.duration_s - 1 / cfg.fs_hz);
    signal = local_simulate_two_rhythm(t, cfg, c);
    signal = local_add_mixed_noise(signal, cfg.snr_db);

    apcFlip = local_run_apc_flag(signal, t, cfg, true);
    apcNoFlip = local_run_apc_flag(signal, t, cfg, false);
    hybridFlip = apc_event_carrier(signal, cfg.fs_hz, apcFlip, cfg.amplitude_scan_hz, 6, 1.5, 0.020);
    hybridNoFlip = apc_event_carrier(signal, cfg.fs_hz, apcNoFlip, cfg.amplitude_scan_hz, 6, 1.5, 0.020);
    spectral = local_spectral_peak_fp(signal, cfg);
    spectralHybrid = apc_event_carrier(signal, cfg.fs_hz, spectral, cfg.amplitude_scan_hz, 6, 1.5, 0.020);

    items = {apcFlip, apcNoFlip, hybridFlip, hybridNoFlip, spectralHybrid, ...
        local_scan_standard_pac(signal, cfg, 'canolty'), ...
        local_scan_standard_pac(signal, cfg, 'ozkurt'), ...
        local_scan_standard_pac(signal, cfg, 'tort'), ...
        local_scan_standard_pac(signal, cfg, 'glm'), ...
        local_scan_standard_pac(signal, cfg, 'event')};
    names = ["APC","APC-noflip","APC-event-carrier","APC-noflip-event-carrier", ...
        "Spectral-peak-event-carrier","MVL-scan","Ozkurt-MVL-scan","KLMI-scan", ...
        "GLM-scan","Event-phase-scan"];
    trialRows = cell(1, numel(items));
    for k = 1:numel(items)
        trialRows{k} = local_pack(names(k), c, repIdx, items{k}, cfg);
    end
end


function row = local_pack(methodName, c, repIdx, item, cfg)
    fp = double(item.fp_hz); fa = double(item.fa_hz);
    if ~item.valid, fp = NaN; fa = NaN; end
    row = struct();
    row.method = string(methodName); row.cell = c.name; row.is_coupled = c.is_coupled;
    row.keep_rate = c.keep_rate; row.rhythm_hz = c.rhythm_hz; row.distractor_hz = c.distractor_hz;
    row.repeat_index = repIdx; row.valid = double(item.valid); row.status_code = double(item.status_code);
    row.recovered_fp_hz = fp; row.recovered_fa_hz = fa; row.score = double(item.score);
    row.fp_abs_error_hz = abs(fp - c.rhythm_hz);
    row.fa_abs_error_hz = abs(fa - cfg.true_fa_hz);
    row.fp_correct = double(isfinite(fp) && abs(fp - c.rhythm_hz) <= cfg.fp_tolerance_hz);
    row.fp_at_distractor = double(isfinite(fp) && isfinite(c.distractor_hz) && ...
        abs(fp - c.distractor_hz) <= cfg.fp_tolerance_hz);
    row.fa_correct = double(isfinite(fa) && abs(fa - cfg.true_fa_hz) <= cfg.fa_tolerance_hz);
    row.pair_correct = double(row.fp_correct == 1 && row.fa_correct == 1);
end


function signal = local_simulate_two_rhythm(t, cfg, c)
    fp = c.rhythm_hz;
    low = c.rhythm_amp * sin(2 * pi * fp * t);
    if c.distractor_amp > 0
        low = low + c.distractor_amp * sin(2 * pi * c.distractor_hz * t + 2 * pi * rand);
    end
    phi0 = deg2rad(cfg.phase_offset_deg);
    cycleTimes = ((phi0 + pi / 2) / (2 * pi * fp)) + (0:ceil(t(end) * fp) + 2) / fp;
    cycleTimes = cycleTimes(cycleTimes >= t(1) - 1 / fp & cycleTimes <= t(end) + 1 / fp);
    if c.is_coupled
        keepMask = rand(size(cycleTimes)) <= c.keep_rate;
        eventTimes = cycleTimes(keepMask) + cfg.burst_phase_jitter_s * randn(1, sum(keepMask));
    else
        nEvents = round(c.keep_rate * numel(cycleTimes));
        eventTimes = t(1) + (t(end) - t(1)) * rand(1, nEvents);
    end
    trueEnv = local_gaussian_burst_envelope(t, eventTimes, cfg.burst_sigma_s);
    if max(trueEnv) > 0, trueEnv = trueEnv ./ max(trueEnv); end
    randTimes = linspace(t(1), t(end), numel(cycleTimes) + 2);
    randTimes = randTimes(2:end-1);
    randTimes = randTimes + (0.45 / fp) * (2 * rand(size(randTimes)) - 1);
    randTimes = min(max(randTimes, t(1)), t(end));
    bgEnv = local_gaussian_burst_envelope(t, randTimes, cfg.burst_sigma_s);
    if max(bgEnv) > 0, bgEnv = bgEnv ./ max(bgEnv); end
    hfEnvelope = cfg.base_hf_amp + cfg.true_high_amp * ...
        (cfg.coupling_level * trueEnv + cfg.background_burst_scale * bgEnv);
    signal = low + hfEnvelope .* sin(2 * pi * cfg.true_fa_hz * t);
end


function out = local_run_apc_flag(signal, time, cfg, flipFlag)
    options = struct('fA', cfg.broad_fa_band_hz, 'epoch', [-0.6 0.6], ...
        'decomposition', 'fft_peak', 'metric', cfg.metric, 'diagm', false, ...
        'surrogates', false, 'num_perm', 0, 'numPhaseBins', 18, ...
        'minPhaseCycles', cfg.min_phase_cycles, 'flipTroughs', flipFlag);
    sApc = bst_apc(struct('data', signal, 'time', time), options);
    out = struct();
    out.status_code = double(sApc.status_code.Value(1));
    out.valid = out.status_code == 0;
    out.fp_hz = double(sApc.phase_frequency_hz.Value(1));
    out.fa_hz = double(sApc.amplitude_frequency_hz.Value(1));
    out.preferred_phase_deg = double(sApc.preferred_phase_deg.Value(1));
    out.score = double(sApc.pac_strength.Value(1));
    if ~out.valid
        out.fp_hz = NaN; out.fa_hz = NaN; out.preferred_phase_deg = NaN; out.score = 0;
    end
end


function out = local_spectral_peak_fp(signal, cfg)
% Trivial baseline: largest Welch peak above a log-log linear aperiodic fit.
    fs = cfg.fs_hz; win = hann(round(cfg.welch_window_s * fs));
    [p, f] = pwelch(double(signal(:)), win, round(numel(win) / 2), cfg.welch_nfft, fs);
    sel = f >= cfg.spectral_range_hz(1) & f <= cfg.spectral_range_hz(2) & p > 0;
    fSel = f(sel); lp = log10(p(sel)); lf = log10(fSel);
    coeffs = polyfit(lf, lp, 1); residual = lp - polyval(coeffs, lf);
    [~, iMax] = max(residual);
    out = struct('valid', true, 'status_code', 0, 'fp_hz', fSel(iMax), ...
        'fa_hz', NaN, 'preferred_phase_deg', NaN, 'score', residual(iMax));
end


function summaryTable = local_summary(runTable, methods, cells)
    rows = cell(0, 15);
    for iCell = 1:numel(cells)
        for iMethod = 1:numel(methods)
            sub = runTable(runTable.cell == cells(iCell).name & runTable.method == methods(iMethod), :);
            [pr, prLo, prHi] = local_binomial_rate_ci(sub.pair_correct);
            [fpr, fpLo, fpHi] = local_binomial_rate_ci(sub.fp_correct);
            rows(end+1, :) = {cells(iCell).name, methods(iMethod), height(sub), mean(sub.valid), ...
                pr, prLo, prHi, fpr, fpLo, fpHi, mean(sub.fp_at_distractor), mean(sub.fa_correct), ...
                median(sub.fp_abs_error_hz, 'omitnan'), median(sub.fa_abs_error_hz, 'omitnan'), ...
                median(sub.recovered_fp_hz, 'omitnan')}; %#ok<AGROW>
        end
    end
    summaryTable = cell2table(rows, 'VariableNames', {'cell','method','n','valid_rate', ...
        'pair_rate','pair_wilson_low','pair_wilson_high','fp_rate','fp_wilson_low','fp_wilson_high', ...
        'fp_at_distractor_rate','fa_rate','median_fp_abs_error_hz','median_fa_abs_error_hz', ...
        'median_recovered_fp_hz'});
end


function contrastTable = local_contrasts(runTable, cfg)
    pairs = { ...
        "APC-event-carrier", "Spectral-peak-event-carrier", "primary"; ...
        "APC-noflip-event-carrier", "Spectral-peak-event-carrier", "secondary"; ...
        "APC", "APC-noflip", "secondary"; ...
        "APC-event-carrier", "GLM-scan", "secondary"; ...
        "APC-event-carrier", "Event-phase-scan", "secondary"};
    cellNames = ["A_keep100","A_keep040","B_keep100","B_keep040","R_single_keep100"];
    rows = cell(0, 8);
    for iPair = 1:size(pairs, 1)
        dByCell = cell(1, numel(cellNames));
        for iCell = 1:numel(cellNames)
            d = local_paired_diff(runTable, cellNames(iCell), pairs{iPair, 1}, pairs{iPair, 2});
            dByCell{iCell} = d;
            [lo, hi] = local_boot_ci({d}, cfg.n_boot);
            rows(end+1, :) = {pairs{iPair, 3}, pairs{iPair, 1}, pairs{iPair, 2}, cellNames(iCell), ...
                numel(d), mean(d), lo, hi}; %#ok<AGROW>
        end
        twoRhythm = dByCell(1:4);
        [lo, hi] = local_boot_ci(twoRhythm, cfg.n_boot);
        rows(end+1, :) = {pairs{iPair, 3}, pairs{iPair, 1}, pairs{iPair, 2}, "two_rhythm_pooled_equal_weight", ...
            sum(cellfun(@numel, twoRhythm)), mean(cellfun(@mean, twoRhythm)), lo, hi}; %#ok<AGROW>
    end
    contrastTable = cell2table(rows, 'VariableNames', {'role','method_a','method_b','cell', ...
        'n_pairs','mean_difference','boot95_low','boot95_high'});
end


function d = local_paired_diff(runTable, cellName, methodA, methodB)
    a = runTable(runTable.cell == cellName & runTable.method == methodA, :);
    b = runTable(runTable.cell == cellName & runTable.method == methodB, :);
    a = sortrows(a, 'repeat_index'); b = sortrows(b, 'repeat_index');
    assert(isequal(a.repeat_index, b.repeat_index), 'Unpaired repeats.');
    d = a.pair_correct - b.pair_correct;
end


function [lo, hi] = local_boot_ci(groups, nBoot)
% Percentile bootstrap, resampling repeats within each group; groups weighted equally.
    stats = zeros(nBoot, 1);
    for b = 1:nBoot
        m = zeros(1, numel(groups));
        for g = 1:numel(groups)
            x = groups{g}; m(g) = mean(x(randi(numel(x), numel(x), 1)));
        end
        stats(b) = mean(m);
    end
    lo = prctile(stats, 2.5); hi = prctile(stats, 97.5);
end


function aucTable = local_null_auc(runTable, methods)
% Secondary: does each method's raw score separate the coupled single-rhythm
% reference from the uncoupled-burst null? (Scores are not calibrated.)
    rows = cell(0, 4);
    for iMethod = 1:numel(methods)
        pos = runTable.score(runTable.cell == "R_single_keep100" & runTable.method == methods(iMethod));
        neg = runTable.score(runTable.cell == "N_uncoupled" & runTable.method == methods(iMethod));
        rows(end+1, :) = {methods(iMethod), numel(pos), numel(neg), local_auc(pos, neg)}; %#ok<AGROW>
    end
    aucTable = cell2table(rows, 'VariableNames', {'method','n_coupled','n_null','auc_coupled_vs_uncoupled'});
end


function auc = local_auc(positive, negative)
    positive = positive(isfinite(positive)); negative = negative(isfinite(negative));
    if isempty(positive) || isempty(negative), auc = NaN; return; end
    auc = mean(positive(:) > negative(:)', 'all') + 0.5 * mean(positive(:) == negative(:)', 'all');
end


function decision = local_decision(contrastTable)
    prim = contrastTable(contrastTable.role == "primary", :);
    okA = prim.boot95_low(prim.cell == "A_keep100") > 0;
    okB = prim.boot95_low(prim.cell == "B_keep100") > 0;
    if okA && okB
        decision = "SUPPORTED: APC-event-carrier exceeds the spectral-peak baseline in both A_keep100 and B_keep100.";
    elseif okA || okB
        decision = "PARTIAL: interval above zero in only one of A_keep100 / B_keep100; premise not supported as a general claim.";
    else
        decision = "NOT SUPPORTED: no interval above zero in A_keep100 or B_keep100.";
    end
end


function local_write_text(file, cfg, summaryTable, contrastTable, aucTable, decision)
    fid = fopen(file, 'w'); cleaner = onCleanup(@() fclose(fid)); %#ok<NASGU>
    fprintf(fid, 'APC premise two-rhythm benchmark (%s; %d repeats/cell; seed %d)\n', ...
        cfg.profile_name, cfg.n_repeats, cfg.random_seed);
    fprintf(fid, 'Prespecified in APC_protocol_amendment_2026-10-20.md before any run.\n');
    fprintf(fid, 'Decision rule: primary contrast 95%% interval above zero in BOTH A_keep100 and B_keep100.\n');
    fprintf(fid, 'DECISION: %s\n\n', decision);
    fprintf(fid, '%s\n\n%s\n\n%s\n', ...
        evalc('disp(summaryTable)'), evalc('disp(contrastTable)'), evalc('disp(aucTable)'));
    if cfg.n_repeats < 100
        fprintf(fid, '\nSMOKE PROFILE: syntax check only. Do not report.\n');
    end
end


function fig = local_plot(summaryTable, methods, cells, cfg)
    fig = figure('Color', 'w', 'Units', 'pixels', 'Position', [80 80 1500 650]);
    tl = tiledlayout(fig, 1, 2, 'Padding', 'compact', 'TileSpacing', 'compact');
    for panel = 1:2
        ax = nexttile(tl); hold(ax, 'on');
        if panel == 1, field = 'pair_rate'; ttl = 'Joint (fP, fA) recovery';
        else, field = 'fp_at_distractor_rate'; ttl = 'fP selected at the uncoupled distractor'; end
        M = nan(numel(cells), numel(methods));
        for i = 1:numel(cells)
            for j = 1:numel(methods)
                v = summaryTable.(field)(summaryTable.cell == cells(i).name & summaryTable.method == methods(j));
                if ~isempty(v), M(i, j) = v; end
            end
        end
        bar(ax, M); ylim(ax, [0 1]); grid(ax, 'on');
        set(ax, 'XTick', 1:numel(cells), 'XTickLabel', [cells.name], 'TickLabelInterpreter', 'none');
        ylabel(ax, 'Proportion of repeats'); title(ax, ttl);
        if panel == 1, legend(ax, methods, 'Location', 'eastoutside', 'Interpreter', 'none'); end
    end
    title(tl, sprintf('APC premise test (%s; %d repeats/cell)', cfg.profile_name, cfg.n_repeats), 'Interpreter', 'none');
end


%% ---- Helpers copied verbatim from run_apc_burst_sparsity_benchmark.m ----

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
                case 'event'
                    eventIdx = local_envelope_events(highEnv{iFa}, fs);
                    if isempty(eventIdx)
                        scoreVal = 0;
                    else
                        scoreVal = abs(mean(exp(1i * lowPhase{iFp}(eventIdx))));
                    end
                    prefDeg = NaN;
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


function indices = local_envelope_events(envelope, fs)
    threshold = median(envelope) + 0.75 * std(envelope);
    [~, indices] = findpeaks(envelope, ...
        'MinPeakProminence', 0.25 * std(envelope), ...
        'MinPeakDistance', max(1, round(0.020 * fs)));
    indices = indices(envelope(indices) >= threshold);
end


function x = local_bandpass(signal, fs, lowHz, highHz)
    wn = [lowHz, highHz] ./ (fs / 2);
    wn(1) = max(wn(1), 1e-4);
    wn(2) = min(wn(2), 0.999);
    if wn(2) <= wn(1)
        x = zeros(size(signal));
        return;
    end
    d = designfilt('bandpassiir', 'FilterOrder', 4, ...
        'HalfPowerFrequency1', wn(1) * fs / 2, ...
        'HalfPowerFrequency2', wn(2) * fs / 2, 'SampleRate', fs);
    x = filtfilt(d, double(signal(:)));
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
