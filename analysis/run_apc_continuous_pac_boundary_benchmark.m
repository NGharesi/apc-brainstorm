function results = run_apc_continuous_pac_boundary_benchmark(profileName)
% RUN_APC_CONTINUOUS_PAC_BOUNDARY_BENCHMARK Repeated APC limitation control.
%
% Continuous amplitude modulation is the positive-control regime for
% conventional PAC. This benchmark therefore compares full-pipeline APC
% with fixed-pair MVL and KLMI PAC (given the known 8-Hz/120-Hz bands),
% across SNR and low-frequency waveform shapes. It reports AUC rather than
% a thresholded detection rate. APC is not expected to dominate here.
%
% Usage:
%   run_apc_continuous_pac_boundary_benchmark('fast')      % 10 repeats/cell
%   run_apc_continuous_pac_boundary_benchmark('reviewer')  % 25 repeats/cell

    if nargin < 1 || isempty(profileName), profileName = 'reviewer'; end
    cfg = local_config(profileName);
    rng(cfg.randomSeed, 'twister');

    rows = cell(numel(cfg.waveforms) * numel(cfg.snrDb) * 2 * cfg.nRepeats, 1);
    index = 0;
    for iWave = 1:numel(cfg.waveforms)
        for iSnr = 1:numel(cfg.snrDb)
            for isCoupled = [false true]
                for iRepeat = 1:cfg.nRepeats
                    index = index + 1;
                    fprintf('[%s] %s, SNR %g dB, coupled=%d, %d/%d\n', ...
                        cfg.profileName, cfg.waveforms(iWave), cfg.snrDb(iSnr), ...
                        isCoupled, iRepeat, cfg.nRepeats);
                    signal = local_simulate(cfg, cfg.waveforms(iWave), cfg.snrDb(iSnr), isCoupled);
                    rows{index} = local_run(signal, cfg, cfg.waveforms(iWave), ...
                        cfg.snrDb(iSnr), isCoupled, iRepeat);
                end
            end
        end
    end
    runTable = struct2table([rows{1:index}]);
    summaryTable = local_summary(runTable, cfg);

    baseDir = fileparts(mfilename('fullpath')); tag = lower(cfg.profileName);
    files.mat = fullfile(baseDir, sprintf('apc_continuous_pac_boundary_%s.mat', tag));
    files.runs = fullfile(baseDir, sprintf('apc_continuous_pac_boundary_runs_%s.csv', tag));
    files.summary = fullfile(baseDir, sprintf('apc_continuous_pac_boundary_summary_%s.csv', tag));
    files.text = fullfile(baseDir, sprintf('apc_continuous_pac_boundary_summary_%s.txt', tag));
    files.png = fullfile(baseDir, sprintf('apc_continuous_pac_boundary_%s.png', tag));
    files.pdf = fullfile(baseDir, sprintf('apc_continuous_pac_boundary_%s.pdf', tag));
    files.fig = fullfile(baseDir, sprintf('apc_continuous_pac_boundary_%s.fig', tag));
    writetable(runTable, files.runs); writetable(summaryTable, files.summary);
    save(files.mat, 'cfg', 'runTable', 'summaryTable', '-v7.3');
    local_write_text(files.text, cfg, summaryTable);
    fig = local_plot(summaryTable, cfg);
    exportgraphics(fig, files.png, 'Resolution', 300);
    exportgraphics(fig, files.pdf, 'ContentType', 'vector'); savefig(fig, files.fig); close(fig);
    fprintf('\nSaved continuous-PAC boundary outputs:\n  %s\n  %s\n  %s\n', files.mat, files.summary, files.png);
    results = struct('config', cfg, 'run_table', runTable, 'summary_table', summaryTable, 'files', files);
end

