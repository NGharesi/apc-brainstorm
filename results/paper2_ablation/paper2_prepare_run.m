function paper2_prepare_run
O=fileparts(mfilename('fullpath'));root=fileparts(fileparts(O));repo=fullfile(root,'apc-brainstorm-publish');cd(O);
addpath(fullfile(repo,'analysis','v1_revision'),'-begin');addpath(fullfile(repo,'analysis','v2_revision'),'-begin');addpath(fullfile(root,'revision_checks','v3_aperiodic'),'-begin');addpath(O,'-begin');
m=jsondecode(fileread(fullfile(O,'provenance.json')));gate=jsondecode(fileread(fullfile(O,'gate_results.json')));assert(strcmp(gate.status,'PASS'),'Paper2:GateRequired','Gates must pass before analysis');
assert(~isfile(fullfile(O,'HB_signal_verification.json')));start=tic;
try
 old=load(fullfile(root,'revision_checks','v3_aperiodic','HB_inputs.mat'),'cases','meta');meta=old.meta;meta.git_commit=m.git_head;meta.protocol_sha256=m.protocol_sha256;meta.paper2_provenance=m;
 generate_v3_hb(O,meta);fresh=load(fullfile(O,'HB_inputs.mat'),'cases');original=load(fullfile(root,'revision_checks','v2','candidate_03','heldout_inputs.mat'),'cases');
 exact=isequaln(old.cases,fresh.cases)&&isequaln(original.cases,fresh.cases);assert(exact,'Paper2:HBSignalReproduction','Regenerated HB complete cases differ from saved inputs');
 record=struct('status','PASS','inputs',numel(fresh.cases),'complete_cases_bit_identical_to_v3_and_original',exact,'elapsed_seconds',toc(start),'provenance',m);writejson(fullfile(O,'HB_signal_verification.json'),record);
 fprintf('HB REPRODUCTION PASS %d complete cases; %.3f s\n',numel(fresh.cases),toc(start));
catch err
 writejson(fullfile(O,'preparation_error.json'),struct('identifier',err.identifier,'message',err.message,'provenance',m));
 if startsWith(err.identifier,'Paper2:')||startsWith(err.identifier,'v2:')
  f=fopen(fullfile(O,'STOPPED.md'),'w','n','UTF-8');fprintf(f,'# STOPPED: HB input verification\n\n%s: %s\n',err.identifier,err.message);fclose(f);
 end
 rethrow(err);
end
end
function writejson(file,value),f=fopen(file,'w','n','UTF-8');assert(f>=0);c=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(value));end
