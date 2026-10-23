function run_sos_correction(action,worker)
if nargin<2,worker=1;end
out='C:\Users\nghare\.brainstorm\process\revision_checks\final';root=fileparts(fileparts(out));repo=fullfile(root,'apc-brainstorm-publish');bank=fullfile(root,'revision_checks','v1_rerun');fu=fullfile(root,'revision_checks','v1_followup');hd=fullfile(root,'revision_checks','v2','candidate_03');
oldDir=pwd;oldThreads=maxNumCompThreads(1);oldPath=path;c=onCleanup(@()restore(oldDir,oldThreads,oldPath)); %#ok<NASGU>
cd(out);addpath(out,'-begin');addpath(fullfile(repo,'analysis','v1_revision'),'-begin');addpath(fullfile(out,'frozen_v1'),'-begin');
meta=jsondecode(fileread(fullfile(out,'sos_correction_provenance.json')));meta.matlab_version=version;meta.action=action;start=tic;
try
 switch action
  case 'audit',audit(out,bank,hd,meta);
  case 'heldout',heldout(out,hd,worker,meta);
  case 'development',development(out,bank,fu,worker,meta);
  case 'rodent',rodent(out,root,meta);
  otherwise,error('Final:Action','Unknown action');
 end
 guards=final_sos_filter('registry');if ~isempty(guards),G=struct2table(guards);G.provenance_json=repmat(string(jsonencode(meta)),height(G),1);v1_write_csv(G,fullfile(out,sprintf('sos_%s_worker%d_filter_guards.csv',action,worker)));end
 writejson(fullfile(out,sprintf('sos_%s_worker%d_runtime.json',action,worker)),struct('status','COMPLETE','elapsed_seconds',toc(start),'metadata',meta));
 fprintf('COMPLETE %s worker%d %.3fs\n',action,worker,toc(start));
catch err
 writejson(fullfile(out,sprintf('sos_%s_worker%d_failure.json',action,worker)),struct('status','FAILED_STOP','elapsed_seconds',toc(start),'identifier',err.identifier,'error',err.message,'metadata',meta));rethrow(err);
end
end
function audit(out,bank,hd,meta)
b=load(fullfile(hd,'heldout_inputs.mat'),'cases');hc=b.cases;selected={};
want={"H1_sparsity",1;"H1_sparsity",.15;"H1_distractor",3;"H2",3;"H4",0};
for j=1:5
 ix=find(cellfun(@(q)q.scenario==want{j,1}&&q.level==want{j,2}&&q.dataset=="coupled"&&q.repeat_index==1,hc),1);q=hc{ix};selected{end+1}=struct('suite',"heldout",'label',"input_"+ix,'signal',q.signal,'source',string(fullfile(hd,'heldout_inputs.mat'))); %#ok<AGROW>
end
sources={'main_sparsity_level_1.mat','main_sparsity_level_0.15.mat','main_distractor_level_3.mat','random_fp_sparsity_level_0.5.mat','random_fp_distractor_level_1.5.mat'};
for j=1:5,b=load(fullfile(bank,sources{j}),'cases');q=b.cases{1};selected{end+1}=struct('suite',"development",'label',string(sources{j})+"_trial1",'signal',q.signal,'source',string(fullfile(bank,sources{j})));end %#ok<AGROW>
bands=struct([]);
for f=3:.5:14,bands=addband(bands,[max(.5,f-1.5),f+1.5],"heldout_phase");end
for f=4:.5:12,bands=addband(bands,[max(.5,f-1.5),f+1.5],"development_phase");end
for fa=80:4:160
 bands=addband(bands,[fa-14,fa+14],"heldout_A2_prime");
 for fp=3:.5:14,bands=addband(bands,[fa-fp,fa+fp],"heldout_A1_prime");end
end
for fa=80:8:152
 for half=[6 12],bands=addband(bands,[fa-half,fa+half],"development_fixed");end
 for fp=4:.5:12,bands=addband(bands,[fa-fp,fa+fp],"development_A1");end
end
rows={};
for j=1:numel(bands)
 band=bands(j).band;[~,info]=final_sos_filter(selected{1}.signal,500,band);wn=band/250;[ba,aa]=butter(4,wn,'bandpass');w=[2*pi*mean(band)/500 2*pi*mean(band)/500+1e-10];h=freqz(ba,aa,w);
 for k=1:numel(selected)
  s=selected{k};[ys,~]=final_sos_filter(s.signal,500,band);yd=filtfilt(ba,aa,double(s.signal(:)));relative=norm(yd-ys)/max(norm(ys),realmin);
  item=struct('input_suite',s.suite,'input_label',s.label,'source_file',s.source,'band_uses',bands(j).uses,'fs_hz',500,'low_hz',band(1),'high_hz',band(2),'direct_max_pole_radius',max(abs(roots(aa))),'sos_max_pole_radius',info.max_pole_radius,'sos_section_max_pole_radius',info.max_sos_section_pole_radius,'direct_center_gain',abs(h(1)),'sos_center_gain',info.center_gain,'relative_L2_difference',relative,'direct_RMS',sqrt(mean(yd.^2)),'sos_RMS',sqrt(mean(ys.^2)),'guard_passed',info.guard_passed,'git_commit',string(meta.git_commit),'matlab_version',string(version),'seed',20261022,'provenance_json',string(jsonencode(meta)));rows{end+1}=item; %#ok<AGROW>
 end
 if mod(j,50)==0,fprintf('AUDIT band%d/%d\n',j,numel(bands));end
