"""Package the prespecified validation result, preserving preflight evidence."""
from pathlib import Path
import sys, json, hashlib, os
ROOT=Path(r'C:\Users\nghare\.brainstorm\process')
OUT=ROOT/'revision_checks/rodent_multi'
sys.path.insert(0,str(ROOT/'pydeps'))
os.environ['MPLCONFIGDIR']=str(OUT/'plot_config')
import numpy as np
import pandas as pd
from scipy.io import loadmat
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''): h.update(b)
    return h.hexdigest()
def link(name,label=None): return f'[{label or name}](<{(OUT/name).as_posix()}>)'
gate=read(OUT/'chunked_behavior_validation.json')
amendment=read(OUT/'protocol_amendments_record.json')
meta=gate['provenance']|{'protocol_sha256':sha(OUT/'PROTOCOL_rodent.md'),
                       'execution_sha256':sha(OUT/'EXECUTION_rodent.md'),
                       'stage':'chunked ec013.157 validation',
                       'validation_file_sha256':sha(OUT/'chunked_behavior_validation.json')}
result=loadmat(OUT/'ec013.157_behavior.mat',simplify_cells=True)['result']
provenance=json.dumps(meta,separators=(',',':'))
chunks=[]
for p in sorted(OUT.glob('ec013.157_speed_chunk_*.mat')):
    s=loadmat(p,simplify_cells=True)
    chunks.append(dict(session='ec013.157',chunk=p.stem.rsplit('_',1)[-1],
                       start_idx=int(s['chunkStart']),stop_idx=int(s['chunkEnd']),
                       samples=int(s['chunkEnd']-s['chunkStart']+1),
                       elapsed_seconds=float(s['elapsed']),route=s['route'],
                       source_mat=p.name,provenance_json=provenance))
pd.DataFrame(chunks).to_csv(OUT/'ec013_157_chunk_inventory.csv',index=False,encoding='utf-8')

summary={k:v for k,v in result.items() if isinstance(v,(float,int,str,np.number))}
for k in ['run_gap_details','rest_gap_details','provenance']: summary[k]=result[k]
summary['provenance']=meta
(OUT/'ec013_157_behavior_summary.json').write_text(json.dumps(summary,indent=2,default=lambda x:x.item()),encoding='utf-8')

# The complete masks and speed are retained in MAT; CSV holds contiguous
# disagreement intervals rather than hundreds of thousands of repeated metadata.
old=loadmat(OUT/'behavior_reproduction.mat',simplify_cells=True)
oldrun=np.abs(old['speed'])>6
ix=np.arange(40799,372500)
newrun=np.asarray(result['run_mask'],bool)[ix]
newrest=np.asarray(result['rest_mask'],bool)[ix]
valid=np.asarray(result['valid'],bool)[ix]
same=(oldrun==newrun)&((~oldrun)==newrest)
assert np.isclose(same.mean()*100,gate['all_sample_agreement_percent'])
t=np.asarray(result['speed_time'])[ix]
delta=np.diff(np.r_[False,~same,False].astype(int))
starts=np.flatnonzero(delta==1);ends=np.flatnonzero(delta==-1)-1
intervals=[]
for a,b in zip(starts,ends):
    intervals.append(dict(start_idx=int(ix[a]+1),stop_idx=int(ix[b]+1),start_time_s=t[a],
                          stop_time_s=t[b],samples=int(b-a+1),unlabelled_samples=int((~valid[a:b+1]).sum()),
                          provenance_json=provenance))
pd.DataFrame(intervals,columns=['start_idx','stop_idx','start_time_s','stop_time_s','samples','unlabelled_samples','provenance_json']).to_csv(OUT/'ec013_157_label_disagreements.csv',index=False,encoding='utf-8')

