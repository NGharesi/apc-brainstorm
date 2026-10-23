from pathlib import Path
import sys,json,csv,hashlib,subprocess,re,datetime
ROOT=Path(r'C:\Users\nghare\.brainstorm\process');OUT=ROOT/'revision_checks/final';HD=ROOT/'revision_checks/v2/candidate_03';REPO=ROOT/'apc-brainstorm-publish'
sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
import pandas as pd
from PIL import Image
GIT=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def git(*a):return subprocess.check_output([str(GIT),'-C',str(REPO),*a],text=True,encoding='utf-8').strip()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def df(p):return pd.read_csv(p,keep_default_na=False,na_values=['NaN','nan',''],float_precision='round_trip')
def read(p):
 with Path(p).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def link(p,label=None):return f'[{label or Path(p).name}](<{Path(p).resolve().as_posix()}>)'
def table(d,cols):
 def f(x):return 'NA' if isinstance(x,(float,np.floating)) and not np.isfinite(x) else (f'{x:.8g}' if isinstance(x,(float,np.floating)) else str(x))
 return '| '+' | '.join(cols)+' |\n| '+' | '.join('---' for c in cols)+' |\n'+'\n'.join('| '+' | '.join(f(r[c]).replace('|','\\|') for c in cols)+' |' for _,r in d.iterrows())+'\n'
meta=load(OUT/'sos_correction_provenance.json');result=load(OUT/'correction_summary.json')
assert result['status']=='COMPLETE'
assert git('rev-parse','v1.0^{commit}')==meta['git_commit']
assert git('rev-parse','v2.0^{commit}')==meta['repo_head']
assert git('rev-parse','HEAD')==meta['repo_head'] and not git('status','--porcelain')
for f in meta['frozen_files']:assert sha(f['path'])==f['sha256']
for p,h in meta['analysis_sources'].items():assert sha(p)==h,(p,'corrected source changed during execution')
for f in load(OUT/'previous_attempt_manifest.json')['files']:assert sha(f['path'])==f['sha256']
prior=load(HD/'final_output_manifest.json')
for f in prior['files']:assert sha(HD/f['path'])==f['sha256']
old=read(HD/'heldout_trials.csv');new=read(OUT/'corrected_heldout/heldout_trials.csv');ix={(r['input_id'],r['configuration'],r['method']):r for r in new}
apc_verified=0
for r in old:
 if r['method']=='APC':
  n=ix[(r['input_id'],r['configuration'],r['method'])];assert all(n[k]==v for k,v in r.items());apc_verified+=1
assert apc_verified==1350
guards=[]
for p in OUT.glob('sos_*_filter_guards.csv'):
 d=df(p);assert d.guard_passed.eq(1).all();assert (d.max_pole_radius<1).all() and (d.max_sos_section_pole_radius<1).all();assert (abs(d.center_gain-1)<1e-3).all();guards.append(d)