end
T=struct2table([rows{:}]);v1_write_csv(T,fullfile(out,'filter_audit_500Hz_trials.csv'));
plan=struct('all_SOS_guards_passed',all(T.guard_passed),'all_direct_relative_differences_below_1e_6',all(T.relative_L2_difference<1e-6),'rerun_heldout',any(T.relative_L2_difference(contains(T.band_uses,'heldout'))>=1e-6),'rerun_development',any(T.relative_L2_difference(contains(T.band_uses,'development'))>=1e-6),'unique_bands',numel(bands),'audit_comparisons',height(T),'maximum_relative_L2_difference',max(T.relative_L2_difference),'metadata',meta);
assert(plan.all_SOS_guards_passed);writejson(fullfile(out,'filter_audit_plan.json'),plan);disp(plan);
end
function b=addband(b,band,use)
j=[];if ~isempty(b),j=find(arrayfun(@(q)isequal(q.band,band),b),1);end
if isempty(j),b=[b;struct('band',band,'uses',use)];else,if ~contains(b(j).uses,use),b(j).uses=b(j).uses+";"+use;end;end
end
function checkplan(out,field)
p=jsondecode(fileread(fullfile(out,'filter_audit_plan.json')));assert(p.all_SOS_guards_passed,'Final:Guard','Audit guard failed');assert(p.(field),'Final:Plan','Rerun not required by audit');
end
function heldout(out,hd,worker,meta)
checkplan(out,'rerun_heldout');b=load(fullfile(hd,'heldout_inputs.mat'),'cases');cases=b.cases;indices=worker:3:numel(cases);allTables={};
for begin=1:25:numel(indices)
 file=fullfile(out,sprintf('sos_heldout_worker%d_chunk%03d.mat',worker,ceil(begin/25)));
 if isfile(file),b=load(file,'T');allTables{end+1}=b.T;continue;end %#ok<AGROW>
 rows={};subset=indices(begin:min(begin+24,numel(indices)));
 for j=1:numel(subset)
  q=cases{subset(j)};before=rng;c=sos_comparators(q.signal,q.cfg.fs_hz,"heldout",["A2_prime","A1_prime"],.5);assert(isequal(before,rng));
  for k=1:numel(c),z=c(k);item=struct('input_id',q.input_id,'paired_coupled_id',q.paired_coupled_id,'scenario',q.scenario,'dataset',q.dataset,'level',q.level,'repeat_index',q.repeat_index,'true_fp_hz',q.cfg.true_fp_hz,'true_fa_hz',q.cfg.true_fa_hz,'true_fd_hz',q.true_fd_hz,'configuration',z.configuration,'method',z.method,'recovered_fp_hz',z.fp,'recovered_fa_hz',z.fa,'score',z.score,'ozkurt_mvl',z.ozkurt_mvl,'status',z.status,'valid',z.status==0,'git_commit',string(meta.git_commit),'matlab_version',string(version),'seed',20261022,'generator_settings_json',string(jsonencode(q.cfg)),'provenance_json',string(jsonencode(meta)));assert(z.status==0,'Final:Comparator','Invalid score');rows{end+1}=item;end %#ok<AGROW>
 end
 T=struct2table([rows{:}]);metadata=meta;save(file,'T','metadata','-v7.3');allTables{end+1}=T;fprintf('HELDOUT worker%d %d/%d\n',worker,min(begin+24,numel(indices)),numel(indices)); %#ok<AGROW>
end
T=vertcat(allTables{:});v1_write_csv(T,fullfile(out,sprintf('sos_heldout_worker%d_trials.csv',worker)));
end
function development(out,bank,fu,worker,meta)
checkplan(out,'rerun_development');tasks={};
for stage=["main","random_fp","null"]
 for bench=["sparsity","distractor"]
  files=dir(fullfile(bank,sprintf('%s_%s_level_*.mat',stage,bench)));
  for k=1:numel(files),tasks{end+1}=struct('stage',stage,'benchmark',bench,'file',string(fullfile(files(k).folder,files(k).name)));end %#ok<AGROW>
 end