plt.rcParams.update({'font.size':10,'svg.fonttype':'none'})
fig,axes=plt.subplots(2,1,figsize=(13,5),sharex=True)
axes[0].plot(t,oldrun.astype(int),lw=.7,label='Historical')
axes[0].plot(t,newrun.astype(float)+.06,lw=.65,alpha=.8,label='Chunked, missing-aware')
axes[0].set(yticks=[0,1],yticklabels=['Rest','Run'],ylim=(-.15,1.4));axes[0].legend(ncol=2,loc='upper right',frameon=False)
axes[1].fill_between(t,0,(~same).astype(float),color='#D55E00',lw=0,label='Disagreement')
axes[1].fill_between(t,0,(~valid).astype(float),color='#555555',lw=0,label='Unlabelled')
axes[1].set(ylabel='Indicator',xlabel='Recording time (s)',ylim=(-.05,1.2));axes[1].legend(ncol=2,loc='upper right',frameon=False)
fig.suptitle(f"ec013.157 validation: {gate['all_sample_agreement_percent']:.3f}% agreement (required 95%)")
fig.tight_layout(rect=(0,.09,1,.95))
fig.text(.5,.015,'APC v1.0 '+meta['git_commit']+'\nSources: behavior_reproduction.mat; ec013.157_behavior.mat; ec013_157_label_disagreements.csv',ha='center',fontsize=8)
figuremeta=meta|{'sources':{p.name:sha(p) for p in [OUT/'behavior_reproduction.mat',OUT/'ec013.157_behavior.mat',OUT/'ec013_157_label_disagreements.csv']}}
fig.savefig(OUT/'ec013_157_label_validation.png',dpi=300,metadata={'Description':json.dumps(figuremeta)})
fig.savefig(OUT/'ec013_157_label_validation.svg',metadata={'Description':json.dumps(figuremeta)})
plt.close(fig)

report=OUT/'RESULTS_rodent.md'
archive=OUT/'RESULTS_preflight.md'
if not archive.exists(): archive.write_bytes(report.read_bytes())
text=archive.read_text(encoding='utf-8')
text=text.replace('# Multi-session rodent analysis — preflight results','# Multi-session rodent analysis')
oldstatus='**Status: channel selection and prerequisite checks complete; new bout analyses pending the time-interval decision.** No new-session APC/comparator outcomes, per-session eligibility decisions, inferential tests or mixed models have been computed. This is a preflight report, not completed replication results.'
status='VALIDATION_PASS' if gate['passed'] else 'STOPPED_CHUNK_LABEL_GATE'
newstatus=(f"**Status: {'PASS' if gate['passed'] else 'STOPPED'} at the ec013.157 chunked-label validation: "
           f"{gate['all_sample_agreement_percent']:.6f}% agreement; required >=95%.** "
           +('The gate passed; the remaining whole-recording analyses can proceed.' if gate['passed'] else
             'The prespecified stopping rule was applied. No other session bout analysis or new APC/comparator estimation was run. This is an incomplete replication report.'))
