function rows=fu_comparators(signal,fs,amplitudeModes,phaseSteps)
% Original comparator filter/metric definitions; A1 changes only band width.
% Each metric independently maximizes its own score over the full grid.
rows=struct('configuration',{},'method',{},'fp_grid_step_hz',{},'fp',{},'fa',{},'score',{},'route',{},'status',{}, ...
 'candidate_half_width_hz',{},'effective_half_width_hz',{},'final_low_hz',{},'final_high_hz',{});
signal=double(signal(:));faGrid=80:8:152;
for step=phaseSteps
 fpGrid=4:step:12;
 for im=1:numel(amplitudeModes)
  mode=amplitudeModes(im);scores=nan(numel(fpGrid),numel(faGrid),4);
  for ip=1:numel(fpGrid)
   fp=fpGrid(ip);phase=angle(hilbert(local_filter(signal,fs,[max(.5,fp-1.5),fp+1.5])));
   for ia=1:numel(faGrid)
    half=6;if mode=="A1",half=fp;elseif mode=="A2",half=12;end
    band=[max(1,faGrid(ia)-half),min(fs/2-1,faGrid(ia)+half)];
    amp=abs(hilbert(local_filter(signal,fs,band)));
    scores(ip,ia,1)=calc_MI_all_methods(phase,amp,'canolty',false,0,1,false,18);
    ampRms=sqrt(mean(amp.^2));
    if ampRms>0,scores(ip,ia,2)=scores(ip,ia,1)/ampRms;else,scores(ip,ia,2)=0;end
    scores(ip,ia,3)=calc_MI_all_methods(phase,amp,'tort',false,0,1,false,18);
    X=[ones(size(phase)),sin(phase),cos(phase)];beta=X\amp;yhat=X*beta;
    ssRes=sum((amp-yhat).^2);ssTot=sum((amp-mean(amp)).^2);
    if ssTot<=0,scores(ip,ia,4)=0;else,scores(ip,ia,4)=max(0,1-ssRes/ssTot);end
   end
  end
  names=["MVL-raw","MVL-Ozkurt","KLMI-scan","GLM-scan"];
  for metric=1:4
   map=scores(:,:,metric);[score,index]=max(map(:),[],'omitnan');[ip,ia]=ind2sub(size(map),index);
   selectedHalf=6;if mode=="A1",selectedHalf=fpGrid(ip);elseif mode=="A2",selectedHalf=12;end
   rows(end+1)=struct('configuration',mode,'method',names(metric),'fp_grid_step_hz',step, ...
    'fp',fpGrid(ip),'fa',faGrid(ia),'score',score,'route',"not_applicable",'status',double(~isfinite(score)), ...
    'candidate_half_width_hz',selectedHalf,'effective_half_width_hz',selectedHalf, ...
    'final_low_hz',max(1,faGrid(ia)-selectedHalf),'final_high_hz',min(fs/2-1,faGrid(ia)+selectedHalf)); %#ok<AGROW>
  end
 end
end
end
function y=local_filter(x,fs,band)
persistent keys coeffs
if isempty(keys),keys={};coeffs={};end
key=sprintf('%.17g,%.17g,%.17g',fs,band(1),band(2));i=find(strcmp(keys,key),1);
if isempty(i)
 wn=band/(fs/2);wn(1)=max(wn(1),1e-4);wn(2)=min(wn(2),.999);
 if wn(2)<=wn(1),y=zeros(size(x));return;end
 [b,a]=butter(4,wn,'bandpass');keys{end+1}=key;coeffs{end+1}={b,a};
else
 b=coeffs{i}{1};a=coeffs{i}{2};
end
y=filtfilt(b,a,double(x(:)));
end
