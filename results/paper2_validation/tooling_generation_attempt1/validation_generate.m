function validation_generate
O=fileparts(mfilename('fullpath'));root=fileparts(fileparts(O));repo=fullfile(root,'apc-brainstorm-publish');cd(O);
addpath(fullfile(repo,'analysis','v1_revision'),'-begin');addpath(fullfile(repo,'analysis','v2_revision'),'-begin');addpath(fullfile(repo,'analysis','v3_aperiodic'),'-begin');addpath(fullfile(repo,'results','paper2_ablation'),'-begin');addpath(O,'-begin');addpath(fullfile(repo,'src'),'-begin');
m=jsondecode(fileread(fullfile(O,'provenance.json')));G=jsondecode(fileread(fullfile(O,'all_gate_results.json')));assert(strcmp(G.status,'PASS'));
assert(~isfile(fullfile(O,'generation_complete.json')),'Validation:RepeatedGeneration','Generation already complete');start=tic;
config=struct;
for pair={ {'V1','heldout'}, {'V2','HA'}, {'V4','heldout'}, {'ecog','ecog'} }
 item=pair{1};q=load(fullfile(O,'gate_checkpoints',sprintf('scan_canonical_0000_%s.mat',item{2})),'settings','maps');
 C=q.settings;C.phase_grid_hz=q.maps{1}.fp_grid_hz;C.apc_options_v1=struct('fA',[80 150]);
 if ismember(string(item{1}),["V1","V4"]),old=load(fullfile(root,'revision_checks','v3_aperiodic','HB_inputs.mat'),'meta');C.apc_options_v1=old.meta.apc_configurations.v1;end
 if string(item{1})=="ecog",C.apc_options_v1=struct('fA',[80 150],'minPhaseHz',6,'maxPhaseHz',30);end
 C.apc_options_v1.version='v1';C.apc_options_v3=C.apc_options_v1;C.apc_options_v3.version='v3';C.apc_options_v3.minPhaseHz=1;C.apc_options_v3.maxPhaseHz=30;config.(item{1})=C;
end
p=validation_p1_generator('profile');config.V3=struct('amplitude_grid_hz',p.amplitude_scan_hz,'amplitude_half_width_hz',14,'phase_grid_hz',3:.5:14, ...
 'apc_options_v1',struct('fA',p.broad_fa_band_hz,'epoch',[-.6 .6],'decomposition','fft_peak','metric',p.metric,'diagm',false,'surrogates',false,'num_perm',0,'numPhaseBins',18,'minPhaseCycles',p.min_phase_cycles,'flipTroughs',true));
config.V3.apc_options_v3=config.V3.apc_options_v1;config.V3.apc_options_v3.version='v3';config.V3.apc_options_v3.minPhaseHz=1;config.V3.apc_options_v3.maxPhaseHz=30;
csvargs={'Delimiter',',','NumHeaderLines',0,'ReadVariableNames',true,'TextType','string','Encoding','UTF-8'};
R=readtable(fullfile(root,'revision_checks','rodent_multi','regional_bout_estimates.csv'),csvargs{:});r=jsondecode(R.provenance_json(1));c=r.comparators;
config.rodent=struct('amplitude_grid_hz',c.amplitude_grid,'amplitude_half_width_hz',c.amplitude_half_width,'phase_grid_hz',c.phase_grid,'apc_options_v1',struct('fA',[80 150]),'apc_options_v3',struct('fA',[80 150],'version','v3','minPhaseHz',1,'maxPhaseHz',30));clear R;
if isfile(fullfile(O,'configuration.json'))
 pinned=jsondecode(fileread(fullfile(O,'configuration.json')));assert(isequaln(pinned,jsondecode(jsonencode(config))),'Validation:ConfigurationChanged','Pinned settings changed');
