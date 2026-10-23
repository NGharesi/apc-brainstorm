function result=chunked_behavior(time,tracking,session,out)
% User-authorized whole-recording historical speed calculation, with checkpoints.
time=double(time(:));tracking=double(tracking);fs=1/median(diff(time));
N=numel(time);L=331702;overlap=round(20*fs);edge=round(10*fs);
first=find(time>=time(1)+2,1);last=find(time<=time(end)-2,1,'last');
assert(last>first,'Rodent:ShortRecord','No samples after edge trim');
raw=tracking(:,1);missing=raw==-1|~isfinite(raw);x=raw;x(missing)=NaN;
[gs,ge]=segments(missing);gapSeconds=(ge-gs+1)/39.06;filled=false(size(missing));
for j=1:numel(gs)
 if gapSeconds(j)<=.5 && gs(j)>1 && ge(j)<numel(x)
  a=gs(j)-1;b=ge(j)+1;x(gs(j):ge(j))=interp1([a b],x([a b]),gs(j):ge(j));filled(gs(j):ge(j))=true;
 end
end
ledTime=(0:size(tracking,1)-1)'/39.06;
pos=interp1(ledTime,x,time,'linear','extrap');validPos=isfinite(pos);
if last-first+1<L
 starts=first;ends=last;short=true;
else
 starts=first:(L-overlap):(last-L+1);starts=unique([starts,last-L+1]);ends=starts+L-1;short=false;
end
coreStart=starts;coreEnd=ends-1;
coreStart(2:end)=coreStart(2:end)+edge;
% Derivative ownership is indexed by its left sample timestamp; keep the
% central boundary sample at an internal right edge (no one-sample seam gap).
coreEnd(1:end-1)=ends(1:end-1)-edge;
seams=zeros(numel(starts)-1,1);
for k=1:numel(seams)
 assert(coreStart(k+1)<=coreEnd(k)+1,'Rodent:ChunkGap','Uncovered chunk seam');
 seams(k)=floor((coreEnd(k)+coreStart(k+1))/2);
end
ownedStart=[first;seams+1];ownedEnd=[seams;last-1];
speed=nan(N-1,1);coverage=zeros(N-1,1,'uint8');routes=cell(numel(starts),1);
rng(0,'twister');clockStart=tic;
for k=1:numel(starts)
 chunkStart=starts(k);chunkEnd=ends(k);checkpoint=fullfile(out,sprintf('%s_speed_chunk_%02d.mat',session,k));
 if isfile(checkpoint)
  Q=load(checkpoint);assert(Q.chunkStart==chunkStart&&Q.chunkEnd==chunkEnd&&isequaln(Q.position,pos(chunkStart:chunkEnd)), 'Rodent:CacheMismatch','Chunk checkpoint differs');
  chunkSpeed=Q.chunkSpeed;route=Q.route;rng(Q.rngAfter);
 else
  position=pos(chunkStart:chunkEnd);rngBefore=rng;chunkClock=tic;
  fprintf('%s chunk %d/%d: %d:%d (%d samples)\n',session,k,numel(starts),chunkStart,chunkEnd,numel(position));
  trend=trenddecomp(position);if isstruct(trend),trend=trend.signal;else,trend=trend(:,1);end
  route='trenddecomp';chunkSpeed=diff(trend)./diff(time(chunkStart:chunkEnd));rngAfter=rng;elapsed=toc(chunkClock);
  provenance=struct('git_tag','v1.0','git_commit','71ebc16aed32ca38be73a800738b975e5806b330','matlab_version',version,'seed',0,'stage','chunked speed; user amended protocol','session',session);
  save(checkpoint,'position','chunkStart','chunkEnd','chunkSpeed','route','rngBefore','rngAfter','elapsed','provenance','-v7');
  fprintf('completed %.1f seconds\n',elapsed);
 end
 globalIdx=ownedStart(k):ownedEnd(k);assert(all(globalIdx>=chunkStart&globalIdx<=chunkEnd-1),'Rodent:SeamBounds','Ownership outside chunk');
 speed(globalIdx)=chunkSpeed(globalIdx-chunkStart+1);coverage(globalIdx)=coverage(globalIdx)+1;routes{k}=route;
