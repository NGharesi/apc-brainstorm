function [fp,d,status]=apc_v3_spectral_peak(power,frequency,flo,fhi)
% Fixed two-pass, no-knee log-log OLS rule shared by APC v3 and SP-raw.
fp=nan;status=3;d=struct('exponent',nan,'offset',nan,'peak_height',nan,'sigma',nan, ...
 'f_lo_hz',flo,'f_hi_hz',fhi,'frequency_hz',[],'power',[],'log10_power',[], ...
 'pass1_residual',[],'pass2_mask',[],'aperiodic_fit',[],'residual',[], ...
 'candidate_indices',[],'selected_index',nan,'selected_grid_fp_hz',nan, ...
 'parabolic_delta_bins',0,'fp_hz',nan);
frequency=double(frequency(:));power=double(power(:));
valid=frequency>=flo&frequency<=fhi&frequency>0&isfinite(power)&power>0;
f=frequency(valid);p=power(valid);d.frequency_hz=f;d.power=p;
if numel(f)<3||~isfinite(flo)||~isfinite(fhi)||fhi<=flo,return;end
x=log10(f);y=log10(p);X=[x ones(size(x))];b1=X\y;r1=y-X*b1;
use=r1<=median(r1);if sum(use)<2,return;end
b2=X(use,:)\y(use);fit=X*b2;r=y-fit;sigma=std(r(use),0);
d.exponent=-b2(1);d.offset=b2(2);d.sigma=sigma;d.log10_power=y;
d.pass1_residual=r1;d.pass2_mask=use;d.aperiodic_fit=fit;d.residual=r;
candidates=find(r(2:end-1)>r(1:end-2)&r(2:end-1)>r(3:end)&r(2:end-1)>=2*sigma)+1;
d.candidate_indices=candidates;if isempty(candidates),return;end
[~,j]=max(r(candidates));i=candidates(j);fp=f(i);d.selected_index=i;d.selected_grid_fp_hz=fp;
neighbors=r(i-1:i+1);den=neighbors(1)-2*neighbors(2)+neighbors(3);delta=0;
if isfinite(den)&&den<0
 delta=.5*(neighbors(1)-neighbors(3))/den;delta=max(-.5,min(.5,delta));
 fp=min(max(f(i)+delta*(f(i+1)-f(i)),flo),fhi);
end
d.parabolic_delta_bins=delta;d.peak_height=neighbors(2)+.5*(neighbors(3)-neighbors(1))*delta+.5*den*delta^2;
d.fp_hz=fp;status=0;
end
