from pathlib import Path
from datetime import datetime,timezone
import json,subprocess,sys,time
O=Path(__file__).resolve().parent
while True:
 counts={s:len(list((O/'checkpoints').glob(s+'_*.mat'))) for s in ['V3','V1','V2','V4']};errors=[]
 for p in O.glob('worker*_error.json'):
  d=json.loads(p.read_text(encoding='utf-8'));errors.append({k:d.get(k) for k in ['key','identifier','message']})
 done=len(list(O.glob('worker*_complete.json')));print(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'classification':'exploratory','checkpoints':counts,'workers_complete':done,'errors':errors}),flush=True)
 if errors or (O/'STOPPED.md').exists():raise SystemExit(1)
 if done==4:break
 time.sleep(45)
with (O/'noflip_analysis.log').open('w',encoding='utf-8') as f:r=subprocess.run([sys.executable,str(O/'noflip_analysis.py')],cwd=O,stdout=f,stderr=subprocess.STDOUT)
print(json.dumps({'analysis_exit_code':r.returncode}),flush=True);raise SystemExit(r.returncode)
