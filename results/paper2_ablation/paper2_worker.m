function paper2_worker(worker,nworkers)
% Disjoint, incremental per-input checkpoints. Never overwrite a finished run.
if nargin<2,nworkers=4;end
O=fileparts(mfilename('fullpath'));root=fileparts(fileparts(O));repo=fullfile(root,'apc-brainstorm-publish');cd(O);
addpath(fullfile(root,'revision_checks','final'),'-begin');addpath(fullfile(repo,'analysis','v1_revision'),'-begin');addpath(O,'-begin');addpath(fullfile(repo,'src'),'-begin');
m=jsondecode(fileread(fullfile(O,'provenance.json')));paper2_error_context('init',fullfile(O,sprintf('worker%d_error.json',worker)),m,worker);paper2_assert(strcmpi(which('bst_apc'),fullfile(repo,'src','bst_apc.m')),'Paper2:SourcePath','Wrong APC source',which('bst_apc'),fullfile(repo,'src','bst_apc.m'));
g=jsondecode(fileread(fullfile(O,'gate_results.json')));h=jsondecode(fileread(fullfile(O,'HB_signal_verification.json')));paper2_assert(strcmp(g.status,'PASS')&&strcmp(h.status,'PASS'),'Paper2:Gates','Required gates did not pass',[string(g.status),string(h.status)],["PASS","PASS"]);
dest=fullfile(O,'checkpoints');if ~isfolder(dest),mkdir(dest);end;start=tic;
try
 suites=["HA","HB"];if isfield(m,'resume_ecog_only')&&m.resume_ecog_only,suites=strings(1,0);fprintf('W%d preserving all simulation files; ECoG-only resume\n',worker);end
 for suite=suites
  if suite=="HA",bank=load(fullfile(root,'revision_checks','v3_aperiodic','HA_inputs.mat'),'cases');opt1=struct('fA',[80 150],'version','v1');profile="HA";seed=20261101;
  else,bank=load(fullfile(O,'HB_inputs.mat'),'cases','meta');opt1=bank.meta.apc_configurations.v1;profile="heldout";seed=20261022;end
  opt3=opt1;opt3.version='v3';csv=fullfile(O,sprintf('%s_worker%d.csv',suite,worker));ids=worker:nworkers:numel(bank.cases);paths=arrayfun(@(id) string(fullfile(dest,sprintf('%s_%04d.mat',suite,id))),ids);done=restore_csv(paths,csv,m);completed=numel(done);fprintf('W%d %s restored %d completed inputs without estimators\n',worker,suite,completed);
  for id=worker:nworkers:numel(bank.cases)
   stopcheck;file=fullfile(dest,sprintf('%s_%04d.mat',suite,id));if any(done==string(file)),continue;end
   if isfile(file),q=load(file,'T','m');paper2_assert(strcmp(q.m.git_head,m.git_head),'Paper2:Checkpoint','Checkpoint commit differs',q.m.git_head,m.git_head);T=q.T;
   else
    c=bank.cases{id};q=load(fullfile(root,'revision_checks','v3_aperiodic','checkpoints',sprintf('%s_estimates_%04d.mat',suite,id)),'r1','i1','r3','i3','sp','comps','T');
    r1=apcref(q.r1,q.i1);r3=apcref(q.r3,q.i3);spRow=q.T(q.T.method=="SP-raw",:);scan=q.comps(string({q.comps.method})=="MVL-Ozkurt");paper2_assert(isscalar(scan),'Paper2:SavedScan','Expected one saved scan',numel(scan),1);
    base=base_sim(c,suite,seed);before=rng;
    [T,detail]=paper2_estimate(c.signal,c.time,profile,opt1,opt3,r1,r3,spRow.recovered_fp_hz,spRow.status,q.sp,scan,m,base);
    paper2_assert(isequal(before,rng),'Paper2:AnalysisRNG','Deterministic analysis changed RNG',rng,before);save(file,'T','detail','m','-v7.3');
   end
   v1_write_csv(T,csv,true);completed=completed+1;
   if mod(completed,10)==0,fprintf('W%d %s %d/%d completed\n',worker,suite,completed,numel(ids));end
  end
  clear bank;
 end
 E=fullfile(root,'revision_checks','ecog_miller_motor');csvargs={'Delimiter',',','NumHeaderLines',0,'ReadVariableNames',true,'TextType','string','Encoding','UTF-8'};B=readtable(fullfile(E,'bouts.csv'),csvargs{:});elig=readtable(fullfile(E,'patient_eligibility.csv'),csvargs{:});
 included=strcmpi(string(elig.eligible),'true')|string(elig.eligible)=="1";patients=elig.patient(included);paper2_assert(numel(patients)==18,'Paper2:Eligibility','Expected unchanged 18 eligible patients',numel(patients),18);B=B(logical(B.analysed)&ismember(B.patient,patients),:);
 old=readtable(fullfile(E,'ecog_bout_estimates.csv'),csvargs{:});WB=B(ismember(B.patient,patients(worker:nworkers:end)),:);paths=strings(height(WB),1);
 for k=1:height(WB),paths(k)=string(fullfile(dest,sprintf('ecog_%s_%s_%03d.mat',WB.patient(k),WB.recording(k),WB.bout(k))));end
 csv=fullfile(O,sprintf('ecog_worker%d.csv',worker));done=restore_csv(paths,csv,m);fprintf('W%d ECoG restored %d completed bouts without estimators\n',worker,numel(done));
 referenceCsv=fullfile(O,sprintf('ecog_v1_reproduction_w%d.csv',worker));referenceLogged=strings(0,1);referenceChecks={};
 for jref=1:height(WB)
  refkey=string(sprintf('%s_%s_%03d',WB.patient(jref),WB.recording(jref),WB.bout(jref)));reffile=fullfile(O,'ecog_v1_references',char(refkey+".mat"));
  if isfile(reffile),rr=load(reffile,'reproduction','verified');if rr.verified,referenceChecks{end+1}=rr.reproduction;referenceLogged(end+1,1)=refkey;end;end %#ok<AGROW>
 end
 if ~isempty(referenceChecks),v1_write_csv(struct2table(vertcat(referenceChecks{:})),referenceCsv);end
 opt1=struct('fA',[80 150],'minPhaseHz',6,'maxPhaseHz',30);opt3=struct('fA',[80 150],'minPhaseHz',1,'maxPhaseHz',30,'version','v3');
 for j=worker:nworkers:numel(patients)
  pt=patients(j);S=load(fullfile(E,'prep',char(pt+".mat")));K=B(B.patient==pt,:);
  for k=1:height(K)
   stopcheck;b=K(k,:);key=string(sprintf('%s_%s_%03d',pt,b.recording,b.bout));paper2_error_context('context',key,nan);file=fullfile(dest,char("ecog_"+key+".mat"));if any(done==string(file)),continue;end
   if isfile(file),q=load(file,'T','m');paper2_assert(strcmp(q.m.git_head,m.git_head),'Paper2:Checkpoint','Checkpoint commit differs',q.m.git_head,m.git_head);T=q.T;
   else
    signal=S.sig;if b.recording=="imagery",signal=S.sigI;end;signal=signal(b.start_sample:b.end_sample);time=(0:numel(signal)-1)/S.fs;before=rng;
    q=load(fullfile(root,'revision_checks','v3_aperiodic','phaseC','checkpoints',char("ecog_"+key+".mat")),'features','info','sp','T');
    p=old(old.key==key & old.method=="APC-v1.0",:);paper2_assert(height(p)==1,'Paper2:SavedReference','Expected one saved v1 CSV row',height(p),1,1,key);[r1,reproduction]=paper2_ecog_v1_reference(signal,time,p,key,m);
    if ~any(referenceLogged==key),v1_write_csv(struct2table(reproduction),referenceCsv,true);referenceLogged(end+1,1)=key;end
    r3=struct('fp',q.features.fP_hz,'fa',q.features.fA_hz,'raw',q.features.raw_mvl,'pref',q.features.preferred_phase_deg,'status',q.features.status,'band',q.info.final_band_hz,'route',string(q.info.route),'normalized_saved',q.features.ozkurt_mvl);
    sp=q.sp;if isempty(sp),[spfp,sp,spstatus]=sp_raw_fp(signal,S.fs,opt3);else,spfp=q.T.sp_raw_fp_hz;spstatus=q.T.sp_raw_status;end
    p=old(old.key==key & old.method=="MVL-Ozkurt",:);paper2_assert(height(p)==1,'Paper2:SavedScan','Expected one saved scan CSV row',height(p),1,nan,key);scan=struct('fp',p.fP_hz,'fa',p.fA_hz,'score',p.score);
    base=struct('suite',"ECoG",'input_id',k,'paired_coupled_id',nan,'scenario',b.recording,'dataset',b.state,'level',nan,'beta',nan,'duration_s',b.duration_s,'repeat_index',b.bout,'true_fp_hz',nan,'true_fa_hz',nan,'patient',pt,'recording',b.recording,'key',key,'state',b.state,'movement_type',b.movement_type,'seed',20261024,'generator_settings_json',"saved ECoG prep and original bout boundaries");
    [T,detail]=paper2_estimate(signal,time,"ecog",opt1,opt3,r1,r3,spfp,spstatus,sp,scan,m,base);detail.reference_reproduction=reproduction;paper2_assert(isequal(before,rng),'Paper2:AnalysisRNG','ECoG deterministic analysis changed RNG',rng,before,nan,key);save(file,'T','detail','m','-v7.3');
   end
   v1_write_csv(T,csv,true);
  end
  fprintf('W%d ECoG %s %d bouts complete\n',worker,pt,height(K));
 end
 guards=final_sos_filter('registry');G=struct2table(guards);G.git_commit=repmat(string(m.git_head),height(G),1);G.protocol_sha256=repmat(string(m.protocol_sha256),height(G),1);v1_write_csv(G,fullfile(O,sprintf('filter_guards_w%d.csv',worker)));
 writejson(fullfile(O,sprintf('worker%d_complete.json',worker)),struct('status','COMPLETE','elapsed_seconds',toc(start),'provenance',m));fprintf('W%d COMPLETE %.3f seconds\n',worker,toc(start));
