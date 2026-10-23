"""Run progress session once, then automatic fixed partitions and stop monitoring."""
from pathlib import Path
from datetime import datetime,timezone
import json,subprocess,time,sys
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O.parent.parent/'pydeps'))
import pandas as pd
MATLAB=r'C:\Program Files\MATLAB\R2022b\bin\matlab.exe'
m=json.loads((O/'analysis_provenance.json').read_text(encoding='utf-8'))
stamp=dict(git_head=m['git_head'],protocol_sha256=m['protocol_sha256'],seed=20261023,provenance_file='analysis_provenance.json')
start=time.monotonic()
def launch(worker):
    log=O/f'am4_worker{worker}_matlab.log'
    return subprocess.Popen([MATLAB,'-batch',f"addpath('{O.as_posix()}'); ieeg_am4_worker({worker},3)",'-logfile',str(log)],cwd=str(O),stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
assert not (O/'ieeg_trial_estimates.csv').exists()
p=launch(0);p.wait()
if p.returncode:
    (O/'am4_pipeline_runtime.json').write_text(json.dumps(dict(status='FAILED_PROGRESS_WORKER',returncode=p.returncode,provenance=stamp),indent=2),encoding='utf-8');sys.exit(1)
progress=json.loads((O/'am4_sub01_ses01_progress_check.json').read_text(encoding='utf-8'));assert progress['status']=='COMPLETE'
print('PROGRESS CHECK (not a gate): '+json.dumps(progress['apc_status_counts_indexed_from_zero']),flush=True)
jobs={w:launch(w) for w in [1,2,3]};last_completed=0
while any(p.poll() is None for p in jobs.values()):
    time.sleep(15)
    if (O/'METHOD_STOP_FLAG.json').exists():continue
    # Counts are monitored only after additional full-run sessions finish.
    completed=0
    for w in jobs:
        log=O/f'am4_worker{w}_matlab.log'
        if log.exists():completed+=log.read_text(encoding='utf-8',errors='replace').count('AM4 SESSION COMPLETE')
    if completed<=last_completed:continue
    last_completed=completed
    csv=O/'ieeg_trial_estimates.csv'
    try:d=pd.read_csv(csv,usecols=['analysis','patient','session','trial','method','status','score'],encoding='utf-8')
    except pd.errors.ParserError:continue # another worker may still be appending
    if d.duplicated(['analysis','patient','session','trial','method']).any():raise RuntimeError('Duplicate estimates')
    rates=[]
    for (a,method),g in d.groupby(['analysis','method']):
        invalid=(g.status.ne(0)|g.score.isna())
        rates.append(dict(analysis=a,method=method,n_completed=len(g),invalid=int(invalid.sum()),fraction_invalid=float(invalid.mean())))
    snapshot=dict(utc=datetime.now(timezone.utc).isoformat(),completed_full_run_sessions=completed,provenance=stamp,rates=rates)
    (O/'am4_failure_monitor_latest.json').write_text(json.dumps(snapshot,indent=2),encoding='utf-8')
    if any(r['fraction_invalid']>.5 for r in rates):
        snapshot.update(identifier='IEEG:MostTrialsInvalid',message='Most completed trials invalid for a method in an analysed signal set; protocol 6.4')
        (O/'METHOD_STOP_FLAG.json').write_text(json.dumps(snapshot,indent=2),encoding='utf-8')
        (O/'am4_failure_first_snapshot.json').write_text(json.dumps(snapshot,indent=2),encoding='utf-8')
        print('METHOD STOP: '+json.dumps(rates),flush=True)
    else:print('MONITOR completed sessions '+str(completed)+' '+json.dumps([r for r in rates if r['method']=='APC-v1.0']),flush=True)
codes={w:p.wait() for w,p in jobs.items()};result=dict(status='COMPLETE' if all(v==0 for v in codes.values()) and not (O/'METHOD_STOP_FLAG.json').exists() else 'STOPPED',returncodes=codes,elapsed_seconds=time.monotonic()-start,provenance=stamp)
(O/'am4_pipeline_runtime.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result),flush=True)
sys.exit(0 if result['status']=='COMPLETE' else 1)
