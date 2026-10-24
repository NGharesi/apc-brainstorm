function [metrics,diagnostics,options]=apc_fa_given_fp(signal,time,phaseFreq,optionsIn)
% Exact v3.0 Steps 3-4; the outer wrapper only adds normalized MVL/metadata.
if nargin<4,optionsIn=struct;end
options=normalize_options(optionsIn);
[metrics,diagnostics,amplitudeEnvelope,phaseSignal]=extracted_steps34(signal,time,phaseFreq,options);
metrics.normalized_mvl=nan;
diagnostics.supplied_fp_hz=phaseFreq;diagnostics.options=options;
if metrics.status_code==0
 metrics.normalized_mvl=metrics.pac_strength/sqrt(mean(amplitudeEnvelope.^2));
 diagnostics.phase_band_hz=get_phase_band(phaseFreq,options.fA(1),1/median(diff(time)));
end
end

function [metrics,diagnostics,amplitudeEnvelope,phaseSignal]=extracted_steps34(signal,time,phaseFreq,options)
amplitudeEnvelope=[];phaseSignal=[];
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

