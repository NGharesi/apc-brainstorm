"""Extend the same diagnostics to every new-scenario status-4 trial."""
from pathlib import Path
OUT=Path(__file__).resolve().parent
s=(OUT/'run_followup.m').read_text(encoding='utf-8')
body=s[s.index('function run_diagnosis('):s.index('\nfunction run_slow(')]
body=body.replace('function run_diagnosis(out,bank,metadata)','function run_slow_diagnosis(out,metadata)',1)
body=body.replace("selection=jsondecode(fileread(fullfile(out,'status4_selection.json')));",'''selection=struct('stage',{},'benchmark',{},'dataset',{},'level',{},'repeat_index',{},'configuration',{});
for ratio=[0 .5 1 1.5 2 3]
 b=load(fullfile(out,sprintf('slow_inputs_level_%g.mat',ratio)),'T');
 t=b.T(b.T.method=="APC" & b.T.status_code==4,:);
 for k=1:height(t)
  selection(end+1)=struct('stage','slow','benchmark','slow_rhythm','dataset',char(t.dataset(k)), ...
   'level',num2str(ratio,17),'repeat_index',num2str(t.repeat_index(k)),'configuration',char(t.configuration(k))); %#ok<AGROW>
 end
end
assert(numel(selection)==122,'followup:SlowStatusCount','Unexpected status-4 selection count');''',1)
a=body.index(' paired=fullfile(')
b=body.index(' latent=cell',a)
body=body[:a]+''' input=fullfile(out,sprintf('slow_inputs_level_%g.mat',level));b=load(input,'cases','nullCases');c=b.cases{ir};signal=c.signal;
 if strcmp(q.dataset,'timing_null'),signal=b.nullCases{ir}.signal;end
'''+body[b:]
body=body.replace('  opt=presets(1).options;if mode==2,opt.fPRefine=false;end',"  opt=presets(1).options;if strcmp(q.configuration,'v1.0_no_flip'),opt.flipTroughs=false;end;if mode==2,opt.fPRefine=false;end",1)
body=body.replace(' rows{end+1}=row;', ''' row.configuration=string(q.configuration);
 row.diagnostic_refined_options_json=string(jsonencode(diagnosticBank{j,1}.options));
 row.diagnostic_unrefined_options_json=string(jsonencode(diagnosticBank{j,2}.options));
 rows{end+1}=row;''',1)
body=body.replace("'status4_diagnosis.csv'","'slow_status4_diagnosis.csv'").replace("'status4_diagnostics.mat'","'slow_status4_diagnostics.mat'")
header='''function diagnose_slow_status4()
out=strrep(fileparts(mfilename('fullpath')),'/','\\');root=fileparts(fileparts(out));repo=fullfile(root,'apc-brainstorm-publish');
oldPath=path;oldDir=pwd;oldRng=rng;oldThreads=maxNumCompThreads(1);
cleanup=onCleanup(@() restore(oldPath,oldDir,oldRng,oldThreads)); %#ok<NASGU>
cd(out);addpath(fullfile(repo,'analysis','v1_revision'),'-begin');addpath(fullfile(repo,'src'),'-begin');addpath(out,'-begin');
assert(strcmpi(which('bst_apc'),fullfile(repo,'src','bst_apc.m')));
assert(strcmp(git(repo,'rev-parse HEAD'),'71ebc16aed32ca38be73a800738b975e5806b330') && isempty(git(repo,'status --porcelain')));
b=load(fullfile(out,'slow_inputs_level_0.mat'),'metadata');metadata=b.metadata;start=tic;
try
 run_slow_diagnosis(out,metadata);
 result=struct('status','COMPLETE','elapsed_seconds',toc(start),'metadata',metadata);
 write_json(fullfile(out,'slow_diagnosis_runtime.json'),result);fprintf('SLOW STATUS4 DIAGNOSIS COMPLETE %.3f seconds\\n',toc(start));
catch err
 result=struct('status','FAILED_STOP','elapsed_seconds',toc(start),'error',err.message,'metadata',metadata);
 write_json(fullfile(out,'slow_diagnosis_runtime.json'),result);rethrow(err);
end
end
'''
helpers=s[s.index('function s=git('):]
target=OUT/'diagnose_slow_status4.m'
assert not target.exists()
target.write_text(header+body+'\n'+helpers,encoding='utf-8')
print('Prepared analysis-only slow status-4 diagnostic')
