function confirm_worker(worker,nworkers)
if nargin<2,nworkers=4;end
O=fileparts(mfilename('fullpath'));R=fileparts(fileparts(O));repo=fullfile(R,'apc-brainstorm-publish');cd(O);
addpath(fullfile(repo,'analysis','v1_revision'),'-begin');addpath(fullfile(repo,'results','paper2_ablation'),'-begin');addpath(fullfile(R,'revision_checks','final'),'-begin');addpath(fullfile(repo,'results','paper2_validation'),'-begin');addpath(fullfile(repo,'src'),'-begin');
assert(strcmpi(which('bst_apc'),fullfile(repo,'src','bst_apc.m')));if worker==1,writejson(fullfile(O,'environment.json'),struct('matlab_version',version,'toolbox_versions',feval('ver')));end;m=jsondecode(fileread(fullfile(O,'provenance.json')));G=jsondecode(fileread(fullfile(O,'generator_check.json')));gen=jsondecode(fileread(fullfile(O,'generation_complete.json')));assert(strcmp(G.status,'PASS')&&strcmp(gen.status,'COMPLETE'));dest=fullfile(O,'checkpoints');if ~isfolder(dest),mkdir(dest);end;start=tic;key="";
try
for suite=["W3","W1"]
 profile="V3";if suite=="W1",profile="V1";end;cfg=validation_settings(profile);bank=load(fullfile(O,char(suite+"_inputs.mat")),'cases','bankmeta');ids=worker:nworkers:numel(bank.cases);csv=fullfile(O,sprintf('%s_worker%d.csv',suite,worker));done=false(size(ids));parts={};
 for j=1:numel(ids),c=bank.cases{ids(j)};file=fullfile(dest,char(suite+"_"+c.input_id+".mat"));if isfile(file),q=load(file,'T');parts{end+1}=q.T;done(j)=true;end;end %#ok<AGROW>
 if ~isempty(parts),v1_write_csv(vertcat(parts{:}),csv);else,assert(~isfile(csv));end
 for j=1:numel(ids)
  if done(j),continue;end
  assert(~isfile(fullfile(O,'STOPPED.md')),'Confirm:Stopped','Another worker stopped');c=bank.cases{ids(j)};key=suite+"_"+c.input_id;fs=1/median(diff(c.time));before=rng;rows={};outputs=cell(2,2);infos=cell(2,2);sourcefps=nan(2,2);sourceStatus=nan(2,2);
  for k=1:2
   opt=cfg.apc_options_v1;ver='v1';if k==2,opt=cfg.apc_options_v3;ver='v3';end
   for flag=1:-1:0
    options=opt;options.flipTroughs=logical(flag);[r,info]=bst_apc(struct('data',c.signal(:).','time',c.time(:).'),options);fp=r.phase_frequency_hz.Value;ss=r.status_code.Value;
    if ~isfinite(fp),z=apc_fp_source(c.signal,c.time,ver,options);fp=z.phase_frequency_hz;ss=z.status_code;end
    if isfinite(fp),ss=0;end;sourcefps(k,flag+1)=fp;sourceStatus(k,flag+1)=ss;outputs{k,flag+1}=r;infos{k,flag+1}=info;
    method="APC-v"+k+".0-flip";if k==2,method="APC-v3.0-flip";end;if flag==0,method=replace(method,"-flip","-noflip");end
    row=pack(method,fp,r.phase_frequency_hz.Value,r.amplitude_frequency_hz.Value,r.status_code.Value,flag,string(jsonencode(info.options)));row.n_bursts=r.n_bursts.Value;row.raw_mvl=r.pac_strength.Value;row.route=string(info.route(1));
    if suite=="W3"&&isfinite(c.true_fd_hz)&&k==2&&isfield(info,'diagnostics')&&isfield(info.diagnostics{1},'aperiodic')
     a=info.diagnostics{1}.aperiodic;if ~isempty(a.frequency_hz)&&~isempty(a.power),[~,ic]=min(abs(a.frequency_hz-c.cfg.true_fp_hz));[~,id]=min(abs(a.frequency_hz-c.true_fd_hz));row.bta_power_coupled=a.power(ic);row.bta_power_dominant=a.power(id);row.bta_sampled_coupled_hz=a.frequency_hz(ic);row.bta_sampled_dominant_hz=a.frequency_hz(id);end
    end
    rows{end+1}=row; %#ok<AGROW>
   end
  end
  [fp,sp,ss]=sp_raw_fp(c.signal,fs,cfg.apc_options_v3);[s,curve,settings]=validation_scan_fa(c.signal,fs,fp,profile);row=pack("F3_A_SCAN",fp,s.fp,s.fa,s.status,nan,string(jsonencode(settings)));row.selection_score=s.selection_score;rows{end+1}=row;
  [scans,maps]=validation_a2_map(c.signal,fs,profile,"A2_prime",.5);s=scans(string({scans.method})=="MVL-Ozkurt");assert(isscalar(s));row=pack("A2_prime_2D",s.fp,s.fp,s.fa,s.status,nan,string(jsonencode(cfg)));row.selection_score=s.score;rows{end+1}=row;
  % Call the unchanged frozen helper; retain the validation candidate subset.
  fp=sourcefps(2,1);[s,allScores,settings]=scan_fa_given_fp(c.signal,fs,fp,"heldout");keep=ismember(settings.amplitude_grid_hz,cfg.amplitude_grid_hz);assert(sum(keep)==numel(cfg.amplitude_grid_hz)&&settings.amplitude_half_width_hz==cfg.amplitude_half_width_hz);
  scores=allScores(keep);fa=nan;score=nan;status=sourceStatus(2,1);
  if isfinite(fp),[score,ia]=max(scores(:),[],'omitnan');fa=cfg.amplitude_grid_hz(ia);status=double(~isfinite(score));end
  settings.computed_amplitude_grid_hz=settings.amplitude_grid_hz;settings.amplitude_grid_hz=cfg.amplitude_grid_hz;row=pack("F2nf_A_SCAN",fp,fp,fa,status,0,string(jsonencode(settings)));row.selection_score=score;rows{end+1}=row;
  assert(isequal(before,rng),'Confirm:RNG','Deterministic methods changed RNG');T=struct2table(vertcat(rows{:}));file=fullfile(dest,char(key+".mat"));save(file,'T','outputs','infos','sourcefps','sourceStatus','sp','maps','curve','scores','m','-v7.3');v1_write_csv(T,csv,true);
  if mod(j,20)==0,fprintf('W%d %s %d/%d\n',worker,suite,j,numel(ids));end
 end
 clear bank parts;
