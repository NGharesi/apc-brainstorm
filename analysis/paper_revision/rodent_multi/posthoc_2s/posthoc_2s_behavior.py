"""POST HOC 2-s sensitivity; unchanged saved tracking masks and channel choices."""
from pathlib import Path
import sys,json,hashlib,time,traceback
OUT=Path(__file__).resolve().parent;PARENT=OUT.parent;ROOT=PARENT.parent.parent
sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
import pandas as pd
from scipy.io import loadmat
META=json.loads((OUT/'posthoc_2s_provenance.json').read_text(encoding='utf-8'))
META=META|dict(stage='POST HOC 2-s bout extraction from unchanged saved tracking masks')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def intervals(mask):
    d=np.diff(np.r_[False,mask,False].astype(int));return np.flatnonzero(d==1),np.flatnonzero(d==-1)-1
def write(rows,name):
    d=pd.DataFrame(rows);d['analysis_type']=META['analysis_type'];d['post_hoc']=True;d['minimum_bout_s']=2;d['provenance_json']=json.dumps(META,separators=(',',':'))
    d.to_csv(OUT/name,index=False,encoding='utf-8');return d
mapping=pd.read_csv(PARENT/'mapping_checks.csv',encoding='utf-8');selection=pd.read_csv(PARENT/'regional_selected_channels.csv',encoding='utf-8')
original=pd.read_csv(PARENT/'regional_behavior_summary.csv',encoding='utf-8');original_bouts=pd.read_csv(PARENT/'regional_bouts.csv',encoding='utf-8')
started=time.perf_counter();allbouts=[];summary=[]
try:
    for _,q in mapping.iterrows():
        p=PARENT/(q.session+'_regional_tracking.npz');data=np.load(p);t=data['time'];base=original[original.session==q.session].iloc[0].to_dict()
        if q.session=='ec013.157':lt=loadmat(Path(r'D:\APC_project\RealDatasets\LFP_data\EC3_dataset_real.mat'),variable_names=['R2'],simplify_cells=True)['R2']['Time']
        else:lt=loadmat(q.lfp_file,variable_names=['Time'],simplify_cells=True)['Time']
        dtlfp=np.median(np.diff(lt));rows=[]
        for state in ['run','rest']:
            a,b=intervals(data[state+'_mask']);n=0
            for s,e in zip(a,b):
                duration=(e-s+1)/39.0625
                if duration<2:continue
                start=float(t[s]);stop=float(t[e]+1/39.0625);first=int(np.searchsorted(lt,start,side='left'));last=int(np.searchsorted(lt,stop,side='left'))-1
                assert 0<=first<=last<len(lt)
                n+=1;rows.append(dict(animal=q.animal,session=q.session,state=state,bout=n,tracking_start_idx=s+1,tracking_stop_idx=e+1,start_time_s=start,stop_exclusive_s=stop,duration_s=duration,
                                     lfp_start_idx=first+1,lfp_stop_idx=last+1,lfp_duration_s=float(lt[last]-lt[first]+dtlfp),cm_per_unit=base['cm_per_unit'],source_tracking_npz=str(p),source_tracking_sha256=sha(p)))
        allbouts+=rows
        for state in ['run','rest']:
            durations=[r['duration_s'] for r in rows if r['state']==state];base[state+'_bouts']=len(durations)
            base.update({state+'_total_duration_s':sum(durations),state+'_mean_duration_s':float(np.mean(durations)) if durations else np.nan,
                         state+'_median_duration_s':float(np.median(durations)) if durations else np.nan,state+'_min_duration_s':min(durations) if durations else np.nan,state+'_max_duration_s':max(durations) if durations else np.nan})
        base['included']=base['run_bouts']>=5 and base['rest_bouts']>=5;base['source_tracking_npz']=str(p);base['source_tracking_sha256']=sha(p)
        base.pop('provenance_json',None);summary.append(base)
        print(f"POST HOC {q.session}: run={base['run_bouts']} rest={base['rest_bouts']} included={base['included']}",flush=True)
    behavior=write(summary,'posthoc_2s_behavior_summary.csv');bouts=write(allbouts,'posthoc_2s_bouts.csv')
    shared=original_bouts.merge(bouts,on=['session','state','lfp_start_idx','lfp_stop_idx'],suffixes=('_5s','_posthoc_2s'),validate='one_to_one')
    assert len(shared)==len(original_bouts),'METHOD-RELEVANT: a prespecified 5-s bout changed or disappeared'
    selected=selection.merge(behavior[['session','run_bouts','rest_bouts','included']],on='session')
    selected['inclusion_reason']=np.where(selected.included,'POST HOC: >=5 run and >=5 rest bouts with >=2-s minimum','POST HOC: fewer than 5 run or 5 rest bouts')
    selected['analysis_type']=META['analysis_type'];selected['post_hoc']=True;selected['minimum_bout_s']=2;selected['provenance_json']=json.dumps(META,separators=(',',':'))
    selected.to_csv(OUT/'posthoc_2s_session_eligibility.csv',index=False,encoding='utf-8')
    counts=dict(status='COMPLETE',analysis_type=META['analysis_type'],post_hoc=True,elapsed_seconds=time.perf_counter()-started,metadata=META,
                sessions=18,included_sessions=behavior[behavior.included].session.tolist(),included_by_analysis=selected[selected.included].groupby('analysis').session.count().to_dict(),bouts_all_sessions=len(bouts),prespecified_5s_bouts_unchanged=len(shared))
    (OUT/'posthoc_2s_behavior_runtime.json').write_text(json.dumps(counts,indent=2),encoding='utf-8');print(json.dumps(counts))
except Exception as err:
    (OUT/'posthoc_2s_behavior_failure.json').write_text(json.dumps(dict(status='FAILED_STOP',analysis_type=META['analysis_type'],error=str(err),traceback=traceback.format_exc(),metadata=META),indent=2),encoding='utf-8');raise
