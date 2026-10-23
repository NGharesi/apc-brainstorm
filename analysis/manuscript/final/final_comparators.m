function [rows,maps]=final_comparators(signal,fs)
% A2-prime rodent scans. Frozen inherited comparator formulas; requested grids.
signal=double(signal(:));fpGrid=4:.5:12;faGrid=80:4:148;
names=["MVL-raw","MVL-Ozkurt","KLMI","GLM"];maps=nan(numel(fpGrid),numel(faGrid),4);
envelopes=cell(1,numel(faGrid));
for ia=1:numel(faGrid),envelopes{ia}=abs(hilbert(filt(signal,fs,[max(1,faGrid(ia)-12),min(fs/2-1,faGrid(ia)+12)])));end
phases=cell(1,numel(fpGrid));
for ip=1:numel(fpGrid)
 phase=angle(hilbert(filt(signal,fs,[fpGrid(ip)-1.5,fpGrid(ip)+1.5])));phases{ip}=phase;X=[ones(size(phase)),sin(phase),cos(phase)];
 for ia=1:numel(faGrid)
  A=envelopes{ia};maps(ip,ia,1)=calc_MI_all_methods(phase,A,'canolty',false,0,1,false,18);
  maps(ip,ia,2)=maps(ip,ia,1)/sqrt(mean(A.^2));
  maps(ip,ia,3)=calc_MI_all_methods(phase,A,'tort',false,0,1,false,18);
  beta=X\A;maps(ip,ia,4)=max(0,1-sum((A-X*beta).^2)/sum((A-mean(A)).^2));
 end
end
rows=struct('method',{},'fp',{},'fa',{},'score',{},'raw_mvl',{},'ozkurt_mvl',{},'preferred_phase_deg',{});
for k=1:4
 map=maps(:,:,k);[score,j]=max(map(:),[],'omitnan');[ip,ia]=ind2sub(size(map),j);
 v=mean(envelopes{ia}.*exp(1i*phases{ip}));raw=abs(v);oz=raw/sqrt(mean(envelopes{ia}.^2));
 rows(end+1)=struct('method',names(k),'fp',fpGrid(ip),'fa',faGrid(ia),'score',score,'raw_mvl',raw,'ozkurt_mvl',oz,'preferred_phase_deg',rad2deg(angle(v))); %#ok<AGROW>
end
end
function y=filt(x,fs,band)
persistent keys coefs
if isempty(keys),keys={};coefs={};end
key=sprintf('%.17g %.17g %.17g',fs,band);j=find(strcmp(keys,key),1);
if isempty(j),wn=band/(fs/2);wn(1)=max(wn(1),1e-4);wn(2)=min(wn(2),.999);[b,a]=butter(4,wn,'bandpass');keys{end+1}=key;coefs{end+1}={b,a};else,b=coefs{j}{1};a=coefs{j}{2};end
y=filtfilt(b,a,x);
end
