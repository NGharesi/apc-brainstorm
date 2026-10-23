function run_final_analysis(stage)
if nargin<1,stage='all';end
root='C:\Users\nghare\.brainstorm\process';out=fullfile(root,'revision_checks','final');
cd(out);addpath(out,'-begin');addpath(fullfile(out,'frozen_v1'),'-begin');clear bst_apc calc_MI_all_methods
assert(strcmp(which('bst_apc'),fullfile(out,'frozen_v1','bst_apc.m')));
start=tic;options=struct('fA',[80 150]);
meta=jsondecode(fileread(fullfile(out,'source_provenance.json')));meta.matlab_version=version;meta.seed=20261022;
meta.comparator_settings=struct('phase_grid_hz',4:.5:12,'phase_half_width_hz',1.5,'amplitude_grid_hz',80:4:148,'amplitude_half_width_hz',12,'filter','butter(4), filtfilt (8th-order bandpass)','metrics',{{'MVL-raw','MVL-Ozkurt','KLMI','GLM'}},'phase_bins',18,'selection','independent full-grid maximum; first column-major tie','ozkurt','raw_MVL/sqrt(mean(A.^2))');
if strcmp(stage,'all')
S=load(fullfile(root,'apc_ec013_run_rest_results.mat'),'results');base=S.results;
assert(height(base.run.bouts)==12&&height(base.rest.bouts)==12);
rows=struct([]);boutRows=struct([]);outputs=cell(24,1);details=cell(24,1);maps=cell(24,1);i=0;
for state=["run","rest"]
 bouts=base.(state).bouts;
 for b=1:height(bouts)
  i=i+1;idx=bouts.start_idx(b):bouts.stop_idx(b);x=double(base.signal_window(idx));t=double(base.signal_time(idx));fs=1/median(diff(t));
  boutRows(i).state=state;boutRows(i).bout=b;boutRows(i).start_idx=bouts.start_idx(b);boutRows(i).stop_idx=bouts.stop_idx(b);boutRows(i).start_s=t(1);boutRows(i).stop_s=t(end);boutRows(i).duration_s=bouts.duration_s(b);boutRows(i).n_samples=numel(idx);
  [a,r]=bst_apc(struct('data',x,'time',t),options);
  [ad,rd]=final_v1_diagnostics(struct('data',x,'time',t),options);assert(isequaln(a,ad));d=rd.diagnostics{1};rd=rmfield(rd,'diagnostics');assert(isequaln(r,rd));
  assert(a.status_code.Value==0,'Final:MethodFailure','APC failed on %s bout %d status %d',state,b,a.status_code.Value);
  oz=a.pac_strength.Value/sqrt(mean(d.amplitude_envelope.^2));v=mean(d.amplitude_envelope.*exp(1i*d.phase_angles));assert(abs(abs(v)-a.pac_strength.Value)<1e-12);
  meta.apc_options=r.options;
  row=pack(state,b,bouts.duration_s(b),"APC v1.0",a.phase_frequency_hz.Value,a.amplitude_frequency_hz.Value,a.pac_strength.Value,a.pac_strength.Value,oz,a.preferred_phase_deg.Value,meta);
  rows=[rows;row];[c,maps{i}]=final_comparators(x,fs); %#ok<AGROW>
  for k=1:numel(c),rows=[rows;pack(state,b,bouts.duration_s(b),c(k).method,c(k).fp,c(k).fa,c(k).score,c(k).raw_mvl,c(k).ozkurt_mvl,c(k).preferred_phase_deg,meta)];end %#ok<AGROW>
  outputs{i}=struct('apc',a,'runInfo',r);details{i}=d;
  fprintf('RODENT %d/24 %s %d fP=%.8g fA=%.8g\n',i,state,b,a.phase_frequency_hz.Value,a.amplitude_frequency_hz.Value);
  save(fullfile(out,'rodent_checkpoint.mat'),'rows','boutRows','outputs','details','maps','meta','-v7.3');
 end
