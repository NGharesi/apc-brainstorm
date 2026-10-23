function run_v3_gates
% Sequential G0/G1/G2 gates. No held-out generation occurs in this function.
A=fileparts(mfilename('fullpath'));repo=fileparts(fileparts(A));root=fileparts(repo);O=fullfile(root,'revision_checks','v3_aperiodic');cd(O);
addpath(A,'-begin');addpath(fullfile(repo,'src'),'-begin');clear bst_apc calc_MI_all_methods;
m=jsondecode(fileread(fullfile(O,'phaseA_implementation.json')));assert(~isfile(fullfile(O,'gate_results.json')),'v3:ExistingRun','Preserve reportable gate results');
gates=struct('G0','NOT_RUN','G1','NOT_RUN','G2','NOT_RUN','G3','NOT_RUN');start=tic;rows={};cells={};
try
 T=readtable(fullfile(root,'revision_checks','final','burst_coupled_input.csv'),'Delimiter',',','NumHeaderLines',0,'ReadVariableNames',true,'VariableNamingRule','preserve','Encoding','UTF-8');input=struct('data',double(T.signal(:).'),'time',double(T.time_s(:).'));options=struct('fA',[80 150]);
 % Tagged references are run once, and their complete structures retained.
 ref=fullfile(O,'reference_v1_0');addpath(ref,'-begin');clear bst_apc calc_MI_all_methods;
 assert(strcmpi(which('bst_apc'),fullfile(ref,'bst_apc.m')));[referenceV1,referenceInfoV1]=bst_apc(input,options);rmpath(ref);
 ref=fullfile(O,'reference_v2_0');addpath(ref,'-begin');clear bst_apc calc_MI_all_methods;
 assert(strcmpi(which('bst_apc'),fullfile(ref,'bst_apc.m')));optionsV2=options;optionsV2.version='v2';[referenceV2,referenceInfoV2]=bst_apc(input,optionsV2);rmpath(ref);
 addpath(fullfile(repo,'src'),'-begin');clear bst_apc calc_MI_all_methods;
 assert(strcmpi(which('bst_apc'),fullfile(repo,'src','bst_apc.m')));
 [currentV1,currentInfoV1]=bst_apc(input,options);explicit=options;explicit.version='v1';[explicitV1,explicitInfoV1]=bst_apc(input,explicit);
 [currentV2,currentInfoV2]=bst_apc(input,optionsV2);
 g0rows={pack('G0',0,20,1,'tag-v1.0',referenceV1,referenceInfoV1,8,120),pack('G0',0,20,1,'default-v1.0',currentV1,currentInfoV1,8,120),pack('G0',0,20,1,'explicit-v1',explicitV1,explicitInfoV1,8,120),pack('G0',0,20,1,'tag-v2.0',referenceV2,referenceInfoV2,8,120),pack('G0',0,20,1,'current-v2.0',currentV2,currentInfoV2,8,120)};
 writetable(struct2table(vertcat(g0rows{:})),fullfile(O,'G0_trials.csv'));
 expected=[7.99792313403792,122,.176907779165945,178.575795410875];observed=[currentV1.phase_frequency_hz.Value,currentV1.amplitude_frequency_hz.Value,currentV1.pac_strength.Value,currentV1.preferred_phase_deg.Value];delta=abs(observed-expected);
 source=jsondecode(fileread(fullfile(O,'source_additions_verification.json')));
 result=struct('canonical_expected',expected,'canonical_observed',observed,'canonical_absolute_differences',delta,'canonical_tolerance',1e-10, ...
  'v1_tag_complete_structures_exact',isequaln(currentV1,referenceV1)&&isequaln(currentInfoV1,referenceInfoV1), ...
  'default_explicit_v1_exact',isequaln(currentV1,explicitV1)&&isequaln(currentInfoV1,explicitInfoV1), ...
  'v2_tag_complete_structures_exact',isequaln(currentV2,referenceV2)&&isequaln(currentInfoV2,referenceInfoV2), ...
  'new_diff_only_additions_and_version_switch',source.passed,'provenance',m);
 pass=all(delta<=1e-10)&&currentV1.status_code.Value==0&&result.v1_tag_complete_structures_exact&&result.default_explicit_v1_exact&&result.v2_tag_complete_structures_exact&&source.passed;result.passed=pass;gates.G0=label(pass);
 save(fullfile(O,'G0.mat'),'input','options','optionsV2','referenceV1','referenceInfoV1','referenceV2','referenceInfoV2','currentV1','currentInfoV1','currentV2','currentInfoV2','explicitV1','explicitInfoV1','result','m','-v7.3');writejson(fullfile(O,'G0.json'),result);
 fprintf('G0 %s canonical max difference %.17g v1 exact%d v2 exact%d\n',gates.G0,max(delta),result.v1_tag_complete_structures_exact,result.v2_tag_complete_structures_exact);
 if ~pass,finish('G0');return;end
 % G1: the canonical v3 trial, no changes after seeing it.
 o3=options;o3.version='v3';[canonicalV3,canonicalInfoV3]=bst_apc(input,o3);pass=canonicalV3.status_code.Value==0&&abs(canonicalV3.phase_frequency_hz.Value-8)<=.1&&abs(canonicalV3.amplitude_frequency_hz.Value-120)<=8;
 gates.G1=label(pass);row=pack('G1',0,20,1,'APC-v3.0',canonicalV3,canonicalInfoV3,8,120);rows{end+1}=row;
 save(fullfile(O,'G1.mat'),'canonicalV3','canonicalInfoV3','input','m','-v7.3');write_curve('G1',canonicalInfoV3);
 writetable(struct2table(vertcat(rows{:})),fullfile(O,'gate_trials.csv'));fprintf('G1 %s status%d fP %.17g fA %.17g\n',gates.G1,row.status,row.fP_hz,row.fA_hz);
 if ~pass,finish('G1');return;end
 % G2: each fixed cell completes its 20 paired repeats; a failed cell stops.
 rng(20261031,'twister');dest=fullfile(O,'gate_inputs');mkdir(dest);
 for beta=[1 2]
  for duration=[2 6]
   countV3=0;countV1=0;statusesV3=zeros(1,6);statusesV1=zeros(1,6);
   for trial=1:20
    [signal,time,parts,cfg]=v3_development_generator(beta,duration,'coupled');before=rng;in=struct('data',signal,'time',time);
    [r3,i3]=bst_apc(in,o3);[r1,i1]=bst_apc(in,options);assert(isequal(before,rng),'v3:RNG','Deterministic methods changed generator RNG');
    z3=pack('G2',beta,duration,trial,'APC-v3.0',r3,i3,15,110);z1=pack('G2',beta,duration,trial,'APC-v1.0',r1,i1,15,110);rows=[rows {z3,z1}]; %#ok<AGROW>
    countV3=countV3+z3.fp_correct;countV1=countV1+z1.fp_correct;statusesV3(z3.status+1)=statusesV3(z3.status+1)+1;statusesV1(z1.status+1)=statusesV1(z1.status+1)+1;
    name=sprintf('G2_beta%g_T%g_trial%02d',beta,duration,trial);save(fullfile(dest,[name '.mat']),'signal','time','parts','cfg','r3','i3','r1','i1','m','-v7.3');write_curve(name,i3);
    writetable(struct2table(vertcat(rows{:})),fullfile(O,'gate_trials.csv'));
    fprintf('G2 beta%g T%g trial%02d v3 status%d fP %.9g v1 status%d fP %.9g\n',beta,duration,trial,z3.status,z3.fP_hz,z1.status,z1.fP_hz);
   end
   pass=countV3>=16;cells{end+1}=struct('gate','G2','beta',beta,'duration_s',duration,'repeats',20,'v3_fp_recovery',countV3,'v1_fp_recovery',countV1,'v3_status_counts',string(jsonencode(statusesV3)),'v1_status_counts',string(jsonencode(statusesV1)),'passed',pass,'git_head',string(m.git_head),'protocol_sha256',string(m.protocol_sha256),'seed',20261031); %#ok<AGROW>
   writetable(struct2table(vertcat(cells{:})),fullfile(O,'G2_cell_summary.csv'));fprintf('G2 CELL beta%g T%g %s v3 %d/20 v1 %d/20\n',beta,duration,label(pass),countV3,countV1);
   if ~pass,gates.G2='FAIL';finish('G2');return;end
  end
 end
 gates.G2='PASS';
 % G3 has no rejection gate: no-rhythm Poisson bursts, same cell/repeat counts.
 rng(20261031,'twister');
 for beta=[1 2],for duration=[2 6],for trial=1:20
  [signal,time,parts,cfg]=v3_development_generator(beta,duration,'poisson_no_rhythm');before=rng;[r3,i3]=bst_apc(struct('data',signal,'time',time),o3);assert(isequal(before,rng));
  rows{end+1}=pack('G3',beta,duration,trial,'APC-v3.0',r3,i3,NaN,110); %#ok<AGROW>
  name=sprintf('G3_beta%g_T%g_trial%02d',beta,duration,trial);save(fullfile(dest,[name '.mat']),'signal','time','parts','cfg','r3','i3','m','-v7.3');write_curve(name,i3);writetable(struct2table(vertcat(rows{:})),fullfile(O,'gate_trials.csv'));
 end;end;end
 gates.G3='DESCRIPTIVE_COMPLETE';finish('');
