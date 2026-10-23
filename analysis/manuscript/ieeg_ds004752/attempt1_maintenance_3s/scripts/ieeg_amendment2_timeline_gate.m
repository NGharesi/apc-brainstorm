function ieeg_amendment2_timeline_gate
% Scalp-only timing check: trialwise resample to 200 Hz. No PAC computation.
out=fileparts(mfilename('fullpath'));cd(out);meta=jsondecode(fileread(fullfile(out,'provenance.json')));gate=jsondecode(fileread(fullfile(out,'edf_reading_gate_attempt2.json')));assert(gate.passed,'IEEG:GateOrder','All iEEG reading gates must pass');clockStart=tic;
files=dir(fullfile(meta.data_root,'sub-*','ses-*','eeg','*_eeg.edf'));[~,order]=sort(string(fullfile({files.folder},{files.name})));files=files(order);assert(numel(files)==68,'IEEG:ScalpInventory','Expected 68 scalp files');
total=zeros(1600,1);squares=total;count=0;fileRows={};trialRows={};
try
 for fi=1:numel(files)
  path=fullfile(files(fi).folder,files(fi).name);base=erase(path,'_eeg.edf');C=readtsv([base '_channels.tsv']);E=readtsv([base '_events.tsv']);J=jsondecode(fileread([base '_eeg.json']));I=edfinfo(compatible_path(path,out));
  labels=string(I.SignalLabels(:));rates=double(I.NumSamples(:))/seconds(I.DataRecordDuration);fs=rates(1);[p,q]=rat(200/fs);
  assert(isequal(labels,string(C.name(:)))&&all(rates==fs)&&all(C.sampling_frequency==fs)&&J.SamplingFrequency==fs&&ismember(fs,[200 2000 4000 4096]),'IEEG:ScalpHeader','Scalp header/channel/JSON rate or channel order mismatch: %s',path);
  assert(all(E.endSample-E.begSample+1==8*fs)&&all(double(I.NumSamples(:))*double(I.NumDataRecords)==E.endSample(end)),'IEEG:ScalpTrialLength','Scalp sample/trial length mismatch');
  if fs==200,assert(p==1&&q==1);elseif fs==2000,assert(p==1&&q==10);elseif fs==4000,assert(p==1&&q==20);elseif fs==4096,assert(p==25&&q==512);end
  chosen=find(ismember(upper(string(C.name)),["O1","O2","OZ"]));assert(~isempty(chosen),'IEEG:NoOccipital','No O1/O2/Oz: %s',path);
  TT=edfread(compatible_path(path,out),'SelectedSignals',cellstr(labels(chosen)));x=zeros(E.endSample(end),numel(chosen));
  for ci=1:numel(chosen)
   raw=TT.(TT.Properties.VariableNames{ci});if iscell(raw),raw=cellfun(@(a)double(a(:)),raw,'UniformOutput',false);v=vertcat(raw{:});else,v=double(raw(:));end
   assert(numel(v)==size(x,1)&&all(isfinite(v))&&var(v)>0,'IEEG:ScalpData','Scalp channel samples invalid');x(:,ci)=v;
  end
  for ti=1:height(E)
   epoch=x(E.begSample(ti):E.endSample(ti),:);if fs~=200,epoch=resample(epoch,p,q);end
   assert(size(epoch,1)==1600&&all(isfinite(epoch),'all'),'IEEG:ScalpResample','Scalp resample must produce 1600 finite samples');epoch=epoch-mean(epoch(1:200,:),1);v=mean(epoch,2);total=total+v;squares=squares+v.^2;count=count+1;
   trialRows{end+1}=struct('file',string(path),'trial',E.nTrial(ti),'native_fs_hz',fs,'resample_p',p,'resample_q',q,'output_fs_hz',200,'output_samples',size(epoch,1),'passed',true,'provenance_json',string(jsonencode(meta))); %#ok<AGROW>
  end
  fileRows{end+1}=struct('file',string(path),'native_fs_hz',fs,'resample_p',p,'resample_q',q,'output_fs_hz',200,'trials',height(E),'channels',strjoin(labels(chosen),';'),'passed',true,'provenance_json',string(jsonencode(meta))); %#ok<AGROW>
  writetable(struct2table(vertcat(fileRows{:})),fullfile(out,'timeline_file_checks.csv'));writetable(struct2table(vertcat(trialRows{:})),fullfile(out,'timeline_resampling_trial_checks.csv'));
  fprintf('SCALP TIMELINE READ %d/68 fs%g p/q%d/%d %s\n',fi,fs,p,q,files(fi).name);clear TT x raw epoch;
 end
 time=(0:1599)'/200;grand=total/count;sem=sqrt(max(0,(squares-total.^2/count)/(count-1))/count);
 T=table(time,grand,sem,repmat(count,1600,1),repmat(string(jsonencode(meta)),1600,1),'VariableNames',{'time_s','grand_average_uv','trial_sem_uv','trial_count','provenance_json'});writetable(T,fullfile(out,'timeline_grand_average.csv'));
 peaks={};
 for onset=[1,6]
  keep=find(time>=onset+.05&time<=onset+.25);baseline=mean(grand(time>=onset-.2&time<onset));[~,j]=max(abs(grand(keep)-baseline));idx=keep(j);
  peaks{end+1}=struct('expected_onset_s',onset,'peak_time_s',time(idx),'latency_ms',round(1000*(time(idx)-onset)/5)*5,'peak_uv',grand(idx),'preonset_mean_uv',baseline,'absolute_peak_difference_uv',abs(grand(idx)-baseline)); %#ok<AGROW>
 end
 writejson(fullfile(out,'timeline_gate_measurements.json'),struct('status','REQUIRES_VISUAL_AND_PAPER_CONFIRMATION','trials',count,'files',numel(files),'latency_resolution_ms',5,'peaks',vertcat(peaks{:}),'elapsed_seconds',toc(clockStart),'processing','Each scalp trial resampled to 200 Hz by Amendment 2; no additional filter; fixation-mean subtraction per trial/channel; O1/O2/Oz averaged per trial; equal trial weights','peak_rule','largest absolute deviation from preceding 200-ms mean within 50-250 ms after each prespecified onset','provenance',meta));
 fprintf('SCALP TIMELINE READY trials%d\n',count);
catch err
 writejson(fullfile(out,'timeline_gate_failure.json'),struct('status','FAILED_STOP','identifier',err.identifier,'message',err.message,'elapsed_seconds',toc(clockStart),'provenance',meta));rethrow(err);
end
end
function T=readtsv(path)
T=readtable(path,'FileType','text','Delimiter','\t','ReadVariableNames',true,'VariableNamingRule','preserve','TextType','string','Encoding','UTF-8');
end
function value=compatible_path(path,out)
value=path;m=jsondecode(fileread(fullfile(out,'edf_header_copies.json')));
for k=1:numel(m.files),if strcmpi(path,m.files(k).original_path),assert(m.files(k).payload_byte_identical);value=m.files(k).read_path;return;end;end
end
function writejson(path,s)
f=fopen(path,'w','n','UTF-8');assert(f~=-1);clean=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(s));
end