else,writejson(fullfile(O,'configuration.json'),config);end
% Only seeds change relative to complete HB generation; preserve its original stream order before selecting V1/H4.
truths={};shiftStream=RandStream('mrg32k3a','Seed',20261115);
for suite=["V1","V2","V3","V4"]
 seed=20261109+str2double(extractAfter(suite,1));
 assert(~isfile(fullfile(O,char(suite+"_inputs.mat"))),'Validation:ExistingInputs','Preserve generated inputs');
 if suite=="V1"||suite=="V4"
  d=fullfile(O,char(suite+"_source"));mkdir(d);old=load(fullfile(root,'revision_checks','v3_aperiodic','HB_inputs.mat'),'meta');meta=old.meta;meta.git_commit=m.git_head;
  validation_hb_cases(d,meta,seed);q=load(fullfile(d,'HB_inputs.mat'),'cases');keep=false(size(q.cases));
  for j=1:numel(keep),c=q.cases{j};keep(j)=startsWith(string(c.scenario),"H1")&&ismember(string(c.dataset),["coupled","timing_null"]);if suite=="V4",keep(j)=string(c.scenario)=="H4";end;end
  cases=q.cases(keep);clear q;expected=350;if suite=="V4",expected=25;end;assert(numel(cases)==expected);
 elseif suite=="V2",cases=validation_ha_cases(seed);assert(numel(cases)==900);
 else
  cfg=validation_p1_generator('profile');cfg.random_seed=seed;cells=validation_p1_generator('cells');rng(seed,'twister');cases={};
  for j=1:numel(cells),for ir=1:100
   [x,t]=validation_p1_generator('trial',cfg,cells(j));cc=cfg;cc.true_fp_hz=cells(j).rhythm_hz;
   dataset="coupled";if ~cells(j).is_coupled,dataset="uncoupled";end
   id=numel(cases)+1;cases{end+1}=struct('input_id',id,'paired_coupled_id',nan,'scenario',cells(j).name,'dataset',dataset,'level',cells(j).keep_rate,'repeat_index',ir,'signal',x,'time',t,'cfg',cc,'true_fd_hz',cells(j).distractor_hz); %#ok<AGROW>
  end;end
  assert(numel(cases)==600);
 end
 for j=1:numel(cases)
  c=cases{j};c.calibration_shifts=round(numel(c.signal)*(.25+.5*rand(shiftStream,1,200)));c.signal_sha256=signalsha(c.signal);cases{j}=c;
  beta=nan;if isfield(c,'beta'),beta=c.beta;end
  truths{end+1}=struct('suite',suite,'input_id',c.input_id,'key',suite+"_"+c.input_id,'paired_coupled_id',c.paired_coupled_id,'scenario',string(c.scenario),'dataset',string(c.dataset),'level',c.level,'beta',beta,'duration_s',numel(c.signal)/c.cfg.fs_hz,'repeat_index',c.repeat_index,'true_fp_hz',c.cfg.true_fp_hz,'true_fa_hz',c.cfg.true_fa_hz,'true_fd_hz',c.true_fd_hz,'seed',seed,'signal_sha256',string(c.signal_sha256),'git_commit',string(m.git_head),'protocol_sha256',string(m.protocol_sha256),'generator_settings_json',string(jsonencode(c.cfg))); %#ok<AGROW>
 end
 meta=m;meta.seed=seed;meta.configuration=config.(char(suite));save(fullfile(O,char(suite+"_inputs.mat")),'cases','meta','-v7.3');fprintf('%s inputs saved: %d\n',suite,numel(cases));clear cases;
end
v1_write_csv(struct2table(vertcat(truths{:})),fullfile(O,'simulation_truths.csv'));
writejson(fullfile(O,'generation_complete.json'),struct('status','COMPLETE','inputs',numel(truths),'elapsed_seconds',toc(start),'provenance',m,'calibration_shift_seed',20261115,'shift_rule','round(N*(.25+.5*rand)), mrg32k3a, one stream, V1/V2/V3/V4 input order, 200 draws per input'));
end
function value=signalsha(x)
md=java.security.MessageDigest.getInstance('SHA-256');md.update(typecast(double(x(:)),'uint8'));bytes=typecast(md.digest(),'uint8');value=lower(reshape(dec2hex(bytes,2).',1,[]));
end
function writejson(file,v),f=fopen(file,'w','n','UTF-8');assert(f>=0);c=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(v));end