catch err
 writejson(fullfile(O,'gate_execution_error.json'),struct('identifier',err.identifier,'message',err.message,'gates',gates,'elapsed_seconds',toc(start),'provenance',m));rethrow(err);
end
function row=pack(gate,beta,duration,trial,method,r,info,truthFP,truthFA)
 exponent=NaN;offset=NaN;height=NaN;sigma=NaN;flo=NaN;branch="not_applicable";
 if isfield(info,'aperiodic_exponent'),exponent=info.aperiodic_exponent;offset=info.aperiodic_offset;height=info.aperiodic_peak_height;sigma=info.aperiodic_sigma;flo=info.f_lo_hz;end
 if isfield(info,'diagnostics')&&strcmp(info.version,'v3.0')
  branch="not_reached";if isfield(info.diagnostics{1},'aperiodic'),branch=string(info.diagnostics{1}.aperiodic.location_branch);end
 end
 fp=r.phase_frequency_hz.Value;fa=r.amplitude_frequency_hz.Value;status=r.status_code.Value;
 row=struct('gate',string(gate),'beta',beta,'duration_s',duration,'trial',trial,'method',string(method),'true_fp_hz',truthFP,'true_fa_hz',truthFA,'fP_hz',fp,'fA_hz',fa,'score',r.pac_strength.Value,'status',status,'route',string(info.route),'n_bursts',r.n_bursts.Value,'fp_correct',status==0&&isfinite(fp)&&abs(fp-truthFP)<=1,'exponent',exponent,'offset',offset,'peak_height',height,'sigma',sigma,'f_lo_hz',flo,'location_branch',branch,'git_head',string(m.git_head),'protocol_sha256',string(m.protocol_sha256),'seed',20261031,'implementation_record','phaseA_implementation.json');
