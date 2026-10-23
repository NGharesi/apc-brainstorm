from pathlib import Path
import sys,json,csv,hashlib,shutil
ROOT=Path(r'C:\Users\nghare\.brainstorm\process');OUT=ROOT/'revision_checks/rodent_multi';DATA=Path(r'D:\APC_project\RealDatasets\LFP_data')
sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
from scipy.io import loadmat
source=Path(r'D:\APC_project\2025\Results_Behavior\behavior_inter.mat')
test=loadmat(source,variable_names=['test'],simplify_cells=True)['test'];r=loadmat(DATA/'EC3_dataset_real.mat',variable_names=['R2'],simplify_cells=True)['R2'];crop=loadmat(DATA/'HC3/data/EC013/ec013.157.eeg/data_230118_2215.mat',variable_names=['F'],simplify_cells=True)['F']
assert test['F'].shape==(65,789000)
assert np.array_equal(test['Time'],r['Time']) and np.array_equal(test['F'][0],r['Value'])
assert np.array_equal(test['F'][:,40799:372501],crop)
fs=1/np.median(np.diff(test['Time']));ratio=(24657/39.0625)/(789000/fs);assert abs(ratio-1)<=.05
meta=json.loads((OUT/'inventory.json').read_text(encoding='utf-8'))['metadata']
e={'metadata':meta,'source_file':str(source),'source_variable':'test','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'channels':65,'n_samples':789000,'fs_hz':fs,'exact_full_E1_match_to_R2':True,'exact_full_time_match_to_R2':True,'exact_65_channel_crop_match':True,'crop_R2_sample_indices_1_based':[40800,372501],'history':str(test.get('History')),'tracking_to_lfp_duration_ratio':ratio}
(OUT/'ec013_157_source_recovery.json').write_text(json.dumps(e,indent=2),encoding='utf-8')
shutil.copy2(OUT/'mapping_checks.csv',OUT/'mapping_checks_initial_missing_file.csv')
with (OUT/'mapping_checks.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
for row in rows:
 if row['session']=='ec013.157':
  row.update(lfp_samples=789000,lfp_fs_hz=fs,lfp_channels=65,lfp_duration_s=789000/fs,tracking_to_lfp_duration_ratio=ratio,absolute_disagreement_fraction=abs(ratio-1),status='PASS_RECOVERED_EQUIVALENT_FULL_RECORDING',lfp_file=str(source))
with (OUT/'mapping_checks.csv').open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps({k:v for k,v in e.items() if k not in ['metadata','history']}))
