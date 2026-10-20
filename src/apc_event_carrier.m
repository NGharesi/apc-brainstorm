function out = apc_event_carrier(signal, fs, apcOutput, amplitudeCandidatesHz, amplitudeHalfWidthHz, phaseHalfWidthHz, minPeakDistanceSec)
% APC_EVENT_CARRIER Frozen event-carrier extension of APC.
% APC estimates fP; independent candidate envelopes are ranked by the
% concentration of their high-amplitude event phases at that fP.
    if nargin < 5 || isempty(amplitudeHalfWidthHz), amplitudeHalfWidthHz = 6; end
    if nargin < 6 || isempty(phaseHalfWidthHz), phaseHalfWidthHz = 1.5; end
    if nargin < 7 || isempty(minPeakDistanceSec), minPeakDistanceSec = 0.020; end
    out = struct('valid', false, 'status_code', NaN, 'fp_hz', NaN, ...
        'fa_hz', NaN, 'preferred_phase_deg', NaN, 'score', 0, ...
        'n_carrier_events', 0);
    if isfield(apcOutput, 'phase_frequency_hz')
        status = double(apcOutput.status_code.Value(1));
        fp = double(apcOutput.phase_frequency_hz.Value(1));
    else
        status = double(apcOutput.status_code);
        fp = double(apcOutput.fp_hz);
    end
    out.status_code = status;
    if status ~= 0 || ~isfinite(fp), return; end
    x = double(signal(:));
    out.fp_hz = fp;
    phase = angle(hilbert(local_bandpass(x, fs, max(0.5, fp-phaseHalfWidthHz), fp+phaseHalfWidthHz)));
    scores = nan(size(amplitudeCandidatesHz));
    phases = nan(size(amplitudeCandidatesHz));
    counts = zeros(size(amplitudeCandidatesHz));
    for i = 1:numel(amplitudeCandidatesHz)
        fa = amplitudeCandidatesHz(i);
        if fa-amplitudeHalfWidthHz <= 0 || fa+amplitudeHalfWidthHz >= fs/2
            continue;
        end
        envelope = abs(hilbert(local_bandpass(x, fs, fa-amplitudeHalfWidthHz, fa+amplitudeHalfWidthHz)));
        threshold = median(envelope) + 0.75 * std(envelope);
        [~, eventIdx] = findpeaks(envelope, ...
            'MinPeakProminence', 0.25 * std(envelope), ...
            'MinPeakDistance', max(1, round(minPeakDistanceSec * fs)));
        eventIdx = eventIdx(envelope(eventIdx) >= threshold);
        if isempty(eventIdx), continue; end
        z = mean(exp(1i * phase(eventIdx)));
        scores(i) = abs(z);
        phases(i) = rad2deg(angle(z));
        counts(i) = numel(eventIdx);
    end
    [best, index] = max(scores, [], 'omitnan');
    out.valid = isfinite(best);
    out.status_code = double(~out.valid);
    if out.valid
        out.fa_hz = amplitudeCandidatesHz(index);
        out.preferred_phase_deg = phases(index);
        out.score = best;
        out.n_carrier_events = counts(index);
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
    d = designfilt('bandpassiir', 'FilterOrder', 4, ...
        'HalfPowerFrequency1', wn(1) * fs / 2, ...
        'HalfPowerFrequency2', wn(2) * fs / 2, 'SampleRate', fs);
    x = filtfilt(d, double(signal(:)));
end
