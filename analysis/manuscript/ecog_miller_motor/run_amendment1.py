"""Run the fixed progress check then four original worker partitions."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,time,sys,hashlib
O=Path(__file__).resolve().parent;MATLAB=r'C:\Program Files\MATLAB\R2022b\bin\matlab.exe'
m=json.loads((O/'provenance.json').read_text(encoding='utf-8'));start=time.monotonic()
assert not (O/'STOP_METHOD').exists() and not (O/'STOP_RUNNER').exists()
pins=['v1_bout_features_ecog.m','ecog_worker.m','ecog_comparators.m','ecog_progress_check.m','run_amendment1.py']
m['amendment1_frozen_code_sha256']={n:hashlib.sha256((O/n).read_bytes()).hexdigest() for n in pins};m['amendment1_frozen_utc']=datetime.now(timezone.utc).isoformat();m['status']='RUNNING_AMENDMENT1'
(O/'analysis_provenance.json').write_text(json.dumps(m,indent=2),encoding='utf-8');(O/'provenance.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
def launch(command,log):
    return subprocess.Popen([MATLAB,'-singleCompThread','-batch',f"addpath('{O.as_posix()}'); {command}",'-logfile',str(O/'logs'/log)],cwd=O,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
p=launch('ecog_progress_check','progress_matlab.log');p.wait()
if p.returncode:
    (O/'amendment1_runtime.json').write_text(json.dumps(dict(status='FAILED_PROGRESS_CHECK',returncode=p.returncode,elapsed_seconds=time.monotonic()-start),indent=2),encoding='utf-8');sys.exit(1)
print('PROGRESS '+(O/'progress_check.json').read_text(encoding='utf-8'),flush=True)
jobs={w:launch(f'ecog_worker({w},4)',f'worker{w}_matlab.log') for w in range(1,5)}
while any(p.poll() is None for p in jobs.values()):
    time.sleep(10)
    if (O/'STOP_METHOD').exists():continue
    failed={w:p.poll() for w,p in jobs.items() if p.poll() not in (None,0)}
    if failed:
        # Stop peers on any error; classification is reported without automatic reruns.
        (O/'STOP_METHOD').write_text(json.dumps(dict(reason='Worker exception; inspect method/tooling classification before any resume',returncodes=failed)),encoding='utf-8')
codes={w:p.wait() for w,p in jobs.items()};result=dict(status='STOPPED' if (O/'STOP_METHOD').exists() or any(codes.values()) else 'COMPLETE',returncodes=codes,elapsed_seconds=time.monotonic()-start,git_head=m['git_head'],protocol_sha256=m['protocol_sha256'],seed=20261024)
(O/'amendment1_runtime.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result),flush=True)
sys.exit(0 if result['status']=='COMPLETE' else 1)