end
assert(all(coverage(first:last-1)==1),'Rodent:Coverage','Speed coverage is not exactly one');
eligible=false(N-1,1);eligible(first:last-1)=true;
valid=eligible&validPos(1:end-1)&validPos(2:end)&isfinite(speed);
run=valid&abs(speed)>6;rest=valid&abs(speed)<=6;
runBouts=bouts(run,time(1:end-1),5);restBouts=bouts(rest,time(1:end-1),5);
baselineRun=bouts(eligible&abs(speed)>6,time(1:end-1),5);baselineRest=bouts(eligible&abs(speed)<=6,time(1:end-1),5);
lossRun=losses(baselineRun,run,valid,time);lossRest=losses(baselineRest,rest,valid,time);
chunkTable=table(starts(:),ends(:),coreStart(:),coreEnd(:),ownedStart,ownedEnd,routes,'VariableNames',{'chunk_start','chunk_end','core_start','core_end','owned_start','owned_end','route'});
result=struct('session',session,'speed',speed,'speed_time',time(1:end-1),'valid',valid,'run_mask',run,'rest_mask',rest,'run_bouts',runBouts,'rest_bouts',restBouts,'chunks',chunkTable,'short_recording',short,'fs',fs,'first_sample',first,'last_sample',last,'raw_x1_missing_fraction',mean(missing),'any_coordinate_missing_fraction',mean(any(tracking==-1|~isfinite(tracking),2)),'short_gap_samples_filled',sum(filled),'long_or_unbounded_gap_count',sum(~arrayfun(@(j)gapSeconds(j)<=.5&&gs(j)>1&&ge(j)<numel(x),1:numel(gs))),'invalid_derivatives_after_trim',sum(eligible&~valid),'run_bouts_lost_to_gaps',lossRun.lost,'rest_bouts_lost_to_gaps',lossRest.lost,'run_gap_details',lossRun,'rest_gap_details',lossRest,'elapsed_seconds',toc(clockStart));
result.provenance=struct('git_tag','v1.0','git_commit','71ebc16aed32ca38be73a800738b975e5806b330','matlab_version',version,'seed',0,'tracking_fs_speed',39.06,'threshold',6,'minimum_bout_s',5,'chunk_samples',L,'overlap_samples',overlap,'edge_trim_s',2,'protocol','PROTOCOL_rodent.md; user amendments','session',session);
save(fullfile(out,[session '_behavior.mat']),'result','-v7');
end
function [s,e]=segments(mask)
d=diff([false;logical(mask(:));false]);s=find(d==1);e=find(d==-1)-1;
end
function B=bouts(mask,t,minDur)
[s,e]=segments(mask);duration=t(e)-t(s)+median(diff(t));keep=duration>=minDur;
B=table(s(keep),e(keep),t(s(keep)),t(e(keep)),duration(keep),'VariableNames',{'start_idx','stop_idx','start_time_s','stop_time_s','duration_s'});
end
function r=losses(base,mask,valid,time)
r=struct('baseline_eligible_bouts',height(base),'intersected_by_gaps',0,'lost',0,'qualifying_pieces',0,'short_pieces',0);
for j=1:height(base)
 a=base.start_idx(j);b=base.stop_idx(j);if all(valid(a:b)),continue;end
 r.intersected_by_gaps=r.intersected_by_gaps+1;[s,e]=segments(mask(a:b));dur=time(a+e-1)-time(a+s-1)+median(diff(time));
 r.lost=r.lost+~any(dur>=5);r.qualifying_pieces=r.qualifying_pieces+sum(dur>=5);r.short_pieces=r.short_pieces+sum(dur<5);
end
end
