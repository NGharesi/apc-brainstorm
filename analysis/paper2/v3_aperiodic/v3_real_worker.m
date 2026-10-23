function v3_real_worker(worker,nworkers)
% Phase C: fixed saved bouts/channels; existing scans are never rerun.
if nargin<2,nworkers=4;end
O=fileparts(mfilename('fullpath'));root=fileparts(fileparts(O));repo=fullfile(root,'apc-brainstorm-publish');C=fullfile(O,'phaseC');cd(C);
addpath(fullfile(repo,'analysis','v1_revision'),'-begin');addpath(O,'-begin');addpath(fullfile(repo,'src'),'-begin');assert(strcmpi(which('bst_apc'),fullfile(repo,'src','bst_apc.m')));
m=jsondecode(fileread(fullfile(C,'provenance.json')));criteria=jsondecode(fileread(fullfile(O,'criteria_decisions.json')));assert(criteria.criteria.A1.passed&&all([criteria.criteria.A3.passed])&&criteria.criteria.A4.passed);
dest=fullfile(C,'checkpoints');if ~isfolder(dest),mkdir(dest);end;start=tic;
try
 E=fullfile(root,'revision_checks','ecog_miller_motor');B=readtable(fullfile(E,'bouts.csv'),'TextType','string','Encoding','UTF-8');B=B(logical(B.analysed),:);patients=unique(B.patient,'stable');tables={};
 for j=worker:nworkers:numel(patients)
  pt=patients(j);S=load(fullfile(E,'prep',char(pt+".mat")));K=B(B.patient==pt,:);
  for k=1:height(K)
   stop_if_needed(O);b=K(k,:);key=string(sprintf('%s_%s_%03d',pt,b.recording,b.bout));file=fullfile(dest,char("ecog_"+key+".mat"));
   if isfile(file),z=load(file,'T','m');assert(strcmp(z.m.freeze_commit,m.freeze_commit));T=z.T;
   else
    x=S.sig;if b.recording=="imagery",x=S.sigI;end
    signal=x(b.start_sample:b.end_sample);time=(0:numel(signal)-1)/S.fs;before=rng;
    [features,info]=v3_bout_features(signal,time);sp=[];spfp=nan;spstatus=nan;
    if b.state=="rest",[spfp,sp,spstatus]=sp_raw_fp(signal,S.fs,struct('fA',[80 150],'minPhaseHz',1,'maxPhaseHz',30));end
    assert(isequal(before,rng),'v3:RealRNG','Deterministic real-data analysis consumed RNG');
    row=pack(features,info,spfp,spstatus,sp,numel(signal)/S.fs,m,20261024);
    row.key=key;row.patient=pt;row.recording=b.recording;row.bout=b.bout;row.state=b.state;row.movement_type=b.movement_type;row.code=b.code;row.rest_index=b.rest_index;row.duration_s=b.duration_s;
    row.boundary_fp_low=abs(row.fP_hz-1)<=.05;row.boundary_fp_high=abs(row.fP_hz-30)<=.05;row.boundary_fa_low=row.fA_hz==80;row.boundary_fa_high=row.fA_hz==150;
    T=struct2table(row);save(file,'T','features','info','sp','m','-v7.3');
   end
   tables{end+1}=T; %#ok<AGROW>
  end
  v1_write_csv(vertcat(tables{:}),fullfile(C,sprintf('ecog_worker%d.csv',worker)));fprintf('C W%d ECoG %s complete; %d bouts\n',worker,pt,numel(tables));clear S;
 end
 I=readtable(fullfile(C,'rodent_inputs.csv'),'TextType','string','Encoding','UTF-8');sessions=unique(I.session,'stable');tables={};
 for j=worker:nworkers:numel(sessions)
  session=sessions(j);K=I(I.session==session,:);q=K(1,:);
  if session=="ec013.157",S=load(q.source_file,'test');record=S.test;else,record=load(q.source_file,'F','Time');end
  for k=1:height(K)
   stop_if_needed(O);b=K(k,:);file=fullfile(dest,sprintf('rodent_%05d.mat',b.input_id));
   if isfile(file),z=load(file,'T','m');assert(strcmp(z.m.freeze_commit,m.freeze_commit));T=z.T;
   else
    ix=b.start_idx:b.stop_idx;time=double(record.Time(ix));signal=double(record.F(b.channel_index,ix));fs=1/median(diff(time));before=rng;
    [features,info]=v3_bout_features(signal,time);assert(isequal(before,rng),'v3:RealRNG','Rodent method consumed RNG');row=pack(features,info,nan,nan,[],numel(signal)/fs,m,20261022);
    row.input_id=b.input_id;row.session=session;row.channel_index=b.channel_index;row.start_idx=b.start_idx;row.stop_idx=b.stop_idx;row.source_file=b.source_file;
    row.boundary_fP_4=row.fP_hz==4;row.boundary_fP_12=row.fP_hz==12;
    T=struct2table(row);save(file,'T','features','info','m','-v7.3');
   end
   tables{end+1}=T; %#ok<AGROW>
   if mod(k,50)==0,fprintf('C W%d rodent %s %d/%d\n',worker,session,k,height(K));end
  end
  v1_write_csv(vertcat(tables{:}),fullfile(C,sprintf('rodent_worker%d.csv',worker)));fprintf('C W%d rodent %s complete; %d inputs\n',worker,session,numel(tables));clear S record;
 end
 write_json(fullfile(C,sprintf('worker%d_complete.json',worker)),struct('status','COMPLETE','elapsed_seconds',toc(start),'provenance',m));
 fprintf('C W%d COMPLETE %.3f seconds\n',worker,toc(start));
