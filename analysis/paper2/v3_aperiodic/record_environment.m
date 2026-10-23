function record_environment
O=fileparts(mfilename('fullpath'));m=jsondecode(fileread(fullfile(O,'provenance.json')));m.matlab_version=version;m.toolbox_versions=ver;m.version_metadata_source='Independent current MATLAB runtime';m.status='STEP0_COMPLETE_BEFORE_IMPLEMENTATION';f=fopen(fullfile(O,'provenance.json'),'w','n','UTF-8');fprintf(f,'%s\n',jsonencode(m));fclose(f);fprintf('STEP0 MATLAB %s; %d toolbox records\n',version,numel(ver));
end
