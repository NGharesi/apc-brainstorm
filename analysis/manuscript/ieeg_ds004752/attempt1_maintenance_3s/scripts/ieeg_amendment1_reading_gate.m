function ieeg_amendment1_reading_gate
% Amended native-rate gate and trialwise resample checks; no PAC estimates.
out=fileparts(mfilename('fullpath'));cd(out);meta=jsondecode(fileread(fullfile(out,'provenance.json')));
eq=jsondecode(fileread(fullfile(out,'equivalence_gate_attempt2.json')));assert(eq.passed,'IEEG:GateOrder','Attempt 2 equivalence must pass first');
assert(strcmp(meta.protocol_sha256,'6f457fd2a2ca714abec723728e1a6617ef23b938f3da03bd025030642d63ad58'),'IEEG:Protocol','Unexpected amendment');
files=dir(fullfile(meta.data_root,'sub-*','ses-*','ieeg','*_ieeg.edf'));[~,ix]=sort(string(fullfile({files.folder},{files.name})));files=files(ix);assert(numel(files)==68,'IEEG:Inventory','Expected 68 iEEG files');
channelRows={};fileRows={};trialRows={};clockStart=tic;oldThreads=maxNumCompThreads(1);cleanup=onCleanup(@()maxNumCompThreads(oldThreads)); %#ok<NASGU>
try
 for fi=1:numel(files)
  path=fullfile(files(fi).folder,files(fi).name);base=erase(path,'_ieeg.edf');C=readtsv([base '_channels.tsv']);E=readtsv([base '_events.tsv']);J=jsondecode(fileread([base '_ieeg.json']));readPath=compatible_path(path,out);I=edfinfo(readPath);
  labels=string(I.SignalLabels(:));rates=double(I.NumSamples(:))/seconds(I.DataRecordDuration);n=double(I.NumSamples(:))*double(I.NumDataRecords);fs=rates(1);[p,q]=rat(2000/fs);
  header=isequal(labels,string(C.name(:)))&&numel(labels)==height(C)&&all(n==E.endSample(end))&&all(rates==fs)&&all(C.sampling_frequency==fs)&&J.SamplingFrequency==fs&&ismember(fs,[2000 4000 4096]);
  lengths=E.endSample-E.begSample+1;trialLength=all(lengths==8*fs)&&all(E.begSample>=1)&&all(E.endSample<=n(1));
  if fs==2000,assert(p==1&&q==1);elseif fs==4000,assert(p==1&&q==2);elseif fs==4096,assert(p==125&&q==256);end
  one=struct('file',string(path),'native_fs_hz',fs,'analysis_fs_hz',2000,'resample_p',p,'resample_q',q,'channels',numel(labels),'samples',n(1),'events_last_end_sample',E.endSample(end),'header_channel_order_match',isequal(labels,string(C.name(:))),'fs_sources_agree',all(rates==fs)&&all(C.sampling_frequency==fs)&&J.SamplingFrequency==fs,'native_rate_allowed',ismember(fs,[2000 4000 4096]),'native_trial_lengths_passed',trialLength,'header_passed',header&&trialLength,'passed',false,'provenance_json',string(jsonencode(meta)));
  if ~(header&&trialLength),fileRows{end+1}=one;writefiles();error('IEEG:AmendedEDFHeaderGate','Amended EDF header/trial gate failed: %s',path);end
  TT=edfread(readPath);assert(width(TT)==height(C),'IEEG:EDFChannelCount','EDF channel count differs');X=zeros(n(1),height(C));passed=true;
  for ci=1:height(C)
   raw=TT.(TT.Properties.VariableNames{ci});if iscell(raw),raw=cellfun(@(a)double(a(:)),raw,'UniformOutput',false);x=vertcat(raw{:});else,x=double(raw(:));end
   u=unit(I.PhysicalDimensions(ci));declared=unit(C.units(ci));unitsOK=strcmpi(declared,'uV')&&(strlength(u)==0||strcmpi(u,'uV'));source="EDF and channels.tsv";if strlength(u)==0,source="channels.tsv; EDF dimension blank";u="<blank>";end
   v=var(x);med=median(abs(x));ok=unitsOK&&numel(x)==n(1)&&all(isfinite(x))&&isfinite(v)&&v>0&&med<1e4;passed=passed&&ok;
   channelRows{end+1}=struct('file',string(path),'channel_index',ci,'channel',labels(ci),'physical_units',u,'declared_units',declared,'units_source',source,'native_fs_hz',fs,'samples',numel(x),'nonfinite_samples',sum(~isfinite(x)),'variance_uv2',v,'median_absolute_uv',med,'min_uv',min(x),'max_uv',max(x),'passed',ok,'provenance_json',string(jsonencode(meta))); %#ok<AGROW>
   if numel(x)==n(1),X(:,ci)=x;end
  end
  clear TT x raw;
  if ~passed,fileRows{end+1}=one;writefiles();error('IEEG:AmendedEDFSignalGate','Amended EDF signal gate failed: %s',path);end
  for ti=1:height(E)
   epoch=X(E.begSample(ti):E.endSample(ti),:);if fs~=2000,epoch=resample(epoch,p,q);end
   outputOK=size(epoch,1)==16000&&size(epoch,2)==height(C)&&all(isfinite(epoch),'all');
   trialRows{end+1}=struct('file',string(path),'trial',E.nTrial(ti),'native_fs_hz',fs,'native_samples',lengths(ti),'resample_p',p,'resample_q',q,'output_fs_hz',2000,'output_samples',size(epoch,1),'channels',size(epoch,2),'passed',outputOK,'provenance_json',string(jsonencode(meta))); %#ok<AGROW>
   if ~outputOK,writefiles();error('IEEG:ResampleLength','Trialwise resample check failed: %s trial %d',path,ti);end
  end
  one.passed=true;fileRows{end+1}=one;writefiles();clear X epoch;
  fprintf('AMENDMENT1 EDF PASS %d/%d fs%g p/q%d/%d %s\n',fi,numel(files),fs,p,q,files(fi).name);
 end
 writejson(fullfile(out,'edf_reading_gate_attempt2.json'),struct('passed',true,'files',numel(files),'channels',numel(channelRows),'resampled_trial_checks',numel(trialRows),'elapsed_seconds',toc(clockStart),'provenance',meta));
 copyfile(fullfile(out,'edf_file_checks_attempt2.csv'),fullfile(out,'edf_file_checks.csv'));copyfile(fullfile(out,'edf_channel_checks_attempt2.csv'),fullfile(out,'edf_channel_checks.csv'));
 fprintf('AMENDMENT1 ALL 68 iEEG READING AND RESAMPLING GATES PASS\n');
