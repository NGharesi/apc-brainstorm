function ieeg_am4_worker(worker,totalWorkers)
% Deterministic, incremental Amendment-4 estimates; worker 0 is progress only.
out=fileparts(mfilename('fullpath'));root=fileparts(fileparts(out));repo=fullfile(root,'apc-brainstorm-publish');cd(out);
addpath(fullfile(root,'revision_checks','final'),'-begin');addpath(fullfile(root,'revision_checks','rodent_multi'),'-begin');addpath(out,'-begin');addpath(fullfile(repo,'src'),'-begin');clear bst_apc calc_MI_all_methods final_sos_filter;
assert(strcmpi(which('bst_apc'),fullfile(repo,'src','bst_apc.m')),'IEEG:MethodPath','Wrong APC source');assert(strcmpi(which('calc_MI_all_methods'),fullfile(repo,'src','calc_MI_all_methods.m')),'IEEG:MetricPath','Wrong metric source');
m=jsondecode(fileread(fullfile(out,'analysis_provenance.json')));I=readtable(fullfile(out,'trial_inclusion_amendment4.csv'),'Delimiter',',','ReadVariableNames',true,'VariableNamingRule','preserve','TextType','string','Encoding','UTF-8');I=I(ismember(lower(string(I.included)),["true","1"]),:);
sessions=unique(I.patient+"_"+I.session,'stable');progress="sub-01_ses-01";assert(ismember(progress,sessions));
if worker==0,sessions=progress;else,sessions=sessions(sessions~=progress);sessions=sessions(worker:totalWorkers:end);end
dest=fullfile(out,'estimates');if ~isfolder(dest),mkdir(dest);end;csv=fullfile(out,sprintf('ieeg_worker%d_trial_estimates.csv',worker));assert(~isfile(csv),'IEEG:ResumeCSV','Existing worker CSV requires explicit checkpoint-based resume');
start=tic;old=maxNumCompThreads(1);cleanup=onCleanup(@()maxNumCompThreads(old));rng(20261023,'twister');rowsWritten=0;computed=0;reused=0;statusCounts=zeros(1,10);
stamp=struct('git_head',m.git_head,'protocol_sha256',m.protocol_sha256,'seed',20261023,'analysis_provenance_file','analysis_provenance.json');
try
 for si=1:numel(sessions)
  key=sessions(si);J=sortrows(I(I.patient+"_"+I.session==key,:),{'analysis','trial'});D=load(J.cache_file(1),'signals','events','metadata');
  for ui=1:height(J)
   if isfile(fullfile(out,'METHOD_STOP_FLAG.json')),error('IEEG:OtherWorkerStopped','A method-relevant failure was reported');end
   u=J(ui,:);t=find(D.events.nTrial==u.trial,1);signal=D.signals.(u.analysis)(:,t);assert(numel(signal)==12000&&all(isfinite(signal)),'IEEG:InputInvalid','Invalid residual input');time=(0:11999)'/2000;
   file=fullfile(dest,char(key+"_trial"+compose('%03d',u.trial)+"_"+u.analysis+".mat"));
   if isfile(file)
    Q=load(file,'features','info','metadata');assert(strcmp(Q.metadata.protocol_sha256,m.protocol_sha256));features=Q.features;info=Q.info;metadata=Q.metadata;reused=reused+1;
   else
    before=rng;[a,info]=v1_bout_features(signal,time);a.n_bursts=ieeg_count_bursts(signal,time,info.options);features=a;c=ieeg_comparators(signal,2000,"ieeg","ieeg_A2_prime",.5);
    for k=1:4
     z=c(k);assert(z.status==0&&isfinite(z.score),'IEEG:ComparatorFailure','Comparator returned invalid score');features(end+1)=struct('method',z.method,'fP_hz',z.fp,'fA_hz',z.fa,'score',z.score,'raw_mvl',z.raw_mvl,'ozkurt_mvl',z.ozkurt_mvl,'preferred_phase_deg',z.preferred_phase_deg,'status',z.status,'route',"not_applicable",'effective_half_width_hz',12,'n_bursts',NaN); %#ok<AGROW>
    end
    assert(isequal(before,rng),'IEEG:RNGChanged','Deterministic method changed RNG');[unitPhase,amplitude]=ieeg_selected_series(signal,time,features,info);
    metadata=stamp;metadata.analysis=u.analysis;metadata.patient=u.patient;metadata.session=u.session;metadata.trial=u.trial;metadata.native_fs_hz=u.native_fs_hz;metadata.analysis_fs_hz=2000;metadata.window_s=[0 6];metadata.samples=12000;metadata.evoked_template_analysis=u.analysis;metadata.candidate_index=u.candidate_index;metadata.matlab_version=version;metadata.apc_options=info.options;metadata.comparator_settings=m.comparator_settings;metadata.source_file=D.metadata.source_file;metadata.preprocessed_cache_file=u.cache_file;
    save(file,'features','info','metadata','unitPhase','amplitude','-v7');computed=computed+1;
   end
   rows={};for k=1:5
    z=features(k);fpLow=z.fP_hz==1;fpHigh=z.fP_hz==12;faHigh=z.fA_hz==148;if k==1,fpLow=abs(z.fP_hz-1)<=.05;fpHigh=abs(z.fP_hz-30)<=.05;faHigh=z.fA_hz==150;end
    rows{k}=struct('analysis',u.analysis,'patient',u.patient,'session',u.session,'trial',u.trial,'SetSize',u.SetSize,'Correct',u.Correct,'method',z.method,'fP_hz',z.fP_hz,'fA_hz',z.fA_hz,'score',z.score,'raw_mvl',z.raw_mvl,'ozkurt_mvl',z.ozkurt_mvl,'preferred_phase_deg',z.preferred_phase_deg,'status',z.status,'route',z.route,'n_bursts',z.n_bursts,'effective_half_width_hz',z.effective_half_width_hz,'boundary_fp_low',fpLow,'boundary_fp_high',fpHigh,'boundary_fa_low',z.fA_hz==80,'boundary_fa_high',faHigh,'native_fs_hz',u.native_fs_hz,'checkpoint_file',string(file),'git_head',string(m.git_head),'protocol_sha256',string(m.protocol_sha256),'seed',20261023,'matlab_version',string(version),'provenance_json',string(jsonencode(metadata)));
   end
   T=struct2table(vertcat(rows{:}));if isfile(csv),writetable(T,csv,'WriteMode','append');else,writetable(T,csv);end;append_shared(T,fullfile(out,'ieeg_trial_estimates.csv'));rowsWritten=rowsWritten+5;statusCounts(features(1).status+1)=statusCounts(features(1).status+1)+1;
   if mod(ui,10)==0||ui==1||ui==height(J),saveguards(out,worker,stamp);fprintf('AM4 worker%d %s %s trial%d %d/%d status%d\n',worker,key,u.analysis,u.trial,ui,height(J),features(1).status);end
  end
  fprintf('AM4 SESSION COMPLETE worker%d %s APC status counts %s\n',worker,key,mat2str(statusCounts));
 end
 saveguards(out,worker,stamp);result=struct('status','COMPLETE','worker',worker,'elapsed_seconds',toc(start),'rows',rowsWritten,'computed_inputs',computed,'reused_inputs',reused,'apc_status_counts_indexed_from_zero',statusCounts,'provenance',stamp);writejson(fullfile(out,sprintf('worker%d_runtime.json',worker)),result);
 if worker==0,writejson(fullfile(out,'am4_sub01_ses01_progress_check.json'),result);fprintf('AM4 PROGRESS CHECK COMPLETE; NOT A GATE; continue automatically unchanged\n');end
