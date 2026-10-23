from pathlib import Path
import sys,json,hashlib,time,traceback
ROOT=Path(r'C:\Users\nghare\.brainstorm\process');OUT=ROOT/'revision_checks/rodent_multi';sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
import pandas as pd
from scipy.io import loadmat
from scipy.ndimage import gaussian_filter1d

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def intervals(mask):
    d=np.diff(np.r_[False,mask,False].astype(int));return np.flatnonzero(d==1),np.flatnonzero(d==-1)-1
def savecsv(rows,name):
    d=pd.DataFrame(rows);d['git_commit']=meta['git_commit'];d['provenance_json']=json.dumps(meta,separators=(',',':'));d.to_csv(OUT/name,index=False,encoding='utf-8');return d
meta=json.loads((OUT/'regional_protocol_record.json').read_text(encoding='utf-8'))|dict(stage='regional tracking-rate behavior',
    position_rule='mean of valid LEDs; a valid LED requires both coordinates',gaussian_sd_seconds=.2,gaussian_radius_samples=32,gaussian_mode='reflect within finite segments',
    linear_position='first PC before smoothing; robust 0.5-99.5 percentile extent',central_interval=[.15,.85],outer_zones='below .15 or above .85 including percentile tails',
    speed='2D central difference, cm/s',speed_threshold_cm_s=6,minimum_bout_s=5,edge_trim_s=2,tracking_fs_hz=39.0625)
