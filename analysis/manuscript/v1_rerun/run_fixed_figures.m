d=fileparts(mfilename('fullpath'));addpath(d,'-begin');
metadata=jsondecode(fileread(fullfile(d,'figure_render_metadata.json')));started=tic;
addpath(fullfile(metadata.paths.repository,'analysis','v1_revision'),'-begin');maxNumCompThreads(1);
render_frozen_figures(d,metadata);
runtime=struct('status','COMPLETE','elapsed_seconds',toc(started),'completed_local',char(datetime('now')),'metadata',metadata);
f=fopen(fullfile(d,'figures_runtime.json'),'w');assert(f>=0);cleanup=onCleanup(@() fclose(f));
fprintf(f,'%s',jsonencode(runtime,'PrettyPrint',true));
fprintf('FIGURES COMPLETE from frozen MAT tables; %.3f seconds\n',runtime.elapsed_seconds);
