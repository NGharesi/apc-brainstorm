function [P,A]=ieeg_selected_series(signal,time,features,info)
% Reconstruct selected analytic series for the prespecified trial-shuffle null.
x=double(signal(:));P=complex(nan(numel(x),5));A=nan(numel(x),5);fs=2000;
for k=1:5
 z=features(k);if z.status~=0||~isfinite(z.score),continue;end
 if k==1
  y=x-mean(x);fsa=1/median(diff(time));half=max(.5,.25*z.fP_hz);band=[max(.5,z.fP_hz-half),min([79.75,z.fP_hz+half,fsa/2-eps])];
  d=designfilt('bandpassiir','FilterOrder',4,'HalfPowerFrequency1',band(1),'HalfPowerFrequency2',band(2),'SampleRate',fsa);phi=angle(hilbert(filtfilt(d,y)));
  [zz,pp,kk]=butter(2,info.final_band_hz/(fsa/2),'bandpass');[sos,g]=zp2sos(zz,pp,kk);amp=abs(hilbert(filtfilt(sos,g,y)));
 else
  phi=angle(hilbert(final_sos_filter(x,fs,[max(.5,z.fP_hz-1.5),z.fP_hz+1.5])));amp=abs(hilbert(final_sos_filter(x,fs,[z.fA_hz-12,z.fA_hz+12])));
 end
 P(:,k)=exp(1i*phi);A(:,k)=amp;oz=abs(mean(amp.*P(:,k)))/sqrt(mean(amp.^2));
 assert(abs(oz-z.ozkurt_mvl)<=1e-8*max(abs(oz),realmin),'IEEG:SelectedSeriesMismatch','Selected normalized MVL series differ');
end
end
