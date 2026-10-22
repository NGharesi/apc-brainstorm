function rows=v2_heldout_comparators(signal,fs)
% Inherited comparator definitions on the predeclared held-out grids.
signal=double(signal(:));fpGrid=3:.5:14;faGrid=80:4:160;
names=["MVL-raw","MVL-Ozkurt","KLMI","GLM"];
rows=struct('configuration',{},'method',{},'fp',{},'fa',{},'score',{},'status',{});
for mode=["A2_prime","A1_prime"]
 scores=nan(numel(fpGrid),numel(faGrid),4);fixed=cell(1,numel(faGrid));
 if mode=="A2_prime"
  for ia=1:numel(faGrid),fixed{ia}=abs(hilbert(filter_band(signal,fs,[max(1,faGrid(ia)-14),min(fs/2-1,faGrid(ia)+14)])));end
 end
 for ip=1:numel(fpGrid)
  fp=fpGrid(ip);phase=angle(hilbert(filter_band(signal,fs,[max(.5,fp-1.5),fp+1.5])));
  X=[ones(size(phase)),sin(phase),cos(phase)];
  for ia=1:numel(faGrid)
   if mode=="A2_prime",amp=fixed{ia};else,amp=abs(hilbert(filter_band(signal,fs,[max(1,faGrid(ia)-fp),min(fs/2-1,faGrid(ia)+fp)])));end
   scores(ip,ia,1)=calc_MI_all_methods(phase,amp,'canolty',false,0,1,false,18);
   rmsAmp=sqrt(mean(amp.^2));if rmsAmp>0,scores(ip,ia,2)=scores(ip,ia,1)/rmsAmp;else,scores(ip,ia,2)=0;end
   scores(ip,ia,3)=calc_MI_all_methods(phase,amp,'tort',false,0,1,false,18);
   beta=X\amp;yhat=X*beta;ssTot=sum((amp-mean(amp)).^2);
   if ssTot<=0,scores(ip,ia,4)=0;else,scores(ip,ia,4)=max(0,1-sum((amp-yhat).^2)/ssTot);end
  end
 end
 for metric=1:4
  map=scores(:,:,metric);[score,index]=max(map(:),[],'omitnan');[ip,ia]=ind2sub(size(map),index);
  rows(end+1)=struct('configuration',mode,'method',names(metric),'fp',fpGrid(ip),'fa',faGrid(ia),'score',score,'status',double(~isfinite(score))); %#ok<AGROW>
 end
end
end
function y=filter_band(x,fs,band)
persistent keys coefficients
if isempty(keys),keys={};coefficients={};end
key=sprintf('%.17g,%.17g,%.17g',fs,band(1),band(2));i=find(strcmp(keys,key),1);
if isempty(i)
 wn=band/(fs/2);wn(1)=max(wn(1),1e-4);wn(2)=min(wn(2),.999);[b,a]=butter(4,wn,'bandpass');
 keys{end+1}=key;coefficients{end+1}={b,a};
else,b=coefficients{i}{1};a=coefficients{i}{2};end
y=filtfilt(b,a,double(x(:)));
end
