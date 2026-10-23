function ieeg_verify_burst_count
out=fileparts(mfilename('fullpath'));root=fileparts(fileparts(out));P=load(fullfile(out,'equivalence_gate_attempt2.mat'),'s','info');
T=readtable(fullfile(root,'revision_checks','final','burst_coupled_input.csv'),'Delimiter',',','ReadVariableNames',true,'VariableNamingRule','preserve','Encoding','UTF-8');
n=ieeg_count_bursts(T.signal,T.time_s,P.info.options);expected=P.s.n_bursts.Value;assert(n==expected,'IEEG:BurstCountDiagnostic','Count-only diagnostic differs from saved source output');
meta=jsondecode(fileread(fullfile(out,'provenance.json')));result=struct('passed',true,'observed_n_bursts',n,'expected_saved_n_bursts',expected,'extra_APC_calls',0,'role','Diagnostic Step 1 count; original v1_bout_features unchanged','provenance',meta);
f=fopen(fullfile(out,'burst_count_diagnostic_verification.json'),'w','n','UTF-8');fprintf(f,'%s\n',jsonencode(result));fclose(f);fprintf('BURST COUNT DIAGNOSTIC PASS %d\n',n);
end
