function validation_real_worker(worker,nworkers)
if nargin<2,nworkers=4;end
O=fileparts(mfilename('fullpath'));root=fileparts(fileparts(O));repo=fullfile(root,'apc-brainstorm-publish');cd(O);
addpath(fullfile(repo,'analysis','v1_revision'),'-begin');addpath(fullfile(repo,'results','paper2_ablation'),'-begin');addpath(fullfile(root,'revision_checks','final'),'-begin');addpath(O,'-begin');addpath(fullfile(repo,'src'),'-begin');
m=jsondecode(fileread(fullfile(O,'provenance.json')));assert(strcmpi(which('bst_apc'),fullfile(repo,'src','bst_apc.m')));start=tic;key="";
dest=fullfile(O,'real_checkpoints');if ~isfolder(dest),mkdir(dest);end
args={'Delimiter',',','NumHeaderLines',0,'ReadVariableNames',true,'TextType','string','Encoding','UTF-8'};
try
 J=readtable(fullfile(O,'rodent_inputs.csv'),args{:});refs=readtable(fullfile(O,'rodent_saved_references.csv'),args{:});sessions=unique(J.session,'stable');csv=fullfile(O,sprintf('rodent_worker%d.csv',worker));sourcecsv=fullfile(O,sprintf('rodent_sources_worker%d.csv',worker));parts={};sources={};done=[];
 for j=worker:nworkers:numel(sessions)
  K=J(J.session==sessions(j),:);
  for k=1:height(K),file=fullfile(dest,sprintf('rodent_%05d.mat',K.input_id(k)));if isfile(file),q=load(file,'T','sources','m');assert(strcmp(q.m.git_head,m.git_head));parts{end+1}=q.T;sources{end+1}=q.sources;done(end+1)=K.input_id(k);end;end %#ok<AGROW>
 end
 if ~isempty(parts),v1_write_csv(vertcat(parts{:}),csv);v1_write_csv(vertcat(sources{:}),sourcecsv);else,assert(~isfile(csv));end;clear parts sources;
 for j=worker:nworkers:numel(sessions)
  K=J(J.session==sessions(j),:);pending=~ismember(K.input_id,done);if ~any(pending),continue;end
  inventory=whos('-file',K.source_file(1));
  if any(strcmp({inventory.name},'test')),q=load(K.source_file(1),'test');record=q.test;
  else,q=load(K.source_file(1),'F','Time');record=q;end
  for k=find(pending).'
   stopcheck;job=K(k,:);key="rodent_"+job.input_id;ix=job.start_idx:job.stop_idx;x=double(record.F(job.channel_index,ix));t=double(record.Time(ix));before=rng;
   [new,detail]=validation_f3(x,t,"rodent");rows=cell(1,4);for z=1:2,rows{z}=new(z);end
   p=refs(refs.input_id==job.input_id,:);assert(height(p)==2,'Validation:RodentReference','Missing saved rodent pair');
   for z=1:2
    target="APC-v1.0";if z==2,target="MVL-Ozkurt";end;a=p(p.method==target,:);assert(height(a)==1);row=new(1);row.method=target;if z==2,row.method="A2_prime_2D";end
    row.source_fp_hz=a.fp;row.source_status=a.status;row.recovered_fp_hz=a.fp;row.recovered_fa_hz=a.fa;row.raw_mvl=a.raw;row.coupling=a.coupling;row.preferred_phase_deg=a.pref;row.status=a.status;row.valid=a.status==0&&all(isfinite([a.fp a.fa a.coupling]));row.selection_score=nan;row.amplitude_band_low_hz=nan;row.amplitude_band_high_hz=nan;
    if z==2&&a.status==0
     band=[a.fa-12 a.fa+12];c=paper2_coupling_at_pair(x,t,a.fp,a.fa,band,"SCAN");row.raw_mvl=c.raw_mvl;row.coupling=c.normalized_mvl;row.preferred_phase_deg=c.preferred_phase_deg;row.status=c.status;row.valid=c.status==0;row.amplitude_band_low_hz=band(1);row.amplitude_band_high_hz=band(2);
    end
    rows{2+z}=row;
   end
   T=struct2table(vertcat(rows{:}));T.input_id=repmat(job.input_id,height(T),1);T.key=repmat(key,height(T),1);T.session=repmat(job.session,height(T),1);T.channel_index=repmat(job.channel_index,height(T),1);T.duration_s=repmat(numel(x)/(1/median(diff(t))),height(T),1);T.signal_sha256=repmat(string(signalsha(x)),height(T),1);T=stamp(T);
   % Descriptive source counts reuse frozen end-to-end statuses; recover only missing Step-2 estimates.
   old3=load(fullfile(root,'revision_checks','v3_aperiodic','phaseC','checkpoints',sprintf('rodent_%05d.mat',job.input_id)),'features');src={};cfg=validation_settings("rodent");
   for z=1:2
    a=p(p.method=="APC-v1.0",:);f=a.fp;ss=a.status;if z==2,f=old3.features.fP_hz;ss=old3.features.status;end
    if ~isfinite(f),opt=cfg.apc_options_v1;v='v1';if z==2,opt=cfg.apc_options_v3;v='v3';end;fout=apc_fp_source(x,t,v,opt);f=fout.phase_frequency_hz;end
    src{z}=struct('input_id',job.input_id,'key',key,'source',"F"+z,'source_fp_hz',f,'endtoend_status',ss,'finite_step2_later_failed',isfinite(f)&&ss~=0); %#ok<AGROW>
   end
   sources=stamp(struct2table(vertcat(src{:})));assert(isequal(before,rng),'Validation:RealRNG','Rodent deterministic code changed RNG');file=fullfile(dest,sprintf('rodent_%05d.mat',job.input_id));save(file,'T','detail','sources','m','-v7.3');v1_write_csv(T,csv,true);v1_write_csv(sources,sourcecsv,true);
  end
  fprintf('W%d rodent %s finished %d physical bouts\n',worker,sessions(j),sum(pending));clear q record;
 end
 E=fullfile(root,'revision_checks','ecog_miller_motor');B=readtable(fullfile(O,'ecog_bouts.csv'),args{:});patients=unique(B.patient,'sorted');old=readtable(fullfile(root,'revision_checks','paper2_ablation','ecog_bout_estimates.csv'),args{:});csv=fullfile(O,sprintf('ecog_worker%d.csv',worker));sourcecsv=fullfile(O,sprintf('ecog_sources_worker%d.csv',worker));parts={};sr={};done=strings(0,1);
 for j=worker:nworkers:numel(patients)
  K=B(B.patient==patients(j),:);
  for k=1:height(K),key=string(sprintf('%s_%s_%03d',patients(j),K.recording(k),K.bout(k)));file=fullfile(dest,char("ecog_"+key+".mat"));if isfile(file),q=load(file,'T','sources','m');assert(strcmp(q.m.git_head,m.git_head));parts{end+1}=q.T;sr{end+1}=q.sources;done(end+1)=key;end;end %#ok<AGROW>
 end
 if ~isempty(parts),v1_write_csv(vertcat(parts{:}),csv);v1_write_csv(vertcat(sr{:}),sourcecsv);else,assert(~isfile(csv));end;clear parts sr;
 for j=worker:nworkers:numel(patients)
  pt=patients(j);S=load(fullfile(E,'prep',char(pt+".mat")));K=B(B.patient==pt,:);
  for k=1:height(K)
   stopcheck;b=K(k,:);key=string(sprintf('%s_%s_%03d',pt,b.recording,b.bout));if any(done==key),continue;end
   x=S.sig;if b.recording=="imagery",x=S.sigI;end;x=double(x(b.start_sample:b.end_sample));t=(0:numel(x)-1)/S.fs;before=rng;
   [new,detail]=validation_f3(x,t,"ecog");saved=old(old.key==key,:);prior=saved(saved.method=="F3_A_SCAN",:);assert(height(prior)==1,'Validation:EcogReference','Missing saved scan');
   obs=[new(1).source_fp_hz new(1).recovered_fa_hz new(1).coupling];exp=[prior.source_fp_hz prior.recovered_fa_hz prior.coupling];finite=isfinite(obs)&isfinite(exp);assert(isequal(isnan(obs),isnan(exp))&&all(abs(obs(finite)-exp(finite))<=1e-10),'Validation:EcogScanReproduction','%s old/new F3 scan mismatch observed%s expected%s',key,mat2str(obs,17),mat2str(exp,17));
   rows=cell(1,5);rows{1}=new(1);rows{2}=new(2);
   names=["APC-v1.0","APC-v3.0","A2_prime_2D"];
   for z=1:3
    a=saved(saved.method==names(z),:);assert(height(a)==1);row=new(1);row.method=names(z);row.source_fp_hz=a.source_fp_hz;row.source_status=a.source_status;row.recovered_fp_hz=a.recovered_fp_hz;row.recovered_fa_hz=a.recovered_fa_hz;row.raw_mvl=a.raw_mvl;row.coupling=a.coupling;row.preferred_phase_deg=a.preferred_phase_deg;row.status=a.status;row.valid=savedlogical(a.valid);row.selection_score=nan;row.amplitude_band_low_hz=a.amplitude_band_low_hz;row.amplitude_band_high_hz=a.amplitude_band_high_hz;rows{2+z}=row;
   end
   T=struct2table(vertcat(rows{:}));T.key=repmat(key,height(T),1);T.patient=repmat(pt,height(T),1);T.recording=repmat(b.recording,height(T),1);T.state=repmat(b.state,height(T),1);T.bout=repmat(b.bout,height(T),1);T.duration_s=repmat(b.duration_s,height(T),1);T.signal_sha256=repmat(string(signalsha(x)),height(T),1);T=stamp(T);
   src={};for z=1:2,a=saved(saved.method=="F"+z+"_A_APC",:);r=saved(saved.method==names(z),:);src{z}=struct('key',key,'patient',pt,'recording',b.recording,'state',b.state,'source',"F"+z,'source_fp_hz',a.source_fp_hz,'endtoend_status',r.status,'finite_step2_later_failed',isfinite(a.source_fp_hz)&&r.status~=0);end %#ok<AGROW>
   sources=stamp(struct2table(vertcat(src{:})));assert(isequal(before,rng),'Validation:RealRNG','ECoG deterministic code changed RNG');file=fullfile(dest,char("ecog_"+key+".mat"));save(file,'T','detail','sources','m','-v7.3');v1_write_csv(T,csv,true);v1_write_csv(sources,sourcecsv,true);
  end
  fprintf('W%d ECoG %s finished %d bouts\n',worker,pt,height(K));
 end
 guards=final_sos_filter('registry');g=stamp(struct2table(guards));v1_write_csv(g,fullfile(O,sprintf('real_filter_guards_w%d.csv',worker)));writejson(fullfile(O,sprintf('real_worker%d_complete.json',worker)),struct('status','COMPLETE','elapsed_seconds',toc(start),'provenance',m));
