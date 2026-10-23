function [sApc, runInfo] = bst_apc(sMatrix, OPTIONS)
% BST_APC  Burst-triggered amplitude-phase coupling estimation.
%
% USAGE:
%   [sApc, runInfo] = bst_apc(sMatrix, OPTIONS)
% runInfo contains version, full normalized options, per-signal route,
% candidate/effective final half-widths and actual clipped final band edges.
% stepFourMode: v1 (default), oct2026, june2026_clipped.
% OPTIONS.version='v2' selects burst-locked-power phase and raw-MVL carrier
% selection. Default/version='v1' preserves the frozen v1 calculations.
% v2 adds event PPC/z/p, normalized MVL, burst times and diagnostic flags.
% fPRefine: true (default), or false for the preserved Welch-bin estimate.
% fPMaxBinSpacingHz: 0.05 (maximum refined spectral-bin spacing).
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
%   OPTIONS.amplitudeBandWidthHz : fixed oct2026 width in Hz (4).
%                                  v1 uses 2*recovered fP; June uses 12 Hz.
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

    requestedVersion=lower(char(string(get_option(OPTIONS,'version','v1'))));
    if ~ismember(requestedVersion,{'v1','v1.0','v2','v3'})
        error('bst_apc:Version','version must be v1, v1.0, v2 or v3.');
    end
    if strcmp(requestedVersion,'v2')
        [sApc,runInfo]=compute_matrix_apc_v2(sMatrix,OPTIONS);
        return;
    end
    if strcmp(requestedVersion,'v3')
        [sApc,runInfo]=compute_matrix_apc_v3(sMatrix,OPTIONS);
        return;
    end
    options = normalize_options(OPTIONS);
    [data, time] = validate_input_matrix(sMatrix);

    nSignals = size(data, 1);
    runInfo=struct('version','v1.0','options',options,'route',strings(nSignals,1), ...
        'candidate_half_width_hz',nan(nSignals,1),'final_half_width_hz',nan(nSignals,1), ...
        'effective_half_width_hz',nan(nSignals,1),'final_band_hz',nan(nSignals,2));
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
        runInfo.route(iSignal) = metrics.route;
        runInfo.candidate_half_width_hz(iSignal)=metrics.candidate_half_width_hz;
        runInfo.final_half_width_hz(iSignal)=metrics.final_half_width_hz;
        runInfo.effective_half_width_hz(iSignal)=metrics.final_half_width_hz;
        runInfo.final_band_hz(iSignal,:)=metrics.final_band_hz;

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
        'status_code', 0, 'route', "not_reached", ...
        'candidate_half_width_hz',nan,'final_half_width_hz',nan,'final_band_hz',[nan nan]);

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
    if isfield(localOptions,'version') && strcmp(localOptions.version,'v3')
        [phaseFreq,diagnostics.aperiodic]=estimate_phase_frequency_v3(burstAverage,fs,localOptions,numel(signal)/fs);
    else
    phaseFreq = estimate_phase_frequency(burstAverage, fs, localOptions);
    end
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
    [ampFreq, ampWidth, metrics.route] = estimate_amplitude_frequency( ...
        signal, ...
        troughLocs, ...
        phaseLockedAverage, ...
        phaseLockedTf, ...
        phaseLockedFreqs, ...
        fs, ...
        phaseFreq, ...
        localOptions.fA, ...
        options.amplitudeBandWidthHz, options.stepFourMode);

    if strcmp(options.stepFourMode,'v1')
        metrics.candidate_half_width_hz=phaseFreq;
        metrics.final_half_width_hz=phaseFreq;
    elseif strcmp(options.stepFourMode,'june2026_clipped')
        metrics.candidate_half_width_hz=6;
        metrics.final_half_width_hz=max(2,ampWidth/2);
    else
        metrics.candidate_half_width_hz=options.amplitudeBandWidthHz/2;
        metrics.final_half_width_hz=max(2,ampWidth/2);
    end

    if ~isfinite(ampFreq)
        metrics.status_code = 5;
        return;
    end

    ampBand = get_amplitude_band(ampFreq, ampWidth, fs, localOptions.fA, options.stepFourMode);
    if numel(ampBand)==2,metrics.final_band_hz=ampBand;end
    ampSignal = carrier_bandpass(signal, fs, ampBand, options.stepFourMode);
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
    maxPhaseHz=min([options.fA(1)-0.5, fs/3, options.maxPhaseHz]);
    if maxPhaseHz<=options.minPhaseHz, phaseFreq=nan; return; end
    signal=epochSignal(:)-mean(epochSignal,'omitnan');
    nfft=max(256,2^nextpow2(numel(signal)));
    if options.fPRefine
        nfft=max(nfft,2^nextpow2(ceil(fs/options.fPMaxBinSpacingHz)));
    end
    [pxx,f]=pwelch(signal,[],[],nfft,fs);
    valid=(f>=options.minPhaseHz)&(f<=maxPhaseHz);
    if ~any(valid), phaseFreq=nan; return; end
    indices=find(valid);[~,iMax]=max(pxx(valid));i=indices(iMax);phaseFreq=f(i);
    if options.fPRefine && i>1 && i<numel(f) && valid(i-1) && valid(i+1)
        y=log(max(pxx(i-1:i+1),realmin));den=y(1)-2*y(2)+y(3);
        if isfinite(den) && den<0
            delta=0.5*(y(1)-y(3))/den;delta=max(-0.5,min(0.5,delta));
            phaseFreq=min(max(f(i)+delta*(fs/nfft),options.minPhaseHz),maxPhaseHz);
        end
    end
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
    persistent filterKeys filterObjects
    if isempty(filterKeys),filterKeys={};filterObjects={};end
    key=sprintf('%.17g,%.17g,%.17g',fs,band(1),band(2));j=find(strcmp(filterKeys,key),1);
    if isempty(j)
    d = designfilt( ...
        'bandpassiir', ...
        'FilterOrder', 4, ...
        'HalfPowerFrequency1', band(1), ...
        'HalfPowerFrequency2', band(2), ...
        'SampleRate', fs);
        filterKeys{end+1}=key;filterObjects{end+1}=d;
    else
        d=filterObjects{j};
    end
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


