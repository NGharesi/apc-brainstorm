function [sApc, routeLog] = rd_apc_instrumented(sMatrix, OPTIONS)
% BST_APC  Burst-triggered amplitude-phase coupling estimation.
%
% USAGE:
%   sApc = bst_apc(sMatrix, OPTIONS)
%
% INPUT:
%   sMatrix.data : [nSignals x nTime] matrix of time series
%   sMatrix.time : [1 x nTime] or [nTime x 1] time vector in seconds
%
%   OPTIONS.fA            : [fLow fHigh] high-frequency search band in Hz
%   OPTIONS.epoch         : [tStart tStop] burst-centered epoch in seconds
%   OPTIONS.decomposition : phase-frequency estimator
%                           {'fft_peak','trend','vmd','vmd_sym'}
%   OPTIONS.metric        : PAC metric {'canolty','tort','ozkurt','plv'}
%   OPTIONS.diagm         : logical or {'yes','no'} to show diagnostics
%   OPTIONS.surrogates    : logical or {'yes','no'} to use surrogates
%   OPTIONS.num_perm      : number of surrogate permutations
%   OPTIONS.numPhaseBins  : number of phase bins for Tort-style methods
%   OPTIONS.burstProminenceScale : multiplier of burst-trace SD used for
%                                  candidate burst peak prominence (0.75)
%   OPTIONS.surrogateMethod : {'circular_shift','phase_scramble'} null
%                            generator used when surrogates are enabled
%   OPTIONS.amplitudeBandWidthHz : final carrier-band width in Hz (4)
%
% OUTPUT:
%   sApc is a structure with one field per exported feature. Each field has:
%       .Value       [nSignals x 1]
%       .Units       string
%       .Description string
%
% NOTES:
%   1) The implementation is self-contained and designed for Brainstorm
%      process integration.
%   2) Experimental decomposition options ('trend', 'vmd', 'vmd_sym') fall
%      back to an FFT peak estimate when their external dependencies are not
%      available in the MATLAB path.
%
% Authors:
%   Niloofar Gharesi
%   Refactored for publication packaging by OpenAI Codex, 2026

    options = normalize_options(OPTIONS);
    [data, time] = validate_input_matrix(sMatrix);

    nSignals = size(data, 1);
    routeLog = strings(nSignals,1);
    pacStrength = nan(nSignals, 1);
    phaseFreq = nan(nSignals, 1);
    amplitudeFreq = nan(nSignals, 1);
    preferredPhase = nan(nSignals, 1);
    nBursts = zeros(nSignals, 1);
    nPhaseEvents = zeros(nSignals, 1);
    statusCode = zeros(nSignals, 1);

    % Process each row independently so the function works for sensors,
    % sources, or arbitrary matrix inputs.
    for iSignal = 1:nSignals
        [metrics, diagnostics] = compute_signal_apc(data(iSignal, :), time, options);
        pacStrength(iSignal)   = metrics.pac_strength;
        phaseFreq(iSignal)     = metrics.phase_frequency_hz;
        amplitudeFreq(iSignal) = metrics.amplitude_frequency_hz;
        preferredPhase(iSignal)= metrics.preferred_phase_deg;
        nBursts(iSignal)       = metrics.n_bursts;
        nPhaseEvents(iSignal)  = metrics.n_phase_events;
        statusCode(iSignal)    = metrics.status_code;
        routeLog(iSignal) = "not_reached";
        if isfield(diagnostics,"selection_route"), routeLog(iSignal)=diagnostics.selection_route; end

        if options.showPlots
            plot_signal_diagnostics(iSignal, diagnostics, metrics, options);
        end
    end

    sApc.pac_strength = pack_feature( ...
        pacStrength, ...
        'a.u.', ...
        'Amplitude-phase coupling strength. With surrogates enabled, this value is z-scored against the surrogate distribution.');
    sApc.phase_frequency_hz = pack_feature( ...
        phaseFreq, ...
        'Hz', ...
        'Estimated low-frequency phase carrier.');
    sApc.amplitude_frequency_hz = pack_feature( ...
        amplitudeFreq, ...
        'Hz', ...
        'Estimated high-frequency amplitude carrier.');
    sApc.preferred_phase_deg = pack_feature( ...
        preferredPhase, ...
        'deg', ...
        'Preferred low-frequency phase associated with maximal high-frequency amplitude.');
    sApc.n_bursts = pack_feature( ...
        nBursts, ...
        'count', ...
        'Number of burst-centered epochs used to estimate the burst-triggered average.');
    sApc.n_phase_events = pack_feature( ...
        nPhaseEvents, ...
        'count', ...
        'Number of phase trough events used for the phase-locked analysis.');
    sApc.status_code = pack_feature( ...
        statusCode, ...
        'code', ...
        'Computation status: 0=ok, 1=invalid signal, 2=no burst epochs, 3=no phase candidate, 4=no phase events, 5=no amplitude candidate.');
