from pathlib import Path
import subprocess, json, hashlib, sys
ROOT=Path(r'C:\Users\nghare\.brainstorm\process'); OUT=ROOT/'revision_checks/final'; REPO=ROOT/'apc-brainstorm-publish'
sys.path.insert(0,str(ROOT/'pydeps'))
import scipy.io as sio
GIT=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def git(*args): return subprocess.check_output([str(GIT),'-C',str(REPO),*args])
assert git('rev-parse','v1.0^{commit}').decode().strip()=='71ebc16aed32ca38be73a800738b975e5806b330'
assert not git('status','--porcelain').strip()
frozen=OUT/'frozen_v1';frozen.mkdir(parents=True,exist_ok=True)
paths=['src/bst_apc.m','src/calc_MI_all_methods.m']
for p in paths:
    dest=frozen/Path(p).name
    assert not dest.exists(),dest
    dest.write_bytes(git('show','v1.0:'+p))
manifest={'git_commit':'71ebc16aed32ca38be73a800738b975e5806b330','git_tag':'v1.0','repo_head':git('rev-parse','HEAD').decode().strip(),'frozen_files':[]}
for p in frozen.iterdir():manifest['frozen_files'].append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(OUT/'source_provenance.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
base=Path(r'D:\APC_project\RealDatasets\LFP_data')
for p in [base/'EC3_dataset_real.mat',base/'HC3/data/EC013/@rawec013.157.eeg/data_0raw_ec013.157.mat',base/'HC3/data/EC013/ec013.157.eeg/channel.mat']:
    print(str(p),sio.whosmat(p))
    if 'data_0raw' in p.name or p.name=='channel.mat':
        s=sio.loadmat(p,simplify_cells=True)
        for k,v in s.items():
            if not k.startswith('__'): print(k,str(v)[:9500])
