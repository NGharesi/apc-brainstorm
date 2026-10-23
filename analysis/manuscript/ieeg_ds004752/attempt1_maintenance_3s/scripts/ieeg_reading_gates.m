function ieeg_reading_gates
% Data-reading and scalp timing checks only. No APC or scan on dataset.
out=fileparts(mfilename('fullpath'));cd(out);meta=jsondecode(fileread(fullfile(out,'provenance.json')));
eq=jsondecode(fileread(fullfile(out,'equivalence_gate.json')));assert(eq.passed,'IEEG:GateOrder','Equivalence must pass first');
files=dir(fullfile(meta.data_root,'sub-*','ses-*','ieeg','*_ieeg.edf'));[~,order]=sort(string(fullfile({files.folder},{files.name})));files=files(order);
rows={};fileRows={};clockStart=tic;
try
 for fi=1:numel(files)
  path=fullfile(files(fi).folder,files(fi).name);base=erase(path,'_ieeg.edf');
  C=readtsv([base '_channels.tsv']);E=readtsv([base '_events.tsv']);readPath=compatible_path(path,out);I=edfinfo(readPath);
  labels=string(I.SignalLabels(:));sameOrder=isequal(labels,string(C.name(:)));countMatches=numel(labels)==height(C);
  n=double(I.NumSamples(:))*double(I.NumDataRecords);fs=double(I.NumSamples(:))/seconds(I.DataRecordDuration);
  headerChecks=sameOrder&&countMatches&&all(n==E.endSample(end))&&all(fs==2000)&&all(C.sampling_frequency==2000);
  one=struct('file',string(path),'header_channel_order_match',sameOrder,'channel_count_match',countMatches,'channels',numel(labels),'samples',n(1),'events_last_end_sample',E.endSample(end),'fs_hz',fs(1),'header_passed',headerChecks,'passed',false,'provenance_json',string(jsonencode(meta)));
  if ~headerChecks,fileRows{end+1}=one;writetable(struct2table(vertcat(fileRows{:})),fullfile(out,'edf_file_checks.csv'));error('IEEG:EDFHeaderGate','EDF header gate failed: %s',path);end
  TT=edfread(readPath);
  assert(width(TT)==height(C),'IEEG:EDFChannelCount','EDF read channel count differs');
  passed=true;
  for ci=1:height(C)
   raw=TT.(TT.Properties.VariableNames{ci});if iscell(raw),raw=cellfun(@(a)double(a(:)),raw,'UniformOutput',false);x=vertcat(raw{:});else,x=double(raw(:));end
   u=string(I.PhysicalDimensions(ci));u=strrep(strrep(strtrim(u),char(181),'u'),char(956),'u');
   declared=string(C.units(ci));declared=strrep(strrep(strtrim(declared),char(181),'u'),char(956),'u');
   unitsOK=strcmpi(declared,'uV')&&(strlength(u)==0||strcmpi(u,'uV'));source="EDF and channels.tsv";if strlength(u)==0,source="channels.tsv; EDF dimension blank";u="<blank>";end
   finite=all(isfinite(x));v=var(x);med=median(abs(x));ok=unitsOK&&numel(x)==E.endSample(end)&&finite&&isfinite(v)&&v>0&&med<1e4;
   r=struct('file',string(path),'channel_index',ci,'channel',labels(ci),'physical_units',u,'declared_units',declared,'units_source',source,'samples',numel(x),'fs_hz',fs(ci),'nonfinite_samples',sum(~isfinite(x)),'variance_uv2',v,'median_absolute_uv',med,'min_uv',min(x),'max_uv',max(x),'passed',ok,'provenance_json',string(jsonencode(meta)));rows{end+1}=r;passed=passed&&ok; %#ok<AGROW>
  end
  one.passed=passed;fileRows{end+1}=one; %#ok<AGROW>
  writetable(struct2table(vertcat(rows{:})),fullfile(out,'edf_channel_checks.csv'));writetable(struct2table(vertcat(fileRows{:})),fullfile(out,'edf_file_checks.csv'));
  clear TT raw x;
  if ~passed,error('IEEG:EDFSignalGate','EDF signal gate failed: %s',path);end
  fprintf('EDF PASS %d/%d %s\n',fi,numel(files),files(fi).name);
 end
 writejson(fullfile(out,'edf_reading_gate.json'),struct('passed',true,'files',numel(files),'channel_rows',numel(rows),'elapsed_seconds',toc(clockStart),'provenance',meta));
 % Raw scalp EEG: all trials, all available O1/O2/Oz channels; equal trial weights.
 % Remove each trial/channel fixation mean (0 <= t < 1 s); no signal filter.
 eeg=dir(fullfile(meta.data_root,'sub-*','ses-*','eeg','*_eeg.edf'));[~,order]=sort(string(fullfile({eeg.folder},{eeg.name})));eeg=eeg(order);
 total=[];count=0;scalpRows={};
 for fi=1:numel(eeg)
  path=fullfile(eeg(fi).folder,eeg(fi).name);base=erase(path,'_eeg.edf');C=readtsv([base '_channels.tsv']);E=readtsv([base '_events.tsv']);readPath=compatible_path(path,out);I=edfinfo(readPath);
  chosen=find(ismember(upper(string(C.name)),["O1","O2","OZ"]));if isempty(chosen),error('IEEG:NoOccipital','No O1/O2/Oz in %s',path);end
  fs=double(I.NumSamples(1))/seconds(I.DataRecordDuration);assert(fs==200,'IEEG:ScalpFs','Scalp sampling rate differs from dataset metadata');
  labels=string(I.SignalLabels(:));assert(isequal(labels,string(C.name(:))),'IEEG:ScalpOrder','Scalp EDF channel order mismatch');
  TT=edfread(readPath,'SelectedSignals',cellstr(labels(chosen)));x=zeros(E.endSample(end),numel(chosen));
  for ci=1:numel(chosen),raw=TT.(TT.Properties.VariableNames{ci});if iscell(raw),raw=cellfun(@(a)double(a(:)),raw,'UniformOutput',false);v=vertcat(raw{:});else,v=double(raw(:));end;assert(numel(v)==size(x,1)&&all(isfinite(v)),'IEEG:ScalpData','Scalp samples invalid');x(:,ci)=v;end
  if isempty(total),total=zeros(8*fs,1);end
  for ti=1:height(E)
   epoch=x(E.begSample(ti):E.endSample(ti),:);assert(size(epoch,1)==8*fs,'IEEG:ScalpTrialLength','Scalp trial is not 8 seconds');epoch=epoch-mean(epoch(1:fs,:),1);total=total+mean(epoch,2);count=count+1;
  end
  scalpRows{end+1}=struct('file',string(path),'trials',height(E),'channels',strjoin(labels(chosen),';'),'fs_hz',fs,'provenance_json',string(jsonencode(meta))); %#ok<AGROW>
  fprintf('SCALP READ %d/%d %s\n',fi,numel(eeg),eeg(fi).name);clear TT x raw v;
 end
 t=(0:numel(total)-1)'/200;grand=total/count;P=table(t,grand,repmat(count,numel(t),1),repmat(string(jsonencode(meta)),numel(t),1),'VariableNames',{'time_s','grand_average_uv','trial_count','provenance_json'});writetable(P,fullfile(out,'timeline_grand_average.csv'));
 writetable(struct2table(vertcat(scalpRows{:})),fullfile(out,'timeline_file_checks.csv'));
 peaks=struct([]);
 for onset=[1,6]
  keep=find(t>=onset+.05&t<=onset+.25);baseline=mean(grand(t>=onset-.2&t<onset));[~,j]=max(abs(grand(keep)-baseline));idx=keep(j);
  peaks(end+1)=struct('expected_onset_s',onset,'peak_time_s',t(idx),'latency_ms',1000*(t(idx)-onset),'peak_uv',grand(idx),'preonset_mean_uv',baseline,'absolute_peak_difference_uv',abs(grand(idx)-baseline)); %#ok<AGROW>
 end
 writejson(fullfile(out,'timeline_gate_measurements.json'),struct('status','REQUIRES_VISUAL_AND_PAPER_CONFIRMATION','trials',count,'files',numel(eeg),'peaks',peaks,'processing','Unfiltered raw O1/O2/Oz; fixation-mean subtraction per trial/channel; available channels averaged per trial; all trials weighted equally','peak_rule','largest absolute deviation from preceding 200-ms mean within 50-250 ms after each prespecified onset','provenance',meta));
 fprintf('READING GATES DATA COMPLETE trials%d\n',count);
catch err
 writejson(fullfile(out,'reading_gate_failure.json'),struct('status','FAILED_STOP','identifier',err.identifier,'message',err.message,'elapsed_seconds',toc(clockStart),'provenance',meta));rethrow(err);
end
end
function T=readtsv(path)
T=readtable(path,'FileType','text','Delimiter','\t','ReadVariableNames',true,'VariableNamingRule','preserve','TextType','string','Encoding','UTF-8');
end
function writejson(path,value)
f=fopen(path,'w','n','UTF-8');assert(f~=-1);clean=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(value));
end
function value=compatible_path(path,out)
value=path;manifest=jsondecode(fileread(fullfile(out,'edf_header_copies.json')));
for k=1:numel(manifest.files),if strcmpi(path,manifest.files(k).original_path),assert(manifest.files(k).payload_byte_identical,'IEEG:HeaderCopyPayload','Header copy payload not verified');value=manifest.files(k).read_path;return;end;end
end
