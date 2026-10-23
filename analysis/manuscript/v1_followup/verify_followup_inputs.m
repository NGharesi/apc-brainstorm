function verify_followup_inputs()
% Independent saved-input checks for the newly generated scenario.
out=strrep(fileparts(mfilename('fullpath')),'/','\');root=fileparts(fileparts(out));
repo=fullfile(root,'apc-brainstorm-publish');addpath(fullfile(repo,'analysis','v1_revision'));
start=tic;rows={};
for ratio=[0 .5 1 1.5 2 3]
 file=fullfile(out,sprintf('slow_inputs_level_%g.mat',ratio));b=load(file,'cases','nullCases','metadata');metadata=b.metadata;
 for ir=1:25
  c=b.cases{ir};p=c.parts;cfg=c.cfg;t=c.time;
  low=cfg.low_amp*sin(2*pi*6*t);ten=ratio*cfg.low_amp*sin(2*pi*10*t+cfg.slow_distractor_phase_rad);
  base=cfg.base_hf_amp*sin(2*pi*120*t);env=zeros(size(t));
  for k=1:numel(p.true_event_times),env=env+exp(-.5*((t-p.true_event_times(k))/cfg.burst_sigma_s).^2);end
  if max(env)>0,env=env/max(env);end
  burst=cfg.true_high_amp*.6*env.*sin(2*pi*120*t);
  clean=low+base+burst+ten;
  residual=max(abs(c.signal-(clean+p.noise)));
  noiseSnr=10*log10(mean(clean.^2)/mean(p.noise.^2));
  assert(isequal(low,p.low_component) && isequal(ten,p.distractor_component));
  assert(isequal(base,p.base_carrier_component) && isequal(env,p.true_envelope) && isequal(burst,p.true_component));
  assert(residual<=1e-12 && abs(noiseSnr-cfg.snr_db)<=1e-10,'followup:InputQA','Saved signal/noise decomposition mismatch');
  nominal=((deg2rad(cfg.phase_offset_deg)+pi/2)/(2*pi*6))+(0:ceil(t(end)*6)+2)/6;
  nominal=nominal(nominal>=t(1)-1/6 & nominal<=t(end)+1/6);
  assert(numel(nominal)==numel(p.true_event_times));
  troughError=max(abs(sin(2*pi*6*nominal)+1));assert(troughError<=1e-12,'followup:NominalTrough','Nominal bursts are not at physical troughs');
  jitter=p.true_event_times-nominal;
  nullResidual=nan;count=nan;
  if ismember(ratio,[0 1 3])
   n=b.nullCases{ir};nullResidual=max(abs((c.signal-n.signal)-(p.true_component-n.new_true_component)));count=numel(n.poisson_times);
   assert(nullResidual<=1e-12,'followup:InputNullQA','Saved null changes more than true-burst component');
  end
  row=struct('ratio',ratio,'repeat_index',ir,'decomposition_residual',residual,'noise_snr_db',noiseSnr, ...
   'nominal_trough_sine_error',troughError,'jitter_mean_s',mean(jitter),'jitter_rms_s',sqrt(mean(jitter.^2)), ...
   'n_true_events',numel(nominal),'null_pair_residual',nullResidual,'poisson_events',count,'no_96Hz_component',true, ...
   'input_file',string(file),'git_commit',string(metadata.git_commit),'matlab_version',string(version),'seed',20260618, ...
   'apc_options_json',string(jsonencode(metadata.apc_configurations)), ...
   'comparator_settings_json',string(jsonencode(metadata.comparator_settings)),'generator_settings_json',string(jsonencode(cfg)));
  rows{end+1}=row; %#ok<AGROW>
 end
end
T=struct2table([rows{:}]);v1_write_csv(T,fullfile(out,'slow_input_verification.csv'));
save(fullfile(out,'slow_input_verification.mat'),'T','metadata','-v7.3');
result=struct('passed',true,'n_coupled',150,'n_null',75,'elapsed_seconds',toc(start),'metadata',metadata);
f=fopen(fullfile(out,'slow_input_verification.json'),'w','n','UTF-8');assert(f>=0);c=onCleanup(@() fclose(f)); %#ok<NASGU>
fprintf(f,'%s',jsonencode(result,'PrettyPrint',true));fprintf('INPUT VERIFICATION PASSED 150 coupled and 75 null\n');
end