end
function write_curve(name,info)
 if ~isfield(info,'diagnostics')||~isfield(info.diagnostics{1},'aperiodic'),return;end
 d=info.diagnostics{1}.aperiodic;if isempty(d.frequency_hz),return;end
 C=table(d.frequency_hz,d.power,d.log10_power,d.aperiodic_fit,d.residual,d.pass2_mask,'VariableNames',{'frequency_hz','power','log10_power','aperiodic_fit','residual','pass2_mask'});C.git_head=repmat(string(m.git_head),height(C),1);C.protocol_sha256=repmat(string(m.protocol_sha256),height(C),1);C.seed=repmat(20261031,height(C),1);writetable(C,fullfile(O,[name '_curve.csv']));
end
function finish(failed)
 result=struct('status','GATES_PASSED','gates',gates,'failed_gate',failed,'elapsed_seconds',toc(start),'heldout_generated',false,'freeze_commit','NOT_CREATED','tag','NOT_CREATED','provenance',m);if ~isempty(failed),result.status='STOPPED_GATE_FAILURE';end
 writejson(fullfile(O,'gate_results.json'),result);
 if ~isempty(failed),f=fopen(fullfile(O,'STOPPED.md'),'w','n','UTF-8');fprintf(f,'# STOPPED: APC v3 prespecified gate %s failed\n\nThe run stopped under protocol section 6.5. No method redesign or workaround was made. No v3.0 tag or freeze commit was created, and no held-out signal was generated. Full gate results are in gate_results.json and gate_trials.csv.\n',failed);fclose(f);end
end
end
function value=label(pass),value='FAIL';if pass,value='PASS';end;end
function writejson(path,s),f=fopen(path,'w','n','UTF-8');assert(f~=-1);clean=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(s));end
