function [y,info]=final_sos_filter(x,fs,band)
% Authorized numerical realization correction; nominal butter(4) unchanged.
persistent keys designs
if isempty(keys),keys={};designs={};end
key=sprintf('%.17g,%.17g,%.17g',fs,band(1),band(2));i=find(strcmp(keys,key),1);
if isempty(i)
 wn=band/(fs/2);wn(1)=max(wn(1),1e-4);wn(2)=min(wn(2),.999);
 assert(wn(2)>wn(1),'Final:FilterGuard','Invalid comparator band');
 [z,p,k]=butter(4,wn,'bandpass');[sos,g]=zp2sos(z,p,k);
 radius=max(abs(p));sectionRadius=0;for j=1:size(sos,1),sectionRadius=max(sectionRadius,max(abs(roots(sos(j,4:6)))));end
 centre=mean(wn)*(fs/2);w=[2*pi*centre/fs,2*pi*centre/fs+1e-10];hh=freqz(sos,w)*g;gain=abs(hh(1));
 info=struct('fs_hz',fs,'low_hz',wn(1)*fs/2,'high_hz',wn(2)*fs/2,'center_hz',centre,'max_pole_radius',radius,'max_sos_section_pole_radius',sectionRadius,'center_gain',gain,'guard_passed',radius<1 && sectionRadius<1 && abs(gain-1)<1e-3);
 assert(info.guard_passed,'Final:FilterGuard','Comparator band guard failed fs %.17g band %.17g %.17g pole %.17g gain %.17g',fs,band,radius,gain);
 keys{end+1}=key;designs{end+1}=struct('sos',sos,'g',g,'info',info);i=numel(keys);
end
d=designs{i};info=d.info;
assert(info.guard_passed,'Final:FilterGuard','Cached guard failed');
y=filtfilt(d.sos,d.g,double(x(:)));
assert(all(isfinite(y)),'Final:FilterOutput','SOS output nonfinite');
end
