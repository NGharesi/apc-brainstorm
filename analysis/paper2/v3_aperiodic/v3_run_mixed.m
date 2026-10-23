function v3_run_mixed
O=fileparts(mfilename('fullpath'));C=fullfile(O,'phaseC');start=tic;
assert(~isfile(fullfile(O,'STOPPED.md')));
folders={'rodent5s','POST_HOC_rodent2s','ecog'};functions={'fit_regional_mixed_models','posthoc_2s_fit_mixed_models','ecog_mixed_model'};runtime={'regional_mixed_models.json','posthoc_2s_mixed_models.json','mixed_model_runtime.json'};
for k=1:numel(folders)
 out=fullfile(C,folders{k});if isfile(fullfile(out,runtime{k})),q=jsondecode(fileread(fullfile(out,runtime{k})));assert(strcmp(q.status,'COMPLETE'));continue;end
 addpath(out,'-begin');assert(strcmpi(which(functions{k}),fullfile(out,[functions{k} '.m'])));feval(functions{k});rmpath(out);clear(functions{k});
end
f=fopen(fullfile(C,'mixed_models_runtime.json'),'w','n','UTF-8');fprintf(f,'%s\n',jsonencode(struct('status','COMPLETE','elapsed_seconds',toc(start),'provenance','phaseC/provenance.json')));fclose(f);
end
