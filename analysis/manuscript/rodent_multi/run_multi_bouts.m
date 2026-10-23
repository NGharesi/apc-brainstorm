function run_multi_bouts
out=fileparts(mfilename('fullpath'));root=fileparts(fileparts(out));start=tic;
gate=jsondecode(fileread(fullfile(out,'chunked_behavior_validation.json')));assert(gate.passed,'Rodent:Gate','No analysis after failed gate');
behaviorStatus=jsondecode(fileread(fullfile(out,'multi_behavior_runtime.json')));assert(strcmp(behaviorStatus.status,'COMPLETE'),'Rodent:IncompleteBehavior','All behavior must finish first');
prior=fullfile(root,'revision_checks','final');addpath(prior,'-begin');addpath(fullfile(prior,'frozen_v1'),'-begin');addpath(out,'-begin');
oldThreads=maxNumCompThreads(1);cleanup=onCleanup(@()maxNumCompThreads(oldThreads)); %#ok<NASGU>
selection=readtable(fullfile(out,'selected_channels.csv'),'TextType','string');eligibility=readtable(fullfile(out,'session_bout_eligibility.csv'),'TextType','string');
protocol=jsondecode(fileread(fullfile(out,'protocol_amendments_record.json')));allRows={};rng(20261022,'twister');
try
 for j=1:height(selection)
  q=selection(j,:);eligible=eligibility.included(eligibility.session==q.session);if ~eligible,continue;end
  if q.session=="ec013.157",S=load(q.source_file,'test');record=S.test;else,record=load(q.source_file,'F','Time');end
  B=load(fullfile(out,char(q.session+"_behavior.mat")),'result');behavior=B.result;
  channels=q.channel_index;labels="theta_delta_primary";
  if q.animal=="EC013",channels=[channels 1];labels=[labels "E1_sensitivity"];end
  for c=1:numel(channels)
   for state=["run","rest"]
    bouts=behavior.(char(state+"_bouts"));
    for b=1:height(bouts)
     file=fullfile(out,sprintf('%s_%s_%s_%04d_pac.mat',q.session,labels(c),state,b));
     if isfile(file),P=load(file,'T');allRows{end+1}=P.T;continue;end %#ok<AGROW>
     ix=bouts.start_idx(b):bouts.stop_idx(b);time=double(record.Time(ix));signal=double(record.F(channels(c),ix));fs=1/median(diff(time));
     before=rng;[apc,info]=v1_bout_features(signal,time);assert(isequal(before,rng),'Rodent:RNG','Frozen APC changed RNG unexpectedly');
     meta=struct('git_tag','v1.0','git_commit','71ebc16aed32ca38be73a800738b975e5806b330','matlab_version',version,'seed',20261022,'protocol_sha256',protocol.protocol_sha256,'apc_options',info.options,'source_file',q.source_file,'session',q.session,'channel_index',channels(c),'state',state,'bout',b,'start_idx',ix(1),'stop_idx',ix(end),'comparators',struct('phase_grid',4:.5:12,'phase_half_width',1.5,'amplitude_grid',80:4:148,'amplitude_half_width',12,'filter','4th-order Butterworth zpk->SOS, zero-phase filtfilt, pole/gain guards'));
     rows={makeRow(apc,q,labels(c),channels(c),state,b,bouts.duration_s(b),meta)};
     comparators=sos_comparators(signal,fs,"rodent","rodent_A2_prime",.5);
     for m=1:numel(comparators)
      z=comparators(m);assert(z.status==0,'Rodent:ComparatorFailure','Invalid comparator score');
      r=struct('method',z.method,'fP_hz',z.fp,'fA_hz',z.fa,'score',z.score,'raw_mvl',z.raw_mvl,'ozkurt_mvl',z.ozkurt_mvl,'preferred_phase_deg',z.preferred_phase_deg,'status',z.status,'route',"not_applicable",'effective_half_width_hz',12);
      rows{end+1}=makeRow(r,q,labels(c),channels(c),state,b,bouts.duration_s(b),meta); %#ok<AGROW>
     end
     assert(isequal(before,rng),'Rodent:RNG','Comparator changed RNG');T=struct2table([rows{:}]);save(file,'T','info','meta','-v7');allRows{end+1}=T; %#ok<AGROW>
     fprintf('PAC %s %s %s %d/%d status%d\n',q.session,labels(c),state,b,height(bouts),apc.status);
    end
   end
  end
  clear record S B;
 end
 T=vertcat(allRows{:});writetable(T,fullfile(out,'bout_estimates.csv'));
 G=struct2table(final_sos_filter('registry'));G.provenance_json=repmat(string(jsonencode(protocol)),height(G),1);writetable(G,fullfile(out,'comparator_filter_guards.csv'));
 status=struct('status','COMPLETE','elapsed_seconds',toc(start),'rows',height(T),'metadata',protocol);
catch err
 status=struct('status','FAILED_STOP','elapsed_seconds',toc(start),'identifier',err.identifier,'error',err.message,'metadata',protocol);writejson(fullfile(out,'multi_bouts_runtime.json'),status);rethrow(err);
end
writejson(fullfile(out,'multi_bouts_runtime.json'),status);
end
function r=makeRow(z,q,analysis,ch,state,b,duration,meta)
r=struct('animal',q.animal,'session',q.session,'analysis',analysis,'channel_index',ch,'state',state,'bout',b,'duration_s',duration,'method',z.method,'fP_hz',z.fP_hz,'fA_hz',z.fA_hz,'score',z.score,'raw_mvl',z.raw_mvl,'ozkurt_mvl',z.ozkurt_mvl,'preferred_phase_deg',z.preferred_phase_deg,'status',z.status,'route',z.route,'effective_half_width_hz',z.effective_half_width_hz,'boundary_fP_4',z.fP_hz==4,'boundary_fP_12',z.fP_hz==12,'region',q.region,'shank',q.shank,'git_commit',string(meta.git_commit),'provenance_json',string(jsonencode(meta)));
end
function writejson(file,s)
f=fopen(file,'w','n','UTF-8');fprintf(f,'%s\n',jsonencode(s));fclose(f);
end
