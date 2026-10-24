from pathlib import Path
import sys,json,time,subprocess,datetime
O=Path(__file__).resolve().parent
def status():
 raw=subprocess.check_output([sys.executable,str(O/'progress.py')],encoding='utf-8')
 return json.loads(raw)
def execute(name):
 print(json.dumps({'stage':'START','script':name,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}),flush=True)
 with (O/(name+'.log')).open('w',encoding='utf-8') as log:
  r=subprocess.run([sys.executable,'-u',str(O/name)],stdout=log,stderr=subprocess.STDOUT,encoding='utf-8',cwd=O)
 if r.returncode:
  print(json.dumps({'stage':'ERROR','script':name,'returncode':r.returncode,'log':str(O/(name+'.log'))}),flush=True)
  raise SystemExit(r.returncode)
 print(json.dumps({'stage':'COMPLETE','script':name}),flush=True)
while True:
 s=status();print(json.dumps(s,separators=(',',':')),flush=True)
 if s['active_errors'] or s['active_stop']:
  print('WORKFLOW PAUSED FOR ERROR REVIEW',flush=True);raise SystemExit(1)
 if s['sim_workers_complete']==4 and s['real_workers_complete']==4:break
 time.sleep(45)
assert not (O/'statistics_complete.json').exists(),'Do not repeat reportable statistics'
execute('validation_statistics.py')
execute('validation_report.py')
print('READY_FOR_VISUAL_QA_AND_FINAL_VERIFICATION',flush=True)