end
T=struct2table(rows);writetable(T,fullfile(out,'rodent_bouts.csv'));
B=struct2table(boutRows);B.git_commit=repmat(string(meta.git_commit),height(B),1);B.provenance_json=repmat(string(jsonencode(meta)),height(B),1);writetable(B,fullfile(out,'bout_definitions.csv'));
writejson(fullfile(out,'analysis_provenance.json'),meta);
else
meta=jsondecode(fileread(fullfile(out,'analysis_provenance.json')));
end
canonical=struct([]);caseNames=["burst_coupled","timing_null","jittered","continuous_pac"];
for k=1:numel(caseNames)
 name=caseNames(k);I=readtable(fullfile(out,name+"_input.csv"),'Delimiter',',','VariableNamingRule','preserve');s=struct('data',I.signal.','time',I.time_s.');
 [a,r]=bst_apc(s,options);[ad,rd]=final_v1_diagnostics(s,options);assert(isequaln(a,ad));d=rd.diagnostics{1};rr=rmfield(rd,'diagnostics');assert(isequaln(r,rr));
 assert(a.status_code.Value==0,'Final:MethodFailure','Canonical %s status %d',name,a.status_code.Value);
 oz=a.pac_strength.Value/sqrt(mean(d.amplitude_envelope.^2));
 canonical=[canonical;pack(name,1,20,"APC v1.0",a.phase_frequency_hz.Value,a.amplitude_frequency_hz.Value,a.pac_strength.Value,a.pac_strength.Value,oz,a.preferred_phase_deg.Value,meta)]; %#ok<AGROW>
 save(fullfile(out,name+"_diagnostics.mat"),'d','a','r','meta','-v7');
 fs=1/median(diff(I.time_s));nfft=max(256,2^nextpow2(max(numel(d.burst_average),ceil(fs/r.options.fPMaxBinSpacingHz))));
 [power,freq]=pwelch(d.burst_average(:)-mean(d.burst_average),[],[],nfft,fs);
 export_curve(fullfile(out,name+"_burst_average.csv"),d.time_epoch(:),d.burst_average(:),'time_s','amplitude',meta);
 export_curve(fullfile(out,name+"_spectrum.csv"),freq,power,'frequency_hz','power',meta);
 export_curve(fullfile(out,name+"_trough_average.csv"),d.phase_epoch_time(:),d.phase_locked_average(:),'time_s','amplitude',meta);
 export_curve(fullfile(out,name+"_fa_score.csv"),d.fa_grid(:),d.fa_score(:),'frequency_hz','score',meta);
 traces=table(I.time_s,I.signal,d.burst_trace(:),d.phase_signal(:),d.amplitude_envelope(:),'VariableNames',{'time_s','signal','burst_trace','phase_signal','amplitude_envelope'});traces.git_commit=repmat(string(meta.git_commit),height(traces),1);traces.provenance_json=repmat(string(jsonencode(meta)),height(traces),1);writetable(traces,fullfile(out,name+"_traces.csv"));
 fprintf('CANONICAL %s fP=%.8g fA=%.8g\n',name,a.phase_frequency_hz.Value,a.amplitude_frequency_hz.Value);
end
writetable(struct2table(canonical),fullfile(out,'canonical_results.csv'));
writejson(fullfile(out,'analysis_runtime.json'),struct('status','COMPLETE','stage',stage,'elapsed_seconds',toc(start),'provenance',meta));
end
function row=pack(state,b,duration,method,fp,fa,score,raw,oz,pref,meta)
row=struct('session',"ec013.157",'state',state,'bout',b,'duration_s',duration,'method',method,'fP_hz',fp,'fA_hz',fa,'score',score,'raw_mvl',raw,'ozkurt_mvl',oz,'preferred_phase_deg',pref,'boundary_fP_4',double(fp==4),'boundary_fP_12',double(fp==12),'git_commit',string(meta.git_commit),'matlab_version',string(meta.matlab_version),'seed',meta.seed,'provenance_json',string(jsonencode(meta)));
end
function export_curve(path,x,y,xname,yname,meta)
T=table(x,y,'VariableNames',{xname,yname});T.git_commit=repmat(string(meta.git_commit),height(T),1);T.provenance_json=repmat(string(jsonencode(meta)),height(T),1);writetable(T,path);
end
function writejson(path,s)
fid=fopen(path,'w','n','UTF-8');assert(fid>0);c=onCleanup(@()fclose(fid));fprintf(fid,'%s\n',jsonencode(s));
end
