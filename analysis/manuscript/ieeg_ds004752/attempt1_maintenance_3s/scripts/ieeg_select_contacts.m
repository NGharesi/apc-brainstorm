function ieeg_select_contacts
out=fileparts(mfilename('fullpath'));cd(out);m=jsondecode(fileread(fullfile(out,'provenance.json')));assert(strcmp(m.protocol_sha256,'087c51b1e5b930dca55e3c1ce63af15c891252399a3da1abc68407b27a2df308'));
gate=jsondecode(fileread(fullfile(out,'timeline_gate_confirmation.json')));assert(gate.passed);start=tic;
cache=dir(fullfile(out,'preprocessing','*.mat'));assert(numel(cache)==62);patients=unique(string(regexp({cache.name},'sub-\d+','match','once')));counts={};rankRows={};contactRows={};inclusions={};spectra={};sessions={};
try
 for patient=patients(:).'
  files=cache(startsWith(string({cache.name}),patient+"_"));S=cell(numel(files),1);
  for s=1:numel(files),S{s}=load(fullfile(files(s).folder,files(s).name));end
  P=S{1}.pairs;np=height(P);ns=numel(S);masks=cell(ns,np);sumPSD=zeros(1001,np);nPSD=zeros(np,1);
  for s=1:ns
   D=S{s};assert(isequal(D.pairs.deeper_contact,P.deeper_contact));flag=D.events.Artifact==1;
   for k=1:np
    x=D.bipolar(:,:,k);pool=x(:,~flag);assert(~isempty(pool),'IEEG:NoUnflaggedTrials','No dataset-unflagged trials');centre=median(pool(:));sd=1.4826*median(abs(pool(:)-centre));dx=diff(x,1,1);poold=dx(:,~flag);dc=median(poold(:));dsd=1.4826*median(abs(poold(:)-dc));
    badAmp=any(abs(x-centre)>6*sd,1).';badDiff=any(abs(dx)>6*dsd,1).';keep=~flag&~badAmp&~badDiff;
    masks{s,k}=struct('flag',flag,'badAmp',badAmp,'badDiff',badDiff,'keep',keep,'centre',centre,'sd',sd,'diffCentre',dc,'diffSD',dsd);
    for t=find(keep).',[psd,f]=pwelch(x(:,t),hann(2000),1000,2000,2000);sumPSD(:,k)=sumPSD(:,k)+psd;nPSD(k)=nPSD(k)+1;end
    counts{end+1}=struct('patient',patient,'session',D.metadata.session,'candidate_index',k,'deeper_contact',P.deeper_contact(k),'adjacent_contact',P.adjacent_contact(k),'trials',height(D.events),'dataset_artifact',sum(flag),'amplitude_reject_unflagged',sum(~flag&badAmp),'difference_reject_unflagged',sum(~flag&badDiff),'both_robust_reject_unflagged',sum(~flag&badAmp&badDiff),'retained_trials',sum(keep),'session_median_uv',centre,'robust_sd_uv',sd,'difference_median_uv',dc,'difference_robust_sd_uv',dsd,'provenance_json',string(jsonencode(m))); %#ok<AGROW>
   end
  end
  ratios=nan(np,1);for k=1:np,if nPSD(k)>0,av=sumPSD(:,k)/nPSD(k);ratios(k)=trapz(f(f>=4&f<=8),av(f>=4&f<=8))/trapz(f(f>=1&f<=4),av(f>=1&f<=4));end;end
  valid=find(isfinite(ratios));assert(~isempty(valid),'IEEG:NoCandidateSpectrum','No retained trials for any candidate');best=max(ratios(valid));ties=find(ratios==best);[~,j]=min(P.k(ties));selected=ties(j);
  for k=1:np,rankRows{end+1}=struct('patient',patient,'candidate_index',k,'deeper_contact',P.deeper_contact(k),'adjacent_contact',P.adjacent_contact(k),'k',P.k(k),'retained_trials_total',nPSD(k),'theta_delta_ratio',ratios(k),'selected',k==selected,'provenance_json',string(jsonencode(m)));end %#ok<AGROW>
  eligible=0;native=[];
  for s=1:ns
   D=S{s};Q=masks{s,selected};eligible=eligible+(sum(Q.keep)>=20);native(end+1)=D.metadata.native_fs_hz; %#ok<AGROW>
   for analysis=["primary","artifact_only","referential"]
    keep=Q.keep;if analysis=="artifact_only",keep=~Q.flag;end
    sessions{end+1}=struct('analysis',analysis,'patient',patient,'session',D.metadata.session,'retained_trials',sum(keep),'eligible',sum(keep)>=20,'native_fs_hz',D.metadata.native_fs_hz,'candidate_index',selected,'provenance_json',string(jsonencode(m))); %#ok<AGROW>
    for t=1:height(D.events)
     inclusions{end+1}=struct('analysis',analysis,'patient',patient,'session',D.metadata.session,'trial',D.events.nTrial(t),'SetSize',D.events.SetSize(t),'Correct',D.events.Correct(t),'dataset_artifact',Q.flag(t),'amplitude_reject',Q.badAmp(t),'difference_reject',Q.badDiff(t),'retained',keep(t),'session_eligible',sum(keep)>=20,'candidate_index',selected,'native_fs_hz',D.metadata.native_fs_hz,'cache_file',string(fullfile(files(s).folder,files(s).name)),'provenance_json',string(jsonencode(m))); %#ok<AGROW>
    end
    x=D.bipolar(:,:,selected);if analysis=="referential",x=D.reference(:,:,selected);end
    if any(keep),[pwr,freq]=pwelch(x(:,keep),hann(2000),1000,2000,2000);pwr=mean(pwr,2);idx=freq>=2&freq<=12;coef=polyfit(log10(freq(idx)),log10(pwr(idx)),1);residual=log10(pwr(idx))-polyval(coef,log10(freq(idx)));ff=freq(idx);[~,pk]=max(residual);peak=ff(pk);else,pwr=nan(1001,1);freq=(0:1000)';peak=NaN;end
    spectra{end+1}=struct('analysis',analysis,'patient',patient,'session',D.metadata.session,'spectral_peak_hz',peak,'retained_trials',sum(keep),'frequency_hz',freq,'mean_psd',pwr); %#ok<AGROW>
   end
  end
  assert(numel(unique(native))==1,'IEEG:MixedNativePatient','Patient has mixed native rates');
  contactRows{end+1}=struct('patient',patient,'deeper_contact',P.deeper_contact(selected),'adjacent_contact',P.adjacent_contact(selected),'deeper_labels',P.deeper_labels(selected),'adjacent_labels',P.adjacent_labels(selected),'candidate_index',selected,'candidate_pairs',np,'theta_delta_ratio',ratios(selected),'retained_trials',nPSD(selected),'eligible_sessions',eligible,'patient_eligible',eligible>=2,'native_fs_hz',native(1),'exclusion_reason',"",'provenance_json',string(jsonencode(m))); %#ok<AGROW>
  fprintf('CONTACT FIXED %s %s-%s retained%d eligible_sessions%d\n',patient,P.deeper_contact(selected),P.adjacent_contact(selected),nPSD(selected),eligible);
  selection=struct('patient',patient,'selected_candidate',selected,'pairs',P,'masks',{masks},'files',{cellstr(string(fullfile({files.folder},{files.name})))},'ratios',ratios,'retained_counts',nPSD,'provenance',m);save(fullfile(out,char("selection_"+patient+".mat")),'selection','-v7.3');
 end
 C=struct2table(vertcat(contactRows{:}));missing=C(1,:);missing.patient="sub-13";missing.deeper_contact="";missing.adjacent_contact="";missing.deeper_labels="";missing.adjacent_labels="";missing.candidate_index=NaN;missing.candidate_pairs=0;missing.theta_delta_ratio=NaN;missing.retained_trials=0;missing.eligible_sessions=0;missing.patient_eligible=false;missing.native_fs_hz=4096;missing.exclusion_reason="No Hipp-labelled candidate pair";C=[C;missing];C=sortrows(C,'patient');writetable(C,fullfile(out,'contacts.csv'));
 I=struct2table(vertcat(inclusions{:}));SE=struct2table(vertcat(sessions{:}));PE={};
 for analysis=unique(SE.analysis).',for patient=unique(SE.patient).',v=SE(SE.analysis==analysis&SE.patient==patient,:);ok=sum(v.eligible)>=2;PE{end+1}=struct('analysis',analysis,'patient',patient,'eligible_sessions',sum(v.eligible),'patient_eligible',ok,'native_fs_hz',v.native_fs_hz(1),'provenance_json',string(jsonencode(m)));I.patient_eligible(I.analysis==analysis&I.patient==patient)=ok;end;end %#ok<AGROW>
 I.included=I.retained&I.session_eligible&I.patient_eligible;writetable(I,fullfile(out,'trial_inclusion.csv'));writetable(SE,fullfile(out,'session_eligibility.csv'));writetable(struct2table(vertcat(PE{:})),fullfile(out,'patient_eligibility.csv'));
 writetable(struct2table(vertcat(counts{:})),fullfile(out,'candidate_trial_counts.csv'));writetable(struct2table(vertcat(rankRows{:})),fullfile(out,'candidate_rankings.csv'));
 save(fullfile(out,'selected_session_spectra.mat'),'spectra','m','-v7.3');SP=struct2table(vertcat(spectra{:}));SP.frequency_hz=[];SP.mean_psd=[];SP.provenance_json=repmat(string(jsonencode(m)),height(SP),1);writetable(SP,fullfile(out,'session_spectral_peaks.csv'));
 writejson(fullfile(out,'selection_runtime.json'),struct('status','COMPLETE','elapsed_seconds',toc(start),'contact_patients',height(C),'candidate_session_counts',numel(counts),'trial_inclusion_rows',height(I),'included_rows',sum(I.included),'provenance',m));
catch err
 writejson(fullfile(out,'selection_failure.json'),struct('status','FAILED_STOP','identifier',err.identifier,'message',err.message,'provenance',m));rethrow(err);
end
end
function writejson(path,s)
f=fopen(path,'w','n','UTF-8');assert(f~=-1);clean=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(s));
end