assert len(guards)==7,('Expected heldout3/development3/rodent1 guard tables',len(guards))
G=pd.concat(guards).drop_duplicates(['fs_hz','low_hz','high_hz']);G.to_csv(OUT/'all_corrected_filter_guards.csv',index=False,encoding='utf-8')
# Verify source inputs against the manifests recorded before previous runs.
v1=load(ROOT/'revision_checks/v1_followup/input_source_manifest.json')
input_checks=0
for p,h in v1.get('input_files',{}).items():assert sha(p)==h,p;input_checks+=1
source_rows=df(OUT/'corrected_heldout/heldout_trials.csv');assert len(source_rows)==6750
comp=source_rows[source_rows.configuration.isin(['A1_prime','A2_prime'])];assert len(comp)==5400
assert comp.valid.eq(1).all();assert np.isin(comp.recovered_fp_hz,np.arange(3,14.01,.5)).all();assert np.isin(comp.recovered_fa_hz,np.arange(80,161,4)).all()
rod=df(OUT/'rodent_bouts_SOS.csv');assert len(rod)==120 and rod.groupby(['state','method']).size().eq(12).all()
oldrod=df(OUT/'previous_direct_form_attempt/rodent_bouts.csv');
cols=['state','bout','duration_s','method','fP_hz','fA_hz','score','raw_mvl','ozkurt_mvl','preferred_phase_deg']
a=oldrod[oldrod.method=='APC v1.0'][cols].sort_values(['state','bout']).reset_index(drop=True);b=rod[rod.method=='APC v1.0'][cols].sort_values(['state','bout']).reset_index(drop=True);pd.testing.assert_frame_equal(a,b)
fm=load(OUT/'figure_manifest.json');assert len(fm['figures'])==9
for figure in fm['figures']:
 with Image.open(figure['png']) as im:
  assert abs(im.info['dpi'][0]-300)<.01;pmeta=json.loads(im.info['Description']);assert pmeta['git_commit']==meta['git_commit'];im.verify()
 for item in pmeta['source_files']:assert sha(item['path'])==item['sha256'],item
 svg=Path(figure['svg']).read_text(encoding='utf-8');assert meta['git_commit'] in svg
