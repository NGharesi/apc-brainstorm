function validation_hb_cases(out,meta,seed)
file=fullfile(out,'HB_inputs.mat');assert(~isfile(file),'v2:ExistingInputs','Preserve existing held-out inputs');
assert(~meta.tpac.available,'v2:TPACReview','Inspect available tPAC interface before deciding inclusion');
signalStream=new_stream(1,seed);frequencyStream=new_stream(2,seed);poissonStream=new_stream(3,seed);RandStream.setGlobalStream(signalStream);
cases={};verification={};draws={};
for scenario=["H1_sparsity","H1_distractor","H2","H4"]
 switch scenario
  case 'H1_sparsity',levels=[1 .55 .25 .15];cfg=v2_heldout_generator('sparsity_profile');generator='sparsity';
  case 'H1_distractor',levels=[0 1.5 3];cfg=v2_heldout_generator('distractor_profile');generator='distractor';
  case 'H2',levels=[0 .5 1 1.5 2 3];cfg=v2_heldout_generator('slow_profile');generator='slow';
  case 'H4',levels=0;cfg=v2_heldout_generator('distractor_profile');cfg.duration_s=12;cfg.continuous_modulation_depth=.70;cfg.continuous_high_amp=1.25;generator='continuous';
 end
 cfg.random_seed=seed;cfg.snr_db=-3;cfg.broad_fa_band_hz=[80 160];
 for level=levels
  for ir=1:25
   fd=nan;phi=nan;
   if scenario=="H2"
    cfg.true_fp_hz=4+3*rand(frequencyStream);fd=cfg.true_fp_hz+3+(13-cfg.true_fp_hz-3)*rand(frequencyStream);phi=2*pi*rand(frequencyStream);cfg.true_fa_hz=90+50*rand(frequencyStream);
    cfg.slow_distractor_hz=fd;cfg.slow_distractor_phase_rad=phi;cfg.slow_amplitude_ratio=level;
   else
    cfg.true_fp_hz=5+6*rand(frequencyStream);cfg.true_fa_hz=90+50*rand(frequencyStream);
    if scenario=="H1_distractor",cfg.distractor_fa_hz=cfg.true_fa_hz-24;end
   end
   before=signalStream.State;
   if scenario=="H4",[signal,time,parts]=v2_heldout_generator(generator,cfg);else,[signal,time,parts]=v2_heldout_generator(generator,cfg,level);end
   id=numel(cases)+1;c=struct('input_id',id,'paired_coupled_id',id,'scenario',scenario,'dataset',"coupled",'level',level,'repeat_index',ir, ...
    'signal',signal,'time',time,'parts',parts,'cfg',cfg,'true_fd_hz',fd,'distractor_phase_rad',phi,'signal_rng_state_before',before, ...
    'signal_rng_state_after',signalStream.State,'poisson_times',[],'removed_true_component',[],'added_true_component',[],'pair_residual',nan);
   cases{end+1}=c; %#ok<AGROW>
   draws{end+1}=struct('scenario',scenario,'level',level,'repeat_index',ir,'coupled_input_id',id,'true_fp_hz',cfg.true_fp_hz,'true_fa_hz',cfg.true_fa_hz,'true_fd_hz',fd,'distractor_phase_rad',phi, ...
    'git_commit',string(meta.git_commit),'matlab_version',string(version),'seed',seed,'apc_options_json',string(jsonencode(meta.apc_configurations)),'comparator_settings_json',string(jsonencode(meta.comparator_settings)),'generator_settings_json',string(jsonencode(cfg))); %#ok<AGROW>
   needTiming=startsWith(scenario,"H1") || (scenario=="H2" && ismember(level,[0 1 3]));
   if needTiming
    rate=cfg.true_fp_hz;if scenario=="H1_sparsity",rate=rate*level;end
    times=poisson_times(poissonStream,rate,time(1)-1/cfg.true_fp_hz,time(end)+1/cfg.true_fp_hz);
    env=zeros(size(time));for k=1:numel(times),env=env+exp(-.5*((time-times(k))/cfg.burst_sigma_s).^2);end
    if max(env)>0,env=env/max(env);end
    newTrue=cfg.true_high_amp*cfg.coupling_level*env.*parts.carrier;
    n=c;n.input_id=numel(cases)+1;n.dataset="timing_null";n.signal=signal-parts.true_component+newTrue;
    n.poisson_times=times;n.parts.true_component=newTrue;n.parts.true_envelope=env;n.removed_true_component=parts.true_component;n.added_true_component=newTrue;
    n.pair_residual=max(abs((c.signal-n.signal)-(parts.true_component-newTrue)));
    assert(n.pair_residual<=1e-12,'v2:NullPair','Timing null changes more than true burst');
    cases{end+1}=n;verification{end+1}=verification_row(n,meta); %#ok<AGROW>
   end
   needAbsent=(scenario=="H1_sparsity" && ismember(level,[1 .15])) || (scenario=="H1_distractor" && level==3);
   if needAbsent
    n=c;n.input_id=numel(cases)+1;n.dataset="no_coupled_burst";n.signal=signal-parts.true_component;n.cfg.coupling_level=0;
    n.parts.true_component=zeros(size(signal));n.removed_true_component=parts.true_component;n.added_true_component=zeros(size(signal));
    n.pair_residual=max(abs((c.signal-n.signal)-parts.true_component));assert(n.pair_residual<=1e-12,'v2:NullPair','Absent control changes other components');
    cases{end+1}=n;verification{end+1}=verification_row(n,meta); %#ok<AGROW>
   end
  end
  fprintf('GENERATED %s level%g 25 paired repeats; total inputs %d\n',scenario,level,numel(cases));
 end
end
assert(numel(cases)==675 && numel(draws)==350 && numel(verification)==325);
save(file,'cases','meta','-v7.3');v1_write_csv(struct2table([draws{:}]),fullfile(out,'HB_frequency_draws.csv'));
v1_write_csv(struct2table([verification{:}]),fullfile(out,'HB_null_pair_verification.csv'));
write_json(fullfile(out,'HB_input_manifest.json'),struct('inputs',675,'coupled',350,'timing_null',250,'no_coupled_burst',75,'metadata',meta));
end

function r=verification_row(c,meta)
r=struct('input_id',c.input_id,'paired_coupled_id',c.paired_coupled_id,'scenario',c.scenario,'dataset',c.dataset,'level',c.level,'repeat_index',c.repeat_index, ...
 'pair_residual',c.pair_residual,'poisson_events',numel(c.poisson_times),'git_commit',string(meta.git_commit),'matlab_version',string(version),'seed',seed, ...
 'apc_options_json',string(jsonencode(meta.apc_configurations)),'comparator_settings_json',string(jsonencode(meta.comparator_settings)),'generator_settings_json',string(jsonencode(c.cfg)));
end
function stream=new_stream(sub,seed)
stream=RandStream('mrg32k3a','Seed',seed);stream.Substream=sub;
end
function times=poisson_times(stream,rate,low,high)
times=[];t=low;while true,t=t-log(max(rand(stream),realmin))/rate;if t>high,break;end;times(end+1)=t;end %#ok<AGROW>
end
function write_json(file,value)
f=fopen(file,'w','n','UTF-8');assert(f>=0);c=onCleanup(@() fclose(f)); %#ok<NASGU>
fprintf(f,'%s',jsonencode(value,'PrettyPrint',true));
end