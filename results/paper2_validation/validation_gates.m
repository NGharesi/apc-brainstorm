function validation_gates
O=fileparts(mfilename('fullpath'));root=fileparts(fileparts(O));repo=fullfile(root,'apc-brainstorm-publish');cd(O);
addpath(fullfile(root,'revision_checks','v3_aperiodic'),'-begin');
addpath(fullfile(repo,'analysis','v1_revision'),'-begin');addpath(fullfile(repo,'analysis','v2_revision'),'-begin');addpath(fullfile(repo,'analysis','v3_aperiodic'),'-begin');
addpath(fullfile(repo,'results','paper2_ablation'),'-begin');addpath(fullfile(root,'revision_checks','final'),'-begin');addpath(O,'-begin');addpath(fullfile(repo,'src'),'-begin');
assert(strcmpi(which('bst_apc'),fullfile(repo,'src','bst_apc.m')));
m=jsondecode(fileread(fullfile(O,'provenance.json')));assert(m.protocol_public_on_origin);
assert(~isfile(fullfile(O,'G_gen.json')),'Validation:RepeatedGate','Do not repeat a completed gate');
start=tic;stage='G-gen';G=struct('status','RUNNING','provenance',m);
try
 environment=struct('matlab_version',version,'toolbox_versions',ver,'bst_apc_path',which('bst_apc'),'event_path',which('apc_event_carrier'),'sp_path',which('sp_raw_fp'));
 writejson(fullfile(O,'environment.json'),environment);
 d=fullfile(O,'gate_generated');if ~isfolder(d),mkdir(d);end
 old=load(fullfile(root,'revision_checks','v3_aperiodic','HB_inputs.mat'),'cases','meta');
 generate_v3_hb(d,old.meta);fresh=load(fullfile(d,'HB_inputs.mat'),'cases');
 hb=isequaln(old.cases,fresh.cases);assert(hb,'Validation:GeneratorHB','Existing held-out inputs differ');
 fprintf('G-gen HB: 675/675 complete cases bit-identical (includes all H1 inputs)\n');clear old fresh;
 old=load(fullfile(root,'revision_checks','v3_aperiodic','HA_inputs.mat'),'cases');fresh=validation_ha_cases(20261101);
 ha=isequaln(old.cases,fresh);assert(ha,'Validation:GeneratorHA','HA inputs differ');
 fprintf('G-gen HA: 900/900 complete cases bit-identical\n');clear old fresh;
 cfg=validation_p1_generator('profile');cfg.random_seed=20261112;cells=validation_p1_generator('cells');first=cell(1,numel(cells));
 rng(cfg.random_seed,'twister');for j=1:numel(cells),[x,t]=validation_p1_generator('trial',cfg,cells(j));first{j}=struct('signal',x,'time',t);end
 rng(cfg.random_seed,'twister');for j=1:numel(cells),[x,t]=validation_p1_generator('trial',cfg,cells(j));assert(isequal(first{j},struct('signal',x,'time',t)),'Validation:GeneratorP1','P1 double generation differs');end
 Ggen=struct('status','PASS','HB_complete_cases_bit_identical',675,'HA_complete_cases_bit_identical',900,'P1_repeat1_cells_twice_bit_identical',6,'P1_seed',20261112,'P1_outcomes_computed',false,'elapsed_seconds',toc(start),'provenance',m);
 writejson(fullfile(O,'G_gen.json'),Ggen);clear first x t;
 stage='G-event';Q=readtable(fullfile(root,'revision_checks','final','burst_coupled_input.csv'),'Delimiter',',','NumHeaderLines',0,'ReadVariableNames',true,'TextType','string','Encoding','UTF-8');
 [r,info]=bst_apc(struct('data',Q.signal(:).','time',Q.time_s(:).'),struct('fA',[80 150]));
 fp=double(r.phase_frequency_hz.Value(1));minimal=struct('status_code',0,'fp_hz',fp);
 a=apc_event_carrier(Q.signal,500,r,80:4:160,6,1.5,.020);
 b=apc_event_carrier(Q.signal,500,minimal,80:4:160,6,1.5,.020);
 c=apc_event_carrier(Q.signal,500,minimal,80:4:160,6,1.5,.020);
 assert(struct_equal(a,b,1e-12)&&struct_equal(b,c,1e-12),'Validation:EventGate','Amended event gate differs');
 Gevent=struct('status','PASS','tolerance',1e-12,'original',a,'minimal',b,'repeated',c,'source_fp_hz',fp,'grid_hz',80:4:160,'provenance',m);
 save(fullfile(O,'G_event.mat'),'r','info','minimal','a','b','c','m');writejson(fullfile(O,'G_event.json'),Gevent);
 fprintf('G-event PASS original/minimal/repeated\n');
 stage='G-abl';validation_ablation_gates;
 G.status='PASS';G.generator=Ggen;G.event=Gevent;G.ablation=jsondecode(fileread(fullfile(O,'gate_results.json')));G.elapsed_seconds=toc(start);
 writejson(fullfile(O,'all_gate_results.json'),G);fprintf('ALL VALIDATION GATES PASS %.3fs\n',toc(start));
catch err
 G.status='STOPPED';G.stage=stage;G.identifier=err.identifier;G.message=err.message;G.stack=err.stack;G.elapsed_seconds=toc(start);
 writejson(fullfile(O,'gate_driver_error.json'),G);
 if startsWith(err.identifier,'Validation:')||startsWith(err.identifier,'Paper2:')||startsWith(err.identifier,'Final:')
  writejson(fullfile(O,'all_gate_results.json'),G);
  f=fopen(fullfile(O,'STOPPED_gate.md'),'w','n','UTF-8');fprintf(f,'# STOPPED: validation gate\n\n%s\n%s: %s\n\nNo full validation suite or endpoint run started.\nCommit %s\nProtocol %s\n',stage,err.identifier,err.message,m.git_head,m.protocol_sha256);fclose(f);
 end
 rethrow(err);
end
end
function tf=struct_equal(a,b,tol)
tf=isequal(fieldnames(a),fieldnames(b));names=fieldnames(a);
for j=1:numel(names)
 x=a.(names{j});y=b.(names{j});
 if isnumeric(x),tf=tf&&isequal(size(x),size(y))&&isequal(isnan(x),isnan(y))&&all(abs(x(isfinite(x))-y(isfinite(y)))<=tol);
 else,tf=tf&&isequaln(x,y);end
end
end
function writejson(file,v),f=fopen(file,'w','n','UTF-8');assert(f>=0);c=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(v));end
