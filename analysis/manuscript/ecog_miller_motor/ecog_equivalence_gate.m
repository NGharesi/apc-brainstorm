function ecog_equivalence_gate
out=fileparts(mfilename('fullpath'));root=fileparts(fileparts(out));repo=fullfile(root,'apc-brainstorm-publish');
cd(out);addpath(fullfile(root,'revision_checks','rodent_multi'));addpath(fullfile(repo,'src'),'-begin');clear bst_apc calc_MI_all_methods;
meta=jsondecode(fileread(fullfile(out,'provenance.json')));meta.matlab_version=version;meta.toolbox_versions=ver;writejson(fullfile(out,'provenance.json'),meta);
expectedPath=fullfile(repo,'src','bst_apc.m');actualPath=which('bst_apc');assert(strcmpi(actualPath,expectedPath),'ECOG:WrongAPCPath','Wrong APC path: %s',actualPath);
T=readtable(fullfile(root,'revision_checks','final','burst_coupled_input.csv'),'Delimiter',',','ReadVariableNames',true,'VariableNamingRule','preserve','Encoding','UTF-8');
try
 [s,info]=bst_apc(struct('data',double(T.signal(:).'),'time',double(T.time_s(:).')),struct('fA',[80 150]));
 observed=[s.phase_frequency_hz.Value,s.amplitude_frequency_hz.Value,s.pac_strength.Value,s.preferred_phase_deg.Value];expected=[7.99792313403792,122,.176907779165945,178.575795410875];
 delta=abs(observed-expected);passed=all(isfinite(observed))&&all(delta<=1e-10)&&s.status_code.Value==0;
 result=struct('passed',passed,'bst_apc_path',actualPath,'observed',observed,'expected',expected,'absolute_differences',delta,'tolerance',1e-10,'status',s.status_code.Value,'options',info.options,'provenance',meta);
 writejson(fullfile(out,'equivalence_gate.json'),result);save(fullfile(out,'equivalence_gate.mat'),'s','info','result','-v7.3');
 if ~passed,error('ECOG:EquivalenceFailed','Equivalence gate failed; stop before any dataset method output');end
 fprintf('EQUIVALENCE PASS max difference %.17g\n',max(delta));
catch err
 writejson(fullfile(out,'equivalence_gate_failure.json'),struct('identifier',err.identifier,'message',err.message,'provenance',meta));rethrow(err);
end
end
function writejson(path,value)
f=fopen(path,'w','n','UTF-8');assert(f~=-1);clean=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(value));
end
