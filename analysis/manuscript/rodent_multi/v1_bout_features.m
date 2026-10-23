function [row,info]=v1_bout_features(signal,time)
% Call the frozen method. Additional normalized feature uses its exact bands
% and filter designs; verify raw MVL and preferred phase against its outputs.
[s,info]=bst_apc(struct('data',double(signal(:).'),'time',double(time(:).')),struct('fA',[80 150]));
row=struct('method',"APC-v1.0",'fP_hz',s.phase_frequency_hz.Value,'fA_hz',s.amplitude_frequency_hz.Value,'score',s.pac_strength.Value,'raw_mvl',s.pac_strength.Value,'ozkurt_mvl',NaN,'preferred_phase_deg',s.preferred_phase_deg.Value,'status',s.status_code.Value,'route',string(info.route),'effective_half_width_hz',info.effective_half_width_hz);
if row.status~=0,return;end
x=double(signal(:).');x=fillmissing(x,'linear','EndValues','nearest');x=x-mean(x,'omitnan');fs=1/median(diff(time));
half=max(.5,.25*row.fP_hz);phaseBand=[max(.5,row.fP_hz-half),min([79.75,row.fP_hz+half,fs/2-eps])];
d=designfilt('bandpassiir','FilterOrder',4,'HalfPowerFrequency1',phaseBand(1),'HalfPowerFrequency2',phaseBand(2),'SampleRate',fs);
phi=angle(hilbert(filtfilt(d,x)));
[z,p,k]=butter(2,info.final_band_hz/(fs/2),'bandpass');[sos,g]=zp2sos(z,p,k);A=abs(hilbert(filtfilt(sos,g,x)));
complexMvl=mean(A.*exp(1i*phi));raw=abs(complexMvl);pref=rad2deg(angle(complexMvl));
assert(abs(raw-row.raw_mvl)<=1e-10*max(abs(raw),realmin),'Rodent:FeatureMismatch','Reconstructed raw APC MVL differs');
assert(abs(mod(pref-row.preferred_phase_deg+180,360)-180)<1e-8,'Rodent:PhaseMismatch','Reconstructed APC preferred phase differs');
row.ozkurt_mvl=raw/sqrt(mean(A.^2));
end
