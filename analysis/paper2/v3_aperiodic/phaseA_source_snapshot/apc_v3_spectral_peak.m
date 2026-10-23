function [fp,d,status]=apc_v3_spectral_peak(power,frequency,flo,fhi)
% Fixed two-pass, no-knee log-log OLS rule shared by APC v3 and SP-raw.
fp=nan;status=3;d=struct('exponent',nan,'offset',nan,'peak_height',nan,'sigma',nan, ...
 'f_lo_hz',flo,'f_hi_hz',fhi,'frequency_hz',[],'power',[],'log10_power',[], ...
 'pass1_residual',[],'pass2_mask',[],'aperiodic_fit',[],'residual',[], ...
 'candidate_indices',[],'selected_index',nan,'selected_grid_fp_hz',nan, ...
 'parabolic_delta_bins',0,'fp_hz',nan,'location_branch','not_reached', ...
 'peak_region_indices',[],'climb_path_indices',[],'location_index',nan,'location_grid_fp_hz',nan);
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
% Amendment 1: residual detects the peak; raw log power locates its summit.
left=i;right=i;
while left>1&&r(left-1)>0,left=left-1;end
while right<numel(r)&&r(right+1)>0,right=right+1;end
d.peak_region_indices=[left right];position=i;path=i;branch='residual_shoulder';
if r(i)>0
 while true
  if position>1&&position<numel(y)&&y(position)>y(position-1)&&y(position)>y(position+1)
   branch='raw_local_max';break;
  end
  adjacent=[position-1 position+1];adjacent=adjacent(adjacent>=left&adjacent<=right);
  if isempty(adjacent),break;end
  [higher,k]=max(y(adjacent));if higher<=y(position),break;end
  position=adjacent(k);path(end+1)=position; %#ok<AGROW>
 end
end
location=i;curve=r;if strcmp(branch,'raw_local_max'),location=position;curve=y;end
d.location_branch=branch;d.climb_path_indices=path;d.location_index=location;d.location_grid_fp_hz=f(location);
neighbors=curve(location-1:location+1);den=neighbors(1)-2*neighbors(2)+neighbors(3);delta=0;fp=f(location);
if isfinite(den)&&den<0
 delta=.5*(neighbors(1)-neighbors(3))/den;delta=max(-.5,min(.5,delta));
 fp=min(max(f(location)+delta*(f(location+1)-f(location)),flo),fhi);
end
d.parabolic_delta_bins=delta;residualNeighbors=r(location-1:location+1);residualDen=residualNeighbors(1)-2*residualNeighbors(2)+residualNeighbors(3);
d.peak_height=residualNeighbors(2)+.5*(residualNeighbors(3)-residualNeighbors(1))*delta+.5*residualDen*delta^2;
d.fp_hz=fp;status=0;
end