end
guards=final_sos_filter('registry');T=struct2table(guards);T.git_commit=repmat(string(m.git_head),height(T),1);T.classification=repmat("confirmatory",height(T),1);T.protocol_sha256=repmat(string(m.protocol_sha256),height(T),1);v1_write_csv(T,fullfile(O,sprintf('filter_guards_w%d.csv',worker)));writejson(fullfile(O,sprintf('worker%d_complete.json',worker)),struct('status','COMPLETE','classification','confirmatory','elapsed_seconds',toc(start),'git_commit',m.git_head,'protocol_sha256',m.protocol_sha256));
catch err
 writejson(fullfile(O,sprintf('worker%d_error.json',worker)),struct('key',key,'identifier',err.identifier,'message',err.message,'stack',err.stack));if ~isfile(fullfile(O,'STOPPED.md')),f=fopen(fullfile(O,'STOPPED.md'),'w','n','UTF-8');fprintf(f,'# Confirmation stopped\n\n%s\n%s: %s\n',key,err.identifier,err.message);fclose(f);end;rethrow(err);
end
 function row=pack(method,sourcefp,fp,fa,status,flag,options)
  row=struct('classification',"confirmatory",'suite',suite,'case_index',ids(j),'key',key,'input_id',c.input_id,'paired_coupled_id',c.paired_coupled_id,'scenario',string(c.scenario),'dataset',string(c.dataset),'level',c.level,'repeat_index',c.repeat_index,'seed',bank.bankmeta.seed,'method',method,'flip_troughs',flag,'source_fp_hz',sourcefp,'endtoend_fp_hz',fp,'endtoend_fa_hz',fa,'status',status,'valid',status==0&&all(isfinite([fp fa])),'true_fp_hz',c.cfg.true_fp_hz,'true_fa_hz',c.cfg.true_fa_hz,'true_fd_hz',c.true_fd_hz,'n_bursts',nan,'fraction_epochs_flipped',"not available",'bta_power_coupled',nan,'bta_power_dominant',nan,'bta_sampled_coupled_hz',nan,'bta_sampled_dominant_hz',nan,'raw_mvl',nan,'selection_score',nan,'route',"not applicable",'options_json',options,'signal_sha256',string(c.signal_sha256),'git_commit',string(m.git_head),'protocol_sha256',string(m.protocol_sha256),'matlab_version',string(version),'provenance_file',"provenance.json");
 end
end
function writejson(p,x),f=fopen(p,'w','n','UTF-8');assert(f>=0);c=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(x));end
