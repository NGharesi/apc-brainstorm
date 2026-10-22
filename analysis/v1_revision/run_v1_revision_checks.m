function run_v1_revision_checks(outDir)
% Committed, clean-source checks; no tag is created by this function.
a=fileparts(mfilename('fullpath'));addpath(a,'-begin');
if nargin<1,outDir=fullfile(fileparts(fileparts(fileparts(a))),'revision_checks','v1_rerun','committed_checks');end
v1_revision('sanity',outDir);
v1_revision('smoke',outDir);
end
