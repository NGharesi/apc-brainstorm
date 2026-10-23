from pathlib import Path
import sys,json,hashlib
ROOT=Path(r'C:\Users\nghare\.brainstorm\process');OUT=ROOT/'revision_checks/final'
sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
from scipy.io import loadmat,whosmat
BASE=Path(r'D:\APC_project\RealDatasets\LFP_data')
r=loadmat(BASE/'EC3_dataset_real.mat',variable_names=['R2'],simplify_cells=True)['R2']
print('R2',[(k,np.shape(v),str(v)[:300] if k not in ['Value','Time'] else '') for k,v in r.items()])
evidence={'R2':{k:str(v) for k,v in r.items() if k not in ['Value','Time']},'matches':[],'local_sessions':[]}
for p in [BASE/'EC3_dataset_real_allChannels.mat', BASE/'HC3/data/EC013/ec013.157.eeg/data_block001_resample.mat', BASE/'HC3/data/EC013/ec013.157.eeg/data_230118_2215.mat']:
    print(str(p),whosmat(p))
    if 'resample' in p.name:
        s=loadmat(p,simplify_cells=True);F=s['F'];x=np.asarray(r['Value']).ravel()
        print('resample',F.shape,'time',s['Time'].shape,'x',x.shape,'history',s.get('History'))
        for i in range(F.shape[0]):
            if F.shape[1]==len(x):
                err=float(np.max(np.abs(F[i]-x)))
                if err==0:evidence['matches'].append({'file':str(p),'row_1_based':i+1,'max_absolute_error':err})
for p in sorted((BASE/'HC3/data/EC013').glob('ec013.*.eeg')):
    boutfiles=list(p.glob('data*run*trial*.mat'))+list(p.glob('data*rest*trial*.mat'))
    item={'session':p.name,'behavior_trial_files':sorted(set(x.name for x in boutfiles))}
    evidence['local_sessions'].append(item)
    print('session',p.name,'behavior_files',len(item['behavior_trial_files']))
for suffix in ['@rawec013.157.eeg/data_0raw_ec013.157.mat','ec013.157.eeg/data_block001_resample.mat','ec013.157.eeg/channel.mat']:
    p=BASE/'HC3/data/EC013'/suffix;s=loadmat(p,simplify_cells=True)
    e={'file':str(p),'history':str(s.get('History'))}
    if 'Channel' in s:e['channel_first']=str(s['Channel'][0]);e['channel_count']=len(s['Channel'])
    if isinstance(s.get('F'),dict):e['raw_file']=s['F']['filename'];e['sampling']=str(s['F']['prop'])
    evidence.setdefault('import_metadata',[]).append(e)
(OUT/'local_data_inspection.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
print('matches',evidence['matches'])
