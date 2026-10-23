from pathlib import Path
import sys,json,csv,math,importlib.util,hashlib,collections,time
ROOT=Path(r'C:\Users\nghare\.brainstorm\process');OUT=ROOT/'revision_checks/final';HD=ROOT/'revision_checks/v2/candidate_03';REPO=ROOT/'apc-brainstorm-publish'
sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
import pandas as pd
START=time.perf_counter()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def read(p):
 with Path(p).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def write(p,rows):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 if 'PJSON' in globals():
  for r in rows:r.setdefault('filter_correction_provenance_json',PJSON)
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with p.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
def module(name,p):
 spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
M=module('heldout_math',REPO/'analysis/v2_revision/build_heldout_results.py');D=module('development_math',ROOT/'revision_checks/v1_followup/build_followup.py')
META=load(OUT/'sos_correction_provenance.json');PJSON=json.dumps(META,separators=(',',':'))
def realized(old):
 d=json.loads(old);d['filter_realization']='[z,p,k]=butter(4,...); [sos,g]=zp2sos(z,p,k); filtfilt(sos,g,x)';d['guard']=META['filter_guard'];return json.dumps(d,separators=(',',':'))
audit=pd.read_csv(OUT/'filter_audit_500Hz_trials.csv');assert audit.guard_passed.eq(1).all()
summary=audit.groupby(['low_hz','high_hz','band_uses'],sort=True).agg(n_inputs=('relative_L2_difference','size'),direct_max_pole_radius=('direct_max_pole_radius','max'),sos_max_pole_radius=('sos_max_pole_radius','max'),direct_center_gain=('direct_center_gain','first'),sos_center_gain=('sos_center_gain','first'),max_relative_L2_difference=('relative_L2_difference','max'),min_relative_L2_difference=('relative_L2_difference','min')).reset_index()
summary['provenance_json']=PJSON;summary.to_csv(OUT/'filter_audit_500Hz_bands.csv',index=False,encoding='utf-8')
old=read(HD/'heldout_trials.csv');new=[]
for w in [1,2,3]:
 assert load(OUT/f'sos_heldout_worker{w}_runtime.json')['status']=='COMPLETE';new+=read(OUT/f'sos_heldout_worker{w}_trials.csv')
assert len(new)==5400
index={(r['input_id'],r['configuration'],r['method']):r for r in new};assert len(index)==5400
changed=[];merged=[]
for r in old:
 s=r.copy();key=(r['input_id'],r['configuration'],r['method'])
 if key in index:
  n=index[key]
  for k in ['recovered_fp_hz','recovered_fa_hz','score','ozkurt_mvl','status','valid']:s[k]=n[k]
  s['comparator_settings_json']=realized(s['comparator_settings_json'])
  changed.append(dict(input_id=r['input_id'],scenario=r['scenario'],dataset=r['dataset'],level=r['level'],configuration=r['configuration'],method=r['method'],old_fP=r['recovered_fp_hz'],new_fP=s['recovered_fp_hz'],old_fA=r['recovered_fa_hz'],new_fA=s['recovered_fa_hz'],old_score=r['score'],new_score=s['score'],old_joint=int(M.success(r)),new_joint=int(M.success(s)),old_strict=int(M.success(r,True)),new_strict=int(M.success(s,True)),provenance_json=PJSON))
 s['filter_correction_provenance_json']=PJSON;merged.append(s)
