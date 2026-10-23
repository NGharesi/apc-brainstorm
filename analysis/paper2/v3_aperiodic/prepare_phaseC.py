"""Lock reuse of existing bouts/channels/prep; no new state/channel choices."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
O=Path(__file__).resolve().parent;R=O.parent.parent;sys.path.insert(0,str(R/'pydeps'))
import pandas as pd
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((O/'phaseB_implementation.json').read_text(encoding='utf-8'));C=json.loads((O/'criteria_decisions.json').read_text(encoding='utf-8'))['criteria'];assert C['A1']['passed'] and all(z['passed'] for z in C['A3']) and C['A4']['passed']
dest=O/'phaseC';assert not dest.exists();dest.mkdir();jobs=[];mapping=[];seen={};files=[]
for label,folder,prefix in [('prespecified_5s',R/'revision_checks/rodent_multi','regional'),('POST_HOC_2s',R/'revision_checks/rodent_multi/posthoc_2s','posthoc_2s')]:
    for tail in ['bout_estimates.csv','bouts.csv','session_eligibility.csv']:
        p=folder/(prefix+'_'+tail);files.append(dict(path=str(p),sha256=sha(p)))
    D=pd.read_csv(folder/(prefix+'_bout_estimates.csv'),encoding='utf-8',float_precision='round_trip');D=D[D.method.eq('APC-v1.0')]
    for _,row in D.iterrows():
        meta=json.loads(row.provenance_json);key=(row.session,int(row.channel_index),int(meta['start_idx']),int(meta['stop_idx']))
        if key not in seen:
            ident=len(jobs)+1;seen[key]=ident;jobs.append(dict(input_id=ident,session=key[0],channel_index=key[1],start_idx=key[2],stop_idx=key[3],source_file=meta['source_file']))
        mapping.append(dict(input_id=seen[key],bout_set=label,animal=row.animal,session=row.session,analysis=row.analysis,channel_index=int(row.channel_index),region=row.region,shank=row.shank,state=row.state,bout=int(row.bout),duration_s=row.duration_s,lfp_duration_s=row.lfp_duration_s))
pd.DataFrame(jobs).to_csv(dest/'rodent_inputs.csv',index=False,encoding='utf-8');pd.DataFrame(mapping).to_csv(dest/'rodent_analysis_rows.csv',index=False,encoding='utf-8')
E=R/'revision_checks/ecog_miller_motor'
for name in ['bouts.csv','electrodes.csv','ecog_bout_estimates.csv','analysed_rest_spectral_peaks.csv','ecog_statistics.py','ecog_postprocess.m']:
    p=E/name;files.append(dict(path=str(p),sha256=sha(p)))
for p in sorted((E/'prep').glob('*.mat')):files.append(dict(path=str(p),sha256=sha(p)))
for name in ['compute_regional_statistics.py','fit_regional_mixed_models.m','v1_bout_features.m']:
    p=R/'revision_checks/rodent_multi'/name;files.append(dict(path=str(p),sha256=sha(p)))
for name in ['posthoc_2s_statistics.py','posthoc_2s_fit_mixed_models.m']:
    p=R/'revision_checks/rodent_multi/posthoc_2s'/name;files.append(dict(path=str(p),sha256=sha(p)))
m.update(stage='PHASE_C_AUTHORIZED_AFTER_A1_A3_A4_PASS',phaseC_prepared_utc=datetime.now(timezone.utc).isoformat(),reused_files_sha256=files,rodent_unique_physical_inputs=len(jobs),rodent_analysis_rows=len(mapping),ECoG_options=dict(fA=[80,150],version='v3',minPhaseHz=1,maxPhaseHz=30),rodent_options=dict(fA=[80,150],version='v3'),statistics_seeds=dict(rodent=20261022,ECoG=20261024),ECoG_spectral_peak='Reuse unchanged analysed_rest_spectral_peaks.csv, original 8-30 Hz residual PSD peak rule',rodent_shared_inputs='Same physical start/stop/channel input reused across analyses and bout sets, with one new v3 estimate')
(dest/'provenance.json').write_text(json.dumps(m,indent=2),encoding='utf-8');print(json.dumps(dict(rodent_unique_inputs=len(jobs),rodent_analysis_rows=len(mapping),ecog_inputs=2648,shared_reuse=len(mapping)-len(jobs))),flush=True)