text=text.replace(oldstatus,newstatus)
begin=text.index('## Inclusion, statistics and remaining interval choice')
end=text.index('## Figures',begin)
validation=f'''## Whole-recording behaviour amendment and validation

The user authorized whole-recording analysis with -1 treated as missing, bounded gaps <=0.5 s linearly interpolated, longer gaps splitting bouts, and the first/last 2 s excluded. The user also authorized exactly 331,702-sample trenddecomp chunks, 20-s overlap, 10-s internal edge rejection and a forced final chunk ending at the trimmed recording end. Amendments were recorded before this validation: {link('protocol_amendments_record.json')}. The original protocol remains in {link('PROTOCOL_rodent_original.md')}; its SHA-256 is `{amendment['original_protocol_sha256']}`. Amended protocol SHA-256: `{amendment['protocol_sha256']}`.

The original historical calculation retains -1 positions and still reproduces **12/12 exactly**, as reported above. The amended calculation uses x1 only and the same speed formula, 39.06-Hz interpolation timestamps, units, threshold and 5-s criterion. trenddecomp internally fills remaining NaNs with the chunk mean; derivatives touching unfilled tracking gaps are then excluded from both state masks. No moving-median fallback was used. Each stitched derivative has exactly one chunk owner; the final excess overlap is divided at its midpoint. Chunk indices and runtimes: {link('ec013_157_chunk_inventory.csv')}.

| Validation measure | Result |
| --- | --- |
| Historical derivative interval | 40800:372500 (positions 40800:372501) |
| All-sample label agreement (gate denominator) | {gate['all_sample_agreement_percent']:.6f}% |
| Agreement among valid new labels | {gate['valid_sample_agreement_percent']:.6f}% |
| Historical derivative samples | {gate['total_historical_derivatives']} |
| Samples without a new run/rest label | {gate['unlabelled_new_derivatives']} |
| Historical run bouts matched at both endpoints within 0.5 s | {gate['matched_run_bouts']}/12 |
| Historical rest bouts matched at both endpoints within 0.5 s | {gate['matched_rest_bouts']}/12 |
| Whole-recording run / rest bouts | {gate['whole_record_run_bouts']} / {gate['whole_record_rest_bouts']} |
| Raw x1 missing samples | {100*gate['raw_x1_missing_fraction']:.6f}% |
| Any LED-coordinate missing samples | {100*gate['any_coordinate_missing_fraction']:.6f}% |
| Run / rest bouts lost to gaps | {gate['run_bouts_lost_to_gaps']} / {gate['rest_bouts_lost_to_gaps']} |
| Gate | {'PASS' if gate['passed'] else 'FAIL — stopped'} |

Unlabelled samples count as disagreement in the primary percentage. Bout matching is one-to-one within state and compares the full whole-recording bout endpoints. Exact per-bout comparison: {link('ec013_157_bout_validation.csv')}. Contiguous disagreement intervals: {link('ec013_157_label_disagreements.csv')}. Full speed and masks: {link('ec013.157_behavior.mat')}. Validation record: {link('chunked_behavior_validation.json')}. Missing-gap counts, short pieces and baseline bout counts: {link('ec013_157_behavior_summary.json')}.

'''
if not gate['passed']:
    validation+='No other session has been assigned bout eligibility. The planned original-interval PAC sensitivity, E1 sensitivity, session statistics, mixed models, within-state spreads and remaining run/rest figures were not run because the required validation failed. No threshold, decomposition, chunk length, missing-data rule or method code was adjusted after the gate result.\n\n'
text=text[:begin]+validation+text[end:]
text=text.replace('Run/rest and session-difference figures await bout analysis.',
                  'Label validation diagnostic: '+link('ec013_157_label_validation.png','300-dpi PNG')+'; '+link('ec013_157_label_validation.svg','SVG')+'. Run/rest and session-difference figures were not generated behind the validation gate.')
text=text.replace('Deviations and pending choice:', 'Deviations:')
text += f"\nChunked validation MATLAB runtime: {gate['elapsed_seconds']:.3f} s (excluding MATLAB startup). Sum of chunk decompositions: {sum(r['elapsed_seconds'] for r in chunks):.3f} s. The tagged APC code was not called or modified during this validation.\n"
report.write_text(text,encoding='utf-8')
deviations=read(OUT/'deviations.json')
deviations['deviations']=[d for d in deviations['deviations'] if d['type']!='pending execution choice']
deviations['metadata']=meta
deviations['deviations'].append({'type':'user-authorized protocol amendment','detail':'Whole recording; missing tracking rules; fixed-length chunking and >=95% label gate. Recorded before validation. No tagged method code modified.'})
if not gate['passed']:
    deviations['deviations'].append({'type':'prespecified validation failure','detail':f"All-sample agreement {gate['all_sample_agreement_percent']:.9f}% <95%; stopped before other sessions and PAC estimation."})
(OUT/'deviations.json').write_text(json.dumps(deviations,indent=2),encoding='utf-8')
state=read(OUT/'STATUS.json');state.update(status=status,metadata=meta,validation=gate,
    new_session_bout_analyses_started=False,ec013_157_chunk_validation_complete=True)
(OUT/'STATUS.json').write_text(json.dumps(state,indent=2),encoding='utf-8')
files=[]
for p in OUT.rglob('*'):
    if p.is_file() and p.name!='output_manifest.json' and not any(q in ['__pycache__','plot_config'] for q in p.relative_to(OUT).parts):
        files.append(dict(path=str(p.relative_to(OUT)),bytes=p.stat().st_size,sha256=sha(p)))
(OUT/'output_manifest.json').write_text(json.dumps({'metadata':meta,'files':files},indent=2),encoding='utf-8')
print(json.dumps({'status':status,'agreement_percent':gate['all_sample_agreement_percent'],'report':str(report)}))