audit=df(OUT/'filter_audit_500Hz_bands.csv');detailed=df(OUT/'filter_audit_500Hz_trials.csv')
crit=df(OUT/'v2_criteria_old_vs_SOS.csv');v1cmp=df(OUT/'v1_vs_A2_old_vs_SOS.csv');hcmp=df(OUT/'heldout_comparator_old_vs_SOS_summary.csv');devcmp=df(OUT/'development_comparator_old_vs_SOS_summary.csv')
summary_devs=devcmp.groupby(['stage','configuration','fp_grid_step_hz']).agg(n_groups=('old_joint_recovery','size'),old_joint=('old_joint_recovery','sum'),SOS_joint=('SOS_joint_recovery','sum'),old_strict=('old_strict_joint_recovery','sum'),SOS_strict=('SOS_strict_joint_recovery','sum')).reset_index();summary_devs['provenance_json']=json.dumps(meta);summary_devs.to_csv(OUT/'development_old_vs_SOS_pooled.csv',index=False,encoding='utf-8')
newstat=df(OUT/'rodent_run_rest_statistics.csv');oldstat=df(OUT/'previous_direct_form_attempt/rodent_run_rest_statistics.csv');rs=oldstat.merge(newstat,on=['method','metric','weighting'],suffixes=('_old','_SOS'));wanted=['method','metric','weighting']+[x+s for x in ['run_mean','rest_mean','mean_difference','welch_t','p_two_sided','hedges_g','bootstrap_ci_low','bootstrap_ci_high'] for s in ['_old','_SOS']];rs=rs[wanted];rs['provenance_json']=json.dumps(meta);rs.to_csv(OUT/'rodent_statistics_old_vs_SOS.csv',index=False,encoding='utf-8')
newsm=df(OUT/'rodent_state_summary.csv');oldsm=df(OUT/'previous_direct_form_attempt/rodent_state_summary.csv');rb=oldsm.merge(newsm,on=['method','state'],suffixes=('_old','_SOS'));rb=rb[['method','state','boundary_4_old','boundary_4_SOS','boundary_12_old','boundary_12_SOS']];rb['provenance_json']=json.dumps(meta);rb.to_csv(OUT/'rodent_boundary_old_vs_SOS.csv',index=False,encoding='utf-8')
v1groups=v1cmp.groupby(['scenario','dataset','endpoint']).agg(v1_count=('v1_count','sum'),old_best_A2=('old_best_A2_count','sum'),SOS_best_A2=('SOS_best_A2_count','sum')).reset_index()
filter_section=['## Filter correction','',
'The user authorized replacement of the direct-form coefficient realization with **the same nominal `butter(4)` Butterworth design in second-order sections**. All tagged APC v1.0/v2.0 code and their saved estimates are unchanged. Only comparator filtering was corrected: `[z,p,k]=butter(4,wn,"bandpass"); [sos,g]=zp2sos(z,p,k); filtfilt(sos,g,x)`. Band edges, cutoff clamps, grids, metrics, ties, generator inputs and seeds remain as originally specified.','',
'Every unique design is checked before use: maximum pole radius <1 for both the ZPK design and the realized SOS sections, and |gain at the arithmetic passband centre−1|<1e-3. A failed guard raises an error and stops execution. All guards passed at 500 Hz and at every actual rodent sampling-rate value. Full guard registry: '+link(OUT/'all_corrected_filter_guards.csv')+'.','',
f'The audit evaluated **{len(audit)} unique bands on ten saved signals ({len(detailed)} comparisons)**: five held-out coupled inputs (H1 keep1, H1 keep.15, H1 distractor3, H2 ratio3, H4; first repeat each), and five development inputs (main sparsity1/.15, main distractor3, random-fP sparsity.5/distractor1.5; first repeat each). Every band was tested on every selected signal. The complete original input paths/IDs, per-input relative L2 differences and RMS values are in '+link(OUT/'filter_audit_500Hz_trials.csv')+'.','',
f'Not every relative difference was <1e-6; the maximum was {detailed.relative_L2_difference.max():.12g}. Both held-out and development phase/amplitude band sets included failures of that tolerance. Therefore all 5,400 held-out comparator rows and all {result["development_comparator_rows_replaced"]:,} previously run affected development comparator rows were replaced in new corrected CSVs. The 1,350 held-out APC rows were reused byte-for-byte by field, and all 24 rodent APC bout estimates were reused unchanged. No signal was regenerated.','',
'Original results remain in their original directories; the earlier final attempt is preserved under '+link(OUT/'previous_direct_form_attempt/RESULTS_final.md','previous_direct_form_attempt')+'. Earlier direct-form rodent rows and inference are **superseded**, as are the direct-form comparator rows in the development/held-out files for this final analysis. Their historical files are retained. Corrected held-out trials: '+link(OUT/'corrected_heldout/heldout_trials.csv')+'. Corrected development trials: '+link(OUT/'corrected_development/all_trials.csv')+'.','',
'### Old versus SOS: v2.0 prespecified C1–C4','',table(crit,['criterion','old_result','new_result','old_numbers','new_numbers']),
'The original criterion formulas, per-level best-metric tie order and paired exact one-sided McNemar calculation were reused unchanged. The table recalculates criteria against the corrected A2′ comparators; v2 frequency picks, scores, event tests and required event-z AUCs were not rerun. Best-A2′ selections and counts: '+link(OUT/'corrected_heldout/best_A2_by_level.csv')+'. Full details: '+link(OUT/'corrected_heldout/decision_details.json')+'. Old/new criterion CSV: '+link(OUT/'v2_criteria_old_vs_SOS.csv')+'.','',
'### APC v1.0 versus A2′: descriptive old/new counts','',
'The following counts pool each scenario/dataset across its requested levels; A2′ is chosen per level to maximize coupled recovery or minimize null false recovery, separately for joint/strict endpoints. Primary v1.0 counts are unchanged. This is descriptive and is not a new v1.0 pass/fail test.','',table(v1groups,['scenario','dataset','endpoint','v1_count','old_best_A2','SOS_best_A2']),
'Per-level choices and counts: '+link(OUT/'v1_vs_A2_old_vs_SOS.csv')+'. All held-out comparator old/new recovery/error/near-fD groups: '+link(OUT/'heldout_comparator_old_vs_SOS_summary.csv')+'. Per-trial picks/scores: '+link(OUT/'heldout_comparator_old_vs_new_trials.csv')+'.','',
'### Development old/new summary','',
'Each row sums successes over its 25-trial method-by-level groups; n_groups identifies the denominator (25*n_groups). Null-stage rows count false recovery; other stages count recovery. The two phase-grid spacings are separate analyses.','',table(summary_devs,['stage','configuration','fp_grid_step_hz','n_groups','old_joint','SOS_joint','old_strict','SOS_strict']),
'All per-method/level error and recovery comparisons: '+link(OUT/'development_comparator_old_vs_SOS_summary.csv')+'. Per-trial comparisons: '+link(OUT/'development_comparator_old_vs_SOS_trials.csv')+'. Updated development null AUCs: '+link(OUT/'corrected_development/null_specificity_auc.csv')+'.','',
'### Rodent: superseded direct-form versus SOS','',
'All 96 comparator rows were rerun on the identical saved 24 bouts. The raw/Ozkurt/KLMI/GLM grids and selected-pair metrics are unchanged. Old/new per-bout values: '+link(OUT/'rodent_old_vs_SOS.csv')+'. Equal-bout and duration-weighted Welch/Hedges/bootstrap results were recomputed, with identical 10,000 shared resample indices at seed 20261022. Full old/new statistics: '+link(OUT/'rodent_statistics_old_vs_SOS.csv')+'.','',
table(rs[rs.weighting=='equal_bout'],['method','metric','mean_difference_old','mean_difference_SOS','welch_t_old','welch_t_SOS','p_two_sided_old','p_two_sided_SOS','hedges_g_old','hedges_g_SOS']),
'Old/new exact boundary counts:','',table(rb,['method','state','boundary_4_old','boundary_4_SOS','boundary_12_old','boundary_12_SOS']),
'### Per-band 500-Hz audit','',
'Bounds are realized passband edges in Hz. Each row has ten input comparisons. Centre gain is the single-pass magnitude; filtfilt applies that realization in both directions. The relative L2 range is calculated on the complete filtered records, including their endpoints. SOS pole radii are from the ZPK design; the detailed CSV and guard registry also contain the realized SOS-section pole radius.','',
table(audit,['low_hz','high_hz','band_uses','direct_max_pole_radius','sos_max_pole_radius','direct_center_gain','sos_center_gain','min_relative_L2_difference','max_relative_L2_difference']),
'Per-band CSV: '+link(OUT/'filter_audit_500Hz_bands.csv')+'.','']
report=OUT/'RESULTS_final.md';body=report.read_text(encoding='utf-8');head,rest=body.split('\n',1)
body=head+'\n\n'+'\n'.join(filter_section)+'\n'+rest
new_results=', '.join(f'{r.criterion} {r.new_result}' for _,r in crit.iterrows())
body=body.replace('APC v2.0 remains a negative result (C1 FAIL, C2 PASS, C3 FAIL, C4 FAIL).',f'APC v2.0 corrected criteria: {new_results}.')
body=body.replace('the same saved held-out input','the same saved held-out input')
# Replace the legacy runtime/deviation prose, retaining all earlier deviation records in the archive.
cut=body.index('## Runtime, deviations and verification')
body=body[:cut]+'## Runtime, deviations and verification\n\n'
runtimes={p.name:load(p)['elapsed_seconds'] for p in OUT.glob('sos_*_runtime.json')}
body+='Elapsed compute seconds by stage/worker (three workers overlap in wall time):\n\n'+table(pd.DataFrame([{'stage':k,'elapsed_seconds':v} for k,v in runtimes.items()]),['stage','elapsed_seconds'])+'\n'
body+='Figure/statistics build elapsed seconds: '+str(load(OUT/'build_runtime.json')['elapsed_seconds'])+'. Startup, inspection and final integrity-check time are excluded. The earlier canonical-only stage took '+str(load(OUT/'analysis_runtime.json')['elapsed_seconds'])+' seconds.\n\n'
olddevs=load(OUT/'previous_direct_form_attempt/deviations.json')['deviations']
deviations=olddevs+[
 {'type':'authorized numerical correction','detail':'User explicitly authorized SOS realization of the unchanged nominal comparator Butterworth filters, guard checks, full affected comparator reruns, and rebuilding summaries/criteria/figures. Tagged source remains untouched.'},
 {'type':'tooling fix','detail':'Wilson errorbar lengths clipped at zero only for floating-point endpoint rounding; the analytic Wilson bounds/formula and trial counts are unchanged.'},
 {'type':'tooling fix','detail':'Figure 1 colorbar corrected to standardized CWT magnitude; canonical numeric outputs unchanged.'},
 {'type':'figure layout','detail':'Visual QA found legend/title and caption/xlabel crowding. Plot margins were increased; no data, intervals or method results changed.'},
 {'type':'export bookkeeping','detail':'Final tables/figures use canonical_results_export_corrected.csv for canonical session/seed metadata. The initial raw export remains preserved.'},
 {'type':'execution scope','detail':f'The common development runner also computed {result["additional_null_A0_rows_not_used"]} A0-null rows absent from the original analysis. They remain only in worker intermediates and were excluded from the corrected original-result tables, criteria and figures.'},
 {'type':'parser handling','detail':'CSV readers for correction comparisons preserve literal stage=null instead of treating null as missing.'}]
