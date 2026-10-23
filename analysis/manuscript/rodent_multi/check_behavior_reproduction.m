function check_behavior_reproduction
root='C:\Users\nghare\.brainstorm\process';out=fullfile(root,'revision_checks','rodent_multi');dataRoot='D:\APC_project\RealDatasets\LFP_data';
start=tic;S=load(fullfile(dataRoot,'EC3_dataset_real.mat'),'R2');rec=S.R2;
M=load(fullfile(dataRoot,'Behavioral_Data','EC013_movement.mat'),'ec013ec2');movementTrace=M.ec013ec2;
B=load(fullfile(root,'apc_ec013_run_rest_results.mat'),'results');base=B.results;
time=double(rec.Time(:).');timeLED=0:(1/39.06):631.25;nLed=min(numel(timeLED),size(movementTrace,1));
posInterp=interp1(timeLED(1:nLed),movementTrace(1:nLed,:),time,'linear','extrap');
idx=40800:min(372501,numel(time));timeWin=time(idx);posWin=posInterp(idx,1);
[trendPos,route]=smooth_original(posWin);speed=diff(trendPos)./diff(timeWin(:));speed=speed(:);speedTime=timeWin(1:end-1);
runMask=abs(speed)>6;restMask=~runMask;runBouts=boolean_to_bouts(runMask,speedTime,5);restBouts=boolean_to_bouts(restMask,speedTime,5);
r=struct('run_bouts',height(runBouts),'rest_bouts',height(restBouts),'run_table_exact',isequaln(runBouts,base.run.bouts),'rest_table_exact',isequaln(restBouts,base.rest.bouts),'run_mask_exact',isequal(runMask(:),base.run_mask(:)),'rest_mask_exact',isequal(restMask(:),base.rest_mask(:)),'speed_exact',isequaln(speed(:),base.speed(:)),'max_speed_difference',max(abs(speed(:)-base.speed(:))),'max_trend_difference',max(abs(trendPos(:)-base.trend_position(:))),'smoothing_route',route,'tracking_array','ec013ec2','tracking_sampling_for_reproduction',39.06,'missing_x1_samples',sum(movementTrace(:,1)==-1),'missing_handling','none in historical producer: -1 values retained','speed_units','raw tracking x1 coordinate units per second; original axis claims cm; no calibration applied in code','matlab_version',version,'git_commit','71ebc16aed32ca38be73a800738b975e5806b330','elapsed_seconds',toc(start));
r.passed=r.run_bouts==12&&r.rest_bouts==12&&r.run_table_exact&&r.rest_table_exact&&r.run_mask_exact&&r.rest_mask_exact&&r.speed_exact;
f=fopen(fullfile(out,'behavior_reproduction.json'),'w','n','UTF-8');fprintf(f,'%s\n',jsonencode(r));fclose(f);
save(fullfile(out,'behavior_reproduction.mat'),'r','runBouts','restBouts','speed','trendPos','-v7');disp(r);
assert(r.passed,'Rodent:BehaviorGate','Historical 12/12 behavior reproduction failed');
end
function [trendPos,route]=smooth_original(pos)
pos=double(pos(:));
try
 trendOut=trenddecomp(pos);if isstruct(trendOut),trendPos=trendOut.signal;else,trendPos=trendOut(:,1);end;route='trenddecomp';
catch
 win=max(5,round(numel(pos)*.005));trendPos=smoothdata(pos,'movmedian',win);route='fallback movmedian max(5,round(N*.005))';
end
end
function bouts=boolean_to_bouts(mask,timeVec,minDur)
mask=logical(mask(:));timeVec=double(timeVec(:));d=diff([false;mask;false]);starts=find(d==1);stops=find(d==-1)-1;
if isempty(starts),bouts=table();return;end
dur=timeVec(stops)-timeVec(starts)+median(diff(timeVec));keep=dur>=minDur;starts=starts(keep);stops=stops(keep);dur=dur(keep);
bouts=table(starts,stops,timeVec(starts),timeVec(stops),dur,'VariableNames',{'start_idx','stop_idx','start_time_s','stop_time_s','duration_s'});
end