catch err
 writejson(fullfile(out,'reading_gate_attempt2_failure.json'),struct('status','FAILED_STOP','identifier',err.identifier,'message',err.message,'elapsed_seconds',toc(clockStart),'provenance',meta));rethrow(err);
end
 function writefiles
  if ~isempty(fileRows),writetable(struct2table(vertcat(fileRows{:})),fullfile(out,'edf_file_checks_attempt2.csv'));end
  if ~isempty(channelRows),writetable(struct2table(vertcat(channelRows{:})),fullfile(out,'edf_channel_checks_attempt2.csv'));end
  if ~isempty(trialRows),writetable(struct2table(vertcat(trialRows{:})),fullfile(out,'resampling_trial_checks_attempt2.csv'));end
 end
end
function T=readtsv(path)
T=readtable(path,'FileType','text','Delimiter','\t','ReadVariableNames',true,'VariableNamingRule','preserve','TextType','string','Encoding','UTF-8');
end
function s=unit(s)
s=string(s);s=strrep(strrep(strtrim(s),char(181),'u'),char(956),'u');
end
function value=compatible_path(path,out)
value=path;m=jsondecode(fileread(fullfile(out,'edf_header_copies.json')));
for k=1:numel(m.files),if strcmpi(path,m.files(k).original_path),assert(m.files(k).payload_byte_identical);value=m.files(k).read_path;return;end;end
end
function writejson(path,s)
f=fopen(path,'w','n','UTF-8');assert(f~=-1);clean=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(s));
end
