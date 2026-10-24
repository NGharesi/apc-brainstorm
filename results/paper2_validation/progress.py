from pathlib import Path
import json,hashlib,datetime
O=Path(__file__).resolve().parent
history=O/'tooling_diagnostic_container_attempt1'
counts={s:len(list((O/'checkpoints').glob(s+'_*.mat'))) for s in ['V1','V2','V3','V4']}
real={s:len(list((O/'real_checkpoints').glob(s+'*.mat'))) for s in ['rodent_','ecog_']}
errors=[]
for p in [*O.glob('worker*_error.json'),*O.glob('real_worker*_error.json')]:
 old=history/p.name
 if old.exists() and old.read_bytes()==p.read_bytes():continue
 d=json.loads(p.read_text(encoding='utf-8'));errors.append({k:d.get(k) for k in ['worker','key','identifier','message']})
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'simulation_checkpoints':counts,'real_checkpoints':real,'active_errors':errors,'active_stop':(O/'STOP_RUN.md').exists(),'sim_workers_complete':len(list(O.glob('worker*_complete.json'))),'real_workers_complete':len(list(O.glob('real_worker*_complete.json')))},indent=2))
