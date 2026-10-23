function ieeg_am4_preprocess
% Amendment 4 preparation; contacts and original masks are immutable inputs.
out=fileparts(mfilename('fullpath'));cd(out);m=jsondecode(fileread(fullfile(out,'provenance.json')));
assert(strcmp(m.protocol_sha256,'95b741822ac085bb96a01f1a5396674b83ecfaa827c199708e95490ad9f70ad3'));
gate=jsondecode(fileread(fullfile(out,'timeline_gate_confirmation.json')));assert(gate.passed);
C=readcsv(fullfile(out,'am4_contacts.csv'));I=readcsv(fullfile(out,'am4_am3_mask.csv'));I=I(I.analysis=="primary",:);
F=readcsv(fullfile(out,'edf_file_checks_attempt2.csv'));cache=fullfile(out,'preprocessing_amendment4');if ~isfolder(cache),mkdir(cache);end
stamp=struct('git_head',m.git_head,'protocol_sha256',m.protocol_sha256,'seed',20261023,'provenance_file','provenance.json');pj=string(jsonencode(stamp));
notches=cell(3,1);guards={};
for j=1:3
 [z,p,k]=butter(2,[50*j-1,50*j+1]/1000,'stop');[sos,g]=zp2sos(z,p,k);assert(numel(p)==4&&max(abs(p))<1,'IEEG:NotchGuard','Notch guard failed');notches{j}=struct('sos',sos,'g',g);
 guards{j}=struct('fs_hz',2000,'notch_hz',50*j,'half_width_hz',1,'digital_order',4,'max_pole_radius',max(abs(p)),'passed',true,'provenance_json',pj);