assert len(merged)==6750
corrected=OUT/'corrected_heldout';corrected.mkdir(exist_ok=True)
write(corrected/'heldout_trials.csv',merged);write(OUT/'heldout_comparator_old_vs_new_trials.csv',changed)
summ=M.summarize(merged);sp=M.specificity(merged)
meta=load(HD/'generate_runtime.json')['metadata'];meta['comparator_settings']['filter_realization']='guarded SOS';meta['filter_correction']=META
decs,details,choices=M.decide(merged,sp,meta)
write(corrected/'heldout_recovery_summary.csv',summ);write(corrected/'heldout_null_specificity_auc.csv',sp);write(corrected/'best_A2_by_level.csv',choices);write(corrected/'decision_criteria.csv',decs)
(corrected/'decision_details.json').write_text(json.dumps(dict(details,filter_correction=META),indent=2),encoding='utf-8')
olddec=read(HD/'decision_criteria.csv');sides=[]
for o,n in zip(olddec,decs):sides.append(dict(criterion=o['criterion'],old_result=o['result'],new_result=n['result'],old_numbers=o['numbers'],new_numbers=n['numbers'],provenance_json=PJSON))
write(OUT/'v2_criteria_old_vs_SOS.csv',sides)
def v1_comparisons(rows):
 result=[]
 for scenario in ['H1_sparsity','H1_distractor','H2','H4']:
  for dataset in ['coupled','timing_null','no_coupled_burst']:
   sub=[r for r in rows if r['scenario']==scenario and r['dataset']==dataset]
   for level in sorted({float(r['level']) for r in sub}):
    rr=[r for r in sub if float(r['level'])==level];primary=[r for r in rr if r['configuration']=='v1.0']
    for strict in [False,True]:
     counts={m:sum(M.success(r,strict) for r in rr if r['configuration']=='A2_prime' and r['method']==m) for m in M.METRICS}
     best=(min if dataset!='coupled' else max)(M.METRICS,key=lambda m:counts[m])
     result.append(dict(scenario=scenario,dataset=dataset,level=level,endpoint='strict_joint' if strict else 'joint',v1_count=sum(M.success(r,strict) for r in primary),best_A2_metric=best,best_A2_count=counts[best]))
 return result
o=v1_comparisons(old);n=v1_comparisons(merged);side=[]
for a,b in zip(o,n):side.append(dict(scenario=a['scenario'],dataset=a['dataset'],level=a['level'],endpoint=a['endpoint'],v1_count=a['v1_count'],old_best_A2_metric=a['best_A2_metric'],old_best_A2_count=a['best_A2_count'],SOS_best_A2_metric=b['best_A2_metric'],SOS_best_A2_count=b['best_A2_count'],provenance_json=PJSON))
write(OUT/'v1_vs_A2_old_vs_SOS.csv',side)
oldsum=M.summarize(old);keys=M.KEYS
ix={tuple(r[k] for k in keys):r for r in oldsum};side=[]
for r in summ:
 if r['configuration'] not in ['A1_prime','A2_prime']:continue
 q=ix[tuple(r[k] for k in keys)];item={k:r[k] for k in keys}
 for field in ['joint','strict_joint','fP_recovery','fA_recovery','mean_fP_error','mean_fA_error','picks_near_fD']:item['old_'+field]=q[field];item['SOS_'+field]=r[field]
 item['provenance_json']=PJSON;side.append(item)
write(OUT/'heldout_comparator_old_vs_SOS_summary.csv',side)

# All development configurations previously run: preserve APC values, replace comparator estimates by key.
DEV=ROOT/'revision_checks/v1_rerun';FU=ROOT/'revision_checks/v1_followup';olddev=[]
for p in [DEV/'main_trials.csv',DEV/'random_fp_trials.csv',DEV/'null_trials.csv',FU/'a2_trials.csv',FU/'slow_trials.csv']:olddev+=read(p)
def keydev(r):return (r['stage'],r['benchmark'],r['dataset'],float(r['level']),int(r['repeat_index']),r['configuration'],r['method'].replace('-scan',''),float(r['fp_grid_step_hz']))
devnew=[]
for w in [1,2,3]:
 assert load(OUT/f'sos_development_worker{w}_runtime.json')['status']=='COMPLETE';devnew+=read(OUT/f'sos_development_worker{w}_trials.csv')
