function [reference,reproduction]=paper2_ecog_v1_reference(signal,time,saved,boutKey,m)
% Recompute the original v1 reference once; preserve exact returned bands.
O=fileparts(mfilename('fullpath'));dest=fullfile(O,'ecog_v1_references');if ~isfolder(dest),mkdir(dest);end
file=fullfile(dest,char(boutKey+".mat"));options=struct('fA',[80 150],'minPhaseHz',6,'maxPhaseHz',30);paper2_error_context('context',boutKey,1);
if isfile(file)
 q=load(file,'reference','reproduction','verified','m');paper2_assert(q.verified,'Paper2:ReferenceCheckpoint','Reference checkpoint is not verified',q.verified,true,1,boutKey);paper2_assert(strcmp(q.m.git_head,m.git_head),'Paper2:ReferenceCheckpoint','Reference checkpoint commit mismatch',q.m.git_head,m.git_head,1,boutKey);reference=q.reference;reproduction=q.reproduction;return;
end
[s,info]=bst_apc(struct('data',double(signal(:).'),'time',double(time(:).')),options);
reference=struct('fp',s.phase_frequency_hz.Value,'fa',s.amplitude_frequency_hz.Value,'raw',s.pac_strength.Value,'pref',s.preferred_phase_deg.Value,'status',s.status_code.Value,'band',info.final_band_hz,'route',string(info.route),'normalized_saved',saved.ozkurt_mvl);
observed=[reference.fp reference.fa reference.raw reference.pref reference.status];expected=[saved.fP_hz saved.fA_hz saved.raw_mvl saved.preferred_phase_deg saved.status];
tolerance=[1e-10 0 1e-10 1e-10 0];names=["fP_hz","fA_hz","raw_mvl","preferred_phase_deg","status"];checks=false(1,5);
for j=1:5,checks(j)=(isnan(observed(j))&&isnan(expected(j)))||(isfinite(observed(j))&&isfinite(expected(j))&&abs(observed(j)-expected(j))<=tolerance(j));end
reproduction=struct('key',boutKey,'method',"APC-v1.0",'source_index',1,'observed_fp_hz',observed(1),'saved_fp_hz',expected(1),'observed_fa_hz',observed(2),'saved_fa_hz',expected(2),'observed_raw_mvl',observed(3),'saved_raw_mvl',expected(3),'observed_preferred_phase_deg',observed(4),'saved_preferred_phase_deg',expected(4),'observed_status',observed(5),'saved_status',expected(5),'band_low_hz',reference.band(1),'band_high_hz',reference.band(2),'pass',all(checks),'git_commit',string(m.git_head),'protocol_sha256',string(m.protocol_sha256),'options_json',string(jsonencode(options)),'matlab_version',string(version),'provenance_file',"provenance.json");
verified=false;save(file,'s','info','reference','reproduction','observed','expected','checks','verified','m','-v7.3');
for j=1:5,paper2_assert(checks(j),'Paper2:ECoGV1Reproducibility',char("Recomputed ECoG v1 "+names(j)+" differs from saved CSV; tolerance "+tolerance(j)),observed(j),expected(j),1,boutKey);end
verified=true;save(file,'s','info','reference','reproduction','observed','expected','checks','verified','m','-v7.3');
end
