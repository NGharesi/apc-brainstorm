function debug_apc_matlab_case(caseName)
% DEBUG_APC_MATLAB_CASE
% Inspect intermediate APC stages for one benchmark case without Brainstorm.
%
% USAGE:
%   debug_apc_matlab_case('burst_coupled')
%
% OUTPUT:
%   Saves a MAT file with intermediate signals to:
%     apc_matlab_benchmark/<caseName>_matlab_debug.mat
%
% PURPOSE:
%   This script helps identify where MATLAB APC diverges from the Python
%   prototype by exposing the main intermediate stages:
%     - high-frequency burst trace
%     - burst indices
%     - burst-triggered average
%     - recovered fP
%     - trough indices
%     - trough-centered average
%     - recovered fA
%     - final phase/amplitude signals

    if nargin < 1 || isempty(caseName)
        caseName = 'burst_coupled';
    end

    baseDir = fileparts(mfilename('fullpath'));
    benchDir = fullfile(baseDir, 'apc_matlab_benchmark');
    manifestFile = fullfile(benchDir, 'manifest.json');

    if ~exist(manifestFile, 'file')
        error('Benchmark manifest not found: %s', manifestFile);
    end

    manifest = jsondecode(fileread(manifestFile));
    caseInfo = [];
    for iCase = 1:numel(manifest.cases)
        if strcmp(manifest.cases(iCase).name, caseName)
            caseInfo = manifest.cases(iCase);
            break;
        end
    end
    if isempty(caseInfo)
        error('Unknown case: %s', caseName);
    end

    csvFile = fullfile(benchDir, caseInfo.csv_file);
    T = readtable(csvFile);
    time = T.time_s(:).';
    signal = T.signal(:).';
    fs = 1 / median(diff(time));

    fA = double(caseInfo.params.fA_range_hz(:).');
    epoch = double(caseInfo.params.epoch_s(:).');

    signal = fillmissing(signal, 'linear', 'EndValues', 'nearest');
    signal = signal - mean(signal, 'omitnan');

    debug = struct();
    debug.case_name = caseName;
    debug.time = time;
    debug.signal = signal;
    debug.fs = fs;
    debug.fA_range_hz = fA;
    debug.epoch_s = epoch;

    % === Stage 1: burst trace ===
    fb = cwtfilterbank( ...
        'SignalLength', numel(signal), ...
        'SamplingFrequency', fs, ...
        'FrequencyLimits', fA, ...
        'TimeBandwidth', 5);
    [cfsBurst, fcBurst] = cwt(signal, 'FilterBank', fb);
    burstTrace = sqrt(mean(abs(cfsBurst).^2, 1));
    burstTrace = smoothdata(burstTrace, 'movmean', max(3, round(0.02 * fs)));
    minPeakDistance = max(1, round(0.9 * fs / max(fA(1), eps)));
    minProminence = 0.75 * std(burstTrace, 0, 2);
    [burstPks, burstLocs] = findpeaks( ...
        burstTrace, ...
        'MinPeakDistance', minPeakDistance, ...
        'MinPeakProminence', minProminence);

    debug.burst.fc_hz = fcBurst;
    debug.burst.trace = burstTrace;
    debug.burst.minPeakDistance_samples = minPeakDistance;
    debug.burst.minProminence = minProminence;
    debug.burst.peaks = burstPks;
    debug.burst.locs = burstLocs;

    % === Stage 1b: burst-triggered average ===
    sampleWindow = round(epoch * fs);
    sampleIdx = sampleWindow(1):sampleWindow(2);
    centerIdx = 1 - sampleWindow(1);
    epochList = {};
    keptBurstLocs = [];
    for iEvent = 1:numel(burstLocs)
        idx = burstLocs(iEvent) + sampleIdx;
        if idx(1) < 1 || idx(end) > numel(signal)
            continue;
        end
        ep = signal(idx);
        local = ep(max(1, centerIdx - 1) : min(numel(ep), centerIdx + 1));
        if abs(min(local)) > abs(max(local))
            ep = -ep;
        end
        epochList{end+1} = ep; %#ok<AGROW>
        keptBurstLocs(end+1) = burstLocs(iEvent); %#ok<AGROW>
    end

    if isempty(epochList)
        error('No valid burst-centered epochs were kept.');
    end
    burstEpochs = vertcat(epochList{:});
    burstAvg = mean(burstEpochs, 1, 'omitnan');
    timeEpoch = sampleIdx / fs;

    debug.burst.kept_locs = keptBurstLocs;
    debug.burst.epochs = burstEpochs;
    debug.burst.average = burstAvg;
    debug.burst.time_epoch = timeEpoch;

    % === Stage 2: fP estimation ===
    fp = estimate_phase_frequency_debug(burstAvg, fs, fA(1));
    debug.phase.phase_frequency_hz = fp;

    phaseBand = [max(0.5, fp - max(0.5, 0.25 * fp)), min(fA(1) - 0.25, fp + max(0.5, 0.25 * fp))];
    dPhase = designfilt( ...
        'bandpassiir', ...
        'FilterOrder', 4, ...
        'HalfPowerFrequency1', phaseBand(1), ...
        'HalfPowerFrequency2', phaseBand(2), ...
        'SampleRate', fs);
    phaseSignal = filtfilt(dPhase, signal);
    debug.phase.band_hz = phaseBand;
    debug.phase.signal = phaseSignal;

    % === Stage 3: trough detection ===
    troughMinDistance = max(1, round(0.8 * fs / max(fp, eps)));
    troughProminence = 0.25 * std(phaseSignal, 0, 2);
    [troughPks, troughLocs] = findpeaks( ...
        -phaseSignal, ...
        'MinPeakDistance', troughMinDistance, ...
        'MinPeakProminence', troughProminence);

    debug.phase.trough_peaks = troughPks;
    debug.phase.trough_locs = troughLocs;
    debug.phase.trough_min_distance_samples = troughMinDistance;
    debug.phase.trough_prominence = troughProminence;

    epochHalfSamples = max(2, round(3 * fs / max(fp, eps)));
    troughIdx = -epochHalfSamples:epochHalfSamples;
    troughEpochList = {};
    for iEvent = 1:numel(troughLocs)
        idx = troughLocs(iEvent) + troughIdx;
        if idx(1) < 1 || idx(end) > numel(signal)
            continue;
        end
        troughEpochList{end+1} = signal(idx); %#ok<AGROW>
    end
    if isempty(troughEpochList)
        error('No valid trough-centered epochs were kept.');
    end
    troughEpochs = vertcat(troughEpochList{:});
    troughAvg = mean(troughEpochs, 1, 'omitnan');
    timeTroughEpoch = troughIdx / fs;

    debug.phase.trough_epochs = troughEpochs;
    debug.phase.trough_average = troughAvg;
    debug.phase.trough_time_epoch = timeTroughEpoch;

    % === Stage 3b: trough-locked TF ===
    fbTf = cwtfilterbank( ...
        'SignalLength', numel(signal), ...
        'SamplingFrequency', fs, ...
        'FrequencyLimits', fA, ...
        'TimeBandwidth', 20);
    [cfsTf, fcTf] = cwt(signal, 'FilterBank', fbTf);
    cfsTf = abs(cfsTf);
    mu = mean(cfsTf, 2, 'omitnan');
    sigma = std(cfsTf, 0, 2, 'omitnan');
    sigma(sigma == 0) = 1;
    cfsTf = (cfsTf - mu) ./ sigma;

    tfList = {};
    for iEvent = 1:numel(troughLocs)
        idx = troughLocs(iEvent) + troughIdx;
        if idx(1) < 1 || idx(end) > numel(signal)
            continue;
        end
        tfList{end+1} = cfsTf(:, idx); %#ok<AGROW>
    end
    tfCube = zeros(size(tfList{1}, 1), size(tfList{1}, 2), numel(tfList));
    for iEpoch = 1:numel(tfList)
        tfCube(:, :, iEpoch) = tfList{iEpoch};
    end
    tfAvg = mean(tfCube, 3, 'omitnan');

    debug.tf.freqs_hz = fcTf;
    debug.tf.average = tfAvg;

    % === Stage 4: fA estimation ===
    [fa, scoreTrace, candidateFreqs, fallbackTrace] = estimate_amplitude_frequency_debug(signal, troughLocs, troughAvg, tfAvg, fcTf, fs, fp, fA);
    debug.amplitude.frequency_hz = fa;
    debug.amplitude.method = 'python_scan';
    debug.amplitude.score_trace = scoreTrace;
    debug.amplitude.candidate_freqs_hz = candidateFreqs;
    debug.amplitude.fallback_trace = fallbackTrace;

    ampBand = [max(fA(1), fa - 6), min(fs / 2 - 1, fa + 6)];
    dAmp = designfilt( ...
        'bandpassiir', ...
        'FilterOrder', 4, ...
        'HalfPowerFrequency1', ampBand(1), ...
        'HalfPowerFrequency2', ampBand(2), ...
        'SampleRate', fs);
    ampSignal = filtfilt(dAmp, signal);
    ampEnv = abs(hilbert(ampSignal));
    phi = angle(hilbert(phaseSignal));
    signalPAC = ampEnv .* exp(1i * phi);
    pacStrength = abs(mean(signalPAC));
    prefPhaseDeg = rad2deg(angle(mean(signalPAC)));

    debug.amplitude.band_hz = ampBand;
    debug.amplitude.signal = ampSignal;
    debug.amplitude.envelope = ampEnv;
    debug.final.phase_rad = phi;
    debug.final.pac_strength = pacStrength;
    debug.final.preferred_phase_deg = prefPhaseDeg;

    outFile = fullfile(benchDir, [caseName '_matlab_debug.mat']);
    save(outFile, 'debug', '-v7.3');

    fprintf('\nSaved debug file:\n  %s\n', outFile);
    fprintf('\nKey outputs:\n');
    fprintf('  n_bursts            : %d\n', numel(keptBurstLocs));
    fprintf('  phase_frequency_hz  : %.6f\n', fp);
    fprintf('  n_phase_events      : %d\n', size(troughEpochs, 1));
    fprintf('  amplitude_frequency : %.6f\n', fa);
    fprintf('  pac_strength        : %.6f\n', pacStrength);
    fprintf('  preferred_phase_deg : %.6f\n\n', prefPhaseDeg);
end


function fp = estimate_phase_frequency_debug(avgSignal, fs, faLow)
    x = avgSignal(:) - mean(avgSignal, 'omitnan');
    nfft = max(256, 2 ^ nextpow2(numel(x)));
    spec = abs(fft(x, nfft)).^2;
    freqs = (0:(nfft - 1)) * fs / nfft;
    half = 1:floor(nfft / 2);
    freqs = freqs(half);
    spec = spec(half);
    valid = (freqs >= 1.0) & (freqs <= min(30.0, faLow - 0.5));
    if ~any(valid)
        fp = NaN;
        return;
    end
    [~, iMax] = max(spec(valid));
    fValid = freqs(valid);
    fp = fValid(iMax);
end


function [fa, scoreTrace, candidateFreqs, fallbackTrace] = estimate_amplitude_frequency_debug(signal, troughLocs, meanEpoch, meanTf, freqs, fs, fp, inputBand)
    candidateFreqs = inputBand(1):4:inputBand(2);
    if isempty(candidateFreqs) || (candidateFreqs(end) ~= inputBand(2))
        candidateFreqs = [candidateFreqs, inputBand(2)];
    end

    fallbackTrace = [];
    scoreTrace = nan(size(candidateFreqs));

    maxLag = max(1, min(round(0.8 * fs / max(fp, eps)), numel(meanEpoch) - 1));
    sampleIdx = -(floor((numel(meanEpoch) - 1) / 2)):floor((numel(meanEpoch) - 1) / 2);
    meanEpoch = meanEpoch(:).' - mean(meanEpoch, 'omitnan');

    for iFreq = 1:numel(candidateFreqs)
        band = [max(1.0, candidateFreqs(iFreq) - 6.0), min(fs / 2 - 1.0, candidateFreqs(iFreq) + 6.0)];
        ampSignal = bandpass_signal_local(signal, fs, band);
        if isempty(ampSignal)
            continue;
        end

        ampEnv = abs(hilbert(ampSignal));
        envEpochs = collect_epochs_local(ampEnv, troughLocs, sampleIdx);
        if isempty(envEpochs)
            continue;
        end

        avgEnv = mean(envEpochs, 1, 'omitnan');
        xc = xcorr(avgEnv - mean(avgEnv, 'omitnan'), meanEpoch, maxLag, 'coeff');
        scoreTrace(iFreq) = max(abs(xc), [], 'omitnan');
    end

    scoreTrace = smoothdata(scoreTrace, 'movmean', min(5, numel(scoreTrace)));
    if any(isfinite(scoreTrace))
        [~, iBest] = max(scoreTrace);
        fa = candidateFreqs(iBest);
        return;
    end

    if freqs(1) > freqs(end)
        freqs = fliplr(freqs);
        meanTf = flipud(meanTf);
    end

    couplingTrace = zeros(1, size(meanTf, 1));
    for iFreq = 1:size(meanTf, 1)
        xc = xcorr(meanTf(iFreq, :), meanEpoch, maxLag, 'coeff');
        couplingTrace(iFreq) = sum(abs(xc), 'omitnan');
    end

    couplingTrace = smoothdata(couplingTrace, 'movmean', min(7, numel(couplingTrace)));
    energyTrace = smoothdata(mean(abs(meanTf), 2, 'omitnan').', 'movmean', min(7, numel(couplingTrace)));
    fallbackTrace = normalize_01_debug(couplingTrace) .* normalize_01_debug(energyTrace);
    fallbackTrace = smoothdata(fallbackTrace, 'movmean', min(7, numel(fallbackTrace)));
    [~, iMax] = max(fallbackTrace);
    fa = freqs(iMax);
    fa = min(max(fa, inputBand(1)), inputBand(2));
end


function y = normalize_01_debug(x)
    x = double(x(:).');
    xmin = min(x, [], 'omitnan');
    xmax = max(x, [], 'omitnan');
    if ~isfinite(xmin) || ~isfinite(xmax) || xmax <= xmin
        y = zeros(size(x));
    else
        y = (x - xmin) ./ (xmax - xmin);
    end
end


function epochs = collect_epochs_local(signal, eventLocs, sampleIdx)
    eventLocs = round(eventLocs(:).');
    sampleIdx = round(sampleIdx(:).');
    epochList = {};

    for iEvent = 1:numel(eventLocs)
        idx = eventLocs(iEvent) + sampleIdx;
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