catch err
 ec=paper2_error_context('get');record=struct('identifier',err.identifier,'message',err.message,'elapsed_seconds',toc(start),'provenance',m,'bout_key',ec.bout_key,'source_index',ec.source_index,'assertion',ec.assertion);if ~isempty(ec.assertion),record.observed=ec.assertion.observed;record.expected=ec.assertion.expected;record.k=ec.assertion.source_index;end
 writejson(fullfile(O,sprintf('worker%d_error.json',worker)),record);
 if startsWith(err.identifier,'Paper2:')||startsWith(err.identifier,'Final:')
  if ~isfile(fullfile(O,'STOPPED.md')),f=fopen(fullfile(O,'STOPPED.md'),'w','n','UTF-8');fprintf(f,'# STOPPED: method-relevant ablation problem\n\nWorker %d: %s: %s\n',worker,err.identifier,err.message);fclose(f);end
 end
 rethrow(err);
end
 function stopcheck,paper2_assert(~isfile(fullfile(O,'STOPPED.md')),'Paper2:StoppedElsewhere','Another worker stopped',isfile(fullfile(O,'STOPPED.md')),false);end
end
function a=apcref(r,i)
a=struct('fp',r.phase_frequency_hz.Value,'fa',r.amplitude_frequency_hz.Value,'raw',r.pac_strength.Value,'pref',r.preferred_phase_deg.Value,'status',r.status_code.Value,'band',i.final_band_hz,'route',string(i.route));
end
function b=base_sim(c,suite,seed)
beta=nan;if suite=="HA",beta=c.beta;end
b=struct('suite',suite,'input_id',c.input_id,'paired_coupled_id',c.paired_coupled_id,'scenario',string(c.scenario),'dataset',string(c.dataset),'level',c.level,'beta',beta,'duration_s',numel(c.signal)/c.cfg.fs_hz,'repeat_index',c.repeat_index,'true_fp_hz',c.cfg.true_fp_hz,'true_fa_hz',c.cfg.true_fa_hz,'patient',"",'recording',"",'key',suite+"_"+c.input_id,'state',"",'movement_type',"",'seed',seed,'generator_settings_json',string(jsonencode(c.cfg)));
end
function writejson(file,value),f=fopen(file,'w','n','UTF-8');paper2_assert(f>=0,'Paper2:ErrorJSON','Cannot open error JSON',f,'file descriptor >= 0');c=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(value));end
function done=restore_csv(paths,csv,m)
done=strings(0,1);parts={};
for file=paths(:).'
 if ~isfile(file),continue;end
 q=load(file,'T','m');paper2_assert(strcmp(q.m.git_head,m.git_head),'Paper2:Checkpoint','Checkpoint commit differs',q.m.git_head,m.git_head);parts{end+1}=q.T;done(end+1,1)=file; %#ok<AGROW>
end
if ~isempty(parts),v1_write_csv(vertcat(parts{:}),csv);else,paper2_assert(~isfile(csv),'Paper2:CheckpointCSV','Unexpected CSV without completed checkpoints',isfile(csv),false);end
end