function [ampFreq, ampWidth, route] = estimate_amplitude_frequency(signal, troughLocs, meanEpoch, meanTf, freqs, fs, phaseFreq, inputBand, candidateBandWidthHz, mode)
    % Match the Python prototype more directly by scanning candidate
    % high-frequency bands, averaging their envelopes around troughs, and
    % selecting the band whose envelope is most locked to the trough
    % waveform. Keep the TF-based rule as a fallback.
    route="not_attempted";
    if strcmp(mode,'june2026_clipped')
        [ampFreq,~,~,fallbackTrace]=estimate_amplitude_frequency_debug(signal,troughLocs,meanEpoch,meanTf,freqs,fs,phaseFreq,inputBand);
        ampWidth=12;
        if isempty(fallbackTrace),route="direct_envelope_scan";else,route="tf_fallback";end
        return;
    end
    if strcmp(mode,'v1'),candidateBandWidthHz=2*phaseFreq;end
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
            if strcmp(mode,'v1')
                thisBand=[max(inputBand(1),candidateFreqs(iFreq)-phaseFreq),min([inputBand(2),fs/2-eps,candidateFreqs(iFreq)+phaseFreq])];
            end
            ampSignal = carrier_bandpass(signal, fs, thisBand, mode);
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
        route="direct_envelope_scan";
        [~, iBest] = max(scoreTrace);
        ampFreq = candidateFreqs(iBest);
        ampWidth = candidateBandWidthHz;
        return;
    end

    route="tf_fallback";
    [ampFreq, ampWidth] = estimate_amplitude_frequency_tf_fallback(meanEpoch, meanTf, freqs, fs, phaseFreq, inputBand);
    if strcmp(mode,'v1'),ampWidth=2*phaseFreq;end
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