ni={keydev(r):r for r in devnew};assert len(ni)==len(devnew)
devmerged=[];dc=[];missing=[];used=set()
for r in olddev:
 s=r.copy()
 if r['method']!='APC':
  key=keydev(r)
  if key not in ni:missing.append(key);continue
  n=ni[key];used.add(key)
  for k in ['recovered_fp_hz','recovered_fa_hz','score','status_code','valid']:s[k]=n[k]
  s['comparator_settings_json']=realized(s['comparator_settings_json'])
  dc.append(dict(stage=r['stage'],benchmark=r['benchmark'],dataset=r['dataset'],level=r['level'],repeat_index=r['repeat_index'],configuration=r['configuration'],method=r['method'],fp_grid_step_hz=r['fp_grid_step_hz'],old_fP=r['recovered_fp_hz'],SOS_fP=s['recovered_fp_hz'],old_fA=r['recovered_fa_hz'],SOS_fA=s['recovered_fa_hz'],old_score=r['score'],SOS_score=s['score'],provenance_json=PJSON))
 s['filter_correction_provenance_json']=PJSON;devmerged.append(s)
assert not missing,missing[:5]
write(OUT/'development_comparator_old_vs_SOS_trials.csv',dc)
write(OUT/'corrected_development/all_trials.csv',devmerged)
devs=D.summaries(devmerged);olds=D.summaries(olddev);ix={tuple(r[k] for k in D.KEYS):r for r in olds};dside=[]
for r in devs:
 if r['method']=='APC':continue
 q=ix[tuple(r[k] for k in D.KEYS)];item={k:r[k] for k in D.KEYS}
 for f in ['joint_recovery','strict_joint_recovery','fP_recovery','fA_recovery','mean_abs_fP_error_hz','mean_abs_fA_error_hz','boundary_fP_4','boundary_fP_12']:item['old_'+f]=q[f];item['SOS_'+f]=r[f]
 item['provenance_json']=PJSON;dside.append(item)
write(OUT/'development_comparator_old_vs_SOS_summary.csv',dside)
base=OUT/'corrected_development';write(base/'all_summary.csv',devs)
for stage,file in [('main','main_summary.csv'),('random_fp','random_fp_summary.csv'),('null','null_recovery_summary.csv')]:
 rows=[r for r in devs if r['stage']==stage and r['configuration']!='A2'];write(base/'v1_rerun'/file,rows)
for stage,file in [('main','a2_main_summary.csv'),('random_fp','a2_random_fp_summary.csv'),('null','a2_null_summary.csv')]:write(base/'v1_followup'/file,[r for r in devs if r['stage']==stage and r['configuration']=='A2'])
write(base/'slow_summary.csv',[r for r in devs if r['stage']=='slow'])
write(base/'null_specificity_auc.csv',D.aucs(devmerged))

# Keep primary rodent APC outputs exactly; replace only the comparator rows.
rod_old=read(OUT/'previous_direct_form_attempt/rodent_bouts.csv');rod_new=read(OUT/'sos_rodent_comparator_bouts.csv');assert len(rod_new)==96
rod=[r for r in rod_old if r['method']=='APC v1.0']+rod_new
for r in rod:r['filter_correction_provenance_json']=PJSON
write(OUT/'rodent_bouts_SOS.csv',rod)
ri={(r['state'],r['bout'],r['method']):r for r in rod_old};rs=[]
for r in rod_new:
 q=ri[(r['state'],r['bout'],r['method'])];item={k:r[k] for k in ['state','bout','method']}
 for f in ['fP_hz','fA_hz','raw_mvl','ozkurt_mvl','preferred_phase_deg','boundary_fP_4','boundary_fP_12']:item['old_'+f]=q[f];item['SOS_'+f]=r[f]
 item['provenance_json']=PJSON;rs.append(item)
write(OUT/'rodent_old_vs_SOS.csv',rs)
result={'status':'COMPLETE','heldout_comparator_rows':len(new),'heldout_APC_rows_reused':1350,'development_comparator_rows_replaced':len(dc),'additional_null_A0_rows_not_used':len(ni)-len(used),'rodent_comparator_rows':96,'criteria':decs,'metadata':META,'elapsed_seconds':time.perf_counter()-START}
(OUT/'correction_summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ['metadata','criteria']}));print(json.dumps([(d['criterion'],d['result'],d['numbers']) for d in decs]))
