function [metrics,diagnostics,options]=apc_fp_source(signal,time,versionName,optionsIn)
% Exact v3.0 Steps 1-2; retain fP before any amplitude-stage failure.
if nargin<4,optionsIn=struct;end
options=normalize_options(optionsIn);
if strcmp(versionName,'v3'),options.version='v3';else,assert(strcmp(versionName,'v1'));end
[metrics,diagnostics]=extracted_steps12(signal,time,options);
end

function [metrics,diagnostics]=extracted_steps12(signal,time,options)
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

    metrics.phase_frequency_hz=phaseFreq;
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