assert json.loads((OUT/'regional_xml_grouping.json').read_text(encoding='utf-8'))['contiguous_eight_channel_blocks']
mapping=pd.read_csv(OUT/'mapping_checks.csv',encoding='utf-8');selection=pd.read_csv(OUT/'regional_selected_channels.csv',encoding='utf-8')
summaries=[];allbouts=[];begin=time.perf_counter();fs=39.0625;dt=1/fs
try:
    for _,q in mapping.iterrows():
        trace=loadmat(q.tracking_file,variable_names=[q.tracking_array],simplify_cells=True)[q.tracking_array].astype(float)
        if q.session=='ec013.157':lt=loadmat(Path(r'D:\APC_project\RealDatasets\LFP_data\EC3_dataset_real.mat'),variable_names=['R2'],simplify_cells=True)['R2']['Time']
        else:lt=loadmat(q.lfp_file,variable_names=['Time'],simplify_cells=True)['Time']
        lt=np.asarray(lt);assert len(lt)==q.lfp_samples and np.all(np.diff(lt)>0)
        t=lt[0]+np.arange(len(trace))/fs
        leds=trace.reshape(-1,2,2);valid_led=np.all(np.isfinite(leds)&(leds!=-1),axis=2);nvalid=valid_led.sum(axis=1)
        pos=np.sum(np.where(valid_led[:,:,None],leds,0),axis=1)/np.maximum(nvalid,1)[:,None];pos[nvalid==0]=np.nan
        original_missing=nvalid==0;filled=np.zeros(len(t),bool);long_gaps=0
        a,b=intervals(original_missing)
        for s,e in zip(a,b):
            if (e-s+1)/fs<=.5 and s>0 and e<len(pos)-1:
                for axis in range(2):pos[s:e+1,axis]=np.interp(np.arange(s,e+1),[s-1,e+1],pos[[s-1,e+1],axis])
                filled[s:e+1]=True
            else:long_gaps+=1
        valid=np.all(np.isfinite(pos),axis=1);assert valid.sum()>=3,f'METHOD-RELEVANT: insufficient valid positions {q.session}'
        center=pos[valid].mean(axis=0);_,singular,vh=np.linalg.svd(pos[valid]-center,full_matrices=False);axis=vh[0]
        if axis[np.argmax(abs(axis))]<0:axis=-axis
        linear=(pos-center)@axis;lo,hi=np.quantile(linear[valid],[.005,.995]);assert hi>lo,f'METHOD-RELEVANT: zero track extent {q.session}'
        scale=250/(hi-lo);fraction=(linear-lo)/(hi-lo);smooth=np.full_like(pos,np.nan)
        a,b=intervals(valid)
        for s,e in zip(a,b):
            if e>=s:
                smooth[s:e+1]=gaussian_filter1d(pos[s:e+1],sigma=.2*fs,axis=0,mode='reflect',radius=32)
        speed=np.full(len(t),np.nan)
        adjacent=valid[:-2]&valid[1:-1]&valid[2:]
        central=np.linalg.norm((smooth[2:]-smooth[:-2])/(2*dt),axis=1)*scale;speed[1:-1]=np.where(adjacent,central,np.nan)
        eligible=valid&np.isfinite(speed)&(t>=lt[0]+2)&(t+dt<=lt[-1]-2)
        run=eligible&(speed>6)&(fraction>=.15)&(fraction<=.85);rest=eligible&(speed<6)&((fraction<.15)|(fraction>.85));assert not np.any(run&rest)
        boutrows=[]
        for state,mask in [('run',run),('rest',rest)]:
            a,b=intervals(mask);number=0
            for s,e in zip(a,b):
                duration=(e-s+1)*dt
                if duration<5:continue
                first=int(np.searchsorted(lt,t[s],side='left'));last=int(np.searchsorted(lt,t[e]+dt,side='left'))-1
                assert 0<=first<=last<len(lt)
                number+=1;row=dict(animal=q.animal,session=q.session,state=state,bout=number,tracking_start_idx=s+1,tracking_stop_idx=e+1,start_time_s=t[s],stop_exclusive_s=t[e]+dt,
                                  duration_s=duration,lfp_start_idx=first+1,lfp_stop_idx=last+1,lfp_duration_s=lt[last]-lt[first]+np.median(np.diff(lt)),cm_per_unit=scale)
                boutrows.append(row);allbouts.append(row)
        counts={s:sum(r['state']==s for r in boutrows) for s in ['run','rest']}
        summary=dict(animal=q.animal,session=q.session,cm_per_unit=scale,pca_axis_x=axis[0],pca_axis_y=axis[1],pca_center_x=center[0],pca_center_y=center[1],linear_q005=lo,linear_q995=hi,
            pca_variance_explained=singular[0]**2/np.sum(singular**2),raw_missing_fraction=original_missing.mean(),missing_after_short_interpolation_fraction=(~valid).mean(),
            both_leds_valid_fraction=(nvalid==2).mean(),single_led_valid_fraction=(nvalid==1).mean(),short_gap_samples_interpolated=int(filled.sum()),long_or_unbounded_gaps=long_gaps,
            classified_run_fraction=run.mean(),classified_rest_fraction=rest.mean(),unclassified_fraction=(~(run|rest)).mean(),run_bouts=counts['run'],rest_bouts=counts['rest'],
            included=counts['run']>=5 and counts['rest']>=5,source_file=q.lfp_file,tracking_file=q.tracking_file,tracking_array=q.tracking_array)
        for state in ['run','rest']:
            durations=[r['duration_s'] for r in boutrows if r['state']==state]
            summary.update({state+'_total_duration_s':sum(durations),state+'_mean_duration_s':float(np.mean(durations)) if durations else np.nan,
                            state+'_median_duration_s':float(np.median(durations)) if durations else np.nan,state+'_min_duration_s':min(durations) if durations else np.nan,state+'_max_duration_s':max(durations) if durations else np.nan})
        summaries.append(summary)
        inputmeta=meta|dict(session=q.session,tracking_file=q.tracking_file,tracking_sha256=sha(Path(q.tracking_file)),lfp_source=q.lfp_file,time_vector_sha256=hashlib.sha256(lt.tobytes()).hexdigest())
        np.savez_compressed(OUT/(q.session+'_regional_tracking.npz'),time=t,position=pos,smoothed_position=smooth,linear_position_cm=250*fraction,speed_cm_s=speed,raw_missing=original_missing,
                            valid_after_interpolation=valid,run_mask=run,rest_mask=rest,provenance_json=json.dumps(inputmeta))
        print(f"BEHAVIOR {q.session}: run={counts['run']} rest={counts['rest']} scale={scale:.6g} included={summary['included']}",flush=True)
    behavior=savecsv(summaries,'regional_behavior_summary.csv');boutframe=savecsv(allbouts,'regional_bouts.csv')
    selected=selection.merge(behavior[['session','run_bouts','rest_bouts','included']],on='session')
    selected['inclusion_reason']=np.where(selected.included,'>=5 run and >=5 rest bouts','fewer than 5 run or 5 rest bouts')
    selected['current_provenance_json']=json.dumps(meta);selected.to_csv(OUT/'regional_session_eligibility.csv',index=False,encoding='utf-8')
    status=dict(status='COMPLETE',elapsed_seconds=time.perf_counter()-begin,metadata=meta,sessions=18,bouts=len(boutframe),included_sessions=int(behavior.included.sum()),
                included_by_analysis=selected[selected.included].groupby('analysis').session.count().to_dict())
    (OUT/'regional_behavior_runtime.json').write_text(json.dumps(status,indent=2),encoding='utf-8');print(json.dumps(status))
except Exception as err:
    (OUT/'regional_behavior_failure.json').write_text(json.dumps(dict(status='FAILED_STOP',error=str(err),traceback=traceback.format_exc(),metadata=meta),indent=2),encoding='utf-8');raise
