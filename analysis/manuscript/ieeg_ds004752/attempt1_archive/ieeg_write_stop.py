"""Report the prespecified 2000-Hz gate failure; do not resume analysis."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib,subprocess
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent;REPO=ROOT/'apc-brainstorm-publish'
sys.path.insert(0,str(ROOT/'pydeps'))
import pandas as pd
GIT=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def git(*args):return subprocess.check_output([str(GIT),'-C',str(REPO),*args],text=True,encoding='utf-8').strip()
def js(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def link(p,label=None):
    p=Path(p);p=p if p.is_absolute() else OUT/p
    return f'[{label or p.name}](<{p.as_posix()}>)'
def table(d,columns):
    def value(x):
        if pd.isna(x):return 'not computed'
        return f'{x:.15g}' if isinstance(x,float) else str(x).replace('|','/')
    return '| '+' | '.join(columns)+' |\n| '+' | '.join('---' for _ in columns)+' |\n'+'\n'.join('| '+' | '.join(value(r[c]) for c in columns)+' |' for _,r in d.iterrows())+'\n'
meta=js('provenance.json');checks=pd.read_csv(OUT/'edf_file_checks.csv',encoding='utf-8');channels=pd.read_csv(OUT/'edf_channel_checks.csv',encoding='utf-8');eq=js('equivalence_gate.json')
bad=checks[checks.header_passed==0];assert len(bad)==1 and checks.passed.eq(1).sum()==38
r=bad.iloc[0];assert r.fs_hz==4000
path=Path(r.file);base=str(path)[:-len('_ieeg.edf')]
c=pd.read_csv(base+'_channels.tsv',sep='\t',encoding='utf-8');sidecar=json.loads(Path(base+'_ieeg.json').read_text(encoding='utf-8'))
with path.open('rb') as f:
    header=f.read(256);ns=int(header[252:256]);signal_header=f.read(ns*256)
record_s=float(header[244:252]);records=int(header[236:244]);offset=ns*(16+80+8+8+8+8+8+80)
samples=[int(signal_header[offset+i*8:offset+(i+1)*8]) for i in range(ns)]
assert ns==36 and set(samples)=={4000} and record_s==1 and set(c.sampling_frequency)=={4000} and sidecar['SamplingFrequency']==4000
assert git('branch','--show-current')=='neuroimage-submission' and git('status','--porcelain')==''
for f in meta['file_sha256_records']:assert sha(Path(f['path']))==f['sha256']
meta['status']='STOPPED_METHOD_RELEVANT';meta['stage']='Stopped at section 3.1 sampling-rate gate; no dataset APC/scan output';meta['stopped_utc']=datetime.now(timezone.utc).isoformat();meta['git_clean_at_stop']=True
meta['push']=dict(status='SUCCEEDED',remote='origin',branch='neuroimage-submission',tags=['v1.0','v2.0'],new_commit_created=False)
(OUT/'provenance.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
evidence=dict(provenance=meta,file=str(path),header_channels=ns,header_records=records,header_record_duration_s=record_s,header_samples_per_record=samples,edf_fs_hz=4000,channels_tsv_fs_hz=sorted(set(map(int,c.sampling_frequency))),json_sampling_frequency=sidecar['SamplingFrequency'],expected_protocol_fs_hz=2000,total_samples=int(r.samples),last_event_end_sample=int(r.events_last_end_sample),channel_order_match=bool(r.header_channel_order_match),channels_tsv=str(base+'_channels.tsv'),json_sidecar=str(base+'_ieeg.json'),sample_payload_not_analyzed=True)
(OUT/'sampling_rate_failure_evidence.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
fields=['fP (Hz)','fA (Hz)','raw Canolty MVL','preferred phase (degrees)']
numbers=pd.DataFrame(dict(metric=fields,expected=eq['expected'],observed=eq['observed'],absolute_difference=eq['absolute_differences']))
inventory=pd.read_csv(OUT/'metadata_file_inventory.csv',encoding='utf-8');pairs=pd.read_csv(OUT/'metadata_candidate_pairs.csv',encoding='utf-8');candidate_counts=pairs.groupby('patient').size().to_dict()
summary=inventory.groupby('patient',sort=True).agg(sessions=('session','count'),metadata_trials=('trials','sum'),dataset_artifact_flag_trials=('artifact_flag_trials','sum')).reset_index();summary['candidate_pairs']=summary.patient.map(candidate_counts).fillna(0).astype(int);summary['selected_pair']='not selected: gate stopped'
summary['provenance_json']=json.dumps(meta,separators=(',',':'));summary.to_csv(OUT/'metadata_patient_counts_at_stop.csv',index=False,encoding='utf-8')
status=dict(status='STOPPED_METHOD_RELEVANT',provenance=meta,reason='Protocol requires fs=2000 Hz; sub-11/ses-01 EDF, channels.tsv and JSON all specify 4000 Hz.',edf_files_total=68,edf_files_signal_checks_passed=38,edf_files_header_gate_failed=1,edf_files_not_attempted_after_failure=29,passed_channel_checks=len(channels),equivalence_passed=True,maximum_equivalence_absolute_difference=max(eq['absolute_differences']),timeline_status='NOT_RUN_AFTER_READING_GATE_FAILURE',contacts_selected=False,dataset_apc_estimates=0,dataset_scan_estimates=0,reportable_endpoint_runs=0,resampling_performed=False,sessions_excluded_to_bypass_gate=False,tagged_code_modified=False,new_commit_created=False)
(OUT/'STATUS.json').write_text(json.dumps(status,indent=2),encoding='utf-8')
stop=['# STOPPED: prespecified iEEG sampling-rate gate','',
      'The run stopped at protocol section 3.1. The EDF for `sub-11/ses-01` is sampled at **4000 Hz**, whereas the committed protocol requires **2000 Hz for every iEEG file**. The EDF header, `channels.tsv` and JSON sidecar independently agree on 4000 Hz. This is a method-relevant mismatch.','',
      'File: '+link(path)+'. Evidence: '+link('sampling_rate_failure_evidence.json')+'.','',
      'The failing file has 36 channels and 1,600,000 samples; channel order and sample count match the sidecars. Its EDF contains 400 records of 1 s with 4000 samples per channel per record.','',
      'Before the stop, 38/68 iEEG files passed all reading checks. The failing file was the 39th; the remaining 29 files were not attempted. The APC equivalence gate passed (maximum absolute difference '+f"{max(eq['absolute_differences']):.16g}"+').','',
      'No ds004752 APC or scan output was computed. No contacts were selected, no trial rejection or endpoint analysis was performed, and the scalp timeline gate was not run after the reading gate failed. No resampling or exclusion was used to bypass the gate.','',
      'The protocol, src files and tagged code remain unchanged. The repository remains clean at `'+meta['git_head']+'`. The requested branch/tags push succeeded. No new commit was created.','',
      'A protocol decision is required before analysis can resume. Full gate report: '+link('RESULTS_ieeg.md')+'.']
(OUT/'STOPPED.md').write_text('\n'.join(stop)+'\n',encoding='utf-8')
lines=['# Human intracranial APC analysis: STOPPED at the reading gate','',
       'Status: **STOPPED_METHOD_RELEVANT**. No dataset APC/scan estimates or endpoint results exist for this prespecified run. See '+link('STOPPED.md')+'.','',
       '## Provenance and requested push','',
       'Clean branch `neuroimage-submission`, HEAD `'+meta['git_head']+'`. Protocol SHA-256 `'+meta['protocol_sha256']+'` matches the requested value. `git push origin neuroimage-submission --tags` succeeded, publishing the branch and tags v1.0/v2.0. No new commit was created.','',
       'MATLAB '+meta['matlab_version']+'. All toolbox versions, full APC options, comparator settings, seed 20261023 and full path/source SHA-256 records are in '+link('provenance.json')+'. The five requested source/helper files and protocol were rehashed at the stop and remain unchanged.','',
       '## Equivalence gate: PASS','',
       'Resolved `bst_apc` path: '+link(eq['bst_apc_path'])+'. The source copy in the repository, rather than frozen_v1, was used on the saved synthetic 500-Hz input with fA=[80,150]. Status 0; all four absolute differences are <=1e-10.','',table(numbers,['metric','expected','observed','absolute_difference']),
       'Evidence: '+link('equivalence_gate.json')+'; '+link('equivalence_gate.mat')+'.','',
       '## EDF reading gate: FAIL; stop required','',
       '**sub-11/ses-01 is 4000 Hz**, verified independently from its EDF sample/record header, all 36 channels.tsv sampling-frequency entries, and JSON SamplingFrequency. The protocol section 3.1 requires 2000 Hz. Sample count 1,600,000 and channel order match the sidecars. No signal check or method estimate was computed for this file after the header gate failed.','',
       '38 files passed all checks before the failure, covering '+str(len(channels))+' channels. Their channel order/count, sample counts, 2000-Hz rate, no nonfinite values, nonzero variance and median absolute magnitude below 10^4 microvolts passed. The 39th file failed; 29 remaining files were not attempted.','',
       'Complete attempted-file checks: '+link('edf_file_checks.csv')+'. Passed-file channel checks: '+link('edf_channel_checks.csv')+'. Failure evidence: '+link('sampling_rate_failure_evidence.json')+'. MATLAB log: '+link('reading_gates_matlab.log')+'.','',
       table(checks.drop(columns='provenance_json'),['file','channels','samples','events_last_end_sample','fs_hz','header_channel_order_match','header_passed','passed']),
       '## Earlier screening NaN cause','',js('earlier_screening_nan_cause.json')['cause'],
       'All 64 saved screening rows have finite APC/scanned coupling strengths and selected frequencies; all 64 apc_z and pac_z entries are NaN. This earlier screening is not a result of the current protocol. Evidence: '+link('earlier_screening_nan_cause.json')+'.','',
       '## Trial timeline: literature evidence recorded; empirical gate not run','',
       'Boran et al. Figure 1a gives 1-s fixation, 2-s encoding and 3-s maintenance before the probe; this places encoding at 1 s and probe at 6 s relative to trial start. [Scientific Data paper, Figure 1a](https://www.nature.com/articles/s41597-020-0364-3.pdf). Dimakopoulos et al. describe the same encoding/maintenance sequence and probe-relative periods. [eLife paper, task methods](https://elifesciences.org/articles/78677).','',
       'The grand-average scalp gate, plot and peak latencies were not computed because the earlier required reading gate failed. The timeline has therefore **not passed the full protocol gate**. Paper evidence: '+link('timeline_paper_evidence.json')+'.','',
       '## Metadata inventory at stop; no fixed contact or trial choices','',
       'Metadata inventory contains 68 iEEG sessions, 15 patients and '+str(int(inventory.trials.sum()))+' trials. There are 99 metadata candidate adjacent hippocampal pairs across 14 patients; sub-13 has none. No power-ratio selection, notch filtering, robust-SD exclusion or eligibility assessment was run. The artifact-flag counts below are metadata counts, not completed preprocessing or inclusion results.','',
       table(summary,['patient','sessions','metadata_trials','dataset_artifact_flag_trials','candidate_pairs','selected_pair']),
       'Metadata sources: '+link('metadata_file_inventory.csv')+', '+link('metadata_candidate_pairs.csv')+', '+link('metadata_patient_counts_at_stop.csv')+'. `contacts.csv` and `trial_inclusion.csv` have not been created because their fixed choices were not made.','',
       '## Endpoints, failure rates and requested final figure: not computed','',
       'Primary endpoint, secondary endpoints 1-6, exploratory load models, sensitivities (a)/(b), boundary-hit/failure rates and the four-panel final figure were not run. No primary decision is stated because no reportable endpoint run occurred. All dataset method counts are zero. No placeholder result CSVs were created.','',
       'The comparator copy was prepared but never run on dataset trials. Reverse edits recover the original helper byte-for-byte: '+link('ieeg_comparators.diff')+'; '+link('ieeg_comparator_copy_verification.json')+'.','',
       '## Deviations and resolved tooling errors','']
for d in js('deviations.json')['deviations']:lines.append('- '+d['type']+': '+d['reason'])
lines+=['','The unit-reader correction and header compatibility corrections were identified without dataset PAC outcomes. Initial failed-reader checks/logs are archived in this folder. Source diffs: '+link('unit_reader_fix.diff')+' and '+link('header_time_reader_fix.diff')+'. Header-copy payload hashes: '+link('edf_header_copies.json')+'. Original EDF files were not modified.','',
        'No method setting was changed after the 4000-Hz finding. The run stopped rather than resampling or excluding the session. Gate/status record: '+link('STATUS.json')+'.']
(OUT/'RESULTS_ieeg.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in status.items() if k!='provenance'}))