(OUT/'deviations.json').write_text(json.dumps({'metadata':meta,'status':'COMPLETE','deviations':deviations},indent=2),encoding='utf-8')
body+='The original direct-form failure is superseded by the authorized numerical correction. All newly used SOS designs passed their guards; no tagged APC method change or new candidate was made. Original simulation inputs and original historical outputs remain unchanged. Full earlier and resumed tooling/deviation records: '+link(OUT/'deviations.json')+'.\n\n'
body+='Additional metadata limits remain: E1/row 1 is documented, but shank/layer/acquisition-index mapping is unavailable locally; no other session with eligible documented run/rest bouts was established. Optional replication was not run.\n\n'
body+='Verification: '+link(OUT/'verification.json')+'. Complete final output hashes: '+link(OUT/'output_manifest.json')+'. The root STOPPED.json is the preserved historical stop record; the current status is '+link(OUT/'RESUME_STATUS.json')+'.\n'
report.write_text(body,encoding='utf-8')
verification={'status':'COMPLETE','metadata':meta,'all_SOS_guards_passed':True,'unique_corrected_bands_including_actual_rodent_fs':len(G),'audit_unique_bands':len(audit),'audit_comparisons':len(detailed),'heldout_APC_rows_identical':apc_verified,'rodent_APC_rows_identical':24,'heldout_comparator_rows_corrected':5400,'development_comparator_rows_corrected':result['development_comparator_rows_replaced'],'original_candidate3_files_unchanged':len(prior['files']),'original_development_input_hashes_unchanged':input_checks,'frozen_files_unchanged':True,'git_clean_and_tags_unchanged':True,'figures_checked':len(fm['figures']),'PNG_dpi':300}
(OUT/'verification.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
(OUT/'RESUME_STATUS.json').write_text(json.dumps({'status':'COMPLETE','metadata':meta,'criteria_old_vs_new':crit[['criterion','old_result','new_result']].to_dict('records')},indent=2),encoding='utf-8')
for a,b in re.findall(r'\]\((?:<([^>]+)>|([^\s)]+))\)',body):
 p=a or b
 if not p.startswith('http'):assert Path(p).exists(),p
files=[]
for p in sorted(OUT.rglob('*')):
 if not p.is_file() or p.name=='output_manifest.json' and p.parent==OUT or any(part in ['__pycache__','plot_config'] for part in p.relative_to(OUT).parts):continue
 files.append({'path':str(p.relative_to(OUT)),'bytes':p.stat().st_size,'sha256':sha(p)})
(OUT/'output_manifest.json').write_text(json.dumps({'status':'COMPLETE','metadata':meta,'files':files},indent=2),encoding='utf-8')
print(json.dumps({'status':'COMPLETE','manifest_files':len(files),'figures':len(fm['figures']),'criteria':new_results,'report':str(report)}))
