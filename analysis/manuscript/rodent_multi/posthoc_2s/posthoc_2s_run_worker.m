% POST HOC 2-s sensitivity; frozen method helpers unchanged.
function posthoc_2s_run_worker(worker,totalWorkers)
out=fileparts(mfilename('fullpath'));parent=fileparts(out);root=fileparts(fileparts(parent));start=tic;
stage=jsondecode(fileread(fullfile(out,'posthoc_2s_behavior_runtime.json')));assert(strcmp(stage.status,'COMPLETE'),'Rodent:IncompleteBehavior','Regional behavior incomplete');
xml=jsondecode(fileread(fullfile(parent,'regional_xml_grouping.json')));assert(xml.contiguous_eight_channel_blocks,'Rodent:XMLGate','Noncontiguous anatomical groups');
prior=fullfile(root,'revision_checks','final');addpath(prior,'-begin');addpath(fullfile(prior,'frozen_v1'),'-begin');addpath(parent,'-begin');addpath(out,'-begin');
cd(out);clear bst_apc calc_MI_all_methods;
assert(strcmpi(which('bst_apc'),fullfile(prior,'frozen_v1','bst_apc.m')),'Rodent:MethodPath','Frozen APC path was not selected');
assert(strcmpi(which('calc_MI_all_methods'),fullfile(prior,'frozen_v1','calc_MI_all_methods.m')),'Rodent:MetricPath','Frozen metric path was not selected');
oldThreads=maxNumCompThreads(1);cleanup=onCleanup(@()maxNumCompThreads(oldThreads)); %#ok<NASGU>
selection=readtable(fullfile(out,'posthoc_2s_session_eligibility.csv'),'TextType','string','Delimiter',',','NumHeaderLines',0,'ReadVariableNames',true,'VariableNamingRule','preserve','Encoding','UTF-8');selection=selection(ismember(lower(string(selection.included)),["true","1"]),:);
bouts=readtable(fullfile(out,'posthoc_2s_bouts.csv'),'TextType','string','Delimiter',',','NumHeaderLines',0,'ReadVariableNames',true,'VariableNamingRule','preserve','Encoding','UTF-8');protocol=jsondecode(fileread(fullfile(out,'posthoc_2s_provenance.json')));tables={};rng(20261022,'twister');
try
 sessions=unique(selection.session,'stable');
 for is=worker:totalWorkers:numel(sessions)
  session=sessions(is);selected=selection(selection.session==session,:);q=selected(1,:);bb=bouts(bouts.session==session,:);
  if session=="ec013.157",S=load(q.source_file,'test');record=S.test;else,record=load(q.source_file,'F','Time');end
  channels=unique(selected.channel_index,'stable');
  for ic=1:numel(channels)
   ch=channels(ic);choices=selected(selected.channel_index==ch,:);
   for ib=1:height(bb)
    b=bb(ib,:);file=fullfile(out,sprintf('posthoc_2s_%s_E%d_%s_%04d_pac.mat',session,ch,b.state,b.bout));
    if isfile(file)
     P=load(file,'features','info','metadata');features=P.features;info=P.info;metadata=P.metadata;
     assert(strcmp(metadata.posthoc_protocol_sha256,protocol.posthoc_protocol_sha256)&&metadata.start_idx==b.lfp_start_idx&&metadata.stop_idx==b.lfp_stop_idx,'Rodent:CacheProtocol','POST HOC cache mismatch');
    else
     ix=b.lfp_start_idx:b.lfp_stop_idx;time=double(record.Time(ix));signal=double(record.F(ch,ix));fs=1/median(diff(time));before=rng;
     [apc,info]=v1_bout_features(signal,time);assert(isequal(before,rng),'Rodent:RNG','Frozen APC changed RNG');features=apc;
     c=sos_comparators(signal,fs,"rodent","rodent_A2_prime",.5);
     for m=1:numel(c)
      z=c(m);assert(z.status==0,'Rodent:ComparatorFailure','Invalid comparator output');
      features(end+1)=struct('method',z.method,'fP_hz',z.fp,'fA_hz',z.fa,'score',z.score,'raw_mvl',z.raw_mvl,'ozkurt_mvl',z.ozkurt_mvl,'preferred_phase_deg',z.preferred_phase_deg,'status',z.status,'route',"not_applicable",'effective_half_width_hz',12); %#ok<AGROW>
     end
     assert(isequal(before,rng),'Rodent:RNG','Comparator changed RNG');
     metadata=struct('analysis_type',protocol.analysis_type,'post_hoc',true,'minimum_bout_s',2,'posthoc_protocol_sha256',protocol.posthoc_protocol_sha256,'worker',worker,'git_tag','v1.0','git_commit',protocol.git_commit,'matlab_version',version,'seed',20261022,'protocol_sha256',protocol.protocol_sha256,'execution_sha256',protocol.execution_sha256,'apc_options',info.options, ...
       'source_file',q.source_file,'session',session,'channel_index',ch,'state',b.state,'bout',b.bout,'start_idx',b.lfp_start_idx,'stop_idx',b.lfp_stop_idx,'tracking_start',b.start_time_s,'tracking_stop_exclusive',b.stop_exclusive_s, ...
       'mapping_evidence',choices.mapping_evidence(1),'region',choices.region(1),'shank',choices.shank(1), ...
       'comparators',struct('phase_grid',4:.5:12,'phase_half_width',1.5,'amplitude_grid',80:4:148,'amplitude_half_width',12,'filter','butter(4) zpk to SOS; filtfilt; pole and center gain guards','metrics',{{'MVL-raw','MVL-Ozkurt','KLMI','GLM'}}));
     save(file,'features','info','metadata','-v7');
    end
    for ia=1:height(choices)
     choice=choices(ia,:);metadata.analysis=choice.analysis;rows={};
     for m=1:numel(features)
      z=features(m);rows{end+1}=struct('analysis_type',protocol.analysis_type,'post_hoc',true,'minimum_bout_s',2,'animal',q.animal,'session',session,'analysis',choice.analysis,'channel_index',ch,'region',choice.region,'shank',choice.shank,'mapping_evidence',choice.mapping_evidence,'state',b.state,'bout',b.bout,'duration_s',b.duration_s,'lfp_duration_s',b.lfp_duration_s, ...
       'method',z.method,'fP_hz',z.fP_hz,'fA_hz',z.fA_hz,'score',z.score,'raw_mvl',z.raw_mvl,'ozkurt_mvl',z.ozkurt_mvl,'preferred_phase_deg',z.preferred_phase_deg,'status',z.status,'route',z.route,'effective_half_width_hz',z.effective_half_width_hz, ...
       'boundary_fP_4',z.fP_hz==4,'boundary_fP_12',z.fP_hz==12,'git_commit',string(protocol.git_commit),'matlab_version',string(version),'seed',20261022,'provenance_json',string(jsonencode(metadata))); %#ok<AGROW>
     end
     tables{end+1}=struct2table([rows{:}]); %#ok<AGROW>
    end
    if mod(ib,10)==0||ib==height(bb),fprintf('POST HOC worker%d %s E%d %s %d/%d status%d\n',worker,session,ch,b.state,ib,height(bb),features(1).status);end
   end
  end
  T=vertcat(tables{:});writetable(T,fullfile(out,sprintf('posthoc_2s_worker%d_progress.csv',worker)));
  clear record S;
 end
 T=vertcat(tables{:});writetable(T,fullfile(out,sprintf('posthoc_2s_worker%d_estimates.csv',worker)));
 guards=final_sos_filter('registry');G=struct2table(guards);G.provenance_json=repmat(string(jsonencode(protocol)),height(G),1);writetable(G,fullfile(out,sprintf('posthoc_2s_worker%d_filter_guards.csv',worker)));
 status=struct('analysis_type',protocol.analysis_type,'post_hoc',true,'worker',worker,'status','COMPLETE','elapsed_seconds',toc(start),'rows',height(T),'unique_input_checkpoints',numel(dir(fullfile(out,'posthoc_2s_*_pac.mat'))),'metadata',protocol,'matlab_version',version);writejson(fullfile(out,sprintf('posthoc_2s_worker%d_runtime.json',worker)),status);
catch err
 writejson(fullfile(out,sprintf('posthoc_2s_worker%d_runtime.json',worker)),struct('analysis_type',protocol.analysis_type,'post_hoc',true,'worker',worker,'status','FAILED_STOP','elapsed_seconds',toc(start),'identifier',err.identifier,'error',err.message,'metadata',protocol));rethrow(err);
end
end
function writejson(file,s)
f=fopen(file,'w','n','UTF-8');fprintf(f,'%s\n',jsonencode(s));fclose(f);
end
