function v3_worker(worker,nworkers)
% Resume-safe disjoint workers. All HB-v1 equivalence checks precede analysis.
if nargin<2,nworkers=4;end
O=fileparts(mfilename('fullpath'));root=fileparts(fileparts(O));repo=fullfile(root,'apc-brainstorm-publish');cd(O);
addpath(fullfile(root,'revision_checks','final'),'-begin');addpath(fullfile(repo,'analysis','v1_revision'),'-begin');addpath(O,'-begin');addpath(fullfile(repo,'src'),'-begin');
assert(strcmpi(which('bst_apc'),fullfile(repo,'src','bst_apc.m')));
m=jsondecode(fileread(fullfile(O,'phaseB_implementation.json')));start=tic;
dest=fullfile(O,'checkpoints');if ~isfolder(dest),mkdir(dest);end
try
 bank=load(fullfile(O,'HB_inputs.mat'),'cases','meta');HB=bank.cases;optionsHB=bank.meta.apc_configurations.v1;
 % MAT tables preserve the exact double values used for original v1 reports.
 files=dir(fullfile(root,'revision_checks','v2','candidate_03','heldout_worker*_chunk*.mat'));reference=table;
 for k=1:numel(files)
  b=load(fullfile(files(k).folder,files(k).name),'T');reference=[reference;b.T(b.T.configuration=="v1.0" & b.T.method=="APC",:)]; %#ok<AGROW>
 end
 assert(height(reference)==675);equivalence={};
 for id=worker:nworkers:numel(HB)
  stop_if_needed(O);c=HB{id};file=fullfile(dest,sprintf('HB_v1_%04d.mat',id));
  if isfile(file)
   q=load(file,'r1','i1','m');assert(strcmp(q.m.freeze_commit,m.freeze_commit));r1=q.r1;i1=q.i1;
  else
   before=rng;[r1,i1]=bst_apc(struct('data',c.signal,'time',c.time),optionsHB);assert(isequal(before,rng));save(file,'r1','i1','m','-v7.3');
  end
  old=reference(reference.input_id==id,:);assert(height(old)==1);
  observed=[r1.phase_frequency_hz.Value,r1.amplitude_frequency_hz.Value,r1.pac_strength.Value,r1.status_code.Value];expected=[old.recovered_fp_hz,old.recovered_fa_hz,old.score,old.status];
  exact=isequaln(observed,expected)&&strcmp(string(i1.route),old.route);
  eq=struct('input_id',id,'scenario',c.scenario,'dataset',c.dataset,'observed_fp_hz',observed(1),'saved_fp_hz',expected(1),'observed_fa_hz',observed(2),'saved_fa_hz',expected(2),'observed_score',observed(3),'saved_score',expected(3),'observed_status',observed(4),'saved_status',expected(4),'route_exact',strcmp(string(i1.route),old.route),'exact',exact,'git_commit',string(m.freeze_commit),'protocol_sha256',string(m.protocol_sha256),'seed',20261022);equivalence{end+1}=eq; %#ok<AGROW>
  assert(exact,'v3:HBV1Reproduction','HB v1 failed exact saved per-trial reproduction at input %d',id);
  if mod(numel(equivalence),10)==0,fprintf('W%d HB-v1 verified %d/%d\n',worker,numel(equivalence),numel(worker:nworkers:numel(HB)));end
 end
 v1_write_csv(struct2table(vertcat(equivalence{:})),fullfile(O,sprintf('HB_v1_equivalence_w%d.csv',worker)));
 write_json(fullfile(O,sprintf('HB_v1_verified_w%d.json',worker)),struct('status','PASS','trials',numel(equivalence),'elapsed_seconds',toc(start),'provenance',m));
 fprintf('W%d awaiting aggregate HB equivalence release\n',worker);
 while ~isfile(fullfile(O,'HB_VERIFIED.json')),stop_if_needed(O);pause(2);end
 check=jsondecode(fileread(fullfile(O,'HB_VERIFIED.json')));assert(strcmp(check.status,'PASS')&&strcmp(check.freeze_commit,m.freeze_commit));
 bank=load(fullfile(O,'HA_inputs.mat'),'cases');HA=bank.cases;
 for suite=["HA","HB"]
  if suite=="HA",cases=HA;options=struct('fA',[80 150],'version','v1');profile="HA";mode="HA_A2_prime";seed=20261101;
  else,cases=HB;options=optionsHB;profile="heldout";mode="A2_prime";seed=20261022;end
  csv=fullfile(O,sprintf('%s_worker%d_trials.csv',suite,worker));tables={};
  for id=worker:nworkers:numel(cases)
   stop_if_needed(O);c=cases{id};file=fullfile(dest,sprintf('%s_estimates_%04d.mat',suite,id));
   if isfile(file)
    q=load(file,'T','m');assert(strcmp(q.m.freeze_commit,m.freeze_commit));T=q.T;
   else
    before=rng;
    if suite=="HB",q=load(fullfile(dest,sprintf('HB_v1_%04d.mat',id)),'r1','i1');r1=q.r1;i1=q.i1;
    else,[r1,i1]=bst_apc(struct('data',c.signal,'time',c.time),options);end
    o3=options;o3.version='v3';[r3,i3]=bst_apc(struct('data',c.signal,'time',c.time),o3);
    [fp,sp,status]=sp_raw_fp(c.signal,c.cfg.fs_hz,options);
    comps=v3_comparators(c.signal,c.cfg.fs_hz,profile,mode,.5);assert(numel(comps)==4&&all([comps.status]==0),'v3:ComparatorStatus','Nonfinite comparator output');
    settings=struct('profile',profile,'phase_grid_hz',3:.5:14,'phase_half_width_hz',1.5,'amplitude_grid_hz',80:4:160,'amplitude_half_width_hz',14,'filter','guarded SOS butter(4), filtfilt','metrics',{{'MVL-raw','MVL-Ozkurt','KLMI','GLM'}},'phase_bins',18,'selection','first column-major maximum');
    if suite=="HA",settings.phase_grid_hz=3:.5:30;settings.amplitude_half_width_hz=30;end
    rows={pack(c,suite,"APC-v1.0",r1.phase_frequency_hz.Value,r1.amplitude_frequency_hz.Value,r1.pac_strength.Value,r1.status_code.Value,i1,[],i1.options,settings,m,seed), ...
     pack(c,suite,"APC-v3.0",r3.phase_frequency_hz.Value,r3.amplitude_frequency_hz.Value,r3.pac_strength.Value,r3.status_code.Value,i3,[],i3.options,settings,m,seed), ...
     pack(c,suite,"SP-raw",fp,nan,nan,status,[],sp,options,settings,m,seed)};
    for k=1:4,z=comps(k);rows{end+1}=pack(c,suite,z.method,z.fp,z.fa,z.score,z.status,[],[],options,settings,m,seed);end %#ok<AGROW>
    assert(isequal(before,rng),'v3:AnalysisRNG','Deterministic analysis changed RNG');
    T=struct2table(vertcat(rows{:}));save(file,'T','r1','i1','r3','i3','sp','comps','settings','m','-v7.3');
   end
   tables{end+1}=T;v1_write_csv(vertcat(tables{:}),csv); %#ok<AGROW>
   if mod(numel(tables),10)==0,fprintf('W%d %s %d/%d completed, input%d\n',worker,suite,numel(tables),numel(worker:nworkers:numel(cases)),id);end
  end
 end
 guards=final_sos_filter('registry');G=struct2table(guards);G.git_commit=repmat(string(m.freeze_commit),height(G),1);G.protocol_sha256=repmat(string(m.protocol_sha256),height(G),1);v1_write_csv(G,fullfile(O,sprintf('filter_guards_w%d.csv',worker)));
 write_json(fullfile(O,sprintf('worker%d_complete.json',worker)),struct('status','COMPLETE','elapsed_seconds',toc(start),'provenance',m));
 fprintf('W%d COMPLETE %.3f seconds\n',worker,toc(start));
