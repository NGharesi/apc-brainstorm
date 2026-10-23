"""Merge new v3 rows with unchanged old estimates and copy fixed statistics."""
from pathlib import Path
import json,hashlib,shutil,difflib,sys
O=Path(__file__).resolve().parent;R=O.parent.parent;C=O/'phaseC';sys.path.insert(0,str(R/'pydeps'))
import pandas as pd
def js(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=js(C/'provenance.json');assert all((C/f'worker{w}_complete.json').exists() for w in range(1,5));assert not (O/'STOPPED.md').exists()
for x in m['reused_files_sha256']:assert sha(Path(x['path']))==x['sha256']
rod=pd.concat([pd.read_csv(C/f'rodent_worker{w}.csv',encoding='utf-8',float_precision='round_trip') for w in range(1,5)]);assert len(rod)==3646 and rod.input_id.nunique()==3646
ecog=pd.concat([pd.read_csv(C/f'ecog_worker{w}.csv',encoding='utf-8',float_precision='round_trip') for w in range(1,5)]);assert len(ecog)==2648 and not ecog.duplicated(['patient','recording','bout']).any()
rod.to_csv(C/'rodent_v3_unique_estimates.csv',index=False,encoding='utf-8',float_format='%.17g');ecog.to_csv(C/'ecog_v3_estimates.csv',index=False,encoding='utf-8',float_format='%.17g')
mapping=pd.read_csv(C/'rodent_analysis_rows.csv',encoding='utf-8');featurecols=[z for z in rod.columns if z not in mapping.columns or z=='input_id'];new=mapping.merge(rod[featurecols],on='input_id',validate='many_to_one')
def write_script(path,old,new):
    path.write_text(new,encoding='utf-8');path.with_suffix(path.suffix+'.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='original fixed pipeline',tofile=str(path))),encoding='utf-8')
for label,source,prefix,subdir in [('prespecified_5s',R/'revision_checks/rodent_multi','regional','rodent5s'),('POST_HOC_2s',R/'revision_checks/rodent_multi/posthoc_2s','posthoc_2s','POST_HOC_rodent2s')]:
    out=C/subdir;assert not out.exists();out.mkdir();old=pd.read_csv(source/(prefix+'_bout_estimates.csv'),encoding='utf-8',float_precision='round_trip');fresh=new[new.bout_set.eq(label)].copy()
    fresh['analysis_type']='POST HOC sensitivity: 2-s minimum bouts' if label=='POST_HOC_2s' else 'Prespecified 5-s analysis';fresh['post_hoc']=label=='POST_HOC_2s';fresh['minimum_bout_s']=2 if label=='POST_HOC_2s' else 5;fresh['provenance_json']=json.dumps(m,separators=(',',':'))
    data=pd.concat([old,fresh],ignore_index=True);assert not data.duplicated(['analysis','session','state','bout','method']).any();data.to_csv(out/(prefix+'_bout_estimates.csv'),index=False,encoding='utf-8',float_format='%.17g')
    meta=m.copy();meta.update(git_commit=m['freeze_commit'],analysis_type=fresh.analysis_type.iloc[0],post_hoc=label=='POST_HOC_2s',minimum_bout_s=int(fresh.minimum_bout_s.iloc[0]),apc_comparison='new v3 plus unchanged saved v1/scans')
    (out/(prefix+'_protocol_record.json' if prefix=='regional' else prefix+'_provenance.json')).write_text(json.dumps(meta,indent=2),encoding='utf-8');(out/(prefix+'_bouts_runtime.json')).write_text(json.dumps(dict(status='COMPLETE',rows=len(data),provenance='phaseC/provenance.json')),encoding='utf-8')
    shutil.copy2(R/'revision_checks/rodent_multi/regional_xml_grouping.json',out/'regional_xml_grouping.json')
    if prefix=='regional':
        p=source/'compute_regional_statistics.py';s=p.read_text(encoding='utf-8');t=s.replace("OUT=ROOT/'revision_checks/rodent_multi'","OUT=Path(__file__).resolve().parent").replace("'APC-v1.0'","'APC-v3.0'")
        write_script(out/'compute_regional_statistics.py',s,t)
        p=source/'fit_regional_mixed_models.m';s=p.read_text(encoding='utf-8');write_script(out/p.name,s,s.replace('APC-v1.0','APC-v3.0'))
    else:
        p=source/'posthoc_2s_statistics.py';s=p.read_text(encoding='utf-8');t=s.replace("PARENT=OUT.parent","PARENT=OUT").replace("'APC-v1.0'","'APC-v3.0'");write_script(out/p.name,s,t)
        p=source/'posthoc_2s_fit_mixed_models.m';s=p.read_text(encoding='utf-8');write_script(out/p.name,s,s.replace('APC-v1.0','APC-v3.0'))
# ECoG: restrict the old statistical pipeline to the v3-protocol endpoints.
E=R/'revision_checks/ecog_miller_motor';out=C/'ecog';assert not out.exists();out.mkdir()
for name in ['bouts.csv','electrodes.csv','analysed_rest_spectral_peaks.csv','bout_burst_counts.csv']:shutil.copy2(E/name,out/name)
old=pd.read_csv(E/'ecog_bout_estimates.csv',encoding='utf-8',float_precision='round_trip');old['estimator_git_head']=old.git_head;old=old.drop(columns=['eligible_patient','valid','flagged']);fresh=ecog.copy();fresh['git_head']=m['freeze_commit'];fresh['estimator_git_head']=m['freeze_commit']
data=pd.concat([old,fresh],ignore_index=True);assert len(data)==2648*6 and not data.duplicated(['patient','recording','bout','method']).any()
for w in range(1,5):data.iloc[w-1::4].to_csv(out/f'estimates_w{w}.csv',index=False,encoding='utf-8',float_format='%.17g')
(out/'analysis_provenance.json').write_text(json.dumps(m,indent=2),encoding='utf-8');(out/'provenance.json').write_text(json.dumps(m,indent=2),encoding='utf-8');(out/'estimates_runtime.json').write_text(json.dumps(dict(status='COMPLETE',source='phaseC workers',rows=len(data))),encoding='utf-8')
s=(E/'ecog_statistics.py').read_text(encoding='utf-8');t=s.replace("O.parent.parent/'pydeps'","Path(r'C:\\Users\\nghare\\.brainstorm\\process\\pydeps')").replace("methods=['APC-v1.0','MVL-raw','MVL-Ozkurt','KLMI','GLM']","methods=['APC-v3.0']").replace("'amendment1_runtime.json'","'estimates_runtime.json'").replace('2648*5','2648*6').replace('.size().eq(5)','.size().eq(6)').replace("'APC-v1.0'","'APC-v3.0'")
t=t.replace(", 'sensitivity_b':d[d.eligible_patient&d.duration_s.ge(2.5)]",'')
t=t.replace("        for field,endpoint in [('mean_fP_hz','fP_state'),('mean_fA_hz','fA_state')]:state_contrast(subset,'movement',method,field,endpoint,direction=False)\n",'').replace("        state_contrast(subset,'imagery',method,'mean_ozkurt_mvl','imagery_coupling')\n",'').replace("        for subtype in ['hand','tongue']:state_contrast(subset,'movement',method,'ozkurt_mvl','subtype_coupling',direction=False,subtype=subtype)\n",'')
write_script(out/'ecog_statistics.py',s,t)
s=(E/'ecog_mixed_model.m').read_text(encoding='utf-8');write_script(out/'ecog_mixed_model.m',s,s.replace('coefficients=dataset2table(model.Coefficients);',"coefficients=model.Coefficients;if isa(coefficients,'dataset'),coefficients=dataset2table(coefficients);end;"))
# Current release returns a table; preserve either supported representation.
print(json.dumps(dict(status='PREPARED',rodent_unique_inputs=len(rod),rodent_analysis_rows=len(new),ecog_rows=len(data))),flush=True)
