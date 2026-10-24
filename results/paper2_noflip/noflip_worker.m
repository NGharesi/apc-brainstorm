function noflip_worker(worker,nworkers)
if nargin<2,nworkers=4;end
O=fileparts(mfilename('fullpath'));R=fileparts(fileparts(O));repo=fullfile(R,'apc-brainstorm-publish');V=fullfile(R,'revision_checks','paper2_validation');cd(O);
addpath(fullfile(repo,'analysis','v1_revision'),'-begin');addpath(fullfile(repo,'results','paper2_ablation'),'-begin');addpath(fullfile(repo,'src'),'-begin');
assert(strcmpi(which('bst_apc'),fullfile(repo,'src','bst_apc.m')));
m=jsondecode(fileread(fullfile(O,'provenance.json')));cfg=jsondecode(fileread(fullfile(V,'configuration.json')));old=readtable(fullfile(V,'simulation_trial_estimates.csv'),'TextType','string','Encoding','UTF-8');dest=fullfile(O,'checkpoints');if ~isfolder(dest),mkdir(dest);end;started=tic;key="";
try
for suite=["V3","V1","V2","V4"]
 bank=load(fullfile(V,char(suite+"_inputs.mat")),'cases','meta');csv=fullfile(O,sprintf('%s_worker%d.csv',suite,worker));parts={};ids=worker:nworkers:numel(bank.cases);done=false(size(ids));
 for j=1:numel(ids)
  c=bank.cases{ids(j)};file=fullfile(dest,char(suite+"_"+c.input_id+".mat"));if isfile(file),q=load(file,'T');parts{end+1}=q.T;done(j)=true;end %#ok<AGROW>
 end
 if ~isempty(parts),v1_write_csv(vertcat(parts{:}),csv);else,assert(~isfile(csv));end
 for j=1:numel(ids)
  if done(j),continue;end
  assert(~isfile(fullfile(O,'STOPPED.md')),'NoFlip:Stopped','Another worker stopped');c=bank.cases{ids(j)};key=suite+"_"+c.input_id;q=load(fullfile(V,'checkpoints',char(key+".mat")),'detail');rows={};new_outputs=cell(1,2);new_info=cell(1,2);before=rng;
  for k=1:2
   name="APC-v1.0";source="F1_A_APC";r=q.detail.r1;info=q.detail.i1;opt=cfg.(suite).apc_options_v1;versionName='v1';
   if k==2,name="APC-v3.0";source="F2_A_APC";r=q.detail.r3;info=q.detail.i3;opt=cfg.(suite).apc_options_v3;versionName='v3';end
   a=old(old.key==key&old.method==name,:);f=old(old.key==key&old.method==source,:);assert(height(a)==1&&height(f)==1);
   rows{end+1}=pack(r,info,f.source_fp_hz,a.recovered_fp_hz,a.recovered_fa_hz,a.status,true,name,c,suite,bank.meta.seed); %#ok<AGROW>
   expectedOptions=info.options;expectedOptions.flipTroughs=false;opt.flipTroughs=false;[r,info]=bst_apc(struct('data',c.signal(:).','time',c.time(:).'),opt);assert(isequaln(expectedOptions,info.options),'NoFlip:Options','Only flipTroughs may differ from validation');fp=r.phase_frequency_hz.Value;
   if ~isfinite(fp),z=apc_fp_source(c.signal,c.time,versionName,opt);fp=z.phase_frequency_hz;end
   new_outputs{k}=r;new_info{k}=info;rows{end+1}=pack(r,info,fp,r.phase_frequency_hz.Value,r.amplitude_frequency_hz.Value,r.status_code.Value,false,name,c,suite,bank.meta.seed); %#ok<AGROW>
  end
  assert(isequal(before,rng),'NoFlip:RNG','Deterministic APC changed RNG');T=struct2table(vertcat(rows{:}));file=fullfile(dest,char(key+".mat"));save(file,'T','new_outputs','new_info','m','-v7.3');v1_write_csv(T,csv,true);
  if mod(j,25)==0,fprintf('W%d exploratory %s %d/%d\n',worker,suite,j,numel(ids));end
 end
 clear bank parts q;
end
writejson(fullfile(O,sprintf('worker%d_complete.json',worker)),struct('status','COMPLETE','classification','exploratory','elapsed_seconds',toc(started),'git_commit',m.git_head,'protocol_sha256',m.protocol_sha256));
catch err
 writejson(fullfile(O,sprintf('worker%d_error.json',worker)),struct('key',key,'identifier',err.identifier,'message',err.message,'stack',err.stack,'git_commit',m.git_head));
 if ~isfile(fullfile(O,'STOPPED.md')),f=fopen(fullfile(O,'STOPPED.md'),'w','n','UTF-8');fprintf(f,'# Exploratory analysis stopped\n\n%s\n%s: %s\n',key,err.identifier,err.message);fclose(f);end
 rethrow(err);
end
 function row=pack(r,info,sourcefp,fp,fa,status,flip,name,c,suite,seed)
  pc=nan;pd=nan;fc=nan;fd=nan;available="not available";
  if suite=="V3"&&isfinite(c.true_fd_hz)&&isfield(info,'diagnostics')&&~isempty(info.diagnostics)&&isfield(info.diagnostics{1},'aperiodic')
   a=info.diagnostics{1}.aperiodic;if ~isempty(a.frequency_hz)&&~isempty(a.power),[~,ic]=min(abs(a.frequency_hz-c.cfg.true_fp_hz));[~,id]=min(abs(a.frequency_hz-c.true_fd_hz));pc=a.power(ic);pd=a.power(id);fc=a.frequency_hz(ic);fd=a.frequency_hz(id);available="returned v3 BTA Welch power: nearest returned bin";end
  end
  row=struct('classification',"exploratory",'suite',suite,'key',key,'input_id',c.input_id,'scenario',string(c.scenario),'dataset',string(c.dataset),'level',c.level,'repeat_index',c.repeat_index,'seed',seed,'method',name,'flip_troughs',flip,'source_fp_hz',sourcefp,'endtoend_fp_hz',fp,'endtoend_fa_hz',fa,'status',status,'valid',status==0&&all(isfinite([fp fa])),'true_fp_hz',c.cfg.true_fp_hz,'true_fa_hz',c.cfg.true_fa_hz,'true_fd_hz',c.true_fd_hz,'n_bursts',r.n_bursts.Value,'n_phase_events',r.n_phase_events.Value,'fraction_epochs_flipped',"not available",'bta_power_coupled',pc,'bta_power_dominant',pd,'bta_sampled_coupled_hz',fc,'bta_sampled_dominant_hz',fd,'bta_power_availability',available,'route',string(info.route(1)),'options_json',string(jsonencode(info.options)),'signal_sha256',string(c.signal_sha256),'git_commit',string(m.git_head),'protocol_sha256',string(m.protocol_sha256),'matlab_version',string(version),'provenance_file',"provenance.json");
 end
end
function writejson(file,v),f=fopen(file,'w','n','UTF-8');assert(f>=0);c=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(v));end