function band = get_amplitude_band(centerHz, widthHz, fs, inputBand, mode)
    % Translate the selected amplitude carrier into a practical bandpass
    % while staying inside the original user-defined search band.
    if ~isfinite(widthHz) || widthHz <= 0
        widthHz = max(4, diff(inputBand) / 6);
    end

    if strcmp(mode,'v1'),halfWidth=widthHz/2;else,halfWidth=max(2,widthHz/2);end
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
    options.fA = get_option(optionsIn, 'fA', [80 150]);
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
    options.stepFourMode=lower(char(string(get_option(optionsIn,'stepFourMode','v1'))));
    options.fPRefine=parse_flag(get_option(optionsIn,'fPRefine',true));
    options.fPMaxBinSpacingHz=get_option(optionsIn,'fPMaxBinSpacingHz',0.05);
    if ~ismember(options.stepFourMode,{'v1','oct2026','june2026_clipped'})
        error('bst_apc:StepFourMode','Unknown Step 4 mode.');
    end
    if ~isscalar(options.fPMaxBinSpacingHz)||~isfinite(options.fPMaxBinSpacingHz)||options.fPMaxBinSpacingHz<=0||options.fPMaxBinSpacingHz>0.05
        error('bst_apc:SpectralSpacing','fPMaxBinSpacingHz must be positive and <=0.05 Hz.');
    end

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


function signalOut = bandpass_signal_local(signalIn,fs,band)
    signalOut=bandpass_signal(signalIn,fs,band);
end



