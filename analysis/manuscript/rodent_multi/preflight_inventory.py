from pathlib import Path
import sys,json,csv,hashlib,subprocess,time
ROOT=Path(r'C:\Users\nghare\.brainstorm\process');OUT=ROOT/'revision_checks/rodent_multi';DATA=Path(r'D:\APC_project\RealDatasets\LFP_data');REAL=DATA.parent
sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
from scipy.io import loadmat,whosmat
import h5py
START=time.perf_counter()
GIT=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def git(*a):return subprocess.check_output([str(GIT),'-C',str(ROOT/'apc-brainstorm-publish'),*a],encoding='utf-8').strip()
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
meta={'git_tag':'v1.0','git_commit':git('rev-parse','v1.0^{commit}'),'current_repo_commit':git('rev-parse','HEAD'),'protocol_file':str(OUT/'PROTOCOL_rodent.md'),'protocol_sha256':sha(OUT/'PROTOCOL_rodent.md'),'stage':'read-only inventory and duration gate','tracking_fs_hz':39.0625,'duration_ratio_definition':'(tracking samples / 39.0625) / (LFP samples / fs)','mapping_tolerance':.05}
assert meta['git_commit']=='71ebc16aed32ca38be73a800738b975e5806b330';assert not git('status','--porcelain')
rows=[];inventory=[]
sessions={'EC013':[156,157,205,206,208,251,252,374,375],'EC012':[239,240,269,270,271,356,357,375,444]}
for animal,numbers in sessions.items():
 movement=DATA/'Behavioral_Data'/(animal+'_movement.mat');mv=loadmat(movement,simplify_cells=True)
 print(animal,'tracking arrays',[(k,np.shape(v)) for k,v in mv.items() if not k.startswith('__')],flush=True)
 for i,number in enumerate(numbers,1):
  prefix='ec013.' if animal=='EC013' else 'ec012ec.';session=prefix+str(number);folder=DATA/'HC3/data'/animal/(session+'.eeg');file=folder/'data_block001.mat';var=animal.lower()+'ec'+str(i)
  trace=mv.get(var);nt=len(trace) if trace is not None else 0;shape=np.shape(trace);n=0;fs=float('nan');ch=0;ratio=float('nan');status='pending';err=''
  if not file.exists():status='missing_requested_LFP_file'
  elif trace is None:status='missing_tracking_array'
  else:
   if h5py.is_hdf5(file):
    with h5py.File(file,'r') as f:t=np.asarray(f['Time']).ravel();fshape=f['F'].shape;n=len(t);ch=next(x for x in fshape if x!=n)
   else:
    fields=whosmat(file);fshape=next(x[1] for x in fields if x[0]=='F');t=np.asarray(loadmat(file,variable_names=['Time'],simplify_cells=True)['Time']).ravel();n=len(t);ch=next(x for x in fshape if x!=n)
   fs=1/np.median(np.diff(t));ratio=(nt/39.0625)/(n/fs);status='PASS' if abs(ratio-1)<=.05 else 'STOP_DURATION_MISMATCH'
  row=dict(animal=animal,session=session,tracking_array=var,tracking_shape=str(shape),tracking_samples=nt,tracking_duration_s=nt/39.0625,lfp_samples=n,lfp_fs_hz=fs,lfp_channels=ch,lfp_duration_s=n/fs if n else float('nan'),tracking_to_lfp_duration_ratio=ratio,absolute_disagreement_fraction=abs(ratio-1),status=status,lfp_file=str(file),tracking_file=str(movement),git_commit=meta['git_commit'],provenance_json=json.dumps(meta,separators=(',',':')));rows.append(row)
  inventory.append({'session':session,'folder':str(folder),'available_mat_files':[p.name for p in folder.glob('*.mat')],'requested_file_exists':file.exists()})
  print(session,var,'channels',ch,'duration ratio',ratio,status,flush=True)
with (OUT/'mapping_checks.csv').open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
metadata_files=[]
for p in REAL.rglob('*'):
 if not p.is_file():continue
 name=p.name.lower()
 if p.suffix.lower() in ['.xml','.csv','.tsv','.xlsx','.xls','.json','.txt'] or (p.suffix.lower()=='.mat' and any(s in name for s in ['hc3','session','shank','region','metadata','info','behav'])):
  metadata_files.append({'path':str(p),'bytes':p.stat().st_size})
summary={'metadata':meta,'sessions':inventory,'metadata_candidate_files':metadata_files,'duration_mismatches':[r['session'] for r in rows if r['status']=='STOP_DURATION_MISMATCH'],'missing_requested_LFP':[r['session'] for r in rows if r['status']=='missing_requested_LFP_file'],'elapsed_seconds':time.perf_counter()-START}
(OUT/'inventory.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps({k:summary[k] for k in ['duration_mismatches','missing_requested_LFP','elapsed_seconds']}))
