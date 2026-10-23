function run_v2_units(outDir)
% Sequential prespecified gates; never generate held-out data in this driver.
A=fileparts(mfilename('fullpath'));repo=fileparts(fileparts(A));root=fileparts(repo);
base=fullfile(root,'revision_checks','v2');
if nargin<1,outDir=fullfile(base,'candidate_03','unit_attempt_01');end
assert(~isfolder(outDir),'v2:ExistingAttempt','Preserve existing attempts');mkdir(outDir);
oldPath=path;oldDir=pwd;oldRng=rng;oldThreads=maxNumCompThreads(1);
cleanup=onCleanup(@() restore(oldPath,oldDir,oldRng,oldThreads)); %#ok<NASGU>
cd(outDir);addpath(fullfile(repo,'analysis','v1_revision'),'-begin');addpath(base,'-begin');addpath(A,'-begin');addpath(fullfile(repo,'src'),'-begin');
assert(strcmpi(strrep(which('bst_apc'),'/','\'),strrep(fullfile(repo,'src','bst_apc.m'),'/','\')));
assert(strcmp(git(repo,'branch --show-current'),'v2-revision'));
% Candidate 3 is tested before the user-authorized conditional commit/tag.
workingStatus=git(repo,'status --porcelain');
assert(strcmp(fileread(fullfile(base,'PROTOCOL_v2.md')),fileread(fullfile(A,'PROTOCOL_v2.md'))));
preset=v1_options();options=preset(1).options;options.version='v2';options.fA=[80 160];
options.eventSurrogateSeed=20260619;options.eventSurrogateSubstream=2;
metadata=struct('candidate',3,'git_commit',git(repo,'rev-parse HEAD'),'git_worktree_status',workingStatus, ...
 'source_committed',isempty(workingStatus),'tag','not_created','matlab_version',version, ...
 'signal_seed',20260618,'heldout_seed',20261022,'heldout_generated',false,'apc_options',options, ...
 'comparator_settings',struct('phase_grid_hz',3:.5:14,'phase_half_width_hz',1.5,'amplitude_grid_hz',80:4:160, ...
 'A2_prime_half_width_hz',14,'A1_prime_half_width','candidate fP','metrics',{{'MVL-raw','MVL-Ozkurt','KLMI','GLM'}}), ...
 'base_tag','v1.0','base_commit',git(repo,'rev-list -n 1 v1.0'),'apc_source_blob',git(repo,'hash-object src/bst_apc.m'), ...
 'protocol_git_blob',git(repo,'hash-object analysis/v2_revision/PROTOCOL_v2.md'), ...
 'unit_profile',v2_unit_generator('profile'),'surrogate_generator','mrg32k3a','surrogate_seed',20260619,'surrogate_substream',2, ...
 'unit_poisson_seeds',20260618:20260627,'unit_poisson_generator','mrg32k3a','unit_poisson_substream',3, ...
 'uncoupled_phase_seed',20260619,'uncoupled_phase_generator','mrg32k3a','uncoupled_phase_substream',1,'repository',repo);
snapshot=fullfile(outDir,'source_snapshot');mkdir(snapshot);
copyfile(fullfile(repo,'src','bst_apc.m'),fullfile(snapshot,'bst_apc.m'));
copyfile(fullfile(A,'PROTOCOL_v2.md'),fullfile(snapshot,'PROTOCOL_v2.md'));
copyfile(fullfile(A,'run_v2_units.m'),fullfile(snapshot,'run_v2_units.m'));
copyfile(fullfile(A,'v2_unit_generator.m'),fullfile(snapshot,'v2_unit_generator.m'));
start=tic;rows={};gates=struct('a','NOT_RUN','a2','NOT_RUN','b','NOT_RUN','c','NOT_RUN','d','NOT_RUN');
fprintf('BEGIN v2 unit gates commit %s %s\n',metadata.git_commit,char(datetime('now')));
try
 % Preserve five independent v1 output structures exactly.
 bank=fullfile(root,'revision_checks','v1_rerun');saved=load(fullfile(bank,'main_distractor_level_0.mat'),'cases');
 for ir=1:5
  c=saved.cases{ir};before=rng;
  [r,i]=bst_apc(struct('data',c.signal,'time',c.time),preset(1).options);
  [reference,ri]=v2_v1_reference(struct('data',c.signal,'time',c.time),preset(1).options);
  assert(isequaln(r,reference)&&isequaln(i,ri),'v2:V1Changed','v1 output changed');assert(isequal(before,rng));
 end
 write_json(fullfile(outDir,'v1_compatibility.json'),struct('passed',true,'exact_trials',5,'metadata',metadata));
 cfg=v2_unit_generator('profile');rng(20260618,'twister');
 [signal,time,parts]=v2_unit_generator('generate',cfg,0);input=struct('signal',signal,'time',time,'parts',parts,'cfg',cfg);
 before=rng;[r,info]=bst_apc(struct('data',signal,'time',time),options);assert(isequal(before,rng),'v2:GlobalRNG','v2 consumed simulation RNG');
 % Independent mathematical and code-path invariants, before performance.
 d=info.diagnostics{1};x=signal-mean(signal);fs=1/median(diff(time));
 fb=cwtfilterbank('SignalLength',numel(x),'SamplingFrequency',fs,'FrequencyLimits',[80 160],'TimeBandwidth',5);
 cfs=cwt(x,'FilterBank',fb);trace=smoothdata(sqrt(mean(abs(cfs).^2,1)),'movmean',max(3,round(.02*fs)));
 [~,locs]=findpeaks(trace,'MinPeakDistance',max(1,round(.9*fs/80)),'MinPeakProminence',.75*std(trace,0,2));
 assert(isequal(trace,d.burst_trace)&&isequal(locs,d.burst_locations),'v2:StepOneChanged','Burst trace/detector differs from v1 definition');
 if double(r.status_code.Value(1))==0
  phases=d.observed_burst_phases;cosines=cos(phases(:)-phases(:).');n=numel(phases);
  independent=(sum(cosines,'all')-n)/(n*(n-1));
  assert(abs(independent-double(r.event_ppc.Value(1)))<1e-12,'v2:PPCFormula','PPC differs from pairwise-cosine definition');
  offsets=round(d.burstlock_relative_time*fs);usable=round(1+(d.usable_burst_times_s-time(1))*fs);
  segments=x(usable(:)+offsets);segments=segments-mean(segments,2);
  basis=exp(-1i*2*pi*d.burstlock_relative_time(:)*d.phase_grid_hz);
  explicit=(segments.*hann(numel(offsets),'symmetric').')*basis;
  n=size(explicit,1);expectedBLP=(abs(sum(explicit,1)).^2-sum(abs(explicit).^2,1))/(n*(n-1));
  assert(max(abs(expectedBLP-d.blp_grid))<=1e-8+1e-10*max(abs(expectedBLP)),'v2:BLPFormula','BLP differs from direct coefficients');
  query=d.first_surrogate_centers(:)+offsets;surrogateSegments=interp1(1:numel(x),x,query,'linear');
  surrogateSegments=surrogateSegments-mean(surrogateSegments,2);
  explicitSurrogate=(surrogateSegments.*hann(numel(offsets),'symmetric').')*basis;
  expectedSurrogateBLP=(abs(sum(explicitSurrogate,1)).^2-sum(abs(explicitSurrogate).^2,1))/(n*(n-1));
  assert(max(abs(expectedSurrogateBLP-d.first_surrogate_blp_grid))<=1e-8+1e-10*max(abs(expectedSurrogateBLP)),'v2:SurrogateDirect','Batched surrogate differs from direct extraction');
  assert(double(r.event_statistic.Value(1))==max(d.blp_grid));
  assert(double(r.event_p.Value(1))==(1+sum(d.surrogate_blp_max>=max(d.blp_grid)))/201);
  baseline=load(fullfile(base,'candidate_02','unit_attempt_01','unit_a.mat'),'r','info','input');
  assert(isequal(signal,baseline.input.signal)&&isequal(time,baseline.input.time),'v2:UnitProfileChanged','Unit a input changed');
  unchanged=setdiff(fieldnames(r),{'pac_strength','amplitude_frequency_hz','preferred_phase_deg','ozkurt_mvl'});
  for k=1:numel(unchanged),assert(isequaln(r.(unchanged{k}),baseline.r.(unchanged{k})),'v2:Candidate2Changed','Step 2/event output changed');end
  assert(isequaln(d.blp_grid,baseline.info.diagnostics{1}.blp_grid)&&isequaln(d.ppc_grid,baseline.info.diagnostics{1}.ppc_grid));
  assert(isequaln(d.surrogate_blp_max,baseline.info.diagnostics{1}.surrogate_blp_max)&&isequaln(d.surrogate_blp_fixed,baseline.info.diagnostics{1}.surrogate_blp_fixed));
  pad=round(fs);padded=[x(pad+1:-1:2),x,x(end-1:-1:end-pad)];nfft=numel(padded);
  bins=0:nfft-1;bins(bins>floor(nfft/2))=bins(bins>floor(nfft/2))-nfft;freqs=bins*fs/nfft;
  center=double(r.amplitude_frequency_hz.Value(1));sigma=1.5*double(r.phase_frequency_hz.Value(1));
  gain=zeros(size(freqs));positive=freqs>0;gain(positive)=2*exp(-.5*((freqs(positive)-center)/sigma).^2);
  analytic=ifft(fft(padded).*gain);envelope=abs(analytic(pad+(1:numel(x))));
  assert(max(abs(envelope-d.amplitude_envelope))<1e-12,'v2:GaussianFormula','Gaussian differs from literal FFT formula');
  assert(abs(abs(mean(envelope.*exp(1i*d.final_phase)))-double(r.pac_strength.Value(1)))<1e-12);
  p=options;p.phaseEpochCycles=100;[forced,forcedInfo]=bst_apc(struct('data',signal,'time',time),p);
  assert(bitand(double(forced.diagnostic_flags.Value(1)),4)>0,'v2:DiagnosticGuard','Forced profile failure did not warn');
  names=fieldnames(r);for k=1:numel(names),if ~strcmp(names{k},'diagnostic_flags'),assert(isequaln(r.(names{k}),forced.(names{k})),'v2:DiagnosticLeak','Diagnostic failure changed estimate');end,end
  p=options;p.flipTroughs=false;flipped=bst_apc(struct('data',signal,'time',time),p);
  assert(isequaln(r,flipped),'v2:FlipLeak','Display flip changed estimates');
  assert(isequal(before,rng)); %#ok<NASGU>
 end
 write_json(fullfile(outDir,'implementation_checks.json'),struct('passed',true,'step1_identical',true,'ppc_pairwise_identity_checked',double(r.status_code.Value(1))==0, ...
  'direct_blp_identity_checked',double(r.status_code.Value(1))==0,'surrogate_direct_identity_checked',double(r.status_code.Value(1))==0, ...
  'step2_event_exact_candidate2',double(r.status_code.Value(1))==0,'gaussian_formula_checked',double(r.status_code.Value(1))==0, ...
  'global_rng_unchanged',true,'diagnostic_failure_isolated',double(r.status_code.Value(1))==0,'flip_isolated',double(r.status_code.Value(1))==0,'metadata',metadata));
 pass=double(r.status_code.Value(1))==0 && abs(double(r.phase_frequency_hz.Value(1))-8)<=.1 && abs(double(r.amplitude_frequency_hz.Value(1))-120)<=4;
 row=pack('a',1,20260618,r,info,cfg,pass,metadata);rows{end+1}=row;
 save(fullfile(outDir,'unit_a.mat'),'input','r','info','metadata','-v7.3');write_curve(outDir,'a',info,metadata,20260618,8,120);
 gates.a=label(pass);fprintf('UNIT a %s fP %.17g fA %.17g\n',gates.a,row.recovered_fp_hz,row.recovered_fa_hz);
 if ~pass,finish(outDir,rows,gates,metadata,start,'a');return;end

 % (a2) New precision gate; all other profile fields/seeds unchanged.
 precisionValues=[5.3 6.7 9.4 10.8];precisionCarriers=[95 108 131 142];precisionCases=cell(1,4);
 for ir=1:4
  precisionCfg=cfg;precisionCfg.true_fp_hz=precisionValues(ir);precisionCfg.true_fa_hz=precisionCarriers(ir);rng(20260618,'twister');
  [precisionSignal,precisionTime,precisionParts]=v2_unit_generator('generate',precisionCfg,0);before=rng;
  [precisionResult,precisionInfo]=bst_apc(struct('data',precisionSignal,'time',precisionTime),options);assert(isequal(before,rng));
  pass=double(precisionResult.status_code.Value(1))==0 && abs(double(precisionResult.phase_frequency_hz.Value(1))-precisionValues(ir))<=.1 && abs(double(precisionResult.amplitude_frequency_hz.Value(1))-precisionCarriers(ir))<=4;
  rows{end+1}=pack('a2',ir,20260618,precisionResult,precisionInfo,precisionCfg,pass,metadata); %#ok<AGROW>
  precisionCases{ir}=struct('signal',precisionSignal,'time',precisionTime,'parts',precisionParts,'cfg',precisionCfg,'r',precisionResult,'info',precisionInfo);
  write_curve(outDir,sprintf('a2_%02d',ir),precisionInfo,metadata,20260618,precisionValues(ir),precisionCarriers(ir));
  fprintf('UNIT a2 true(%.17g,%.17g) %s fP %.17g fA %.17g\n',precisionValues(ir),precisionCarriers(ir),label(pass),double(precisionResult.phase_frequency_hz.Value(1)),double(precisionResult.amplitude_frequency_hz.Value(1)));
  save(fullfile(outDir,'unit_a2.mat'),'precisionCases','metadata','-v7.3');
  if ~pass,gates.a2='FAIL';finish(outDir,rows,gates,metadata,start,'a2');return;end
 end
 gates.a2='PASS';

 % (b) Same carrier, bursts and noise; independently phased 11-Hz sine.
 phaseStream=RandStream('mrg32k3a','Seed',20260619);phaseStream.Substream=1;phi=2*pi*rand(phaseStream);
 bSignal=signal+3*sin(2*pi*11*time+phi);before=rng;[r,info]=bst_apc(struct('data',bSignal,'time',time),options);assert(isequal(before,rng));
 pass=double(r.status_code.Value(1))==0 && abs(double(r.phase_frequency_hz.Value(1))-8)<=.5;
 recordCfg=cfg;recordCfg.slow_amplitude_ratio=3;recordCfg.slow_distractor_phase_rad=phi;
 row=pack('b',1,20260618,r,info,recordCfg,pass,metadata);rows{end+1}=row;
 save(fullfile(outDir,'unit_b.mat'),'bSignal','time','r','info','metadata','recordCfg','-v7.3');write_curve(outDir,'b',info,metadata,20260618,8,120);
 gates.b=label(pass);fprintf('UNIT b %s fP %.17g fA %.17g\n',gates.b,row.recovered_fp_hz,row.recovered_fa_hz);
 if ~pass,finish(outDir,rows,gates,metadata,start,'b');return;end

 % (c) Ten fixed seeds, no choice after seeing p-values.
 nullCount=0;cases=cell(1,10);
 for ir=1:10
  seed=20260618+ir-1;rng(seed,'twister');[coupled,time,parts]=v2_unit_generator('generate',cfg,0);
  stream=RandStream('mrg32k3a','Seed',seed);stream.Substream=3;
  times=poisson_times(stream,8,time(1)-1/8,time(end)+1/8);env=zeros(size(time));
  for k=1:numel(times),env=env+exp(-.5*((time-times(k))/cfg.burst_sigma_s).^2);end
  if max(env)>0,env=env/max(env);end
  newTrue=cfg.true_high_amp*cfg.coupling_level*env.*parts.carrier;
  null=coupled-parts.true_component+newTrue;
  residual=max(abs((coupled-null)-(parts.true_component-newTrue)));assert(residual<=1e-12,'v2:NullPair','Null changes other components');
  opt=options;opt.eventSurrogateSeed=seed+1;before=rng;[r,info]=bst_apc(struct('data',null,'time',time),opt);assert(isequal(before,rng));
  pass=double(r.status_code.Value(1))==0 && double(r.event_p.Value(1))>.05;nullCount=nullCount+pass;
  rows{end+1}=pack('c',ir,seed,r,info,cfg,pass,metadata); %#ok<AGROW>
  write_curve(outDir,sprintf('c_%02d',ir),info,metadata,seed,8,120);
  cases{ir}=struct('coupled',coupled,'null',null,'time',time,'parts',parts,'poisson_times',times,'new_true_component',newTrue, ...
   'pair_residual',residual,'result',r,'info',info,'cfg',cfg);
  fprintf('UNIT c seed%d p %.17g status%d\n',seed,double(r.event_p.Value(1)),double(r.status_code.Value(1)));
 end
 save(fullfile(outDir,'unit_c.mat'),'cases','metadata','-v7.3');gates.c=label(nullCount>=8);
 fprintf('UNIT c %s p>.05 %d/10\n',gates.c,nullCount);
 if nullCount<8,finish(outDir,rows,gates,metadata,start,'c');return;end

 % (d) Existing first 25 distractor inputs; no held-out data.
 oldCases=saved.cases;cases=cell(1,25);
 for ir=1:25
  c=oldCases{ir};before=rng;[r,info]=bst_apc(struct('data',c.signal,'time',c.time),options);assert(isequal(before,rng));
  rows{end+1}=pack('d',ir,20260618,r,info,c.cfg,double(r.status_code.Value(1))==0,metadata); %#ok<AGROW>
  write_curve(outDir,sprintf('d_%02d',ir),info,metadata,20260618,8,120);
  cases{ir}=struct('input',c,'result',r,'info',info);
  fprintf('UNIT d %d/25 status%d fP %.6g fA %.6g\n',ir,double(r.status_code.Value(1)),double(r.phase_frequency_hz.Value(1)),double(r.amplitude_frequency_hz.Value(1)));
 end
 save(fullfile(outDir,'unit_d.mat'),'cases','metadata','-v7.3');gates.d='COMPLETE';finish(outDir,rows,gates,metadata,start,'');
catch err
 result=struct('status','EXECUTION_FAILURE','gates',gates,'elapsed_seconds',toc(start),'error_identifier',err.identifier,'error_message',err.message,'metadata',metadata);
 if ~isempty(rows),v1_write_csv(struct2table([rows{:}]),fullfile(outDir,'unit_trials.csv'));end
 write_json(fullfile(outDir,'unit_results.json'),result);rethrow(err);
end
end

function row=pack(test,ir,seed,r,info,cfg,passed,metadata)
row=struct('test',string(test),'trial_index',ir,'seed',seed,'true_fp_hz',cfg.true_fp_hz,'true_fa_hz',cfg.true_fa_hz, ...
 'recovered_fp_hz',double(r.phase_frequency_hz.Value(1)),'recovered_fa_hz',double(r.amplitude_frequency_hz.Value(1)), ...
 'C_APC',double(r.pac_strength.Value(1)),'ozkurt_mvl',double(r.ozkurt_mvl.Value(1)), ...
 'event_ppc',double(r.event_ppc.Value(1)),'event_z',double(r.event_z.Value(1)),'event_p',double(r.event_p.Value(1)), ...
 'event_blp',double(r.event_blp.Value(1)),'event_statistic',double(r.event_statistic.Value(1)), ...
 'event_z_fixed',double(r.event_z_fixed.Value(1)),'event_p_fixed',double(r.event_p_fixed.Value(1)), ...
 'burst_count',double(r.burst_count.Value(1)),'usable_burst_count',double(r.n_usable_bursts.Value(1)), ...
 'diagnostic_flags',double(r.diagnostic_flags.Value(1)),'status',double(r.status_code.Value(1)),'passed',passed, ...
 'surrogate_seed',info.surrogate_seed(1),'surrogate_substream',info.surrogate_substream(1), ...
 'git_commit',string(metadata.git_commit),'apc_source_blob',string(metadata.apc_source_blob),'source_committed',metadata.source_committed, ...
 'matlab_version',string(version),'apc_options_json',string(jsonencode(info.options)), ...
 'comparator_settings_json',string(jsonencode(metadata.comparator_settings)),'generator_settings_json',string(jsonencode(cfg)));
end
function finish(out,rows,gates,metadata,start,failed)
assert(strcmp(git(metadata.repository,'hash-object src/bst_apc.m'),metadata.apc_source_blob),'v2:SourceChanged','Method source changed during unit tests');
status='UNIT_GATES_PASSED';if ~isempty(failed),status='STOP_UNIT_GATE';end
T=struct2table([rows{:}]);v1_write_csv(T,fullfile(out,'unit_trials.csv'));
result=struct('status',status,'failed_gate',failed,'gates',gates,'elapsed_seconds',toc(start), ...
 'heldout_generated',false,'implementation_bug_fixes',{{}},'tooling_deviations',{{}},'metadata',metadata);
write_json(fullfile(out,'unit_results.json'),result);fprintf('%s failed_gate=%s %.3f seconds\n',status,failed,toc(start));
end
function write_curve(out,name,info,metadata,seed,trueFp,trueFa)
d=info.diagnostics{1};n=numel(d.phase_grid_hz);
T=table(d.phase_grid_hz(:),d.blp_grid(:),d.ppc_grid(:),d.usable_count_grid(:),'VariableNames',{'candidate_fP_hz','BLP','PPC','usable_bursts'});
T.git_commit=repmat(string(metadata.git_commit),n,1);T.apc_source_blob=repmat(string(metadata.apc_source_blob),n,1);
T.matlab_version=repmat(string(version),n,1);T.seed=repmat(seed,n,1);T.true_fp_hz=repmat(trueFp,n,1);
T.apc_options_json=repmat(string(jsonencode(info.options)),n,1);T.comparator_settings_json=repmat(string(jsonencode(metadata.comparator_settings)),n,1);
v1_write_csv(T,fullfile(out,['unit_' name '_curves.csv']));
centers=d.amplitude_grid_hz(:);scores=d.amplitude_scores_raw(:);reached=~isempty(centers);
if ~reached,centers=(info.options.fA(1):1:info.options.fA(2)).';scores=nan(size(centers));end
na=numel(centers);S=table(centers,scores,'VariableNames',{'candidate_fA_hz','raw_MVL'});
S.step4_reached=repmat(reached,na,1);S.gaussian_sigma_hz=repmat(d.amplitude_gaussian_sigma_hz,na,1);
S.git_commit=repmat(string(metadata.git_commit),na,1);S.apc_source_blob=repmat(string(metadata.apc_source_blob),na,1);
S.matlab_version=repmat(string(version),na,1);S.seed=repmat(seed,na,1);S.true_fp_hz=repmat(trueFp,na,1);S.true_fa_hz=repmat(trueFa,na,1);
S.apc_options_json=repmat(string(jsonencode(info.options)),na,1);S.comparator_settings_json=repmat(string(jsonencode(metadata.comparator_settings)),na,1);
v1_write_csv(S,fullfile(out,['unit_' name '_fa_scores.csv']));
end
function s=label(p)
if p,s='PASS';else,s='FAIL';end
end
function times=poisson_times(stream,rate,low,high)
times=[];t=low;while true,t=t-log(max(rand(stream),realmin))/rate;if t>high,break;end;times(end+1)=t;end %#ok<AGROW>
end
function s=git(repo,args)
exe='C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe';
[status,s]=system(sprintf('"%s" -C "%s" %s',exe,repo,args));assert(status==0);s=strtrim(s);
end
function write_json(file,value)
f=fopen(file,'w','n','UTF-8');assert(f>=0);c=onCleanup(@() fclose(f)); %#ok<NASGU>
fprintf(f,'%s',jsonencode(value,'PrettyPrint',true));
end
function restore(p,d,r,t)
path(p);cd(d);rng(r);maxNumCompThreads(t);
end
