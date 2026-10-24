function result=paper2_coupling_at_pair(signal,time,fp,fa,band,family)
% Common APC phase-band rule, with each selected amplitude-band realization.
result=struct('normalized_mvl',nan,'raw_mvl',nan,'preferred_phase_deg',nan,'phase_band_hz',[nan nan],'amplitude_band_hz',band,'status',3);
if any(~isfinite([fp,fa,band]))||fp<=0,return;end
signal=double(signal(:).');time=double(time(:).');signal=fillmissing(signal,'linear','EndValues','nearest');signal=signal-mean(signal,'omitnan');fs=1/median(diff(time));
phaseBand=get_phase_band(fp,80,fs);phaseSignal=bandpass_signal(signal,fs,phaseBand);
if family=="APC",ampSignal=carrier_bandpass(signal,fs,band,'v1');else,assert(family=="SCAN");ampSignal=final_sos_filter(signal,fs,band).';end
if isempty(phaseSignal)||isempty(ampSignal),return;end
phase=angle(hilbert(phaseSignal));A=abs(hilbert(ampSignal));
[raw,pref]=calc_MI_all_methods(phase,A,'canolty','no',200,1,'no',18,'circular_shift');
result.raw_mvl=raw;result.normalized_mvl=raw/sqrt(mean(A.^2));result.preferred_phase_deg=pref;result.phase_band_hz=phaseBand;result.status=double(~isfinite(result.normalized_mvl));
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


function signalOut=carrier_bandpass(signal,fs,band,mode)
    if ~strcmp(mode,'v1'),signalOut=bandpass_signal(signal,fs,band);return;end
    signalOut=[];
    if numel(band)~=2||any(~isfinite(band))||band(1)<=0||band(2)>=fs/2||band(1)>=band(2),return;end
    % Fourth-order Butterworth bandpass, in SOS form. The v1 carrier bands
    % change with continuous fP; design the same IIR family directly.
    [z,p,k]=butter(2,band/(fs/2),'bandpass');[sos,g]=zp2sos(z,p,k);
    signalOut=filtfilt(sos,g,double(signal(:).'));
end