function cfg = local_config(profileName)
    cfg.profileName = char(lower(string(profileName))); cfg.randomSeed = 20261006;
    cfg.fs = 500; cfg.durationSec = 12; cfg.fP = 8; cfg.fA = 120;
    cfg.fABand = [80 150]; cfg.modulationDepth = .70; cfg.snrDb = [-9 -3 3];
    cfg.waveforms = ["sinusoidal", "asymmetric", "harmonic_contaminated"];
    switch lower(string(profileName))
        case "fast", cfg.nRepeats = 10;
        case "reviewer", cfg.nRepeats = 25;
        case "frozen_smoke", cfg.nRepeats = 1;      % syntax check only; never reported
        case "frozen_reviewer", cfg.nRepeats = 25;  % amendment 2026-10-20; seed paired with 'reviewer'
        otherwise, error('Use profileName ''fast'', ''reviewer'', ''frozen_smoke'' or ''frozen_reviewer''.');
    end
    cfg.includeScans = startsWith(lower(string(profileName)), "frozen");
    cfg.minPhaseCycles = 3;
    % Scanned comparators (frozen profiles only): matched grid, stable IIR filters,
    % amplitude centers chosen so center +/- 6 Hz stays inside the APC 80-150 Hz range.
    cfg.fs_hz = cfg.fs; cfg.phase_scan_hz = 1:1:30; cfg.amplitude_scan_hz = 88:4:144;
    cfg.fpTolerance = 1; cfg.faTolerance = 8;
end

function signal = local_simulate(cfg, waveform, snrDb, isCoupled)
    t = 0:1/cfg.fs:(cfg.durationSec - 1/cfg.fs); phase = 2*pi*cfg.fP*t;
    switch waveform
        case "sinusoidal"
            low = sin(phase);
        case "asymmetric"
            % Fixed harmonics alter waveform shape but not the true fP.
            low = sin(phase) + .45*sin(2*phase + .45) + .20*sin(3*phase - .30);
        case "harmonic_contaminated"
            low = sin(phase) + .35*sin(2*phase + .25) + .18*sin(3*phase - .40);
        otherwise
            error('Unknown waveform.');
    end
    low = low ./ std(low);
    if isCoupled
        envelope = 1 + cfg.modulationDepth*cos(phase - pi/2);
    else
        envelope = ones(size(t));
    end
    high = 1.25 * envelope .* sin(2*pi*cfg.fA*t + .2);
    if waveform == "harmonic_contaminated"
        % Broadband sharp transients add harmonic energy without fA modulation.
        sharp = .18 * (sin(phase) + .6*sin(2*phase) + .35*sin(3*phase) + .2*sin(4*phase));
        signal = low + high + sharp;
    else
        signal = low + high;
    end
    signal = local_add_noise(signal, snrDb);
end