catch err
 write_json(fullfile(C,sprintf('worker%d_error.json',worker)),struct('identifier',err.identifier,'message',err.message,'elapsed_seconds',toc(start),'provenance',m));
 if startsWith(err.identifier,'v3:')||startsWith(err.identifier,'Rodent:')
  f=fopen(fullfile(O,'STOPPED.md'),'w','n','UTF-8');fprintf(f,'# STOPPED: Phase C method-relevant problem\n\nWorker%d: %s: %s\n',worker,err.identifier,err.message);fclose(f);
 end
 rethrow(err);
end
end
function row=pack(features,info,spfp,spstatus,sp,T,m,seed)
row=features;row.location_branch="not_reached";row.exponent=nan;row.offset=nan;row.peak_height=nan;row.sigma=nan;row.f_lo_hz=max(1,7/T);
if isfield(info.diagnostics{1},'aperiodic'),d=info.diagnostics{1}.aperiodic;row.location_branch=string(d.location_branch);row.exponent=d.exponent;row.offset=d.offset;row.peak_height=d.peak_height;row.sigma=d.sigma;end
if isfield(info.diagnostics{1},'burst_times'),row.n_bursts=numel(info.diagnostics{1}.burst_times);end
row.fp_at_flo=abs(row.fP_hz-row.f_lo_hz)<=.05;row.sp_raw_fp_hz=spfp;row.sp_raw_status=spstatus;row.sp_raw_branch="not_computed";if ~isempty(sp),row.sp_raw_branch=string(sp.location_branch);end
row.git_commit=string(m.freeze_commit);row.git_tag="v3.0";row.protocol_sha256=string(m.protocol_sha256);row.matlab_version=string(version);row.seed=seed;row.apc_options_json=string(jsonencode(info.options));row.provenance_record="phaseC/provenance.json";
end
function stop_if_needed(O),assert(~isfile(fullfile(O,'STOPPED.md')),'v3:StoppedElsewhere','Another worker stopped');end
function write_json(file,value),f=fopen(file,'w','n','UTF-8');assert(f>=0);c=onCleanup(@() fclose(f));fprintf(f,'%s\n',jsonencode(value));end