catch err
 writejson(fullfile(O,sprintf('real_worker%d_error.json',worker)),struct('key',key,'identifier',err.identifier,'message',err.message,'stack',err.stack,'provenance',m));
 if startsWith(err.identifier,'Validation:')||startsWith(err.identifier,'Final:')
  if ~isfile(fullfile(O,'STOPPED_ACTIVE.md')),f=fopen(fullfile(O,'STOPPED_ACTIVE.md'),'w','n','UTF-8');fprintf(f,'# STOPPED: real-data validation\n\n%s\n%s: %s\n',key,err.identifier,err.message);fclose(f);end
 end
 rethrow(err);
end
 function T=stamp(T),T.git_commit=repmat(string(m.git_head),height(T),1);T.protocol_sha256=repmat(string(m.protocol_sha256),height(T),1);T.matlab_version=repmat(string(version),height(T),1);T.provenance_file=repmat("provenance.json",height(T),1);end
 function stopcheck,assert(~isfile(fullfile(O,'STOPPED_ACTIVE.md')),'Validation:OtherWorkerStopped','Another worker stopped');end
end
function value=signalsha(x),md=java.security.MessageDigest.getInstance('SHA-256');md.update(typecast(double(x(:)),'uint8'));bytes=typecast(md.digest(),'uint8');value=lower(reshape(dec2hex(bytes,2).',1,[]));end
function writejson(file,v),f=fopen(file,'w','n','UTF-8');assert(f>=0);c=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(v));end

function value=savedlogical(x)
if islogical(x)||isnumeric(x),assert(isscalar(x)&&ismember(x,[0 1]));value=logical(x);return;end
s=lower(strtrim(string(x)));assert(isscalar(s)&&ismember(s,["true","false","1","0"]),'Validation:SavedBoolean','Unexpected saved boolean %s',s);value=ismember(s,["true","1"]);
end
