function n=ieeg_count_bursts(signal,time,options)
% Diagnostic count only, from unchanged v1 Step 1. Does not choose fP/fA.
% v1_bout_features remains the sole APC estimator call for each trial.
signal=double(signal(:).');signal=fillmissing(signal,'linear','EndValues','nearest');signal=signal-mean(signal,'omitnan');fs=1/median(diff(time));
band=[options.fA(1),min(options.fA(2),fs/2-eps)];
fb=cwtfilterbank('SignalLength',numel(signal),'SamplingFrequency',fs,'FrequencyLimits',band,'TimeBandwidth',options.burstTimeBandwidth);
[cfs,~]=cwt(signal,'FilterBank',fb);trace=sqrt(mean(abs(cfs).^2,1));trace=smoothdata(trace,'movmean',max(3,round(.02*fs)));
distance=max(1,round(.9*fs/max(band(1),eps)));prominence=options.burstProminenceScale*std(trace,0,2);
if ~isfinite(prominence)||prominence<=0,[~,locs]=findpeaks(trace,'MinPeakDistance',distance);
else,[~,locs]=findpeaks(trace,'MinPeakDistance',distance,'MinPeakProminence',prominence);end
sampleWindow=round(options.epoch*fs);n=sum(locs+sampleWindow(1)>=1&locs+sampleWindow(2)<=numel(signal));
end
