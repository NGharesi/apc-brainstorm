"""Register Amendment-4 preprocessing details before processing the new window."""
from pathlib import Path
import json,hashlib,sys
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O.parent.parent/'pydeps'))
import pandas as pd
m=json.loads((O/'provenance.json').read_text(encoding='utf-8'))
assert not (O/'trial_inclusion_amendment4.csv').exists()
m['analysis_window_s']=[0,6]
m['stage']='AMENDMENT4_FIXED_PREPARATION_BEFORE_NEW_WINDOW_METHOD_OUTPUTS'
m['amendment4_numerical_details']={
    'robust_pool':'Selected analysed signal, all 0-6-s samples from dataset-unflagged trials, before evoked subtraction; first differences within trials only',
    'robust_thresholds':'Same amplitude median/MAD and absolute first-difference threshold as Amendment 3',
    'primary_mask':'Amendment-3 selected-pair retained mask AND selected bipolar 0-6-s robust mask',
    'sensitivity_b_mask':'Amendment-3 selected-pair retained mask AND deeper-contact 0-6-s robust mask',
    'sensitivity_a_mask':'Dataset artifact flags only: the unchanged sensitivity (a) omits robust amplitude/first-difference rejection at both stages',
    'templates':'Separate included-trial mean waveform per analysis/patient/session/signal, computed after its own mask; no post-subtraction rejection; session/patient eligibility after masking',
    'notch':'Full native trial cut and MATLAB resample, full 8-s mean removal, same fourth-order digital SOS notches at 50/100/150 +/-1 Hz, then samples 1:12000',
    'welch':'Symmetric hann(2000), overlap1000, nfft2000, fs2000, equal-trial mean PSD after evoked subtraction',
    'spectral_peak':'Largest residual over 1-12 Hz above ordinary log10(power)-on-log10(frequency) linear fit',
    'progress_check':'sub-01 ses-01 all planned analysed signals first; counts logged, not a gate; automatic continuation without tuning'
}
cols=['patient','deeper_contact','adjacent_contact','candidate_index','native_fs_hz']
c=pd.read_csv(O/'contacts.csv',usecols=cols,encoding='utf-8');c=c[c.patient!='sub-13'];c.to_csv(O/'am4_contacts.csv',index=False,encoding='utf-8')
m['amendment4_preparation_code_sha256']=hashlib.sha256((O/'ieeg_am4_preprocess.m').read_bytes()).hexdigest()
(O/'provenance.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
(O/'am4_fixed_preprocessing_choices.json').write_text(json.dumps(dict(git_head=m['git_head'],protocol_sha256=m['protocol_sha256'],seed=20261023,choices=m['amendment4_numerical_details']),indent=2),encoding='utf-8')
print('Amendment 4 preprocessing choices recorded; fixed pairs:',len(c))
