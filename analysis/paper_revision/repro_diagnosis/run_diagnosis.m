% Standalone diagnosis; all new files remain in repro_diagnosis.
diagnosisDirectory=fileparts(mfilename('fullpath'));
addpath(diagnosisDirectory,'-begin');
rd_run_all(diagnosisDirectory);
