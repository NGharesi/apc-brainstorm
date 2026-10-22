function run_v1_revision_suite(outDir)
% Tag and clean-tree checks run before every stage. Exceptions stop execution.
a=fileparts(mfilename('fullpath'));addpath(a,'-begin');
if nargin<1,outDir=fullfile(fileparts(fileparts(fileparts(a))),'revision_checks','v1_rerun');end
v1_revision('main',outDir);
v1_revision('random_fp',outDir);
v1_revision('null',outDir);
v1_revision('figures',outDir);
end
