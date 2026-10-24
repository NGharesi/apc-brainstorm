function value=paper2_error_context(action,varargin)
% Persist comparison details before an assertion raises; worker catch retains them.
persistent state
if isempty(state),state=struct('error_file','','provenance',[],'worker',nan,'bout_key',"not_applicable",'source_index',nan,'assertion',[]);end
switch action
 case 'init'
  state=struct('error_file',varargin{1},'provenance',varargin{2},'worker',varargin{3},'bout_key',"startup",'source_index',nan,'assertion',[]);
 case 'context'
  state.bout_key=string(varargin{1});state.source_index=varargin{2};state.assertion=[];
 case 'failure'
  state.assertion=varargin{1};record=state.assertion;record.worker=state.worker;record.provenance=state.provenance;
  if ~isempty(state.error_file),f=fopen(state.error_file,'w','n','UTF-8');if f>=0,c=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(record));end;end
 case 'get'
 otherwise,error('Paper2:ErrorContext','Unknown error-context action');
end
value=state;
end
