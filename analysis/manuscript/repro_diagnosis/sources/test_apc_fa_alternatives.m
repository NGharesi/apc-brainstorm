function results = test_apc_fa_alternatives(caseName)
% TEST_APC_FA_ALTERNATIVES
% Compare alternative amplitude-frequency recovery rules on one APC
% benchmark case without changing the main implementation first.
%
% USAGE:
%   results = test_apc_fa_alternatives('burst_coupled')
%
% OUTPUT:
%   Saves:
%     apc_matlab_benchmark/<caseName>_fa_method_comparison.mat
%     apc_matlab_benchmark/<caseName>_fa_method_comparison.png
%
% METHODS:
%   1) current_main   : frequency selected by the current MATLAB APC path
%   2) python_scan    : Python-style envelope scan around phase troughs
%   3) burst_centered : burst-centered envelope concentration score

    if nargin < 1 || isempty(caseName)
        caseName = 'burst_coupled';
    end

    baseDir = fileparts(mfilename('fullpath'));
    benchDir = fullfile(baseDir, 'apc_matlab_benchmark');
    manifestFile = fullfile(benchDir, 'manifest.json');
    debugFile = fullfile(benchDir, [caseName '_matlab_debug.mat']);

    if ~exist(manifestFile, 'file')
        error('Manifest not found: %s', manifestFile);
    end
    if ~exist(debugFile, 'file')
        debug_apc_matlab_case(caseName);
    end

    manifest = jsondecode(fileread(manifestFile));
    caseInfo = find_case_info(manifest, caseName);

    S = load(debugFile, 'debug');
    debug = S.debug;

    signal = double(debug.signal(:).');
    fs = double(debug.fs);
    fp = double(debug.phase.phase_frequency_hz);
    fARange = double(debug.fA_range_hz(:).');
    trueFa = double(caseInfo.params.true_fa_hz);
    pythonFa = double(caseInfo.python_apc_result_no_surrogates.amplitude_frequency_hz);

    troughLocs = double(debug.phase.trough_locs(:).');
    troughEpochIdx = round(double(debug.phase.trough_time_epoch(:).') * fs);
    burstLocs = double(debug.burst.kept_locs(:).');
    burstEpochIdx = round(double(debug.burst.time_epoch(:).') * fs);
    troughAvg = double(debug.phase.trough_average(:).');
    phaseSignal = double(debug.phase.signal(:).');

    candidateFreqs = fARange(1):4:fARange(2);
    if candidateFreqs(end) ~= fARange(2)
        candidateFreqs = [candidateFreqs, fARange(2)];
    end

    % Keep the current result as the baseline.
    currentFa = double(debug.amplitude.frequency_hz);
    [currentPac, currentPref] = compute_pac_at_frequency(signal, phaseSignal, fs, currentFa, fARange);

    [pythonFaAlt, pythonScore] = estimate_fa_python_scan( ...
        signal, troughLocs, troughEpochIdx, troughAvg, fs, fp, candidateFreqs);
    [pythonPac, pythonPref] = compute_pac_at_frequency(signal, phaseSignal, fs, pythonFaAlt, fARange);

    [burstFaAlt, burstScore] = estimate_fa_burst_centered( ...
        signal, burstLocs, burstEpochIdx, fs, candidateFreqs);
    [burstPac, burstPref] = compute_pac_at_frequency(signal, phaseSignal, fs, burstFaAlt, fARange);

    results = struct();
    results.case_name = caseName;
    results.true_fa_hz = trueFa;
    results.python_reference_fa_hz = pythonFa;
    results.current_main = pack_method_result('current_main', currentFa, currentPac, currentPref, trueFa, pythonFa);
    results.python_scan = pack_method_result('python_scan', pythonFaAlt, pythonPac, pythonPref, trueFa, pythonFa);
    results.burst_centered = pack_method_result('burst_centered', burstFaAlt, burstPac, burstPref, trueFa, pythonFa);
    results.candidate_freqs_hz = candidateFreqs;
    results.python_scan_score = pythonScore;
    results.burst_centered_score = burstScore;
    results.recommended_method = choose_best_method(results);

    outMat = fullfile(benchDir, [caseName '_fa_method_comparison.mat']);
    save(outMat, 'results');

    outPng = fullfile(benchDir, [caseName '_fa_method_comparison.png']);
    plot_method_scores(results, outPng);

    fprintf('\nAPC fA alternative comparison: %s\n', caseName);
    fprintf('  true fA              : %.3f Hz\n', trueFa);
    fprintf('  python reference fA  : %.3f Hz\n', pythonFa);
    print_method_result(results.current_main);
    print_method_result(results.python_scan);
    print_method_result(results.burst_centered);
    fprintf('  recommended method   : %s\n', results.recommended_method);
    fprintf('  saved MAT            : %s\n', outMat);
    fprintf('  saved figure         : %s\n\n', outPng);
end


function caseInfo = find_case_info(manifest, caseName)
    caseInfo = [];
    for iCase = 1:numel(manifest.cases)
        if strcmp(manifest.cases(iCase).name, caseName)
            caseInfo = manifest.cases(iCase);
            return;
        end
    end
    error('Unknown case: %s', caseName);
end


function result = pack_method_result(name, fa, pac, prefPhase, trueFa, pythonFa)
    result = struct( ...
        'name', name, ...
        'frequency_hz', fa, ...
        'pac_strength', pac, ...
        'preferred_phase_deg', prefPhase, ...
        'abs_error_true_hz', abs(fa - trueFa), ...
        'abs_error_python_hz', abs(fa - pythonFa));
end


function methodName = choose_best_method(results)
    names = {'current_main', 'python_scan', 'burst_centered'};
    bestScore = inf;
    bestPacPenalty = inf;
    methodName = names{1};

    for iName = 1:numel(names)
        item = results.(names{iName});
        if ~isfinite(item.frequency_hz)
            continue;
        end
        score = item.abs_error_true_hz;
        pacPenalty = -item.pac_strength;
        if (score < bestScore) || ((abs(score - bestScore) < 1e-9) && (pacPenalty < bestPacPenalty))
            bestScore = score;
            bestPacPenalty = pacPenalty;
            methodName = item.name;
        end
    end
end


function print_method_result(item)
    fprintf('  %-17s fA = %7.3f Hz | PAC = %8.6f | Pref = %8.2f deg | |err true| = %6.3f\n', ...
        item.name, ...
        item.frequency_hz, ...
        item.pac_strength, ...
        item.preferred_phase_deg, ...
        item.abs_error_true_hz);
end


function [fa, scoreTrace] = estimate_fa_python_scan(signal, troughLocs, epochIdx, avgWaveform, fs, fp, candidateFreqs)
    scoreTrace = nan(size(candidateFreqs));
    maxLag = max(1, min(round(0.8 * fs / max(fp, eps)), numel(avgWaveform) - 1));
    avgWaveform = avgWaveform(:).' - mean(avgWaveform, 'omitnan');

    for iFreq = 1:numel(candidateFreqs)
        freq = candidateFreqs(iFreq);
        band = [max(1.0, freq - 6.0), min(fs / 2 - 1.0, freq + 6.0)];
        ampSignal = bandpass_signal_local(signal, fs, band);
        if isempty(ampSignal)
            continue;
        end
        env = abs(hilbert(ampSignal));
        envEpochs = collect_epochs_local(env, troughLocs, epochIdx);
        if isempty(envEpochs)
            continue;
        end
        avgEnv = mean(envEpochs, 1, 'omitnan');
        xc = xcorr(avgEnv - mean(avgEnv, 'omitnan'), avgWaveform, maxLag, 'coeff');
        scoreTrace(iFreq) = max(abs(xc), [], 'omitnan');
    end

    [~, iBest] = max(scoreTrace);
    fa = candidateFreqs(iBest);
end


function [fa, scoreTrace] = estimate_fa_burst_centered(signal, burstLocs, epochIdx, fs, candidateFreqs)
    scoreTrace = nan(size(candidateFreqs));
    epochTime = epochIdx / fs;
    centerMask = abs(epochTime) <= 0.05;
    flankMask = (abs(epochTime) >= 0.15) & (abs(epochTime) <= 0.35);

    for iFreq = 1:numel(candidateFreqs)
        freq = candidateFreqs(iFreq);
        band = [max(1.0, freq - 6.0), min(fs / 2 - 1.0, freq + 6.0)];
        ampSignal = bandpass_signal_local(signal, fs, band);
        if isempty(ampSignal)
            continue;
        end
        env = abs(hilbert(ampSignal));
        envEpochs = collect_epochs_local(env, burstLocs, epochIdx);
        if isempty(envEpochs)
            continue;
        end
        avgEnv = mean(envEpochs, 1, 'omitnan');
        centerEnergy = mean(avgEnv(centerMask), 'omitnan');
        flankEnergy = mean(avgEnv(flankMask), 'omitnan');
        scoreTrace(iFreq) = centerEnergy - flankEnergy;
    end

    [~, iBest] = max(scoreTrace);
    fa = candidateFreqs(iBest);
end


function epochs = collect_epochs_local(signal, eventLocs, epochIdx)
    eventLocs = round(eventLocs(:).');
    epochIdx = round(epochIdx(:).');
    epochList = {};

    for iEvent = 1:numel(eventLocs)
        idx = eventLocs(iEvent) + epochIdx;
        if idx(1) < 1 || idx(end) > numel(signal)
            continue;
        end
        epochList{end+1} = signal(idx); %#ok<AGROW>
    end

    if isempty(epochList)
        epochs = [];
    else
        epochs = vertcat(epochList{:});
    end
end


function [pacStrength, preferredPhaseDeg] = compute_pac_at_frequency(signal, phaseSignal, fs, fa, inputBand)
    pacStrength = nan;
    preferredPhaseDeg = nan;
    if ~isfinite(fa)
        return;
    end

    band = [max(inputBand(1), fa - 6.0), min(fs / 2 - 1.0, fa + 6.0)];
    ampSignal = bandpass_signal_local(signal, fs, band);
    if isempty(ampSignal)
        return;
    end

    ampEnv = abs(hilbert(ampSignal));
    phi = angle(hilbert(phaseSignal));
    z = ampEnv .* exp(1i * phi);
    meanVec = mean(z, 'omitnan');
    pacStrength = abs(meanVec);
    preferredPhaseDeg = rad2deg(angle(meanVec));
end


function signalOut = bandpass_signal_local(signalIn, fs, band)
    signalOut = [];
    if numel(band) ~= 2 || any(~isfinite(band)) || band(1) <= 0 || band(2) >= (fs / 2) || band(1) >= band(2)
        return;
    end

    d = designfilt( ...
        'bandpassiir', ...
        'FilterOrder', 4, ...
        'HalfPowerFrequency1', band(1), ...
        'HalfPowerFrequency2', band(2), ...
        'SampleRate', fs);
    signalOut = filtfilt(d, double(signalIn(:).'));
end


function plot_method_scores(results, outPng)
    fig = figure('Visible', 'off', 'Color', 'w', 'Position', [100 100 1200 450]);
    tl = tiledlayout(fig, 1, 3, 'Padding', 'compact', 'TileSpacing', 'compact');
    title(tl, sprintf('APC fA comparison - %s', strrep(results.case_name, '_', '\_')));

    nexttile;
    bar(categorical({'current', 'python', 'burst'}), ...
        [results.current_main.frequency_hz, results.python_scan.frequency_hz, results.burst_centered.frequency_hz]);
    hold on;
    yline(results.true_fa_hz, '--r', 'True fA', 'LineWidth', 1.2);
    yline(results.python_reference_fa_hz, ':k', 'Python fA', 'LineWidth', 1.2);
    ylabel('Recovered fA (Hz)');
    title('Recovered frequency');
    grid on;

    nexttile;
    plot(results.candidate_freqs_hz, results.python_scan_score, 'k', 'LineWidth', 1.5);
    hold on;
    xline(results.python_scan.frequency_hz, '--b', 'LineWidth', 1.2);
    xline(results.true_fa_hz, '--r', 'LineWidth', 1.2);
    xlabel('Frequency (Hz)');
    ylabel('Score');
    title('Python-style trough scan');
    grid on;

    nexttile;
    plot(results.candidate_freqs_hz, results.burst_centered_score, 'm', 'LineWidth', 1.5);
    hold on;
    xline(results.burst_centered.frequency_hz, '--b', 'LineWidth', 1.2);
    xline(results.true_fa_hz, '--r', 'LineWidth', 1.2);
    xlabel('Frequency (Hz)');
    ylabel('Score');
    title('Burst-centered envelope score');
    grid on;

    exportgraphics(fig, outPng, 'Resolution', 180);
    close(fig);
end