function row = local_run(signal, cfg, waveform, snrDb, isCoupled, repeat)
    time = (0:numel(signal)-1)./cfg.fs;
    opts = struct('fA', cfg.fABand, 'epoch', [-.6 .6], 'decomposition', 'fft_peak', ...
        'metric', 'canolty', 'diagm', false, 'surrogates', false, 'num_perm', 0, ...
        'numPhaseBins', 18, 'burstProminenceScale', .75, 'amplitudeBandWidthHz', 12);
    if cfg.includeScans, opts.minPhaseCycles = cfg.minPhaseCycles; end
    apc = bst_apc(struct('data', signal, 'time', time), opts);
    [phase, amplitude] = local_known_pair(signal, cfg);
    [mvl, ~] = calc_MI_all_methods(phase, amplitude, 'canolty', false, 0, 1, false, 18);
    [klmi, ~] = calc_MI_all_methods(phase, amplitude, 'tort', false, 0, 1, false, 18);
    status = double(apc.status_code.Value(1)); score = double(apc.pac_strength.Value(1));
    if status ~= 0 || ~isfinite(score), score = 0; end
    row = struct('waveform', string(waveform), 'snr_db', snrDb, 'is_coupled', logical(isCoupled), ...
        'repeat_index', repeat, 'apc_status_code', status, 'apc_valid', status == 0, ...
        'apc_score', score, 'apc_fP_hz', double(apc.phase_frequency_hz.Value(1)), ...
        'apc_fA_hz', double(apc.amplitude_frequency_hz.Value(1)), ...
        'mvl_fixed_pair_score', double(mvl), 'klmi_fixed_pair_score', double(klmi));
    scanNames = {'mvl','klmi','glm','event'}; scanMetrics = {'canolty','tort','glm','event'};
    for k = 1:numel(scanNames)
        if cfg.includeScans
            sc = local_scan_standard_pac(signal(:).', cfg, scanMetrics{k});
        else
            sc = struct('score', NaN, 'fp_hz', NaN, 'fa_hz', NaN);
        end
        row.([scanNames{k} '_scan_score']) = double(sc.score);
        row.([scanNames{k} '_scan_fP_hz']) = double(sc.fp_hz);
        row.([scanNames{k} '_scan_fA_hz']) = double(sc.fa_hz);
    end
end

function [phase, amplitude] = local_known_pair(signal, cfg)
    low = local_bandpass(signal, cfg.fs, cfg.fP-1.5, cfg.fP+1.5);
    high = local_bandpass(signal, cfg.fs, cfg.fA-8, cfg.fA+8);
    phase = angle(hilbert(low(:))); amplitude = abs(hilbert(high(:)));
end

function y = local_bandpass(x, fs, low, high)
    [b,a] = butter(4, [low high]./(fs/2), 'bandpass'); y = filtfilt(b,a,double(x(:)));
end

function y = local_add_noise(x, snrDb)
    pink = cumsum(randn(size(x))); pink = (pink-mean(pink))/std(pink);
    white = randn(size(x)); noise = pink + .5*white; noise = noise/std(noise);
    y = x + sqrt(mean(x.^2)/(10^(snrDb/10))) * noise;
end

function summary = local_summary(T, cfg)
    methods = ["APC", "MVL_fixed", "KLMI_fixed"];
    if cfg.includeScans, methods = [methods, "MVL_scan", "KLMI_scan", "GLM_scan", "Event_scan"]; end
    rows = cell(0, 10);
    for iWave = 1:numel(cfg.waveforms)
        for iSnr = 1:numel(cfg.snrDb)
            sub = T(T.waveform == cfg.waveforms(iWave) & T.snr_db == cfg.snrDb(iSnr), :);
            for iMethod = 1:numel(methods)
                field = local_field(methods(iMethod));
                positive = sub.(field)(sub.is_coupled); negative = sub.(field)(~sub.is_coupled);
                [fpField, faField] = local_carrier_fields(methods(iMethod));
                if isempty(fpField)
                    pairRate = NaN;
                else
                    cp = sub(sub.is_coupled, :);
                    pairRate = mean(abs(cp.(fpField)-cfg.fP) <= 1 & abs(cp.(faField)-cfg.fA) <= 8);
                end
                rows(end+1,:) = {cfg.waveforms(iWave), cfg.snrDb(iSnr), methods(iMethod), ...
                    local_auc(positive, negative), mean(positive), mean(negative), ...
                    mean(sub.apc_valid), median(abs(sub.apc_fP_hz-cfg.fP), 'omitnan'), ...
                    pairRate, local_fp_median_error(sub, fpField, cfg)}; %#ok<AGROW>
            end
        end
    end
    summary = cell2table(rows, 'VariableNames', {'waveform','snr_db','method','auc', ...
        'mean_coupled_score','mean_null_score','apc_valid_rate','apc_fP_abs_error_median_hz', ...
        'coupled_pair_recovery_rate','method_fP_abs_error_median_hz'});
end

function [fpField, faField] = local_carrier_fields(method)
    switch method
        case "APC", fpField = 'apc_fP_hz'; faField = 'apc_fA_hz';
        case "MVL_scan", fpField = 'mvl_scan_fP_hz'; faField = 'mvl_scan_fA_hz';
        case "KLMI_scan", fpField = 'klmi_scan_fP_hz'; faField = 'klmi_scan_fA_hz';
        case "GLM_scan", fpField = 'glm_scan_fP_hz'; faField = 'glm_scan_fA_hz';
        case "Event_scan", fpField = 'event_scan_fP_hz'; faField = 'event_scan_fA_hz';
        otherwise, fpField = ''; faField = '';   % fixed-pair oracle: no carrier selection
    end
end

function e = local_fp_median_error(sub, fpField, cfg)
    if isempty(fpField), e = NaN; else, e = median(abs(sub.(fpField) - cfg.fP), 'omitnan'); end
end

function field = local_field(method)
    switch method
        case "APC", field = 'apc_score';
        case "MVL_fixed", field = 'mvl_fixed_pair_score';
        case "KLMI_fixed", field = 'klmi_fixed_pair_score';
        case "MVL_scan", field = 'mvl_scan_score';
        case "KLMI_scan", field = 'klmi_scan_score';
        case "GLM_scan", field = 'glm_scan_score';
        case "Event_scan", field = 'event_scan_score';
    end
end

function auc = local_auc(positive, negative)
    positive = positive(isfinite(positive)); negative = negative(isfinite(negative));
    if isempty(positive) || isempty(negative), auc = NaN; return; end
    comparisons = positive(:) > negative(:)'; ties = positive(:) == negative(:)';
    auc = mean(comparisons(:)) + .5*mean(ties(:));
end

function local_write_text(file, cfg, summary)
    fid = fopen(file, 'w'); cleanup = onCleanup(@() fclose(fid));
    fprintf(fid, 'Continuous-PAC boundary benchmark (%s; %d repeats/cell)\n', cfg.profileName, cfg.nRepeats);
    fprintf(fid, 'Conventional PAC uses the known simulated 8-Hz phase and 120-Hz amplitude bands; APC selects carriers from raw data.\n');
    fprintf(fid, 'AUC compares continuously modulated signals against amplitude-unmodulated matched signals.\n\n%s\n', evalc('disp(summary)'));
    if cfg.includeScans
        fprintf(fid, '\nScanned comparators (frozen profiles): matched grid fP 1:30 Hz, fA 88:4:144 Hz, stable IIR filters; AUC uses each scan''s maximum score.\n');
        fprintf(fid, 'Noise model in this benchmark: cumulative-sum (random-walk) noise + 0.5 white noise, as in the earlier ''reviewer'' run.\n');
    end
end

function fig = local_plot(S, cfg)
    fig = figure('Color','w','Position',[100 100 1200 620]);
    tl = tiledlayout(1,3,'Padding','compact','TileSpacing','compact');
    methods = unique(S.method, 'stable').'; colors = lines(numel(methods));
    for iWave = 1:numel(cfg.waveforms)
        ax = nexttile(tl,iWave); hold(ax,'on');
        for iMethod = 1:numel(methods)
            sub = S(S.waveform == cfg.waveforms(iWave) & S.method == methods(iMethod), :);
            [x,order] = sort(sub.snr_db); plot(ax,x,sub.auc(order),'-o','LineWidth',2,'Color',colors(iMethod,:), ...
                'DisplayName',strrep(methods(iMethod),'_',' '));
        end
        yline(ax,.5,':','Chance','Color',[.4 .4 .4]); ylim(ax,[0 1]); grid(ax,'off'); box(ax,'off');
        xlabel(ax,'SNR (dB)'); ylabel(ax,'AUC: coupled vs matched null');
        title(ax,strrep(cfg.waveforms(iWave),'_',' '),'FontWeight','bold');
        if iWave == 1, legend(ax,'Location','southwest','Box','off'); end
    end
    sgtitle(sprintf('Continuous-PAC Boundary Benchmark (%s; %d repeats/cell)', cfg.profileName, cfg.nRepeats),'FontWeight','bold');
end


%% ---- Scanned-comparator helpers copied from run_apc_burst_sparsity_benchmark.m (amendment 2026-10-20) ----

function out = local_scan_standard_pac(signal, cfg, metricName)
    fs = cfg.fs_hz;
    fpCandidates = cfg.phase_scan_hz(:).';
    faCandidates = cfg.amplitude_scan_hz(:).';
    lowPhase = cell(size(fpCandidates));
    highEnv = cell(size(faCandidates));

    for iFp = 1:numel(fpCandidates)
        band = [max(0.5, fpCandidates(iFp) - 1.5), fpCandidates(iFp) + 1.5];
        lowPhase{iFp} = angle(hilbert(local_stable_bandpass(signal, fs, band(1), band(2))));
    end
    for iFa = 1:numel(faCandidates)
        band = [max(1.0, faCandidates(iFa) - 6.0), min(fs / 2 - 1.0, faCandidates(iFa) + 6.0)];
        highEnv{iFa} = abs(hilbert(local_stable_bandpass(signal, fs, band(1), band(2))));
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

function x = local_stable_bandpass(signal, fs, lowHz, highHz)
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

