function rows=v3_comparators(signal,fs,profile,modes,steps)
% Metrics/grids/ties unchanged; all filtering goes through guarded SOS helper.
signal=double(signal(:));names=["MVL-raw","MVL-Ozkurt","KLMI","GLM"];
if profile=="HA",faGrid=80:4:160;fpStart=3;fpStop=30;
elseif profile=="heldout",faGrid=80:4:160;fpStart=3;fpStop=14;
elseif profile=="rodent",faGrid=80:4:148;fpStart=4;fpStop=12;
else,faGrid=80:8:152;fpStart=4;fpStop=12;end
rows=struct([]);
for step=steps
 fpGrid=fpStart:step:fpStop;
 % Cache analytic series within the input: identical bands are reused.
 bands={};envs={};phases=cell(1,numel(fpGrid));
 for ip=1:numel(fpGrid),phases{ip}=angle(hilbert(final_sos_filter(signal,fs,[max(.5,fpGrid(ip)-1.5),fpGrid(ip)+1.5])));end
 for mode=modes
  scores=nan(numel(fpGrid),numel(faGrid),4);ozscores=nan(numel(fpGrid),numel(faGrid));pref=ozscores;
  for ip=1:numel(fpGrid)
   fp=fpGrid(ip);phase=phases{ip};X=[ones(size(phase)),sin(phase),cos(phase)];
   for ia=1:numel(faGrid)
    half=6;if mode=="A1"||mode=="A1_prime",half=fp;elseif mode=="A2"||mode=="rodent_A2_prime",half=12;elseif mode=="A2_prime",half=14;elseif mode=="HA_A2_prime",half=30;end
    band=[max(1,faGrid(ia)-half),min(fs/2-1,faGrid(ia)+half)];key=sprintf('%.17g %.17g',band);j=find(strcmp(bands,key),1);
    if isempty(j),A=abs(hilbert(final_sos_filter(signal,fs,band)));bands{end+1}=key;envs{end+1}=A;else,A=envs{j};end %#ok<AGROW>
    scores(ip,ia,1)=calc_MI_all_methods(phase,A,'canolty',false,0,1,false,18);
    ampRms=sqrt(mean(A.^2));if ampRms>0,scores(ip,ia,2)=scores(ip,ia,1)/ampRms;else,scores(ip,ia,2)=0;end
    scores(ip,ia,3)=calc_MI_all_methods(phase,A,'tort',false,0,1,false,18);
    beta=X\A;ssTot=sum((A-mean(A)).^2);if ssTot<=0,scores(ip,ia,4)=0;else,scores(ip,ia,4)=max(0,1-sum((A-X*beta).^2)/ssTot);end
    ozscores(ip,ia)=scores(ip,ia,2);pref(ip,ia)=rad2deg(angle(mean(A.*exp(1i*phase))));
   end
  end
  for k=1:4
   map=scores(:,:,k);[score,j]=max(map(:),[],'omitnan');[ip,ia]=ind2sub(size(map),j);fp=fpGrid(ip);fa=faGrid(ia);
   item=struct('configuration',mode,'method',names(k),'fp_grid_step_hz',step,'fp',fp,'fa',fa,'score',score,'status',double(~isfinite(score)),'raw_mvl',scores(ip,ia,1),'ozkurt_mvl',ozscores(ip,ia),'preferred_phase_deg',pref(ip,ia));rows=[rows;item]; %#ok<AGROW>
  end
 end
end
end
