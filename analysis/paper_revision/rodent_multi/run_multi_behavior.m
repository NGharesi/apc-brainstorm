function run_multi_behavior
% This entry point enforces the user-prespecified reference gate.
out=fileparts(mfilename('fullpath'));start=tic;
gate=jsondecode(fileread(fullfile(out,'chunked_behavior_validation.json')));
assert(gate.passed&&gate.all_sample_agreement_percent>=95,'Rodent:ValidationGate','Reference gate failed: no new-session analysis allowed');
mapping=readtable(fullfile(out,'mapping_checks.csv'),'TextType','string');
record=jsondecode(fileread(fullfile(out,'protocol_amendments_record.json')));
rows={};
try
 for j=1:height(mapping)
  q=mapping(j,:);session=char(q.session);file=fullfile(out,[session '_behavior.mat']);
  if isfile(file)
   B=load(file,'result');r=B.result;
  else
   S=load(q.lfp_file,'Time');time=S.Time;clear S;
   M=load(fullfile('D:\APC_project\RealDatasets\LFP_data\Behavioral_Data',char(q.animal+"_movement.mat")),char(q.tracking_array));
   tracking=M.(char(q.tracking_array));clear M;
   r=chunked_behavior(time,tracking,session,out);
  end
  nr=height(r.run_bouts);ns=height(r.rest_bouts);included=nr>=5&&ns>=5;
  reason="included";if ~included,reason="fewer than 5 run or 5 rest bouts";end
  meta=r.provenance;meta.protocol_sha256=record.protocol_sha256;meta.execution_sha256=record.execution_sha256;meta.source_file=q.lfp_file;meta.tracking_array=q.tracking_array;
  item=struct('animal',q.animal,'session',q.session,'run_bouts',nr,'rest_bouts',ns,'included',included,'reason',reason,'short_recording',r.short_recording,'raw_x1_missing_fraction',r.raw_x1_missing_fraction,'any_coordinate_missing_fraction',r.any_coordinate_missing_fraction,'invalid_derivatives_after_trim',r.invalid_derivatives_after_trim,'run_bouts_lost_to_gaps',r.run_bouts_lost_to_gaps,'rest_bouts_lost_to_gaps',r.rest_bouts_lost_to_gaps,'elapsed_seconds',r.elapsed_seconds,'git_commit',string(meta.git_commit),'provenance_json',string(jsonencode(meta)));
  rows{end+1}=item;T=struct2table([rows{:}]);writetable(T,fullfile(out,'session_bout_eligibility.csv')); %#ok<AGROW>
  for state=["run","rest"]
   bouts=r.(char(state+"_bouts"));bouts.state=repmat(state,height(bouts),1);bouts.session=repmat(q.session,height(bouts),1);bouts.provenance_json=repmat(string(jsonencode(meta)),height(bouts),1);
   writetable(bouts,fullfile(out,sprintf('%s_%s_bouts.csv',session,state)));
  end
  C=r.chunks;C.provenance_json=repmat(string(jsonencode(meta)),height(C),1);writetable(C,fullfile(out,[session '_chunks.csv']));
  fprintf('BEHAVIOR %d/18 %s: run %d rest %d included %d\n',j,session,nr,ns,included);
 end
 status=struct('status','COMPLETE','elapsed_seconds',toc(start),'metadata',record,'sessions',height(T),'included_sessions',sum(T.included));
catch err
 status=struct('status','FAILED_STOP','elapsed_seconds',toc(start),'metadata',record,'identifier',err.identifier,'error',err.message);
 writejson(fullfile(out,'multi_behavior_runtime.json'),status);rethrow(err);
end
writejson(fullfile(out,'multi_behavior_runtime.json'),status);
end
function writejson(file,s)
f=fopen(file,'w','n','UTF-8');fprintf(f,'%s\n',jsonencode(s));fclose(f);
end
