function validation_worker(worker,nworkers)
if nargin<2,nworkers=4;end
O=fileparts(mfilename('fullpath'));root=fileparts(fileparts(O));repo=fullfile(root,'apc-brainstorm-publish');cd(O);
addpath(fullfile(repo,'analysis','v1_revision'),'-begin');addpath(fullfile(repo,'results','paper2_ablation'),'-begin');addpath(fullfile(root,'revision_checks','final'),'-begin');addpath(O,'-begin');addpath(fullfile(repo,'src'),'-begin');
m=jsondecode(fileread(fullfile(O,'provenance.json')));G=jsondecode(fileread(fullfile(O,'all_gate_results.json')));generation=jsondecode(fileread(fullfile(O,'generation_complete.json')));assert(strcmp(G.status,'PASS')&&strcmp(generation.status,'COMPLETE'));
assert(strcmpi(which('bst_apc'),fullfile(repo,'src','bst_apc.m')));dest=fullfile(O,'checkpoints');if ~isfolder(dest),mkdir(dest);end;start=tic;key="";
try
 for suite=["V1","V2","V3","V4"]
  bank=load(fullfile(O,char(suite+"_inputs.mat")),'cases','meta');csv=fullfile(O,sprintf('%s_worker%d.csv',suite,worker));ids=worker:nworkers:numel(bank.cases);parts={};done=false(size(ids));
  for j=1:numel(ids)
   c=bank.cases{ids(j)};file=fullfile(dest,char(suite+"_"+c.input_id+".mat"));
   if isfile(file),q=load(file,'T','m');assert(strcmp(q.m.git_head,m.git_head),'Validation:Checkpoint','Checkpoint commit changed');parts{end+1}=q.T;done(j)=true;end %#ok<AGROW>
  end
  if ~isempty(parts),v1_write_csv(vertcat(parts{:}),csv);else,assert(~isfile(csv),'Validation:CheckpointCSV','CSV without checkpoints');end
  count=sum(done);
  for j=1:numel(ids)
   if done(j),continue;end
   assert(~isfile(fullfile(O,'STOPPED_ACTIVE.md')),'Validation:OtherWorkerStopped','Another worker stopped');c=bank.cases{ids(j)};key=suite+"_"+c.input_id;file=fullfile(dest,char(key+".mat"));beta=nan;if isfield(c,'beta'),beta=c.beta;end
   base=struct('suite',suite,'input_id',c.input_id,'paired_coupled_id',c.paired_coupled_id,'scenario',string(c.scenario),'dataset',string(c.dataset),'level',c.level,'beta',beta,'duration_s',numel(c.signal)/c.cfg.fs_hz,'repeat_index',c.repeat_index,'true_fp_hz',c.cfg.true_fp_hz,'true_fa_hz',c.cfg.true_fa_hz,'true_fd_hz',c.true_fd_hz,'key',key,'seed',bank.meta.seed,'signal_sha256',string(c.signal_sha256));
   before=rng;[T,detail]=validation_estimate(c.signal,c.time,suite,base,m,c.calibration_shifts);assert(isequal(before,rng),'Validation:MethodRNG','Deterministic methods changed RNG');
   save(file,'T','detail','m','-v7.3');v1_write_csv(T,csv,true);count=count+1;
   if mod(count,10)==0,fprintf('W%d %s %d/%d finished\n',worker,suite,count,numel(ids));end
  end
  clear bank parts;
 end
 guards=final_sos_filter('registry');g=struct2table(guards);g.git_commit=repmat(string(m.git_head),height(g),1);g.protocol_sha256=repmat(string(m.protocol_sha256),height(g),1);v1_write_csv(g,fullfile(O,sprintf('simulation_filter_guards_w%d.csv',worker)));
 writejson(fullfile(O,sprintf('worker%d_complete.json',worker)),struct('status','COMPLETE','elapsed_seconds',toc(start),'provenance',m));
catch err
 e=struct('status','ERROR','key',key,'worker',worker,'identifier',err.identifier,'message',err.message,'stack',err.stack,'elapsed_seconds',toc(start),'provenance',m);writejson(fullfile(O,sprintf('worker%d_error.json',worker)),e);
 if startsWith(err.identifier,'Validation:')||startsWith(err.identifier,'Final:')
  if ~isfile(fullfile(O,'STOPPED_ACTIVE.md')),f=fopen(fullfile(O,'STOPPED_ACTIVE.md'),'w','n','UTF-8');fprintf(f,'# STOPPED: validation method problem\n\n%s\n%s: %s\n',key,err.identifier,err.message);fclose(f);end
 end
 rethrow(err);
end
end
function writejson(file,v),f=fopen(file,'w','n','UTF-8');assert(f>=0);c=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(v));end
