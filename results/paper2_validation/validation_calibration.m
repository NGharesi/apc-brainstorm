function result=validation_calibration(x,fs,fp,cfg,shifts)
% Circular-shift maximum over every amplitude envelope at the fixed F3 fP.
result=struct('p',nan,'observed',nan,'surrogate_max',nan(1,200),'status',3,'seed',20261115,'shifts_samples',shifts);
if ~isfinite(fp),return;end
x=double(x(:));phase=angle(hilbert(final_sos_filter(x,fs,[max(.5,fp-1.5),fp+1.5])));z=exp(1i*phase);A=zeros(numel(x),numel(cfg.amplitude_grid_hz));
for j=1:size(A,2),fa=cfg.amplitude_grid_hz(j);h=cfg.amplitude_half_width_hz;A(:,j)=abs(hilbert(final_sos_filter(x,fs,[max(1,fa-h),min(fs/2-1,fa+h)])));end
rmsA=sqrt(mean(A.^2));rmsA(rmsA==0)=inf;observed=max(abs(mean(A.*z))./rmsA);
correlations=ifft(conj(fft(A)).*fft(z));values=abs(correlations)/numel(x)./rmsA;
% Check the numerical shortcut against the defining shifted time-domain sum.
for shift=[0 shifts(1) shifts(end)]
 exact=abs(mean(circshift(A,shift).*z))./rmsA;actual=values(mod(shift,numel(x))+1,:);
 assert(max(abs(exact-actual))<=1e-12,'Validation:ShiftComputation','Circular-shift computation differs from definition');
end
surrogate=max(values(shifts+1,:),[],2).';result.p=(1+sum(surrogate>=observed))/201;result.observed=observed;result.surrogate_max=surrogate;result.status=0;
end
