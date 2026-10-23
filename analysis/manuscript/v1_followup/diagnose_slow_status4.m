function diagnose_slow_status4()
out=strrep(fileparts(mfilename('fullpath')),'/','\');root=fileparts(fileparts(out));repo=fullfile(root,'apc-brainstorm-publish');
oldPath=path;oldDir=pwd;oldRng=rng;oldThreads=maxNumCompThreads(1);
cleanup=onCleanup(@() restore(oldPath,oldDir,oldRng,oldThreads)); %#ok<NASGU>
cd(out);addpath(fullfile(repo,'analysis','v1_revision'),'-begin');addpath(fullfile(repo,'src'),'-begin');addpath(out,'-begin');
assert(strcmpi(which('bst_apc'),fullfile(repo,'src','bst_apc.m')));
assert(strcmp(git(repo,'rev-parse HEAD'),'71ebc16aed32ca38be73a800738b975e5806b330') && isempty(git(repo,'status --porcelain')));
b=load(fullfile(out,'slow_inputs_level_0.mat'),'metadata');metadata=b.metadata;start=tic;
try
 run_slow_diagnosis(out,metadata);
 result=struct('status','COMPLETE','elapsed_seconds',toc(start),'metadata',metadata);
 write_json(fullfile(out,'slow_diagnosis_runtime.json'),result);fprintf('SLOW STATUS4 DIAGNOSIS COMPLETE %.3f seconds\n',toc(start));
catch err
 result=struct('status','FAILED_STOP','elapsed_seconds',toc(start),'error',err.message,'metadata',metadata);
 write_json(fullfile(out,'slow_diagnosis_runtime.json'),result);rethrow(err);
end
end
function run_slow_diagnosis(out,metadata)
selection=struct('stage',{},'benchmark',{},'dataset',{},'level',{},'repeat_index',{},'configuration',{});
for ratio=[0 .5 1 1.5 2 3]
 b=load(fullfile(out,sprintf('slow_inputs_level_%g.mat',ratio)),'T');
 t=b.T(b.T.method=="APC" & b.T.status_code==4,:);
 for k=1:height(t)
  selection(end+1)=struct('stage','slow','benchmark','slow_rhythm','dataset',char(t.dataset(k)), ...
   'level',num2str(ratio,17),'repeat_index',num2str(t.repeat_index(k)),'configuration',char(t.configuration(k))); %#ok<AGROW>
 end
end
assert(numel(selection)==122,'followup:SlowStatusCount','Unexpected status-4 selection count');
source=fileread(fullfile(metadata.paths.repository,'src','bst_apc.m'));
manifest=jsondecode(fileread(metadata.input_source_manifest_path)); %#ok<NASGU>
presets=v1_options();rows={};diagnosticBank=cell(numel(selection),2);
for j=1:numel(selection)
 q=selection(j);level=str2double(q.level);ir=str2double(q.repeat_index);
 input=fullfile(out,sprintf('slow_inputs_level_%g.mat',level));b=load(input,'cases','nullCases');c=b.cases{ir};signal=c.signal;
 if strcmp(q.dataset,'timing_null'),signal=b.nullCases{ir}.signal;end
 latent=cell(1,2);trace=cell(1,2);status=zeros(1,2);
 for mode=1:2
  opt=presets(1).options;if strcmp(q.configuration,'v1.0_no_flip'),opt.flipTroughs=false;end;if mode==2,opt.fPRefine=false;end
  [actual,~]=bst_apc(struct('data',signal,'time',c.time),opt);
  [r,info]=fu_apc_diagnostic(struct('data',signal,'time',c.time),opt);
  assert(isequaln(r,actual),'followup:DiagnosticMismatch','Diagnostic copy changed output');
  d=info.diagnostics{1};latent{mode}=d;status(mode)=double(r.status_code.Value(1));
  [fp,tr]=fu_phase_trace(d.burst_average,d.fs,info.options);trace{mode}=tr;
  assert(isequal(fp,d.estimated_fp_hz),'followup:TraceMismatch','Welch trace differs from frozen estimate');
  diagnosticBank{j,mode}=struct('diagnostics',d,'trace',tr,'result',r,'options',info.options);
 end
 d=latent{1};u=latent{2};tr=trace{1};tu=trace{2};assert(status(1)==4);
 ownOutside=d.estimated_fp_hz<tr.left_hz || d.estimated_fp_hz>tr.right_hz;
 oldOutside=d.estimated_fp_hz<tu.left_hz || d.estimated_fp_hz>tu.right_hz;
 limitOutside=d.estimated_fp_hz<presets(1).options.minPhaseHz || d.estimated_fp_hz>presets(1).options.maxPhaseHz;
 assert(~ownOutside && ~limitOutside,'followup:RefinementBounds','Refined estimate violates its neighboring bins or phase limits');
 assert(d.trough_count_before==numel(d.trough_locations));
 assert(d.trough_count_after==0,'followup:Status4Unexpected','Status 4 despite an edge-valid trough');
 lines=splitlines(string(source));conditionLine=find(contains(lines,'if '+d.return_condition),1);
 returnLine=conditionLine+1; % original assignment line immediately after condition
 row=struct('stage',string(q.stage),'benchmark',string(q.benchmark),'dataset',string(q.dataset),'level',level,'repeat_index',ir, ...
  'refined_fp_hz',d.estimated_fp_hz,'unrefined_fp_hz',u.estimated_fp_hz, ...
  'refined_phase_low_hz',d.phase_band_hz(1),'refined_phase_high_hz',d.phase_band_hz(2), ...
  'unrefined_phase_low_hz',u.phase_band_hz(1),'unrefined_phase_high_hz',u.phase_band_hz(2), ...
  'refined_troughs_before',d.trough_count_before,'refined_troughs_after',d.trough_count_after, ...
  'unrefined_troughs_before',u.trough_count_before,'unrefined_troughs_after',u.trough_count_after, ...
  'refined_epoch_half_samples',d.epoch_half_samples,'unrefined_epoch_half_samples',u.epoch_half_samples, ...
  'refined_welch_peak_hz',tr.peak_hz,'refined_welch_left_hz',tr.left_hz,'refined_welch_right_hz',tr.right_hz, ...
  'refined_interpolation_delta_bins',tr.delta,'refined_interpolated',tr.interpolated, ...
  'unrefined_welch_peak_hz',tu.peak_hz,'unrefined_welch_left_hz',tu.left_hz,'unrefined_welch_right_hz',tu.right_hz, ...
  'outside_padded_neighbors',ownOutside,'outside_unpadded_neighbors',oldOutside,'outside_configured_limits',limitOutside, ...
  'refined_status',status(1),'unrefined_status',status(2),'condition',d.return_condition, ...
  'source_file',string(fullfile(metadata.paths.repository,'src','bst_apc.m')),'condition_line',conditionLine,'status_assignment_line',returnLine, ...
  'classification',"b: legitimate failure: no complete trough epoch after edge rejection", ...
  'input_file',string(input),'git_commit',string(metadata.git_commit),'matlab_version',string(version),'seed',metadata.seed, ...
  'apc_options_json',string(jsonencode(metadata.apc_configurations)), ...
  'comparator_settings_json',string(jsonencode(metadata.comparator_settings)),'generator_settings_json',string(jsonencode(c.cfg)));
 row.configuration=string(q.configuration);
 row.diagnostic_refined_options_json=string(jsonencode(diagnosticBank{j,1}.options));
 row.diagnostic_unrefined_options_json=string(jsonencode(diagnosticBank{j,2}.options));
 rows{end+1}=row; %#ok<AGROW>
 fprintf('DIAGNOSIS %d/%d %s %s %g trial%d fP %.6g -> %.6g troughs %d/%d vs %d/%d\n',j,numel(selection),q.benchmark,q.dataset,level,ir,u.estimated_fp_hz,d.estimated_fp_hz,u.trough_count_before,u.trough_count_after,d.trough_count_before,d.trough_count_after);
end
T=struct2table([rows{:}]);v1_write_csv(T,fullfile(out,'slow_status4_diagnosis.csv'));
save(fullfile(out,'slow_status4_diagnostics.mat'),'T','diagnosticBank','metadata','-v7.3');
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