end
files=dir(fullfile(fu,'slow_inputs_level_*.mat'));for k=1:numel(files),tasks{end+1}=struct('stage',"slow",'benchmark',"slow_rhythm",'file',string(fullfile(files(k).folder,files(k).name)));end %#ok<AGROW>
allTables={};
for taskIndex=worker:3:numel(tasks)
 task=tasks{taskIndex};file=fullfile(out,sprintf('sos_development_task%03d.mat',taskIndex));
 if isfile(file),b=load(file,'T');allTables{end+1}=b.T;continue;end %#ok<AGROW>
 b=load(task.file);if task.stage=="null",paired=strrep(task.file,'null_','main_');p=load(paired,'cases');cases=p.cases;else,cases=b.cases;end
 rows={};
 for ir=1:25
  q=cases{ir};datasets="coupled";if task.stage=="null",datasets=["timing_null","no_coupled_burst"];elseif task.stage=="slow"&&isfield(b,'nullCases')&&~isempty(b.nullCases{ir}),datasets=["coupled","timing_null"];end
  for dataset=datasets
   cfg=q.cfg;signal=q.signal;
   if task.stage=="null",n=b.nullCases{ir};signal=n.(dataset);if dataset=="no_coupled_burst",cfg.coupling_level=0;end
   elseif task.stage=="slow"&&dataset=="timing_null",n=b.nullCases{ir};signal=n.signal;end
   before=rng;
   if task.stage=="slow",c=sos_comparators(signal,cfg.fs_hz,"development",["A1","A2"],[1 .5]);
   elseif task.stage=="random_fp",c=sos_comparators(signal,cfg.fs_hz,"development",["A0","A1","A2"],[1 .5]);
   else,c=[sos_comparators(signal,cfg.fs_hz,"development",["A0","A1"],1);sos_comparators(signal,cfg.fs_hz,"development","A2",[1 .5])];end
   assert(isequal(before,rng));
   for k=1:numel(c),z=c(k);assert(z.status==0,'Final:Comparator','Invalid development score');item=struct('stage',task.stage,'benchmark',task.benchmark,'dataset',dataset,'level',q.level,'repeat_index',ir,'true_fp_hz',cfg.true_fp_hz,'true_fa_hz',cfg.true_fa_hz,'configuration',z.configuration,'method',z.method,'fp_grid_step_hz',z.fp_grid_step_hz,'recovered_fp_hz',z.fp,'recovered_fa_hz',z.fa,'score',z.score,'status_code',z.status,'valid',z.status==0,'route',"not_applicable",'input_file',task.file,'git_commit',string(meta.git_commit),'matlab_version',string(version),'seed',20260618,'generator_settings_json',string(jsonencode(cfg)),'provenance_json',string(jsonencode(meta)));rows{end+1}=item;end %#ok<AGROW>
  end
 end
 T=struct2table([rows{:}]);metadata=meta;save(file,'T','metadata','-v7.3');allTables{end+1}=T;fprintf('DEVELOPMENT worker%d task%d/%d %s\n',worker,taskIndex,numel(tasks),task.file); %#ok<AGROW>
end
T=vertcat(allTables{:});v1_write_csv(T,fullfile(out,sprintf('sos_development_worker%d_trials.csv',worker)));
end
function rodent(out,root,meta)
b=load(fullfile(root,'apc_ec013_run_rest_results.mat'),'results');base=b.results;rows={};
for state=["run","rest"]
 bouts=base.(state).bouts;
 for j=1:height(bouts)
  ix=bouts.start_idx(j):bouts.stop_idx(j);x=base.signal_window(ix);time=base.signal_time(ix);fs=1/median(diff(time));c=sos_comparators(x,fs,"rodent","rodent_A2_prime",.5);
  for k=1:numel(c),z=c(k);item=struct('session',"ec013.157",'state',state,'bout',j,'duration_s',bouts.duration_s(j),'method',z.method,'fP_hz',z.fp,'fA_hz',z.fa,'score',z.score,'raw_mvl',z.raw_mvl,'ozkurt_mvl',z.ozkurt_mvl,'preferred_phase_deg',z.preferred_phase_deg,'boundary_fP_4',double(z.fp==4),'boundary_fP_12',double(z.fp==12),'git_commit',string(meta.git_commit),'matlab_version',string(version),'seed',20261022,'provenance_json',string(jsonencode(meta)));rows{end+1}=item;end %#ok<AGROW>
  fprintf('RODENT SOS %s %d/12\n',state,j);
 end
end
T=struct2table([rows{:}]);v1_write_csv(T,fullfile(out,'sos_rodent_comparator_bouts.csv'));
end
function writejson(file,s)
f=fopen(file,'w','n','UTF-8');assert(f>=0);c=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(s));
end
function restore(d,t,p),cd(d);maxNumCompThreads(t);path(p);end