end


function [metrics, diagnostics] = compute_signal_apc(signal, time, options)
    % Hold per-signal scalar outputs plus intermediate arrays that can be
    % plotted for quality control when requested.
    metrics = struct( ...
        'pac_strength', nan, ...
        'phase_frequency_hz', nan, ...
        'amplitude_frequency_hz', nan, ...
        'preferred_phase_deg', nan, ...
        'n_bursts', 0, ...
        'n_phase_events', 0, ...
        'status_code', 0);

    diagnostics = struct( ...
        'time_epoch', [], ...
        'burst_average', [], ...
        'phase_epoch_time', [], ...
        'phase_locked_average', [], ...
        'phase_locked_tf', [], ...
        'phase_locked_freqs', []);

    signal = double(signal(:).');
    time = double(time(:).');

    if numel(signal) ~= numel(time) || numel(signal) < 10 || all(~isfinite(signal))
        metrics.status_code = 1;
        return;
    end

    signal = fillmissing(signal, 'linear', 'EndValues', 'nearest');
    signal = signal - mean(signal, 'omitnan');

    dt = median(diff(time));
    fs = 1 / dt;
    if ~isfinite(fs) || fs <= 0
        metrics.status_code = 1;
        return;
    end

    localOptions = options;
    localOptions.fA = [options.fA(1), min(options.fA(2), fs / 2 - eps)];
    if localOptions.fA(2) <= localOptions.fA(1)
        metrics.status_code = 1;
        return;
    end

    % Use the broadband high-frequency energy trace to anchor candidate
    % burst events before estimating the slower phase carrier.
    [burstTrace, ~] = compute_burst_trace(signal, fs, localOptions.fA, options.burstTimeBandwidth);
    burstTrace = smoothdata(burstTrace, 'movmean', max(3, round(0.02 * fs)));
    burstLocs = detect_peaks_with_defaults( ...
        burstTrace, ...
        max(1, round(0.9 * fs / max(localOptions.fA(1), eps))), ...
        options.burstProminenceScale * std(burstTrace, 0, 2));

    % Align burst-centered epochs and optionally flip trough-centered
    % epochs so the burst-triggered average has a consistent polarity.
    [burstEpochs, timeEpoch] = collect_burst_epochs(signal, burstLocs, fs, options.epoch, options.flipTroughs);
    metrics.n_bursts = size(burstEpochs, 1);

    if isempty(burstEpochs)
        metrics.status_code = 2;
        return;
    end

    burstAverage = mean(burstEpochs, 1, 'omitnan');
    diagnostics.time_epoch = timeEpoch;
    diagnostics.burst_average = burstAverage;

    % Estimate the slow carrier directly from the burst-triggered average.
    phaseFreq = estimate_phase_frequency(burstAverage, fs, localOptions);
    if ~isfinite(phaseFreq) || phaseFreq < options.minPhaseHz || phaseFreq >= localOptions.fA(1)
        metrics.status_code = 3;
        return;
    end

    phaseBand = get_phase_band(phaseFreq, localOptions.fA(1), fs);
    phaseSignal = bandpass_signal(signal, fs, phaseBand);
    if isempty(phaseSignal)
        metrics.status_code = 3;
        return;
    end

    troughLocs = detect_troughs(phaseSignal, fs, phaseFreq);
    metrics.n_phase_events = numel(troughLocs);
    if isempty(troughLocs)
        metrics.status_code = 4;
        return;
    end

    % Re-epoch the signal around troughs of the candidate slow rhythm to
    % localize the high-frequency component that is most phase-locked.
    [phaseLockedAverage, phaseLockedTf, phaseLockedFreqs, phaseEpochTime] = ...
        collect_phase_locked_tf(signal, troughLocs, fs, phaseFreq, localOptions);

    if isempty(phaseLockedAverage) || isempty(phaseLockedTf)
        metrics.status_code = 4;
        return;
    end

    diagnostics.phase_epoch_time = phaseEpochTime;
    diagnostics.phase_locked_average = phaseLockedAverage;
    diagnostics.phase_locked_tf = phaseLockedTf;
    diagnostics.phase_locked_freqs = phaseLockedFreqs;

    % Pick the amplitude carrier from the frequency profile that shows the
    % strongest phase-locked structure around the troughs.
    [ampFreq, ampWidth, selectionRoute] = estimate_amplitude_frequency( ...
        signal, ...
        troughLocs, ...
        phaseLockedAverage, ...
        phaseLockedTf, ...
        phaseLockedFreqs, ...
        fs, ...
        phaseFreq, ...
        localOptions.fA, ...
        options.amplitudeBandWidthHz);
    diagnostics.selection_route=selectionRoute;

    if ~isfinite(ampFreq)
        metrics.status_code = 5;
        return;
    end

    ampBand = get_amplitude_band(ampFreq, ampWidth, fs, localOptions.fA);
    ampSignal = bandpass_signal(signal, fs, ampBand);
    if isempty(ampSignal)
        metrics.status_code = 5;
        return;
    end

    phaseAngles = angle(hilbert(phaseSignal));
    amplitudeEnvelope = abs(hilbert(ampSignal));

    % Final PAC estimate is computed from the low-frequency phase and the
    % high-frequency amplitude envelope of the original signal.
    [pacStrength, preferredPhase] = calc_MI_all_methods( ...
        phaseAngles, ...
        amplitudeEnvelope, ...
        options.metric, ...
        yesno(options.useSurrogates), ...
        options.numPerm, ...
        1, ...
        yesno(options.showPlots), ...
        options.numPhaseBins, ...
        options.surrogateMethod);

    metrics.pac_strength = pacStrength;
    metrics.phase_frequency_hz = phaseFreq;
    metrics.amplitude_frequency_hz = ampFreq;
    metrics.preferred_phase_deg = preferredPhase;
end


function [burstTrace, freqs] = compute_burst_trace(signal, fs, freqBand, timeBandwidth)
    % The wavelet magnitude averaged across frequencies provides a compact
    % burst-energy trace in the user-selected high-frequency band.
    fb = cwtfilterbank( ...
        'SignalLength', numel(signal), ...
        'SamplingFrequency', fs, ...
        'FrequencyLimits', freqBand, ...
        'TimeBandwidth', timeBandwidth);
    [cfs, freqs] = cwt(signal, 'FilterBank', fb);
    burstTrace = sqrt(mean(abs(cfs).^2, 1));
end


function [epochs, timeEpoch] = collect_burst_epochs(signal, eventLocs, fs, epochWindow, flipTroughs)
    % Convert each burst event into a fixed sample window so averaging is
    % done in a consistent local coordinate system around the event.
    sampleWindow = round(epochWindow * fs);
    sampleIdx = sampleWindow(1):sampleWindow(2);
    centerIdx = 1 - sampleWindow(1);

    epochList = {};
    for iEvent = 1:numel(eventLocs)
        idx = eventLocs(iEvent) + sampleIdx;
        if idx(1) < 1 || idx(end) > numel(signal)
            continue;
        end

        epoch = signal(idx);
        % Polarity alignment makes the average less sensitive to bursts
        % that were detected on troughs instead of peaks.
        if flipTroughs && should_flip_epoch(epoch, centerIdx)
            epoch = -epoch;
        end
        epochList{end+1} = epoch; %#ok<AGROW>
    end

    if isempty(epochList)
        epochs = [];
    else
        epochs = vertcat(epochList{:});
    end
    timeEpoch = sampleIdx / fs;
end


function tfFlip = should_flip_epoch(epoch, centerIdx)
    % Use the local extremum around the alignment point to decide whether
    % the event was centered on a trough rather than a peak.
    leftIdx = max(1, centerIdx - 1);
    rightIdx = min(numel(epoch), centerIdx + 1);
    localValues = epoch(leftIdx:rightIdx);
    tfFlip = abs(min(localValues)) > abs(max(localValues));
end


function phaseFreq = estimate_phase_frequency(epochSignal, fs, options)
    % Centralize the choice of low-frequency estimator so method switching
    % stays isolated from the rest of the APC pipeline.
    method = lower(strtrim(options.decomposition));
    phaseFreq = nan;

    % Experimental decompositions are used when available; otherwise a
    % conservative FFT peak estimate keeps the process self-contained.
    switch method
        case 'trend'
            if exist('trenddecomp', 'file') == 2
                phaseFreq = estimate_phase_frequency_trend(epochSignal, fs);
            end
        case 'vmd'
            if exist('vmd', 'file') == 2
                phaseFreq = estimate_phase_frequency_vmd(epochSignal, fs, false);
            end
        case 'vmd_sym'
            if exist('vmd', 'file') == 2
                phaseFreq = estimate_phase_frequency_vmd(epochSignal, fs, true);
            end
        otherwise
            phaseFreq = nan;
    end

    if ~isfinite(phaseFreq)
        phaseFreq = estimate_phase_frequency_fft(epochSignal, fs, options);
    end
end


function phaseFreq = estimate_phase_frequency_fft(epochSignal, fs, options)
    maxPhaseHz = min([options.fA(1) - 0.5, fs / 3, options.maxPhaseHz]);
    if maxPhaseHz <= options.minPhaseHz
        phaseFreq = nan;
        return;
    end

    signal = epochSignal(:) - mean(epochSignal, 'omitnan');
    nfft = max(256, 2^nextpow2(numel(signal)));
    % Fallback phase estimate: dominant spectral peak below the
    % high-frequency search band.
    [pxx, f] = pwelch(signal, [], [], nfft, fs);
    valid = (f >= options.minPhaseHz) & (f <= maxPhaseHz);
    if ~any(valid)
        phaseFreq = nan;
        return;
    end

    [~, iMax] = max(pxx(valid));
    fValid = f(valid);
    phaseFreq = fValid(iMax);
end


function phaseFreq = estimate_phase_frequency_trend(epochSignal, fs)
    % Rank trend components by energy near the center of the burst average,
    % where the burst-locked structure should be strongest.
    [~, trendSignals, ~] = trenddecomp(epochSignal);
    if isempty(trendSignals)
        phaseFreq = nan;
        return;
    end

    midIdx = round(size(trendSignals, 1) * [0.25 0.75]);
    powerScore = rms(trendSignals(midIdx(1):midIdx(2), :), 1);
    [~, order] = sort(powerScore, 'descend');

    phaseFreq = nan;
    for iComp = 1:numel(order)
        candidate = meanfreq(trendSignals(:, order(iComp)), fs);
        if isfinite(candidate) && candidate > 0
            phaseFreq = candidate;
            return;
        end
    end
end


function phaseFreq = estimate_phase_frequency_vmd(epochSignal, fs, useSymmetry)
    % Rank VMD modes either by central energy or by symmetry around the
    % burst center, then use the leading mode as the phase candidate.
    modes = vmd(epochSignal(:));
    if isempty(modes)
        phaseFreq = nan;
        return;
    end

    if useSymmetry
        score = compute_vmd_symmetry_score(modes);
    else
        midIdx = round(size(modes, 1) * [0.25 0.75]);
        score = rms(modes(midIdx(1):midIdx(2), :), 1);
    end

    [~, order] = sort(score, 'descend');
    phaseFreq = nan;
    for iComp = 1:numel(order)
        candidate = meanfreq(modes(:, order(iComp)), fs);
        if isfinite(candidate) && candidate > 0
            phaseFreq = candidate;
            return;
        end
    end
end


function score = compute_vmd_symmetry_score(modes)
    % Symmetric modes around the epoch center are favored because the
    % burst-triggered average should approximate a cycle-centered waveform.
    nModes = size(modes, 2);
    score = zeros(1, nModes);
    midPoint = floor(size(modes, 1) / 2) + 1;

    for iMode = 1:nModes
        thisMode = modes(:, iMode);
        mse = zeros(1, midPoint - 1);
        for iOffset = 1:(midPoint - 1)
            if (midPoint + iOffset) > numel(thisMode)
                break;
            end
            mse(iOffset) = (thisMode(midPoint + iOffset) - thisMode(midPoint - iOffset)).^2;
        end
        score(iMode) = 1 ./ max(mean(mse, 'omitnan'), eps);
    end
end


function band = get_phase_band(centerHz, ampBandLow, fs)
    % Build a conservative low-frequency band that stays separated from the
    % high-frequency search range and within the valid sampling range.
    halfWidth = max(0.5, 0.25 * centerHz);
    lowHz = max(0.5, centerHz - halfWidth);
    highHz = min(ampBandLow - 0.25, centerHz + halfWidth);
    if highHz >= fs / 2
        highHz = fs / 2 - eps;
    end

    if lowHz >= highHz
        band = [];
    else
        band = [lowHz, highHz];
    end
end


function signalOut = bandpass_signal(signalIn, fs, band)
    signalOut = [];
    if isempty(band) || numel(band) ~= 2 || any(~isfinite(band))
        return;
    end
    if band(1) <= 0 || band(2) >= (fs / 2) || band(1) >= band(2)
        return;
    end

    % A compact IIR bandpass is sufficient here because PAC is measured
    % from Hilbert phase/amplitude after the candidate bands are chosen.
    d = designfilt( ...
        'bandpassiir', ...
        'FilterOrder', 4, ...
        'HalfPowerFrequency1', band(1), ...
        'HalfPowerFrequency2', band(2), ...
        'SampleRate', fs);
    signalOut = filtfilt(d, double(signalIn(:).'));
end


function troughLocs = detect_troughs(signal, fs, phaseFreq)
    % Trough events define the reference phase used for the second-stage
    % averaging that reveals the amplitude carrier.
    minPeakDistance = max(1, round(0.8 * fs / max(phaseFreq, eps)));
    troughLocs = detect_peaks_with_defaults(-signal, minPeakDistance, 0.25 * std(signal, 0, 2));
end


function [meanEpoch, meanTf, freqs, epochTime] = collect_phase_locked_tf(signal, troughLocs, fs, phaseFreq, options)
    % Create both a time-domain average and a time-frequency average around
    % troughs of the candidate phase signal.
    epochHalfSamples = max(2, round(options.phaseEpochCycles * fs / max(phaseFreq, eps)));
    sampleIdx = -epochHalfSamples:epochHalfSamples;
    epochTime = sampleIdx / fs;

    % Build a higher-resolution time-frequency map around the troughs to
    % identify the most phase-locked amplitude carrier.
    fb = cwtfilterbank( ...
        'SignalLength', numel(signal), ...
        'SamplingFrequency', fs, ...
        'FrequencyLimits', options.fA, ...
        'TimeBandwidth', options.phaseTimeBandwidth);
    [cfs, freqs] = cwt(signal, 'FilterBank', fb);
    cfs = abs(cfs);
    cfs = zscore_rows(cfs);

    epochList = {};
    tfList = {};
    for iEvent = 1:numel(troughLocs)
        idx = troughLocs(iEvent) + sampleIdx;
        if idx(1) < 1 || idx(end) > numel(signal)
            continue;
        end
        epochList{end+1} = signal(idx); %#ok<AGROW>
        tfList{end+1} = cfs(:, idx); %#ok<AGROW>
    end

    if isempty(epochList)
        meanEpoch = [];
        meanTf = [];
        return;
    end

    epochs = vertcat(epochList{:});
    meanEpoch = mean(epochs, 1, 'omitnan');

    nFreq = size(tfList{1}, 1);
    nTime = size(tfList{1}, 2);
    % Stack epochs into a 3-D array so the induced map can be averaged
    % across phase events frequency-by-frequency.
    tfCube = zeros(nFreq, nTime, numel(tfList));
    for iEpoch = 1:numel(tfList)
        tfCube(:, :, iEpoch) = tfList{iEpoch};
    end
    meanTf = mean(tfCube, 3, 'omitnan');
end


function dataOut = zscore_rows(dataIn)
    % Standardize each frequency row independently before cross-frequency
    % comparison of the phase-locked maps.
    mu = mean(dataIn, 2, 'omitnan');
    sigma = std(dataIn, 0, 2, 'omitnan');
    sigma(sigma == 0) = 1;
    dataOut = (dataIn - mu) ./ sigma;
end


function [ampFreq, ampWidth, selectionRoute] = estimate_amplitude_frequency(signal, troughLocs, meanEpoch, meanTf, freqs, fs, phaseFreq, inputBand, candidateBandWidthHz)
    % Match the Python prototype more directly by scanning candidate
    % high-frequency bands, averaging their envelopes around troughs, and
    % selecting the band whose envelope is most locked to the trough
    % waveform. Keep the TF-based rule as a fallback.
    selectionRoute="not_attempted";
    ampFreq = nan;
    ampWidth = nan;

    if isempty(signal) || isempty(troughLocs) || isempty(meanEpoch)
        return;
    end

    % Use a dense grid of genuinely narrow candidate bands.  The previous
    % +/-6 Hz scan made the lower candidate overlap slow-wave/theta power
    % (for example, an 8 Hz candidate covered 2-14 Hz), creating a strong
    % lower-bound bias in sleep data.
    candidateFreqs = inputBand(1):1:inputBand(2);
    if isempty(candidateFreqs) || (candidateFreqs(end) ~= inputBand(2))
        candidateFreqs = [candidateFreqs, inputBand(2)];
    end

    maxLag = min(round(0.8 * fs / max(phaseFreq, eps)), numel(meanEpoch) - 1);
    sampleIdx = -(floor((numel(meanEpoch) - 1) / 2)):floor((numel(meanEpoch) - 1) / 2);
    meanEpoch = meanEpoch(:).' - mean(meanEpoch, 'omitnan');
    scoreTrace = nan(size(candidateFreqs));

    if maxLag >= 1
        % Evaluate each frequency as a narrow candidate carrier rather than
        % relying on a broad, often flat trough-locked TF profile.
        for iFreq = 1:numel(candidateFreqs)
            halfWidth = candidateBandWidthHz / 2;
            thisBand = [max(inputBand(1), candidateFreqs(iFreq) - halfWidth), ...
                min([inputBand(2), fs / 2 - 1.0, candidateFreqs(iFreq) + halfWidth])];
            ampSignal = bandpass_signal(signal, fs, thisBand);
            if isempty(ampSignal)
                continue;
            end

            ampEnv = abs(hilbert(ampSignal));
            envEpochs = collect_event_epochs_by_index(ampEnv, troughLocs, sampleIdx);
            if isempty(envEpochs)
                continue;
            end

            avgEnv = mean(envEpochs, 1, 'omitnan');
            xc = xcorr(avgEnv - mean(avgEnv, 'omitnan'), meanEpoch, maxLag, 'coeff');
            scoreTrace(iFreq) = max(abs(xc), [], 'omitnan');
        end
    end

    scoreTrace = smoothdata(scoreTrace, 'movmean', min(5, numel(scoreTrace)));
    if any(isfinite(scoreTrace))
        selectionRoute="direct_envelope_scan";
        [~, iBest] = max(scoreTrace);
        ampFreq = candidateFreqs(iBest);
        ampWidth = candidateBandWidthHz;
        return;
    end

    selectionRoute="tf_fallback";
    [ampFreq, ampWidth] = estimate_amplitude_frequency_tf_fallback(meanEpoch, meanTf, freqs, fs, phaseFreq, inputBand);
end


function [ampFreq, ampWidth] = estimate_amplitude_frequency_tf_fallback(meanEpoch, meanTf, freqs, fs, phaseFreq, inputBand)
    % Fall back to the TF-profile heuristic if the direct envelope scan did
    % not yield a usable score trace.
    ampFreq = nan;
    ampWidth = nan;

    if isempty(meanTf) || isempty(freqs)
        return;
    end

    if freqs(1) > freqs(end)
        freqs = fliplr(freqs);
        meanTf = flipud(meanTf);
    end

    maxLag = min(round(0.8 * fs / max(phaseFreq, eps)), numel(meanEpoch) - 1);
    if maxLag < 1
        couplingTrace = mean(abs(meanTf), 2, 'omitnan').';
    else
        couplingTrace = zeros(1, size(meanTf, 1));
        for iFreq = 1:size(meanTf, 1)
            xc = xcorr(meanTf(iFreq, :), meanEpoch, maxLag, 'coeff');
            couplingTrace(iFreq) = sum(abs(xc), 'omitnan');
        end
    end

    couplingTrace = smoothdata(couplingTrace, 'movmean', min(5, numel(couplingTrace)));
    energyTrace = smoothdata(mean(abs(meanTf), 2, 'omitnan').', 'movmean', min(5, numel(couplingTrace)));
    if all(~isfinite(couplingTrace)) || all(~isfinite(energyTrace))
        return;
    end

    compositeTrace = normalize_01(couplingTrace) .* normalize_01(energyTrace);
    compositeTrace = smoothdata(compositeTrace, 'movmean', min(7, numel(compositeTrace)));

    [~, iMax] = max(compositeTrace);
    ampFreq = freqs(iMax);
    ampWidth = max(2, diff(inputBand) / 6);
end


function y = normalize_01(x)
    x = double(x(:).');
    xmin = min(x, [], 'omitnan');
    xmax = max(x, [], 'omitnan');
    if ~isfinite(xmin) || ~isfinite(xmax) || xmax <= xmin
        y = zeros(size(x));
    else
        y = (x - xmin) ./ (xmax - xmin);
    end
end


function epochs = collect_event_epochs_by_index(signal, eventLocs, sampleIdx)
    % Gather a fixed sample window around each event without any polarity
    % flipping so the envelope scan can be compared across candidates.
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


function band = get_amplitude_band(centerHz, widthHz, fs, inputBand)
    % Translate the selected amplitude carrier into a practical bandpass
    % while staying inside the original user-defined search band.
    if ~isfinite(widthHz) || widthHz <= 0
        widthHz = max(4, diff(inputBand) / 6);
    end

    halfWidth = max(2, widthHz / 2);
    lowHz = max([inputBand(1), centerHz - halfWidth, eps]);
    highHz = min([inputBand(2), centerHz + halfWidth, fs / 2 - eps]);

    if lowHz >= highHz
        band = [];
    else
        band = [lowHz, highHz];
    end
end


function peakLocs = detect_peaks_with_defaults(signal, minDistance, minProminence)
    % Prefer prominence-aware detection when possible, but allow a simpler
    % distance-only fallback for flatter signals.
    if nargin < 3 || isempty(minProminence) || ~isfinite(minProminence) || (minProminence <= 0)
        [~, peakLocs] = findpeaks(signal, 'MinPeakDistance', minDistance);
    else
        [~, peakLocs] = findpeaks( ...
            signal, ...
            'MinPeakDistance', minDistance, ...
            'MinPeakProminence', minProminence);
    end
end


function sFeature = pack_feature(values, units, description)
    % Store each output feature with minimal metadata so the Brainstorm
    % process wrapper can export it consistently.
    sFeature = struct( ...
        'Value', values(:), ...
        'Units', units, ...
        'Description', description);
end


function options = normalize_options(optionsIn)
    % Fill in missing options so direct script calls and Brainstorm GUI
    % calls both reach the computational code in a uniform format.
    options = struct();
    options.fA = get_option(optionsIn, 'fA', [16 250]);
    options.epoch = get_option(optionsIn, 'epoch', [-0.6 0.6]);
    options.decomposition = get_option(optionsIn, 'decomposition', 'fft_peak');
    options.metric = lower(get_option(optionsIn, 'metric', 'canolty'));
    options.showPlots = parse_flag(get_option(optionsIn, 'diagm', false));
    options.useSurrogates = parse_flag(get_option(optionsIn, 'surrogates', false));
    options.numPerm = get_option(optionsIn, 'num_perm', 200);
    options.numPhaseBins = get_option(optionsIn, 'numPhaseBins', 18);
    options.burstTimeBandwidth = get_option(optionsIn, 'burstTimeBandwidth', 5);
    options.phaseTimeBandwidth = get_option(optionsIn, 'phaseTimeBandwidth', 20);
    options.phaseEpochCycles = get_option(optionsIn, 'phaseEpochCycles', 3);
    options.minPhaseHz = get_option(optionsIn, 'minPhaseHz', 1);
    options.maxPhaseHz = get_option(optionsIn, 'maxPhaseHz', 30);
    options.flipTroughs = parse_flag(get_option(optionsIn, 'flipTroughs', true));
    options.burstProminenceScale = get_option(optionsIn, 'burstProminenceScale', 0.75);
    options.surrogateMethod = lower(string(get_option(optionsIn, 'surrogateMethod', 'circular_shift')));
    options.amplitudeBandWidthHz = get_option(optionsIn, 'amplitudeBandWidthHz', 4);

    options.fA = double(options.fA(:).');
    options.epoch = double(options.epoch(:).');

    if numel(options.fA) ~= 2 || options.fA(1) <= 0 || options.fA(2) <= options.fA(1)
        error('bst_apc:InvalidFrequencyBand', 'OPTIONS.fA must be [fLow fHigh] in Hz.');
    end
    if numel(options.epoch) ~= 2 || options.epoch(1) >= options.epoch(2)
        error('bst_apc:InvalidEpoch', 'OPTIONS.epoch must be [tStart tStop] in seconds.');
    end
    if ~isscalar(options.burstProminenceScale) || ~isfinite(options.burstProminenceScale) || options.burstProminenceScale <= 0
        error('bst_apc:InvalidBurstProminenceScale', ...
            'OPTIONS.burstProminenceScale must be a positive finite scalar.');
    end
    if ~ismember(options.surrogateMethod, ["circular_shift", "phase_scramble"])
        error('bst_apc:InvalidSurrogateMethod', ...
            'OPTIONS.surrogateMethod must be circular_shift or phase_scramble.');
    end
    options.surrogateMethod = char(options.surrogateMethod);
    if ~isscalar(options.amplitudeBandWidthHz) || ~isfinite(options.amplitudeBandWidthHz) || options.amplitudeBandWidthHz <= 0
        error('bst_apc:InvalidAmplitudeBandWidth', ...
            'OPTIONS.amplitudeBandWidthHz must be a positive finite scalar.');
    end
end


function value = get_option(optionsIn, fieldName, defaultValue)
    % Return a default when optional fields were not supplied by the
    % caller.
    if isstruct(optionsIn) && isfield(optionsIn, fieldName) && ~isempty(optionsIn.(fieldName))
        value = optionsIn.(fieldName);
    else
        value = defaultValue;
    end
end


function tf = parse_flag(value)
    % Accept logicals, numerics, and common yes/no strings for convenience.
    if islogical(value)
        tf = value;
    elseif isnumeric(value)
        tf = (value ~= 0);
    elseif ischar(value)
        tf = any(strcmpi(value, {'yes','true','on'}));
    else
        tf = false;
    end
end


function out = yesno(tf)
    % Legacy helper used by the PAC metric function interface.
    if tf
        out = 'yes';
    else
        out = 'no';
    end
end


function [data, time] = validate_input_matrix(sMatrix)
    % Validate the minimal structure required by the APC core before any
    % signal processing starts.
    if ~isstruct(sMatrix) || ~isfield(sMatrix, 'data') || ~isfield(sMatrix, 'time')
        error('bst_apc:InvalidInput', 'Input must be a structure with fields ''data'' and ''time''.');
    end
    data = double(sMatrix.data);
    time = double(sMatrix.time(:).');
    if isempty(data) || isempty(time) || size(data, 2) ~= numel(time)
        error('bst_apc:DimensionMismatch', 'sMatrix.data must be [nSignals x nTime] and match sMatrix.time.');
    end
end


function plot_signal_diagnostics(iSignal, diagnostics, metrics, options)
    % Keep diagnostic plotting separate from the numerical path so the main
    % algorithm remains easier to test and reuse.
    if isempty(diagnostics.time_epoch) || isempty(diagnostics.burst_average)
        return;
    end

    figure('Name', sprintf('APC Diagnostics - signal %d', iSignal), 'Color', 'w');
    tiledlayout(2, 1, 'Padding', 'compact', 'TileSpacing', 'compact');

    nexttile;
    plot(diagnostics.time_epoch, diagnostics.burst_average, 'k', 'LineWidth', 1.5);
    xlabel('Time (s)');
    ylabel('Amplitude');
    title(sprintf('Burst-triggered average | fP = %.2f Hz', metrics.phase_frequency_hz));
    grid on;

    if ~isempty(diagnostics.phase_locked_tf)
        nexttile;
        imagesc(diagnostics.phase_epoch_time, diagnostics.phase_locked_freqs, diagnostics.phase_locked_tf);
        axis xy;
        xlabel('Time (s)');
        ylabel('Frequency (Hz)');
        title(sprintf('Phase-locked high-frequency map | fA = %.2f Hz | metric = %s', ...
            metrics.amplitude_frequency_hz, options.metric));
        colorbar;
    end
end