function signalOut=carrier_bandpass(signal,fs,band,mode)
    if ~strcmp(mode,'v1'),signalOut=bandpass_signal(signal,fs,band);return;end
    signalOut=[];
    if numel(band)~=2||any(~isfinite(band))||band(1)<=0||band(2)>=fs/2||band(1)>=band(2),return;end
    % Fourth-order Butterworth bandpass, in SOS form. The v1 carrier bands
    % change with continuous fP; design the same IIR family directly.
    [z,p,k]=butter(2,band/(fs/2),'bandpass');[sos,g]=zp2sos(z,p,k);
    signalOut=filtfilt(sos,g,double(signal(:).'));
end

function [sApc,runInfo]=compute_matrix_apc_v2(sMatrix,optionsIn)
% Fixed v2 specification. All v1 helpers/calculations remain selectable.
if ~isfield(optionsIn,'fA') || isempty(optionsIn.fA),optionsIn.fA=[80 160];end
options=normalize_options(optionsIn);options.version='v2';
options.phaseGridStepHz=.05;options.minUsableBursts=10;options.phaseMinimumRecordCycles=10;
options.burstLockWindowSeconds=2;options.burstLockHannStyle='symmetric';
options.eventTestStatistic='grid_max_BLP';options.eventSecondaryStatistic='BLP_at_refined_fP';
options.eventSegmentInterpolation='linear signal samples';options.eventJitterBounds='window-usable center range';
options.amplitudeGridStepHz=1;options.amplitudeScoreSmoothPoints=1;options.eventSurrogateCount=200;
options.amplitudeKernel='positive-frequency Gaussian';options.amplitudeSigmaPhaseMultiplier=1.5;
options.amplitudeMirrorPaddingSeconds=1;
options.eventSurrogateSeed=get_option(optionsIn,'eventSurrogateSeed',20261022);
options.eventSurrogateSubstream=get_option(optionsIn,'eventSurrogateSubstream',1);
options.eventSurrogateGenerator='mrg32k3a';
assert(isscalar(options.minPhaseHz)&&isfinite(options.minPhaseHz)&&options.minPhaseHz>0 && ...
 isscalar(options.maxPhaseHz)&&isfinite(options.maxPhaseHz)&&options.maxPhaseHz>=options.minPhaseHz,'bst_apc:V2PhaseLimits','Invalid phase limits');
assert(isscalar(options.eventSurrogateSeed)&&options.eventSurrogateSeed>=0&&options.eventSurrogateSeed<2^32&&fix(options.eventSurrogateSeed)==options.eventSurrogateSeed,'bst_apc:V2Seed','Invalid surrogate seed');
assert(isscalar(options.eventSurrogateSubstream)&&options.eventSurrogateSubstream>=1&&fix(options.eventSurrogateSubstream)==options.eventSurrogateSubstream,'bst_apc:V2Substream','Invalid surrogate substream');
[data,time]=validate_input_matrix(sMatrix);n=size(data,1);
runInfo=struct('version','v2.0','options',options,'route',strings(n,1),'amplitude_sigma_hz',nan(n,1),'candidate_half_width_hz',nan(n,1), ...
 'final_half_width_hz',nan(n,1),'effective_half_width_hz',nan(n,1),'final_band_hz',nan(n,2), ...
 'burst_times_s',{cell(n,1)},'usable_burst_times_s',{cell(n,1)},'diagnostics',{cell(n,1)}, ...
 'surrogate_ppc',{cell(n,1)},'surrogate_blp_max',{cell(n,1)},'surrogate_blp_fixed',{cell(n,1)},'surrogate_seed',repmat(options.eventSurrogateSeed,n,1), ...
 'surrogate_substream',(options.eventSurrogateSubstream:options.eventSurrogateSubstream+n-1).');
names={'pac_strength','phase_frequency_hz','amplitude_frequency_hz','preferred_phase_deg','n_bursts','n_phase_events', ...
 'status_code','ozkurt_mvl','event_ppc','event_z','event_p','n_usable_bursts','diagnostic_flags', ...
 'event_blp','event_statistic','event_z_fixed','event_p_fixed'};
values=nan(n,numel(names));
for j=1:n
 local=options;local.eventSurrogateSubstream=runInfo.surrogate_substream(j);
 [m,d]=compute_signal_apc_v2(data(j,:),time,local);
 for k=1:numel(names),values(j,k)=m.(names{k});end
 runInfo.route(j)=m.route;runInfo.amplitude_sigma_hz(j)=1.5*m.phase_frequency_hz;
 runInfo.final_band_hz(j,:)=m.final_band_hz;runInfo.burst_times_s{j}=d.burst_times_s;
 runInfo.usable_burst_times_s{j}=d.usable_burst_times_s;runInfo.diagnostics{j}=d;runInfo.surrogate_ppc{j}=d.surrogate_ppc;
 runInfo.surrogate_blp_max{j}=d.surrogate_blp_max;runInfo.surrogate_blp_fixed{j}=d.surrogate_blp_fixed;
 if options.showPlots,plot_signal_diagnostics(j,d,m,options);end
end
units={'a.u.','Hz','Hz','deg','count','count','code','a.u.','a.u.','z','p','count','bitmask','a.u.^2','a.u.^2','z','p'};
for k=1:numel(names),sApc.(names{k})=pack_feature(values(:,k),units{k},['APC v2 fixed specification: ' names{k}]);end
sApc.burst_count=sApc.n_bursts;
end

function [m,d]=compute_signal_apc_v2(signal,time,options)
m=struct('pac_strength',nan,'phase_frequency_hz',nan,'amplitude_frequency_hz',nan,'preferred_phase_deg',nan, ...
 'n_bursts',0,'n_phase_events',0,'status_code',0,'ozkurt_mvl',nan,'event_ppc',nan,'event_z',nan,'event_p',nan, ...
 'n_usable_bursts',0,'diagnostic_flags',0,'route',"not_reached",'final_band_hz',[nan nan], ...
 'event_blp',nan,'event_statistic',nan,'event_z_fixed',nan,'event_p_fixed',nan);
d=struct('burst_times_s',[],'usable_burst_times_s',[],'burst_locations',[],'burst_trace',[], ...
 'phase_grid_hz',[],'ppc_grid',[],'usable_count_grid',[],'selected_grid_fp_hz',nan,'parabolic_delta_bins',0, ...
 'phase_band_hz',[],'final_phase',[],'observed_burst_phases',[],'amplitude_grid_hz',[],'amplitude_scores_raw',[], ...
 'amplitude_scores_smoothed',[],'surrogate_ppc',[],'time_epoch',[],'burst_average',[], ...
 'phase_epoch_time',[],'phase_locked_average',[],'phase_locked_tf',[],'phase_locked_freqs',[], ...
 'trough_locations',[],'diagnostic_error_identifier','','diagnostic_error_message','', ...
 'blp_grid',[],'coefficients_grid',[],'coefficients_at_fp',[],'burstlock_relative_time',[],'burstlock_window',[], ...
 'usable_center_sample_bounds',[],'surrogate_blp_max',[],'surrogate_blp_fixed',[],'first_surrogate_centers',[], ...
 'first_surrogate_blp_grid',[],'selected_grid_fa_hz',nan,'amplitude_parabolic_delta_bins',0, ...
 'amplitude_gaussian_sigma_hz',nan,'amplitude_padding_samples',0,'amplitude_envelope',[]);
signal=double(signal(:).');time=double(time(:).');
if numel(signal)<10 || all(~isfinite(signal)),m.status_code=1;return;end
signal=fillmissing(signal,'linear','EndValues','nearest');signal=signal-mean(signal,'omitnan');
fs=1/median(diff(time));duration=numel(signal)/fs;
if ~isfinite(fs)||fs<=0,m.status_code=1;return;end
if duration<4-32*eps(4),m.status_code=1;return;end
ampRange=[options.fA(1),min(options.fA(2),fs/2-eps)];
if ampRange(2)<=ampRange(1),m.status_code=1;return;end

% Step 1 is exactly the frozen v1 burst trace and peak detection.
[burstTrace,~]=compute_burst_trace(signal,fs,ampRange,options.burstTimeBandwidth);
burstTrace=smoothdata(burstTrace,'movmean',max(3,round(.02*fs)));
burstLocs=detect_peaks_with_defaults(burstTrace,max(1,round(.9*fs/max(ampRange(1),eps))), ...
 options.burstProminenceScale*std(burstTrace,0,2));
m.n_bursts=numel(burstLocs);d.burst_locations=burstLocs;d.burst_times_s=time(burstLocs);d.burst_trace=burstTrace;

% Candidate 2 Step 2: direct, debiased burst-locked Fourier power.
winLen=round(2*fs);offsets=-floor(winLen/2):ceil(winLen/2)-1;
minCenter=1-offsets(1);maxCenter=numel(signal)-offsets(end);
usable=burstLocs(burstLocs>=minCenter & burstLocs<=maxCenter);
m.n_usable_bursts=numel(usable);d.usable_burst_times_s=time(usable);
d.usable_center_sample_bounds=[minCenter maxCenter];
d.burstlock_relative_time=offsets/fs;d.burstlock_window=hann(winLen,'symmetric').';
fmin=max([options.minPhaseHz,10/duration,3/2]);fmax=min([options.maxPhaseHz,ampRange(1)/2,fs/3]);
grid=fmin:.05:fmax;d.phase_grid_hz=grid;d.usable_count_grid=repmat(numel(usable),size(grid));
d.blp_grid=nan(size(grid));d.ppc_grid=nan(size(grid));
if numel(usable)<10 || isempty(grid),m.status_code=3;return;end
coefficients=v2_direct_coefficients(signal,usable,offsets,fs,grid);
[blp,ppc]=v2_blp_and_ppc(coefficients);d.blp_grid=blp;d.ppc_grid=ppc;d.coefficients_grid=coefficients;
if ~any(isfinite(blp)),m.status_code=3;return;end
[observedMax,best]=max(blp,[],'omitnan');fp=grid(best);d.selected_grid_fp_hz=fp;
if best>1 && best<numel(grid) && all(isfinite(blp(best-1:best+1)))
 y=blp(best-1:best+1);den=y(1)-2*y(2)+y(3);
 if isfinite(den)&&den<0
  delta=.5*(y(1)-y(3))/den;delta=max(-.5,min(.5,delta));fp=fp+delta*.05;d.parabolic_delta_bins=delta;
 end
end
phaseBand=v2_phase_band(fp);phaseSignal=carrier_bandpass(signal,fs,phaseBand,'v1');
if isempty(phaseSignal),m.status_code=3;return;end
phase=angle(hilbert(phaseSignal));d.phase_band_hz=phaseBand;d.final_phase=phase;
coeffAtFp=v2_direct_coefficients(signal,usable,offsets,fs,fp);d.coefficients_at_fp=coeffAtFp;
[observedFixed,ppcAtFp]=v2_blp_and_ppc(coeffAtFp);d.observed_burst_phases=angle(coeffAtFp).';
m.phase_frequency_hz=fp;m.event_ppc=ppcAtFp;m.event_blp=observedFixed;m.event_statistic=observedMax;

% Step 3 affects diagnostics only. A failed profile never stops Step 4.
try
 [epochs,epochTime]=collect_burst_epochs(signal,burstLocs,fs,options.epoch,options.flipTroughs);
 d.time_epoch=epochTime;
 if isempty(epochs),m.diagnostic_flags=bitor(m.diagnostic_flags,1);else,d.burst_average=mean(epochs,1,'omitnan');end
 troughs=detect_troughs(phaseSignal,fs,fp);d.trough_locations=troughs;m.n_phase_events=numel(troughs);
 if isempty(troughs)
  m.diagnostic_flags=bitor(m.diagnostic_flags,2);
 else
  local=options;local.fA=ampRange;
  [avg,tf,freqs,epochTime]=collect_phase_locked_tf(signal,troughs,fs,fp,local);
  if isempty(avg)||isempty(tf)
   m.diagnostic_flags=bitor(m.diagnostic_flags,4);
  else
   d.phase_locked_average=avg;d.phase_locked_tf=tf;d.phase_locked_freqs=freqs;d.phase_epoch_time=epochTime;
  end
 end
catch err
 m.diagnostic_flags=bitor(m.diagnostic_flags,8);d.diagnostic_error_identifier=err.identifier;d.diagnostic_error_message=err.message;
end

% Candidate 3 Step 4: positive-frequency Gaussian analytic kernel.
faGrid=ampRange(1):1:ampRange(2);scores=nan(size(faGrid));sigma=1.5*fp;pad=round(fs);
padded=[signal(pad+1:-1:2),signal,signal(end-1:-1:end-pad)];spectrum=fft(padded);
bins=0:numel(padded)-1;bins(bins>floor(numel(padded)/2))=bins(bins>floor(numel(padded)/2))-numel(padded);
frequencies=bins*fs/numel(padded);
crop=pad+(1:numel(signal));
for k=1:numel(faGrid)
 envelope=v2_gaussian_envelope(spectrum,frequencies,faGrid(k),sigma,crop);
 scores(k)=abs(mean(envelope.*exp(1i*phase)));
end
d.amplitude_grid_hz=faGrid;d.amplitude_scores_raw=scores;d.amplitude_gaussian_sigma_hz=sigma;d.amplitude_padding_samples=pad;
if isempty(scores)||~any(isfinite(scores)),m.status_code=5;return;end
[~,best]=max(scores,[],'omitnan');fa=faGrid(best);d.selected_grid_fa_hz=fa;
if best>1 && best<numel(faGrid) && all(isfinite(scores(best-1:best+1)))
 y=scores(best-1:best+1);den=y(1)-2*y(2)+y(3);
 if isfinite(den)&&den<0
  delta=.5*(y(1)-y(3))/den;delta=max(-.5,min(.5,delta));fa=fa+delta;d.amplitude_parabolic_delta_bins=delta;
 end
end
envelope=v2_gaussian_envelope(spectrum,frequencies,fa,sigma,crop);d.amplitude_envelope=envelope;
vector=mean(envelope.*exp(1i*phase));raw=abs(vector);rmsAmp=sqrt(mean(envelope.^2));
m.amplitude_frequency_hz=fa;m.pac_strength=raw;m.preferred_phase_deg=rad2deg(angle(vector));
if rmsAmp>0,m.ozkurt_mvl=raw/rmsAmp;else,m.ozkurt_mvl=0;end
m.route="gaussian_mvl_scan";

% Candidate 2 event test: full-grid maximum and secondary fixed frequency.
stream=RandStream(options.eventSurrogateGenerator,'Seed',options.eventSurrogateSeed);stream.Substream=options.eventSurrogateSubstream;
jitterCenters=zeros(200,numel(usable));
low=max(-1/fp,(minCenter-usable)/fs);high=min(1/fp,(maxCenter-usable)/fs);
for k=1:200
 jitter=low+(high-low).*rand(stream,size(usable));jitterCenters(k,:)=usable+jitter*fs;
end
assert(all(jitterCenters>=minCenter & jitterCenters<=maxCenter,'all'),'bst_apc:V2JitterBounds','Event surrogate escaped usable range');
% Exact linearity of demean/window/Fourier: evaluate direct sums once at
% every unique bracketing sample center, then interpolate coefficients.
lower=floor(jitterCenters);upper=ceil(jitterCenters);fraction=jitterCenters-lower;
uniqueCenters=unique([lower(:);upper(:)]);frequencies=[grid fp];
allCoefficients=v2_direct_coefficients(signal,uniqueCenters,offsets,fs,frequencies);
[~,lowerIndex]=ismember(lower,uniqueCenters);[~,upperIndex]=ismember(upper,uniqueCenters);
surrMax=nan(1,200);surrFixed=nan(1,200);
for k=1:200
 surrogateCoefficients=(1-fraction(k,:).').*allCoefficients(lowerIndex(k,:),:) + ...
  fraction(k,:).'.*allCoefficients(upperIndex(k,:),:);
 surrogateBLP=v2_blp_and_ppc(surrogateCoefficients);
 if k==1,d.first_surrogate_blp_grid=surrogateBLP(1:numel(grid));end
 surrMax(k)=max(surrogateBLP(1:numel(grid)));surrFixed(k)=surrogateBLP(end);
end
d.first_surrogate_centers=jitterCenters(1,:);d.surrogate_blp_max=surrMax;d.surrogate_blp_fixed=surrFixed;
sd=std(surrMax,0);sdFixed=std(surrFixed,0);
if isfinite(sd)&&sd>0,m.event_z=(observedMax-mean(surrMax))/sd;else,m.diagnostic_flags=bitor(m.diagnostic_flags,16);end
if isfinite(sdFixed)&&sdFixed>0,m.event_z_fixed=(observedFixed-mean(surrFixed))/sdFixed;else,m.diagnostic_flags=bitor(m.diagnostic_flags,16);end
m.event_p=(1+sum(surrMax>=observedMax))/201;m.event_p_fixed=(1+sum(surrFixed>=observedFixed))/201;
end

function coefficients=v2_direct_coefficients(signal,centers,offsets,fs,frequencies)
indices=centers(:)+offsets;segments=signal(indices);segments=segments-mean(segments,2);
segments=segments.*hann(numel(offsets),'symmetric').';
basis=exp(-1i*2*pi*(offsets(:)/fs)*frequencies(:).');
coefficients=segments*basis;
end
function [blp,ppc]=v2_blp_and_ppc(coefficients)
n=size(coefficients,1);blp=(abs(sum(coefficients,1)).^2-sum(abs(coefficients).^2,1))/(n*(n-1));
unit=exp(1i*angle(coefficients));ppc=(abs(sum(unit,1)).^2-n)/(n*(n-1));
end

function band=v2_phase_band(fp)
half=max(.5,.25*fp);band=[fp-half,fp+half];
end
function envelope=v2_gaussian_envelope(spectrum,frequencies,center,sigma,crop)
gain=2*exp(-((frequencies-center).^2)/(2*sigma^2));gain(frequencies<=0)=0;
analytic=ifft(spectrum.*gain);envelope=abs(analytic(crop));
end
function value=v2_ppc(phases)
phases=phases(isfinite(phases));n=numel(phases);
if n<2,value=nan;else,value=(abs(sum(exp(1i*phases)))^2-n)/(n*(n-1));end
end

function [sApc,runInfo]=compute_matrix_apc_v3(sMatrix,optionsIn)
% v3 changes only the Step-2 spectral peak rule in the shared v1 pipeline.
options=normalize_options(optionsIn);options.version='v3';
[data,time]=validate_input_matrix(sMatrix);n=size(data,1);
runInfo=struct('version','v3.0','options',options,'route',strings(n,1), ...
 'candidate_half_width_hz',nan(n,1),'final_half_width_hz',nan(n,1), ...
 'effective_half_width_hz',nan(n,1),'final_band_hz',nan(n,2), ...
 'aperiodic_exponent',nan(n,1),'aperiodic_offset',nan(n,1), ...
 'aperiodic_peak_height',nan(n,1),'aperiodic_sigma',nan(n,1), ...
 'f_lo_hz',nan(n,1),'f_hi_hz',nan(n,1),'diagnostics',{cell(n,1)});
names={'pac_strength','phase_frequency_hz','amplitude_frequency_hz','preferred_phase_deg','n_bursts','n_phase_events','status_code'};
units={'a.u.','Hz','Hz','deg','count','count','code'};values=nan(n,numel(names));
for j=1:n
 [m,d]=compute_signal_apc(data(j,:),time,options);
 for k=1:numel(names),values(j,k)=m.(names{k});end
 runInfo.route(j)=m.route;runInfo.candidate_half_width_hz(j)=m.candidate_half_width_hz;
 runInfo.final_half_width_hz(j)=m.final_half_width_hz;runInfo.effective_half_width_hz(j)=m.final_half_width_hz;
 runInfo.final_band_hz(j,:)=m.final_band_hz;runInfo.diagnostics{j}=d;
 if isfield(d,'aperiodic')
  a=d.aperiodic;runInfo.aperiodic_exponent(j)=a.exponent;runInfo.aperiodic_offset(j)=a.offset;
  runInfo.aperiodic_peak_height(j)=a.peak_height;runInfo.aperiodic_sigma(j)=a.sigma;
  runInfo.f_lo_hz(j)=a.f_lo_hz;runInfo.f_hi_hz(j)=a.f_hi_hz;
 end
 if options.showPlots,plot_signal_diagnostics(j,d,m,options);end
end
for k=1:numel(names),sApc.(names{k})=pack_feature(values(:,k),units{k},['APC v3: ' names{k}]);end
extra={'aperiodic_exponent','aperiodic_offset','aperiodic_peak_height','aperiodic_sigma'};
for k=1:numel(extra),sApc.(extra{k})=pack_feature(runInfo.(extra{k}),'log10-power diagnostics',['APC v3 Step 2: ' extra{k}]);end
end

function [phaseFreq,d]=estimate_phase_frequency_v3(epochSignal,fs,options,T)
% Same v1 BTA demeaning, Welch call and refined spectral-bin spacing.
signal=epochSignal(:)-mean(epochSignal,'omitnan');
nfft=max(256,2^nextpow2(numel(signal)));
nfft=max(nfft,2^nextpow2(ceil(fs/options.fPMaxBinSpacingHz)));
[pxx,f]=pwelch(signal,[],[],nfft,fs);
flo=max(options.minPhaseHz,7/T);fhi=min([options.maxPhaseHz,fs/3,options.fA(1)-.5]);
[phaseFreq,d]=apc_v3_spectral_peak(pxx,f,flo,fhi);
d.nfft=nfft;d.fs_hz=fs;d.duration_s=T;d.spectrum='v1 BTA Welch';
end
