function ecog_progress_check
% First ten bp bouts are computed once and seeded into the worker's resume CSV.
R=fileparts(mfilename('fullpath'));root=fileparts(fileparts(R));repo=fullfile(root,'apc-brainstorm-publish');cd(R);
addpath(fullfile(root,'revision_checks','final'));addpath(fullfile(root,'revision_checks','rodent_multi'));addpath(R);addpath(fullfile(repo,'src'),'-begin');clear bst_apc calc_MI_all_methods final_sos_filter;
assert(strcmpi(which('bst_apc'),fullfile(repo,'src','bst_apc.m')));assert(strcmpi(which('v1_bout_features_ecog'),fullfile(R,'v1_bout_features_ecog.m')));
m=jsondecode(fileread(fullfile(R,'provenance.json')));start=tic;
% Synthetic reconstruction check uses the exact copied asserts; no data setting changes.
T=readtable(fullfile(root,'revision_checks','final','burst_coupled_input.csv'),'VariableNamingRule','preserve','Encoding','UTF-8');[canonical,canonicalInfo]=v1_bout_features_ecog(T.signal,T.time_s);assert(canonical.status==0,'ECOG:ReconstructionCheck','Canonical wrapper check invalid');
S=load(fullfile(R,'prep','bp.mat'));B=S.B(S.B.analysed,:);B=B(1:10,:);features=cell(10,1);infos=cell(10,1);
for b=1:10
 seg=S.sig(B.start_sample(b):B.end_sample(b));t=(0:numel(seg)-1)/S.fs;[features{b},infos{b}]=v1_bout_features_ecog(seg,t);
 fprintf('BP PROGRESS bout%d state%s status%d fP %.17g Hz\n',B.bout(b),B.state(b),features{b}.status,features{b}.fP_hz);
end
z=vertcat(features{:});statuses=[z.status];fprintf('BP PROGRESS STATUS COUNTS status0=%d status1=%d status2=%d status3=%d status4=%d status5=%d; NOT A GATE; CONTINUE UNCHANGED\n',arrayfun(@(k)sum(statuses==k),0:5));
save(fullfile(R,'progress_check.mat'),'features','infos','B','canonical','canonicalInfo','m','-v7');
result=struct('git_head',m.git_head,'protocol_sha256',m.protocol_sha256,'seed',20261024,'patient','bp','recording','movement','bouts',B.bout.','status',statuses,'fP_hz',[z.fP_hz],'canonical_status',canonical.status,'valid_bout_reconstruction_asserts_passed',sum(statuses==0),'progress_not_gate',true,'elapsed_seconds',toc(start));writejson(fullfile(R,'progress_check.json'),result);
file=fullfile(R,'estimates_w1.csv');assert(~isfile(file));fid=fopen(file,'w','n','UTF-8');clean=onCleanup(@()fclose(fid));
fprintf(fid,'key,patient,recording,bout,state,movement_type,code,rest_index,duration_s,method,fP_hz,fA_hz,score,raw_mvl,ozkurt_mvl,preferred_phase_deg,status,route,n_bursts,boundary_fp_low,boundary_fp_high,boundary_fa_low,boundary_fa_high\n');
for b=1:10
 key=sprintf('bp_movement_%03d',B.bout(b));a=features{b};bf=[abs(a.fP_hz-6)<=.05,abs(a.fP_hz-30)<=.05,a.fA_hz==80,a.fA_hz==150];writeRow(fid,key,B(b,:),a.method,a.fP_hz,a.fA_hz,a.score,a.raw_mvl,a.ozkurt_mvl,a.preferred_phase_deg,a.status,a.route,bf);
 seg=S.sig(B.start_sample(b):B.end_sample(b));c=ecog_comparators(seg,S.fs,"ecog","ecog_A2_prime",.5);
 for k=1:4,a=c(k);bf=[a.fp==6,a.fp==30,a.fa==80,a.fa==148];writeRow(fid,key,B(b,:),a.method,a.fp,a.fa,a.score,a.raw_mvl,a.ozkurt_mvl,a.preferred_phase_deg,a.status,"not_applicable",bf);end
end
G=final_sos_filter('registry');writetable(struct2table(G),fullfile(R,'filter_guards_progress.csv'));fprintf('BP PROGRESS CACHE COMPLETE: 10 complete keys; worker 1 resumes without repeating them\n');
end
function writeRow(fid,key,Bb,method,fp,fa,score,raw,oz,pref,status,route,bf)
fprintf(fid,'%s,bp,movement,%d,%s,%s,%d,%d,%.6f,%s,%.15g,%.15g,%.15g,%.15g,%.15g,%.15g,%d,%s,NaN,%d,%d,%d,%d\n',key,Bb.bout,Bb.state,Bb.movement_type,Bb.code,Bb.rest_index,Bb.duration_s,method,fp,fa,score,raw,oz,pref,status,string(route),bf);
end
function writejson(path,value)
f=fopen(path,'w','n','UTF-8');clean=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(value));
end
