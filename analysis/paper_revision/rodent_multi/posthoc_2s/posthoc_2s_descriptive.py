"""POST HOC 2-s descriptive analysis; historical reference remains 12/12."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(r'C:\Users\nghare\.brainstorm\process');OUT=Path(__file__).resolve().parent;PARENT=OUT.parent;sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
import pandas as pd
from scipy.io import loadmat
meta=json.loads((OUT/'posthoc_2s_provenance.json').read_text(encoding='utf-8'))|dict(stage='POST HOC 2-s descriptive overlap; no gate')
def intervals(mask):
    d=np.diff(np.r_[False,mask,False].astype(int));return np.flatnonzero(d==1),np.flatnonzero(d==-1)-1
def write(rows,name):
    d=pd.DataFrame(rows);d['analysis_type']=meta['analysis_type'];d['post_hoc']=True;d['minimum_bout_s']=2;d['provenance_json']=json.dumps(meta);d.to_csv(OUT/name,index=False,encoding='utf-8');return d
qc=[]
for p in sorted(PARENT.glob('*_regional_tracking.npz')):
    with np.load(p) as s:
        row=dict(session=p.name.removesuffix('_regional_tracking.npz'),source_npz=p.name,samples=len(s['time']),median_speed_cm_s=float(np.nanmedian(s['speed_cm_s'])),
                 speed_95th_cm_s=float(np.nanquantile(s['speed_cm_s'],.95)),speed_99th_cm_s=float(np.nanquantile(s['speed_cm_s'],.99)))
        for state in ['run','rest']:
            a,b=intervals(s[state+'_mask']);dur=(b-a+1)/39.0625
            row.update({state+'_candidate_intervals':len(a),state+'_max_candidate_duration_s':float(dur.max()) if len(dur) else 0,
                        state+'_candidate_intervals_ge_2_s':int((dur>=2).sum())})
        assert not np.any(s['run_mask']&s['rest_mask'])
        assert not np.any((s['run_mask']|s['rest_mask'])&~s['valid_after_interpolation'])
        qc.append(row)
write(qc,'posthoc_2s_behavior_qc.csv')
old=loadmat(PARENT/'behavior_reproduction.mat',simplify_cells=True)
time=loadmat(Path(r'D:\APC_project\RealDatasets\LFP_data\EC3_dataset_real.mat'),variable_names=['R2'],simplify_cells=True)['R2']['Time']
oldtime=time[40799:372500];dt=np.median(np.diff(oldtime));scope=(float(oldtime[0]),float(oldtime[-1]+dt))
allnew=pd.read_csv(OUT/'posthoc_2s_bouts.csv',encoding='utf-8');allnew=allnew[allnew.session=='ec013.157']
oldsets={};newsets={};detail=[];summary=[]
def intersect(a,b):return max(0.,min(a[1],b[1])-max(a[0],b[0]))
for state in ['run','rest']:
    mask=(abs(old['speed'])>6) if state=='run' else (abs(old['speed'])<=6)
    a,b=intervals(mask);keep=(oldtime[b]-oldtime[a]+dt)>=5;a=a[keep];b=b[keep];assert len(a)==12
    historic=[(float(oldtime[s]),float(oldtime[e]+dt)) for s,e in zip(a,b)]
    newer=[(float(r.start_time_s),float(r.stop_exclusive_s)) for _,r in allnew[allnew.state==state].iterrows()]
    clipped=[(max(x,scope[0]),min(y,scope[1])) for x,y in newer if intersect((x,y),scope)>0]
    oldsets[state]=historic;newsets[state]=clipped
    overlap=sum(intersect(x,y) for x in historic for y in clipped);oldtotal=sum(y-x for x,y in historic);newtotal=sum(y-x for x,y in clipped)
    summary.append(dict(state=state,comparison_start_s=scope[0],comparison_stop_exclusive_s=scope[1],historical_bouts=12,new_bouts_whole_recording=len(newer),new_bouts_intersecting_original_interval=len(clipped),
        historical_duration_s=oldtotal,new_duration_in_original_interval_s=newtotal,same_state_intersection_s=overlap,union_s=oldtotal+newtotal-overlap,jaccard=overlap/(oldtotal+newtotal-overlap),
        historical_bouts_with_any_same_state_overlap=sum(any(intersect(x,y)>0 for y in clipped) for x in historic)))
    for i,x in enumerate(historic):
        durations=[intersect(x,y) for y in clipped];detail.append(dict(state=state,historical_bout=i+1,historical_start_s=x[0],historical_stop_exclusive_s=x[1],historical_duration_s=x[1]-x[0],
            new_same_state_overlap_s=sum(durations),fraction_historical_bout_covered=sum(durations)/(x[1]-x[0]),new_bouts_overlapping=sum(d>0 for d in durations)))
write(detail,'posthoc_2s_historical_overlap_bouts.csv');write(summary,'posthoc_2s_historical_overlap_summary.csv')
cross=[]
for h in ['run','rest']:
    for n in ['run','rest']:
        cross.append(dict(historical_bout_state=h,new_bout_state=n,intersection_seconds=sum(intersect(x,y) for x in oldsets[h] for y in newsets[n])))
write(cross,'posthoc_2s_historical_overlap_cross_state.csv')
print(json.dumps(dict(status='PASS',sessions_checked=18,overlap_summary=summary)))
