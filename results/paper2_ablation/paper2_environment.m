function paper2_environment
% Record current runtime without processing a signal or calling an estimator.
O=fileparts(mfilename('fullpath'));R=fileparts(fileparts(O));repo=fullfile(R,'apc-brainstorm-publish');cd(O);addpath(fullfile(repo,'src'),'-begin');
assert(strcmpi(which('bst_apc'),fullfile(repo,'src','bst_apc.m')));
m=struct('matlab_version',version,'toolbox_versions',ver,'bst_apc_path',which('bst_apc'),'SP_raw_path',which('sp_raw_fp'),'spectral_helper_path',which('apc_v3_spectral_peak'),'metric_helper_path',which('calc_MI_all_methods'));
f=fopen(fullfile(O,'environment.json'),'w','n','UTF-8');assert(f>=0);c=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(m));fprintf('ENVIRONMENT RECORDED %s\n',version);
end
