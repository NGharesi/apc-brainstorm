function run_v3_generate
% Generate once, only after the public v3.0 freeze. No method outputs here.
O=fileparts(mfilename('fullpath'));root=fileparts(fileparts(O));repo=fullfile(root,'apc-brainstorm-publish');cd(O);
addpath(O,'-begin');addpath(fullfile(repo,'analysis','v1_revision'),'-begin');addpath(fullfile(repo,'analysis','v2_revision'),'-begin');addpath(fullfile(repo,'analysis','v3_aperiodic'),'-begin');
m=jsondecode(fileread(fullfile(O,'phaseB_implementation.json')));assert(strcmp(git(repo,'rev-parse HEAD'),m.freeze_commit));assert(strcmp(git(repo,'rev-list -n 1 v3.0'),m.freeze_commit));assert(strcmp(git(repo,'rev-parse origin/neuroimage-submission'),m.freeze_commit));assert(isempty(git(repo,'status --porcelain')));
assert(~isfile(fullfile(O,'HA_inputs.mat'))&&~isfile(fullfile(O,'HB_inputs.mat')),'v3:ExistingInputs','Do not regenerate reportable inputs');start=tic;
meta=m;p=v1_options();v1=p(1).options;v1.fA=[80 160];v1.version='v1';
meta.git_commit=m.freeze_commit;meta.apc_configurations=struct('v1',v1,'v3',setfield(v1,'version','v3')); %#ok<SFLD>
meta.comparator_settings=struct('phase_grid_hz',3:.5:14,'phase_half_width_hz',1.5,'amplitude_grid_hz',80:4:160,'A2_prime_half_width_hz',14,'filter','guarded SOS butter(4), filtfilt','metrics',{{'MVL-raw','MVL-Ozkurt','KLMI','GLM'}},'phase_bins',18,'selection','first column-major maximum');
meta.tpac=struct('available',false,'reason','not a method in v3 protocol');
generate_v3_hb(O,meta);
old=load(fullfile(root,'revision_checks','v2','candidate_03','heldout_inputs.mat'),'cases');fresh=load(fullfile(O,'HB_inputs.mat'),'cases');
assert(isequaln(old.cases,fresh.cases),'v3:HBSignalReproduction','Regenerated HB cases differ from saved original cases');
write_json(fullfile(O,'HB_signal_verification.json'),struct('status','PASS','inputs',numel(fresh.cases),'complete_cases_bit_identical',true,'provenance',m));
clear old fresh;fprintf('HB signals: all 675 complete cases bit-identical to saved inputs\n');
signalStream=new_stream(1);frequencyStream=new_stream(2);poissonStream=new_stream(3);cases={};draws={};
for beta=[1 1.5 2],for amplitude=[.3 .5 .8],for duration=[2 6]
 for trial=1:25
  fp=6+19*rand(frequencyStream);fa=80+60*rand(frequencyStream);before=signalStream.State;
  [signal,nullSignal,time,parts,cfg]=v3_ha_generator(beta,amplitude,duration,fp,fa,signalStream,poissonStream);
  id=numel(cases)+1;c=struct('input_id',id,'paired_coupled_id',id,'scenario',"HA",'dataset',"coupled",'level',amplitude,'beta',beta,'duration_s',duration,'repeat_index',trial,'signal',signal,'time',time,'parts',parts,'cfg',cfg,'true_fd_hz',nan,'signal_rng_state_before',before,'signal_rng_state_after',signalStream.State,'pair_residual',parts.pair_residual);
  cases{end+1}=c;n=c;n.input_id=id+1;n.dataset="timing_null";n.signal=nullSignal;cases{end+1}=n; %#ok<AGROW>
  draws{end+1}=struct('coupled_input_id',id,'null_input_id',id+1,'beta',beta,'rhythm_amplitude',amplitude,'duration_s',duration,'repeat_index',trial,'true_fp_hz',fp,'true_fa_hz',fa,'pair_residual',parts.pair_residual,'poisson_events',numel(parts.poisson_times_s),'git_commit',string(m.freeze_commit),'protocol_sha256',string(m.protocol_sha256),'seed',20261101,'generator_settings_json',string(jsonencode(cfg))); %#ok<AGROW>
 end
 fprintf('HA beta%g amplitude%g T%g: 25 coupled + 25 paired timing null; %d inputs\n',beta,amplitude,duration,numel(cases));
end;end;end
assert(numel(cases)==900);meta=m;save(fullfile(O,'HA_inputs.mat'),'cases','meta','-v7.3');v1_write_csv(struct2table(vertcat(draws{:})),fullfile(O,'HA_frequency_draws.csv'));
write_json(fullfile(O,'generation_runtime.json'),struct('status','COMPLETE','HB_inputs',675,'HA_inputs',900,'elapsed_seconds',toc(start),'provenance',m));
fprintf('GENERATION COMPLETE %.3f seconds\n',toc(start));
end
function stream=new_stream(sub),stream=RandStream('mrg32k3a','Seed',20261101);stream.Substream=sub;end
function s=git(repo,args)
exe='C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe';[status,s]=system(sprintf('"%s" -C "%s" %s',exe,repo,args));assert(status==0);s=strtrim(s);
end
function write_json(file,value),f=fopen(file,'w','n','UTF-8');assert(f>=0);c=onCleanup(@() fclose(f));fprintf(f,'%s\n',jsonencode(value));end
