function ieeg_preprocess_candidates
% Common input preparation only: no spectra, contact choice or PAC output.
out=fileparts(mfilename('fullpath'));cd(out);meta=jsondecode(fileread(fullfile(out,'provenance.json')));gate=jsondecode(fileread(fullfile(out,'timeline_gate_confirmation.json')));assert(gate.passed,'IEEG:GateOrder','Timeline must pass');
cache=fullfile(out,'preprocessing');if ~isfolder(cache),mkdir(cache);end
C=readtable(fullfile(out,'metadata_candidate_pairs.csv'),'Delimiter',',','ReadVariableNames',true,'VariableNamingRule','preserve','TextType','string','Encoding','UTF-8');C=C(:,{'patient','deeper_contact','adjacent_contact','prefix','k','deeper_labels','adjacent_labels'});
F=readtable(fullfile(out,'edf_file_checks_attempt2.csv'),'Delimiter',',','ReadVariableNames',true,'VariableNamingRule','preserve','TextType','string','Encoding','UTF-8');
notches=cell(3,1);guards=struct([]);
for j=1:3
 centre=50*j;[z,p,k]=butter(2,[centre-1 centre+1]/1000,'stop');[sos,g]=zp2sos(z,p,k);
 % A fourth-order digital bandstop has four poles (prototype order 2).
 assert(numel(p)==4&&max(abs(p))<1,'IEEG:NotchGuard','Notch order or pole guard failed');
 notches{j}=struct('sos',sos,'g',g);one=struct('fs_hz',2000,'notch_hz',centre,'half_width_hz',1,'digital_filter_order',numel(p),'butter_prototype_order',2,'max_pole_radius',max(abs(p)),'passed',true,'provenance_json',string(jsonencode(meta)));guards=[guards;one]; %#ok<AGROW>
end
writetable(struct2table(guards),fullfile(out,'notch_filter_guards.csv'));progress={};start=tic;
try
 for fi=1:height(F)
  path=char(F.file(fi));patient=string(regexp(path,'sub-\d+','match','once'));session=string(regexp(path,'ses-\d+','match','once'));P=C(C.patient==patient,:);if isempty(P),continue;end
  dest=fullfile(cache,char(patient+"_"+session+".mat"));
  if isfile(dest)
   saved=load(dest,'metadata');assert(strcmp(saved.metadata.protocol_sha256,meta.protocol_sha256),'IEEG:PreprocessCache','Protocol differs from saved preprocessing');
   fprintf('PREPROCESS CACHE %s %s\n',patient,session);continue;
  end
  contacts=unique([P.deeper_contact;P.adjacent_contact],'stable');base=erase(path,'_ieeg.edf');E=readtsv([base '_events.tsv']);nativeFs=F.native_fs_hz(fi);[p,q]=rat(2000/nativeFs);
  TT=edfread(compatible_path(path,out),'SelectedSignals',cellstr(contacts));X=zeros(E.endSample(end),numel(contacts));
  for ci=1:numel(contacts)
   name=matlab.lang.makeValidName(contacts(ci));assert(ismember(name,string(TT.Properties.VariableNames)),'IEEG:ContactRead','Selected contact not found');raw=TT.(char(name));
   if iscell(raw),raw=cellfun(@(a)double(a(:)),raw,'UniformOutput',false);v=vertcat(raw{:});else,v=double(raw(:));end
   assert(numel(v)==size(X,1)&&all(isfinite(v)));X(:,ci)=v;
  end
  clear TT raw v;
  bipolar=zeros(6000,height(E),height(P));reference=bipolar;
  for ti=1:height(E)
   trial=X(E.begSample(ti):E.endSample(ti),:);if nativeFs~=2000,trial=resample(trial,p,q);end;assert(size(trial,1)==16000,'IEEG:ResampleLength','Expected 16000 samples');
   for pi=1:height(P)
    a=find(contacts==P.deeper_contact(pi),1);b=find(contacts==P.adjacent_contact(pi),1);
    y=trial(:,a)-trial(:,b);y=y-mean(y);r=trial(:,a);r=r-mean(r);
    for j=1:3,d=notches{j};y=filtfilt(d.sos,d.g,y);r=filtfilt(d.sos,d.g,r);end
    assert(all(isfinite(y))&&all(isfinite(r)),'IEEG:NotchOutput','Notch output nonfinite');bipolar(:,ti,pi)=y(6001:12000);reference(:,ti,pi)=r(6001:12000);
   end
  end
  metadata=meta;metadata.patient=patient;metadata.session=session;metadata.source_file=path;metadata.native_fs_hz=nativeFs;metadata.analysis_fs_hz=2000;metadata.window_samples=[6001,12000];metadata.notch_digital_order=4;metadata.notch_butter_prototype_order=2;metadata.notch_half_width_hz=1;metadata.preparation_only_no_spectra_or_PAC=true;
  pairs=P;events=E;save(dest,'bipolar','reference','pairs','events','metadata','-v7.3');
  progress{end+1}=struct('patient',patient,'session',session,'candidate_pairs',height(P),'trials',height(E),'native_fs_hz',nativeFs,'cache_file',string(dest),'provenance_json',string(jsonencode(meta)));writetable(struct2table(vertcat(progress{:})),fullfile(out,'preprocessing_progress.csv')); %#ok<AGROW>
  fprintf('PREPROCESS %d/%d %s %s trials%d pairs%d\n',fi,height(F),patient,session,height(E),height(P));clear X trial bipolar reference;
 end
 writejson(fullfile(out,'preprocessing_runtime.json'),struct('status','COMPLETE','elapsed_seconds',toc(start),'cache_files',numel(dir(fullfile(cache,'*.mat'))),'provenance',meta));
catch err
 writejson(fullfile(out,'preprocessing_failure.json'),struct('status','FAILED_STOP','identifier',err.identifier,'message',err.message,'elapsed_seconds',toc(start),'provenance',meta));rethrow(err);
end
end
function T=readtsv(path)
T=readtable(path,'FileType','text','Delimiter','\t','ReadVariableNames',true,'VariableNamingRule','preserve','TextType','string','Encoding','UTF-8');
end
function value=compatible_path(path,out)
value=path;m=jsondecode(fileread(fullfile(out,'edf_header_copies.json')));for k=1:numel(m.files),if strcmpi(path,m.files(k).original_path),assert(m.files(k).payload_byte_identical);value=m.files(k).read_path;return;end;end
end
function writejson(path,s)
f=fopen(path,'w','n','UTF-8');assert(f~=-1);clean=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(s));
end
