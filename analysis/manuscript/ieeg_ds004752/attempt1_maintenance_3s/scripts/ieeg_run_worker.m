function ieeg_run_worker(worker,totalWorkers)
out=fileparts(mfilename('fullpath'));root=fileparts(fileparts(out));repo=fullfile(root,'apc-brainstorm-publish');cd(out);
addpath(fullfile(root,'revision_checks','final'),'-begin');addpath(fullfile(root,'revision_checks','rodent_multi'),'-begin');addpath(out,'-begin');addpath(fullfile(repo,'src'),'-begin');clear bst_apc calc_MI_all_methods final_sos_filter;
assert(strcmpi(which('bst_apc'),fullfile(repo,'src','bst_apc.m')),'IEEG:MethodPath','Wrong APC source');assert(strcmpi(which('calc_MI_all_methods'),fullfile(repo,'src','calc_MI_all_methods.m')),'IEEG:MetricPath','Wrong metric source');
m=jsondecode(fileread(fullfile(out,'analysis_provenance.json')));sel=jsondecode(fileread(fullfile(out,'selection_runtime.json')));assert(strcmp(sel.status,'COMPLETE'));
I=readtable(fullfile(out,'trial_inclusion.csv'),'Delimiter',',','ReadVariableNames',true,'VariableNamingRule','preserve','TextType','string','Encoding','UTF-8');I=I(ismember(lower(string(I.included)),["true","1"]),:);
I.signal_type=repmat("bipolar",height(I),1);I.signal_type(I.analysis=="referential")="reference";
sessions=unique(I.patient+"_"+I.session,'stable');dest=fullfile(out,'estimates');if ~isfolder(dest),mkdir(dest);end
csv=fullfile(out,sprintf('ieeg_worker%d_trial_estimates.csv',worker));assert(~isfile(csv),'IEEG:ResumeCSV','Worker CSV exists; use documented cache-based resume packaging before restarting');
start=tic;old=maxNumCompThreads(1);cleanup=onCleanup(@()maxNumCompThreads(old));rng(20261023,'twister');rowsWritten=0;computed=0;reused=0; %#ok<NASGU>
try
 for si=worker:totalWorkers:numel(sessions)
  key=sessions(si);J=I(I.patient+"_"+I.session==key,:);D=load(J.cache_file(1));candidate=J.candidate_index(1);assert(all(J.candidate_index==candidate));
  [~,idx]=unique(string(J.trial)+"_"+J.signal_type,'stable');U=J(idx,:);U=sortrows(U,{'trial','signal_type'});
  for ui=1:height(U)
   if isfile(fullfile(out,'METHOD_STOP_FLAG.json')),error('IEEG:OtherWorkerStopped','A method-relevant failure was reported by another worker');end
   u=U(ui,:);t=find(D.events.nTrial==u.trial,1);signal=D.bipolar(:,t,candidate);if u.signal_type=="reference",signal=D.reference(:,t,candidate);end;time=(0:5999)'/2000;
   file=fullfile(dest,char(key+"_trial"+compose('%03d',u.trial)+"_"+u.signal_type+".mat"));
   if isfile(file)
    Q=load(file,'features','info','metadata','unitPhase','amplitude');assert(strcmp(Q.metadata.protocol_sha256,m.protocol_sha256));features=Q.features;info=Q.info;metadata=Q.metadata;reused=reused+1;
   else
    before=rng;[a,info]=v1_bout_features(signal,time);a.n_bursts=ieeg_count_bursts(signal,time,info.options);features=a;
    c=ieeg_comparators(signal,2000,"ieeg","ieeg_A2_prime",.5);
    for k=1:4,z=c(k);assert(z.status==0&&isfinite(z.score),'IEEG:ComparatorFailure','Comparator returned invalid score');features(end+1)=struct('method',z.method,'fP_hz',z.fp,'fA_hz',z.fa,'score',z.score,'raw_mvl',z.raw_mvl,'ozkurt_mvl',z.ozkurt_mvl,'preferred_phase_deg',z.preferred_phase_deg,'status',z.status,'route',"not_applicable",'effective_half_width_hz',12,'n_bursts',NaN);end %#ok<AGROW>
    assert(isequal(before,rng),'IEEG:RNGChanged','Deterministic methods changed RNG');[unitPhase,amplitude]=ieeg_selected_series(signal,time,features,info);
    metadata=struct('patient',u.patient,'session',u.session,'trial',u.trial,'signal_type',u.signal_type,'native_fs_hz',u.native_fs_hz,'analysis_fs_hz',2000,'candidate_index',candidate,'git_head',m.git_head,'protocol_sha256',m.protocol_sha256,'seed',20261023,'matlab_version',version,'apc_options',info.options,'comparator_settings',m.comparator_settings,'source_file',D.metadata.source_file,'preprocessed_cache_file',u.cache_file,'analysis_provenance_file','analysis_provenance.json');
    save(file,'features','info','metadata','unitPhase','amplitude','-v7');computed=computed+1;
   end
   aliases=J(J.trial==u.trial&J.signal_type==u.signal_type,:);rows={};
   for ai=1:height(aliases)
    q=aliases(ai,:);
    for k=1:5
     z=features(k);fpLow=z.fP_hz==2;fpHigh=z.fP_hz==12;faHigh=z.fA_hz==148;if k==1,fpLow=abs(z.fP_hz-1)<=.05;fpHigh=abs(z.fP_hz-30)<=.05;faHigh=z.fA_hz==150;end
     rows{end+1}=struct('analysis',q.analysis,'patient',q.patient,'session',q.session,'trial',q.trial,'SetSize',q.SetSize,'Correct',q.Correct,'method',z.method,'fP_hz',z.fP_hz,'fA_hz',z.fA_hz,'score',z.score,'raw_mvl',z.raw_mvl,'ozkurt_mvl',z.ozkurt_mvl,'preferred_phase_deg',z.preferred_phase_deg,'status',z.status,'route',z.route,'n_bursts',z.n_bursts,'effective_half_width_hz',z.effective_half_width_hz,'boundary_fp_low',fpLow,'boundary_fp_high',fpHigh,'boundary_fa_low',z.fA_hz==80,'boundary_fa_high',faHigh,'native_fs_hz',q.native_fs_hz,'checkpoint_file',string(file),'git_head',string(m.git_head),'protocol_sha256',string(m.protocol_sha256),'seed',20261023,'matlab_version',string(version),'provenance_json',string(jsonencode(metadata))); %#ok<AGROW>
    end
   end
   T=struct2table(vertcat(rows{:}));if isfile(csv),writetable(T,csv,'WriteMode','append');else,writetable(T,csv);end;append_shared(T,fullfile(out,'ieeg_trial_estimates.csv'));rowsWritten=rowsWritten+height(T);
   if mod(ui,10)==0||ui==height(U),fprintf('IEEG worker%d %s %d/%d saved status%d\n',worker,key,ui,height(U),features(1).status);end
  end
  fprintf('IEEG worker%d SESSION COMPLETE %s\n',worker,key);
 end
 guards=final_sos_filter('registry');if ~isempty(guards),G=struct2table(guards);G.provenance_json=repmat(string(jsonencode(m)),height(G),1);writetable(G,fullfile(out,sprintf('filter_guards_worker%d.csv',worker)));end
 writejson(fullfile(out,sprintf('worker%d_runtime.json',worker)),struct('status','COMPLETE','elapsed_seconds',toc(start),'rows',rowsWritten,'computed_inputs',computed,'reused_inputs',reused,'worker',worker,'provenance',m));
catch err
 failure=struct('status','FAILED_STOP','identifier',err.identifier,'message',err.message,'worker',worker,'computed_inputs',computed,'rows_written',rowsWritten,'elapsed_seconds',toc(start),'provenance',m);writejson(fullfile(out,sprintf('worker%d_runtime.json',worker)),failure);writejson(fullfile(out,'METHOD_STOP_FLAG.json'),failure);rethrow(err);
end
end
function writejson(path,s)
f=fopen(path,'w','n','UTF-8');assert(f~=-1);clean=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(s));
end
function append_shared(T,path)
lock=java.io.File([path '.lock']);start=tic;
while ~lock.createNewFile(),assert(toc(start)<120,'IEEG:CSVLockTimeout','Incremental CSV lock timed out');pause(.1);end
cleanup=onCleanup(@()lock.delete()); %#ok<NASGU>
if isfile(path),writetable(T,path,'WriteMode','append');else,writetable(T,path);end
end