end
writetable(struct2table(vertcat(guards{:})),fullfile(out,'am4_notch_filter_guards.csv'));inclusions={};sessions={};templatesAudit={};start=tic;
try
 for fi=1:height(F)
  path=char(F.file(fi));patient=string(regexp(path,'sub-\d+','match','once'));session=string(regexp(path,'ses-\d+','match','once'));c=C(C.patient==patient,:);if isempty(c),continue;end
  dest=fullfile(cache,char(patient+"_"+session+".mat"));assert(~isfile(dest),'IEEG:PreparationAlreadyExists','Use explicit verified cache resume after tooling interruption');
  old=I(I.patient==patient&I.session==session,:);base=erase(path,'_ieeg.edf');events=readtable([base '_events.tsv'],'FileType','text','Delimiter','\t','VariableNamingRule','preserve','TextType','string','Encoding','UTF-8');
  assert(height(old)==height(events)&&isequal(double(old.trial),double(events.nTrial)),'IEEG:MaskAlignment','Amendment-3 trial alignment differs');
  contacts=[c.deeper_contact;c.adjacent_contact];TT=edfread(compatible_path(path,out),'SelectedSignals',cellstr(contacts));X=zeros(events.endSample(end),2);
  for ci=1:2
   name=matlab.lang.makeValidName(contacts(ci));raw=TT.(char(name));if iscell(raw),v=vertcat(raw{:});else,v=raw(:);end;X(:,ci)=double(v(:));
  end
  assert(all(isfinite(X(:))));clear TT raw v;
  nativeFs=F.native_fs_hz(fi);[p,q]=rat(2000/nativeFs);bipolar=zeros(12000,height(events));reference=bipolar;
  for ti=1:height(events)
   trial=X(events.begSample(ti):events.endSample(ti),:);if nativeFs~=2000,trial=resample(trial,p,q);end;assert(size(trial,1)==16000,'IEEG:ResampleLength','Not 16000 samples');
   y=trial(:,1)-trial(:,2);r=trial(:,1);y=y-mean(y);r=r-mean(r);
   for j=1:3,d=notches{j};y=filtfilt(d.sos,d.g,y);r=filtfilt(d.sos,d.g,r);end
   assert(all(isfinite(y))&&all(isfinite(r)));bipolar(:,ti)=y(1:12000);reference(:,ti)=r(1:12000);
  end
  clear X trial;
  flag=events.Artifact==1;oldkeep=bool(old.retained);qb=robust_mask(bipolar,flag);qr=robust_mask(reference,flag);signals=struct;means=struct;masks=struct;
  for analysis=["primary","artifact_only","referential"]
   raw=bipolar;Q=qb;keep=oldkeep&Q.keep;if analysis=="referential",raw=reference;Q=qr;keep=oldkeep&Q.keep;elseif analysis=="artifact_only",keep=~flag;end
   if any(keep),template=mean(raw(:,keep),2);else,template=nan(12000,1);end
   signals.(analysis)=raw-template;means.(analysis)=template;masks.(analysis)=keep;
   err=NaN;if any(keep),err=max(abs(mean(signals.(analysis)(:,keep),2)));assert(err<1e-10*max(1,max(abs(raw(:)))),'IEEG:EvokedSubtraction','Included residual mean nonzero');end
   templatesAudit{end+1}=struct('analysis',analysis,'patient',patient,'session',session,'retained_trials',sum(keep),'included_residual_mean_max_abs_uv',err,'template_rms_uv',sqrt(mean(template.^2)),'window_start_s',0,'window_stop_s',6,'samples',12000,'provenance_json',pj); %#ok<AGROW>
   sessions{end+1}=struct('analysis',analysis,'patient',patient,'session',session,'retained_trials',sum(keep),'eligible',sum(keep)>=20,'native_fs_hz',nativeFs,'candidate_index',c.candidate_index,'cache_file',string(dest),'provenance_json',pj); %#ok<AGROW>
   for ti=1:height(events)
    inclusions{end+1}=struct('analysis',analysis,'patient',patient,'session',session,'trial',events.nTrial(ti),'SetSize',events.SetSize(ti),'Correct',events.Correct(ti),'dataset_artifact',flag(ti),'am3_amplitude_reject',bool(old.amplitude_reject(ti)),'am3_difference_reject',bool(old.difference_reject(ti)),'am3_retained',oldkeep(ti),'am4_amplitude_reject',Q.badAmp(ti),'am4_difference_reject',Q.badDiff(ti),'am4_session_median_uv',Q.centre,'am4_robust_sd_uv',Q.sd,'am4_difference_median_uv',Q.diffCentre,'am4_difference_robust_sd_uv',Q.diffSD,'robust_rules_applied',analysis~="artifact_only",'retained',keep(ti),'session_eligible',sum(keep)>=20,'candidate_index',c.candidate_index,'native_fs_hz',nativeFs,'cache_file',string(dest),'provenance_json',pj); %#ok<AGROW>
   end
  end
  metadata=stamp;metadata.source_file=path;metadata.native_fs_hz=nativeFs;metadata.analysis_fs_hz=2000;metadata.window_samples=[1 12000];metadata.analysis_window_s=[0 6];metadata.notch_order=4;metadata.full_trial_demean_before_notch=true;metadata.evoked_mean_per_analysis=true;metadata.selected_contacts=contacts;
  save(dest,'signals','means','masks','bipolar','reference','events','metadata','-v7.3');
  fprintf('AM4 PREPARED %s %s primary%d artifact%d reference%d\n',patient,session,sum(masks.primary),sum(masks.artifact_only),sum(masks.referential));
 end
 T=struct2table(vertcat(inclusions{:}));SE=struct2table(vertcat(sessions{:}));PE={};
 for analysis=unique(SE.analysis).',for patient=unique(SE.patient).'
  v=SE(SE.analysis==analysis&SE.patient==patient,:);ok=sum(v.eligible)>=2;PE{end+1}=struct('analysis',analysis,'patient',patient,'eligible_sessions',sum(v.eligible),'patient_eligible',ok,'native_fs_hz',v.native_fs_hz(1),'provenance_json',pj);T.patient_eligible(T.analysis==analysis&T.patient==patient)=ok; %#ok<AGROW>
 end;end
 T.included=T.retained&T.session_eligible&T.patient_eligible;writetable(T,fullfile(out,'trial_inclusion_amendment4.csv'));writetable(SE,fullfile(out,'session_eligibility_amendment4.csv'));writetable(struct2table(vertcat(PE{:})),fullfile(out,'patient_eligibility_amendment4.csv'));writetable(struct2table(vertcat(templatesAudit{:})),fullfile(out,'am4_evoked_template_audit.csv'));
 % Spectra after evoked subtraction, using retained trials in eligible sessions/patients.
 spectra={};for si=1:height(SE)
  v=SE(si,:);J=T(T.analysis==v.analysis&T.patient==v.patient&T.session==v.session,:);if ~any(J.included),continue;end
  D=load(v.cache_file,'signals','events');keep=bool(J.included);assert(isequal(double(J.trial),double(D.events.nTrial)));
  [pwr,freq]=pwelch(D.signals.(v.analysis)(:,keep),hann(2000),1000,2000,2000);pwr=mean(pwr,2);idx=freq>=1&freq<=12;assert(all(isfinite(pwr(idx))&pwr(idx)>0),'IEEG:SpectrumInvalid','Invalid spectrum');coef=polyfit(log10(freq(idx)),log10(pwr(idx)),1);residual=log10(pwr(idx))-polyval(coef,log10(freq(idx)));ff=freq(idx);[~,pk]=max(residual);
  spectra{end+1}=struct('analysis',v.analysis,'patient',v.patient,'session',v.session,'spectral_peak_hz',ff(pk),'retained_trials',sum(keep),'frequency_hz',freq,'mean_psd',pwr,'loglog_fit',coef,'provenance_json',pj); %#ok<AGROW>
 end
 save(fullfile(out,'am4_selected_session_spectra.mat'),'spectra','m','-v7.3');SP=struct2table(vertcat(spectra{:}));SP.frequency_hz=[];SP.mean_psd=[];SP.loglog_fit=[];writetable(SP,fullfile(out,'am4_session_spectral_peaks.csv'));
 writejson(fullfile(out,'am4_preprocessing_runtime.json'),struct('status','COMPLETE','elapsed_seconds',toc(start),'sessions',height(SE)/3,'inclusion_rows',height(T),'included_rows',sum(T.included),'provenance',stamp));
