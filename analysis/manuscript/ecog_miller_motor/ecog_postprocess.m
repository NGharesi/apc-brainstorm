function ecog_postprocess
% Supplemental recorded diagnostics and analysed-rest spectra, no APC reruns.
R=fileparts(mfilename('fullpath'));root=fileparts(fileparts(R));cd(R);addpath(fullfile(root,'revision_checks','ieeg_ds004752'));addpath(fullfile(root,'apc-brainstorm-publish','src'),'-begin');
assert(~isfile(fullfile(R,'STOP_METHOD')),'ECOG:Stopped','Method stop flag present');m=jsondecode(fileread(fullfile(R,'provenance.json')));P=load(fullfile(R,'progress_check.mat'),'canonicalInfo');opts=P.canonicalInfo.options;
% Confirm detector count against an existing canonical output, no estimator call.
V=load(fullfile(R,'equivalence_gate.mat'));fields=fieldnames(V);expected=NaN;
for j=1:numel(fields),item=V.(fields{j});if isstruct(item)&&isfield(item,'n_bursts'),expected=item.n_bursts.Value;end;end
T=readtable(fullfile(root,'revision_checks','final','burst_coupled_input.csv'),'Delimiter',',','ReadVariableNames',true,'NumHeaderLines',0,'Encoding','UTF-8');observed=ieeg_count_bursts(T.signal,T.time_s,opts);assert(isfinite(expected)&&observed==expected,'ECOG:BurstDiagnostic','Diagnostic count differs from saved canonical count');
B=readtable(fullfile(R,'bouts.csv'),'TextType','string','Encoding','UTF-8');B=B(logical(B.analysed),:);pts=unique(B.patient,'stable');rows={};peaks={};start=tic;
for pi=1:numel(pts)
 pt=pts(pi);S=load(fullfile(R,'prep',char(pt+".mat")));J=B(B.patient==pt,:);
 for ri=["movement","imagery"]
  K=J(J.recording==ri,:);if isempty(K),continue;end;sig=S.sig;if ri=="imagery",sig=S.sigI;end;assert(~isempty(sig));
  psdSum=zeros(501,1);nrest=0;
  for b=1:height(K)
   seg=sig(K.start_sample(b):K.end_sample(b));time=(0:numel(seg)-1)/S.fs;nb=ieeg_count_bursts(seg,time,opts);
   rows{end+1}=struct('patient',pt,'recording',ri,'bout',K.bout(b),'n_bursts',nb,'git_head',string(m.git_head),'protocol_sha256',string(m.protocol_sha256),'seed',20261024); %#ok<AGROW>
   if K.state(b)=="rest",[px,f]=pwelch(seg,hann(1000),500,1000,S.fs);psdSum=psdSum+px;nrest=nrest+1;end
  end
  meanPSD=psdSum/nrest;idx=f>=8&f<=30;coef=polyfit(log10(f(idx)),log10(meanPSD(idx)),1);res=log10(meanPSD(idx))-polyval(coef,log10(f(idx)));ff=f(idx);[heightPeak,k]=max(res);
  peaks{end+1}=struct('patient',pt,'recording',ri,'rest_bouts',nrest,'rest_spectral_peak_hz',ff(k),'peak_log10_residual',heightPeak,'git_head',string(m.git_head),'protocol_sha256',string(m.protocol_sha256),'seed',20261024); %#ok<AGROW>
  fprintf('POSTPROCESS %s %s bouts%d rest%d\n',pt,ri,height(K),nrest);
 end
end
writetable(struct2table(vertcat(rows{:})),fullfile(R,'bout_burst_counts.csv'));writetable(struct2table(vertcat(peaks{:})),fullfile(R,'analysed_rest_spectral_peaks.csv'));
result=struct('status','COMPLETE','elapsed_seconds',toc(start),'canonical_saved_bursts',expected,'canonical_detector_bursts',observed,'APC_estimator_calls',0,'git_head',m.git_head,'protocol_sha256',m.protocol_sha256,'seed',20261024);f=fopen(fullfile(R,'postprocess_runtime.json'),'w','n','UTF-8');fprintf(f,'%s\n',jsonencode(result));fclose(f);
end