catch err
 saveguards(out,worker,stamp);failure=struct('status','FAILED_STOP','identifier',err.identifier,'message',err.message,'worker',worker,'computed_inputs',computed,'rows_written',rowsWritten,'elapsed_seconds',toc(start),'provenance',stamp);writejson(fullfile(out,sprintf('worker%d_runtime.json',worker)),failure);if ~isfile(fullfile(out,'METHOD_STOP_FLAG.json')),writejson(fullfile(out,'METHOD_STOP_FLAG.json'),failure);end;rethrow(err);
end
end
function saveguards(out,worker,stamp)
guards=final_sos_filter('registry');if ~isempty(guards),G=struct2table(guards);G.provenance_json=repmat(string(jsonencode(stamp)),height(G),1);writetable(G,fullfile(out,sprintf('filter_guards_worker%d.csv',worker)));end
end
function writejson(path,s)
f=fopen(path,'w','n','UTF-8');assert(f~=-1);clean=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(s));
end
function append_shared(T,path)
lock=java.io.File([path '.lock']);start=tic;while ~lock.createNewFile(),assert(toc(start)<120,'IEEG:CSVLockTimeout','CSV lock timeout');pause(.1);end;cleanup=onCleanup(@()lock.delete());if isfile(path),writetable(T,path,'WriteMode','append');else,writetable(T,path);end
end