catch err
 writejson(fullfile(out,'am4_preprocessing_failure.json'),struct('status','FAILED_STOP','identifier',err.identifier,'message',err.message,'elapsed_seconds',toc(start),'provenance',stamp));rethrow(err);
end
end
function q=robust_mask(x,flag)
pool=x(:,~flag);assert(~isempty(pool),'IEEG:NoUnflaggedTrials','No unflagged trials');centre=median(pool(:));sd=1.4826*median(abs(pool(:)-centre));dx=diff(x,1,1);poold=dx(:,~flag);dc=median(poold(:));dsd=1.4826*median(abs(poold(:)-dc));assert(sd>0&&dsd>0,'IEEG:DegenerateRobustScale','Zero robust scale');badAmp=any(abs(x-centre)>6*sd,1).';badDiff=any(abs(dx)>6*dsd,1).';q=struct('badAmp',badAmp,'badDiff',badDiff,'keep',~flag&~badAmp&~badDiff,'centre',centre,'sd',sd,'diffCentre',dc,'diffSD',dsd);
end
function b=bool(x),b=ismember(lower(string(x)),["true","1"]);end
function T=readcsv(path),T=readtable(path,'Delimiter',',','ReadVariableNames',true,'VariableNamingRule','preserve','TextType','string','Encoding','UTF-8');end
function value=compatible_path(path,out)
value=path;m=jsondecode(fileread(fullfile(out,'edf_header_copies.json')));for k=1:numel(m.files),if strcmpi(path,m.files(k).original_path),assert(m.files(k).payload_byte_identical);value=m.files(k).read_path;return;end;end
end
function writejson(path,s)
f=fopen(path,'w','n','UTF-8');assert(f~=-1);clean=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(s));
end
