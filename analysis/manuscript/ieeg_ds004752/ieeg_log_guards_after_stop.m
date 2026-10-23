function ieeg_log_guards_after_stop
% Logging recovery only: fixed filter designs, zero input, no dataset reading.
out=fileparts(mfilename('fullpath'));root=fileparts(fileparts(out));cd(out);addpath(fullfile(root,'revision_checks','final'),'-begin');clear final_sos_filter;
m=jsondecode(fileread(fullfile(out,'analysis_provenance.json')));assert(isfile(fullfile(out,'STOPPED.md')));x=zeros(6000,1);
for fp=2:.5:12,final_sos_filter(x,2000,[max(.5,fp-1.5),fp+1.5]);end
for fa=80:4:148,final_sos_filter(x,2000,[fa-12,fa+12]);end
G=struct2table(final_sos_filter('registry'));assert(height(G)==39&&all(G.guard_passed));G.reconstructed_logging_after_stop=true(height(G),1);G.dataset_trials_rerun=zeros(height(G),1);G.logging_note=repmat("Deterministic design metadata recovered with unchanged helper on zero input; no dataset PAC computation",height(G),1);G.provenance_json=repmat(string(jsonencode(m)),height(G),1);writetable(G,fullfile(out,'filter_guards.csv'));
fprintf('39 fixed comparator band guards recovered for logging; zero dataset trials rerun\n');
end