catch err
 record=struct('status','STOPPED','worker',worker,'identifier',err.identifier,'message',err.message,'elapsed_seconds',toc(start),'provenance',m);
 write_json(fullfile(O,sprintf('worker%d_error.json',worker)),record);
 if startsWith(err.identifier,'v3:')||startsWith(err.identifier,'Final:')
  f=fopen(fullfile(O,'STOPPED.md'),'w','n','UTF-8');fprintf(f,'# STOPPED: method-relevant Phase B problem\n\nWorker %d: %s: %s\n',worker,err.identifier,err.message);fclose(f);
 end
 rethrow(err);
end
end
function row=pack(c,suite,method,fp,fa,score,status,info,sp,options,settings,m,seed)
branch="not_applicable";route="not_applicable";exponent=nan;offset=nan;peak=nan;sigma=nan;flo=nan;
if ~isempty(info)
 route=string(info.route);if strcmp(method,'APC-v3.0')
  branch="not_reached";if isfield(info.diagnostics{1},'aperiodic'),sp=info.diagnostics{1}.aperiodic;end
 end
end
if ~isempty(sp),branch=string(sp.location_branch);exponent=sp.exponent;offset=sp.offset;peak=sp.peak_height;sigma=sp.sigma;flo=sp.f_lo_hz;end
beta=nan;amplitude=nan;duration=numel(c.signal)/c.cfg.fs_hz;if suite=="HA",beta=c.beta;amplitude=c.level;end
valid=status==0&&isfinite(fp);if method~="SP-raw",valid=valid&&isfinite(fa)&&isfinite(score);end
row=struct('suite',suite,'input_id',c.input_id,'paired_coupled_id',c.paired_coupled_id,'scenario',c.scenario,'dataset',c.dataset,'level',c.level,'beta',beta,'rhythm_amplitude',amplitude,'duration_s',duration,'repeat_index',c.repeat_index,'true_fp_hz',c.cfg.true_fp_hz,'true_fa_hz',c.cfg.true_fa_hz,'true_fd_hz',c.true_fd_hz,'method',method,'recovered_fp_hz',fp,'recovered_fa_hz',fa,'score',score,'status',status,'valid',valid,'route',route,'location_branch',branch,'exponent',exponent,'offset',offset,'peak_height',peak,'sigma',sigma,'f_lo_hz',flo,'pair_residual',c.pair_residual,'git_commit',string(m.freeze_commit),'git_tag',"v3.0",'protocol_sha256',string(m.protocol_sha256),'matlab_version',string(version),'seed',seed,'apc_options_json',string(jsonencode(options)),'comparator_settings_json',string(jsonencode(settings)),'generator_settings_json',string(jsonencode(c.cfg)),'implementation_record',"phaseB_implementation.json");
end
function stop_if_needed(O),assert(~isfile(fullfile(O,'STOPPED.md')),'v3:StoppedElsewhere','Another worker reported a method-relevant stop');end
function write_json(file,value),f=fopen(file,'w','n','UTF-8');assert(f>=0);c=onCleanup(@() fclose(f));fprintf(f,'%s\n',jsonencode(value));end
