from pathlib import Path
import sys,json,hashlib,datetime
O=Path(__file__).resolve().parent;R=O.parent.parent;sys.path.insert(0,str(R/'pydeps'))
import pandas as pd
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return pd.read_csv(p,encoding='utf-8',float_precision='round_trip')
jobs=read(R/'revision_checks/v3_aperiodic/phaseC/rodent_inputs.csv')
mapping=read(R/'revision_checks/v3_aperiodic/phaseC/rodent_analysis_rows.csv')
lookup={(z.session,int(z.channel_index),int(z.start_idx),int(z.stop_idx)):int(z.input_id) for z in jobs.itertuples()}
refs={};source_files=[];mapped=[];precision=[];all_references=[]
for label,folder,prefix in [('prespecified_5s',R/'revision_checks/rodent_multi','regional'),('POST_HOC_2s',R/'revision_checks/rodent_multi/posthoc_2s','posthoc_2s')]:
 p=folder/(prefix+'_bout_estimates.csv');D=read(p);source_files.append({'path':str(p),'sha256':sha(p)})
 for z in D[D.method.isin(['APC-v1.0','MVL-Ozkurt'])].itertuples():
  meta=json.loads(z.provenance_json);key=(z.session,int(z.channel_index),int(meta['start_idx']),int(meta['stop_idx']));ident=lookup[key]
  values={'input_id':ident,'method':z.method,'fp':z.fP_hz,'fa':z.fA_hz,'raw':z.raw_mvl,'coupling':z.ozkurt_mvl,'pref':z.preferred_phase_deg,'status':int(z.status)}
  all_references.append(values|{'bout_set':label,'animal':z.animal,'session':z.session,'analysis':z.analysis,'state':z.state,'bout':int(z.bout)})
  prior=refs.get((ident,z.method))
  if prior:
   for col in ['fp','fa','status']:
    assert prior[col]==values[col] or pd.isna(prior[col]) and pd.isna(values[col]),(ident,col)
   for col in ['raw','coupling','pref']:
    if prior[col]!=values[col] and not (pd.isna(prior[col]) and pd.isna(values[col])):
     precision.append({'input_id':ident,'method':z.method,'field':col,'first_saved':prior[col],'other_saved':values[col],'difference':values[col]-prior[col]})
  else:refs[ident,z.method]=values
  if z.method=='APC-v1.0':mapped.append((ident,label,z.animal,z.session,z.analysis,int(z.channel_index),z.state,int(z.bout)))
expected=[(int(z.input_id),z.bout_set,z.animal,z.session,z.analysis,int(z.channel_index),z.state,int(z.bout)) for z in mapping.itertuples()]
assert sorted(mapped)==sorted(expected)
assert len(refs)==2*len(jobs)
jobs.to_csv(O/'rodent_inputs.csv',index=False,encoding='utf-8');mapping.to_csv(O/'rodent_analysis_rows.csv',index=False,encoding='utf-8');pd.DataFrame(refs.values()).to_csv(O/'rodent_saved_references.csv',index=False,encoding='utf-8',float_format='%.17g')
pd.DataFrame(all_references).to_csv(O/'rodent_all_saved_references.csv',index=False,encoding='utf-8',float_format='%.17g')
pd.DataFrame(precision).to_csv(O/'rodent_saved_csv_precision_differences.csv',index=False,encoding='utf-8',float_format='%.17g')
E=R/'revision_checks/ecog_miller_motor';B=read(E/'bouts.csv');elig=read(E/'patient_eligibility.csv');patients=elig.loc[elig.eligible.astype(str).str.lower().isin(['1','true']),'patient']
B=B[B.analysed.astype(bool)&B.patient.isin(patients)];assert len(patients)==18 and len(B)==2642
B.to_csv(O/'ecog_bouts.csv',index=False,encoding='utf-8')
for p in [E/'bouts.csv',E/'electrodes.csv',E/'patient_eligibility.csv',E/'analysed_rest_spectral_peaks.csv',R/'revision_checks/paper2_ablation/ecog_bout_estimates.csv',R/'revision_checks/rodent_multi/compute_rodent_statistics.py',R/'revision_checks/rodent_multi/compute_regional_statistics.py',R/'revision_checks/rodent_multi/posthoc_2s/posthoc_2s_statistics.py',*sorted((E/'prep').glob('*.mat'))]:
 source_files.append({'path':str(p),'sha256':sha(p)})
for p in sorted(set(jobs.source_file)):
 f=Path(p);source_files.append({'path':str(f),'sha256':sha(f),'bytes':f.stat().st_size})
record={'status':'PREPARED','rodent_physical_inputs':len(jobs),'rodent_analysis_rows':len(mapping),'ecog_bouts':len(B),'eligible_ecog_patients':18,'source_files':source_files,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(O/'real_input_provenance.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in record.items() if k!='source_files'},indent=2))
