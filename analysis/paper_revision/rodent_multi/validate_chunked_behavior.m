function validate_chunked_behavior
root='C:\Users\nghare\.brainstorm\process';out=fullfile(root,'revision_checks','rodent_multi');start=tic;
S=load('D:\APC_project\RealDatasets\LFP_data\EC3_dataset_real.mat','R2');time=S.R2.Time;clear S;
M=load('D:\APC_project\RealDatasets\LFP_data\Behavioral_Data\EC013_movement.mat','ec013ec2');
result=chunked_behavior(time,M.ec013ec2,'ec013.157',out);
B=load(fullfile(root,'apc_ec013_run_rest_results.mat'),'results');base=B.results;
idx=(40800:372500)';assert(numel(idx)==numel(base.run_mask),'Rodent:ReferenceLength','Unexpected historical derivative length');
valid=result.valid(idx);same=(result.run_mask(idx)==base.run_mask(:))&(result.rest_mask(idx)==base.rest_mask(:));
agreement=100*mean(same);conditional=100*mean(same(valid));
rows=table();states={'run','rest'};
for q=1:2
 state=states{q};historical=base.(state).bouts;current=result.([state '_bouts']);used=false(height(current),1);
 for k=1:height(historical)
  a=historical.start_time_s(k);b=historical.stop_time_s(k);distance=max(abs(current.start_time_s-a),abs(current.stop_time_s-b));distance(used)=Inf;
  [best,j]=min(distance);matched=~isempty(best)&&best<=.5;
  if matched,used(j)=true;newStart=current.start_time_s(j);newStop=current.stop_time_s(j);else,newStart=NaN;newStop=NaN;end
  rows=[rows;table(string(state),k,a,b,matched,newStart,newStop,'VariableNames',{'state','historical_bout','historical_start_s','historical_stop_s','matched_within_0_5_s','new_start_s','new_stop_s'})]; %#ok<AGROW>
 end
end
provenance=result.provenance;rows.git_commit=repmat(string(provenance.git_commit),height(rows),1);rows.provenance_json=repmat(string(jsonencode(provenance)),height(rows),1);
writetable(rows,fullfile(out,'ec013_157_bout_validation.csv'));
gate=struct('session','ec013.157','all_sample_agreement_percent',agreement,'valid_sample_agreement_percent',conditional,'total_historical_derivatives',numel(idx),'valid_new_derivatives',sum(valid),'unlabelled_new_derivatives',sum(~valid),'required_agreement_percent',95,'passed',agreement>=95,'historical_run_bouts',12,'historical_rest_bouts',12,'matched_run_bouts',sum(rows.matched_within_0_5_s(rows.state=="run")),'matched_rest_bouts',sum(rows.matched_within_0_5_s(rows.state=="rest")),'whole_record_run_bouts',height(result.run_bouts),'whole_record_rest_bouts',height(result.rest_bouts),'raw_x1_missing_fraction',result.raw_x1_missing_fraction,'any_coordinate_missing_fraction',result.any_coordinate_missing_fraction,'run_bouts_lost_to_gaps',result.run_bouts_lost_to_gaps,'rest_bouts_lost_to_gaps',result.rest_bouts_lost_to_gaps,'elapsed_seconds',toc(start),'provenance',provenance);
fid=fopen(fullfile(out,'chunked_behavior_validation.json'),'w','n','UTF-8');fprintf(fid,'%s\n',jsonencode(gate));fclose(fid);disp(gate);
assert(gate.passed,'Rodent:ChunkLabelGate','Chunked whole-recording label agreement is below 95 percent; stop');
end
