function [phaseFreq,trace] = fu_phase_trace(epochSignal, fs, options)
    trace=struct();
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
    trace.peak_hz=f(i);trace.bin_spacing_hz=fs/nfft;
    trace.left_hz=f(max(1,i-1));trace.right_hz=f(min(numel(f),i+1));
    trace.nfft=nfft;trace.delta=0;trace.interpolated=false;
    if options.fPRefine && i>1 && i<numel(f) && valid(i-1) && valid(i+1)
        y=log(max(pxx(i-1:i+1),realmin));den=y(1)-2*y(2)+y(3);
        if isfinite(den) && den<0
            delta=0.5*(y(1)-y(3))/den;delta=max(-0.5,min(0.5,delta));
            trace.delta=delta;trace.interpolated=true;
            phaseFreq=min(max(f(i)+delta*(fs/nfft),options.minPhaseHz),maxPhaseHz);
        end
    end
end

