"""Metadata-only recovery: never calls the already completed statistical routines."""
from pathlib import Path
from datetime import datetime, timezone
import sys, json, hashlib, time
O = Path(__file__).resolve().parent
sys.path.insert(0, str(O.parent.parent / 'pydeps'))
import pandas as pd
start = time.perf_counter()
P = json.loads((O/'provenance.json').read_text(encoding='utf-8'))
manifest = json.loads((O/'tooling_statistics_collation_attempt1/computed_statistics_manifest.json').read_text(encoding='utf-8'))
for row in manifest:
    assert hashlib.sha256((O/row['path']).read_bytes()).hexdigest() == row['sha256'], row['path']
assert not (O/'statistics_complete.json').exists() and not (O/'STOP_RUN.md').exists()
read = lambda name: pd.read_csv(O/name, encoding='utf-8', float_precision='round_trip')
parts = []
for endpoint, name in [('P-A','P_A.csv'),('P-B','P_B.csv'),('P-C','P_C.csv'),('Recovery','recovery_overall.csv'),('Specificity','false_joint_recovery.csv'),('AUC','coupling_auc.csv'),('Calibrated','calibrated_specificity.csv'),('Rodent','rodent_across_session_statistics.csv'),('ECoG','ecog_summary.csv')]:
    q = read(name)
    q.insert(0, 'endpoint_family', endpoint)
    parts.append(q)
pd.concat(parts, ignore_index=True, sort=False).to_csv(O/'statistics.csv', index=False, encoding='utf-8', float_format='%.17g')
sim = read('simulation_trial_estimates.csv'); rodent = read('rodent_bout_estimates.csv'); ecog = read('ecog_bout_estimates.csv')
assert len(sim)==22500 and sim.key.nunique()==1875 and len(rodent)==15928 and ecog.key.nunique()==2642
r=P['statistics_collation_recovery']
elapsed=(datetime.fromisoformat(r['original_statistics_error_log_mtime_utc'])-datetime.fromisoformat(r['original_statistics_subprocess_start_utc'])).total_seconds()
result={'status':'COMPLETE','elapsed_seconds':elapsed,'elapsed_seconds_basis':'original statistics subprocess wall start to error-log modification; no statistical calculations repeated','collation_recovery_seconds':time.perf_counter()-start,'completed_utc':datetime.now(timezone.utc).isoformat(),'simulation_inputs':1875,'simulation_rows':22500,'rodent_analysis_rows':len(rodent),'ecog_bouts':2642,'decisions':[{k:v for k,v in row.items() if pd.notna(v)} for row in read('primary_decisions.csv').drop(columns=['git_commit','protocol_sha256','provenance_file']).to_dict('records')],'computed_statistics_csvs_unchanged':len(manifest),'git_commit':P['git_head'],'protocol_sha256':P['protocol_sha256']}
(O/'statistics_complete.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
