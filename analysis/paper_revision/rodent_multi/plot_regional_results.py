from pathlib import Path
import sys,os,json,hashlib
ROOT=Path(r'C:\Users\nghare\.brainstorm\process');OUT=ROOT/'revision_checks/rodent_multi';sys.path.insert(0,str(ROOT/'pydeps'));os.environ['MPLCONFIGDIR']=str(OUT/'plot_config')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def read(name):return pd.read_csv(OUT/name,encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
meta=json.loads((OUT/'regional_protocol_record.json').read_text(encoding='utf-8'))|dict(stage='regional figures',plot_scan='MVL-Ozkurt; prespecified independently of state effects')
assert json.loads((OUT/'regional_bouts_runtime.json').read_text(encoding='utf-8'))['status']=='COMPLETE'
assert json.loads((OUT/'regional_statistics_runtime.json').read_text(encoding='utf-8'))['status']=='COMPLETE'
sample_metadata=json.loads(read('regional_bout_estimates.csv').provenance_json.iloc[0])
meta.update({k:sample_metadata[k] for k in ['matlab_version','apc_options','comparators']})
plt.rcParams.update({'font.size':9,'font.family':'DejaVu Sans','svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
figures=[]
def save(fig,stem,sources,description):
    provenance=meta|dict(sources={s:sha(OUT/s) for s in sources},description=description)
    fig.text(.5,.016,'APC v1.0 '+meta['git_commit']+'\nSources: '+', '.join(sources),ha='center',fontsize=7)
    for ext in ['png','svg']:fig.savefig(OUT/(stem+'.'+ext),dpi=300,metadata={'Description':json.dumps(provenance)})
    plt.close(fig);figures.append(dict(stem=stem,description=description,sources=sources,png=str(OUT/(stem+'.png')),svg=str(OUT/(stem+'.svg'))))

selected=read('regional_session_eligibility.csv');behavior=read('regional_behavior_summary.csv');sessions=behavior.session.tolist();x=np.arange(len(sessions));pos={s:i for i,s in enumerate(sessions)}
colors={'CA1':'#0072B2','EC':'#D55E00','E1_sensitivity':'#777777'};offsets={'CA1':-.2,'EC':0.,'E1_sensitivity':.2}
fig,axes=plt.subplots(2,1,figsize=(15,9),sharex=True)
for analysis in ['CA1','EC','E1_sensitivity']:
    d=selected[selected.analysis==analysis];xx=np.array([pos[s] for s in d.session])+offsets[analysis];included=d.included.astype(bool).to_numpy()
    for ax,col in zip(axes,['theta_delta_ratio','channel_index']):
        ax.scatter(xx[~included],d[col].to_numpy()[~included],facecolors='none',edgecolors=colors[analysis],s=45,label=analysis+' (excluded)' if ax is axes[0] else None)
        ax.scatter(xx[included],d[col].to_numpy()[included],color=colors[analysis],s=55,marker='s',label=analysis+' (included)' if ax is axes[0] else None)
    for xx0,(_,r) in zip(xx,d.iterrows()):axes[1].annotate(r.channel_name,(xx0,r.channel_index),xytext=(0,-8 if analysis=='E1_sensitivity' else 6),textcoords='offset points',ha='center',va='top' if analysis=='E1_sensitivity' else 'bottom',fontsize=7,color=colors[analysis])
axes[0].set(yscale='log',ylabel='Whole-recording theta/delta ratio')
handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.94),ncol=3,fontsize=8,frameon=False)
axes[1].set(ylabel='Selected channel (one-based)',ylim=(-6,72),yticks=range(0,71,10),xticks=x,xticklabels=sessions)
for ax in axes:ax.axvline(8.5,color='#999999',ls=':',lw=1);ax.grid(axis='y',alpha=.15)
plt.setp(axes[1].get_xticklabels(),rotation=50,ha='right');fig.suptitle('Regional channel selection; auxiliary channels excluded',fontsize=15);fig.subplots_adjust(top=.83,bottom=.23,hspace=.25)
save(fig,'regional_channel_selection',['regional_session_eligibility.csv','regional_channel_map.csv'],'Regional theta/delta maxima; filled squares meet >=5 run and >=5 rest eligibility')
if '--channel-only' in sys.argv:
    existing=json.loads((OUT/'regional_figures.json').read_text(encoding='utf-8'));existing['figures'][0]=figures[0];(OUT/'regional_figures.json').write_text(json.dumps(existing,indent=2),encoding='utf-8');print('Channel figure updated');raise SystemExit(0)

fig,axes=plt.subplots(3,1,figsize=(15,10),sharex=True)
axes[0].bar(x,behavior.cm_per_unit,color='#777777');axes[0].set(ylabel='cm per coordinate unit',title='Tracking-rate behaviour across all local sessions')
axes[1].bar(x-.17,100*behavior.raw_missing_fraction,width=.34,label='Neither LED valid',color='#777777');axes[1].bar(x+.17,100*behavior.missing_after_short_interpolation_fraction,width=.34,label='After short-gap interpolation',color='#D55E00');axes[1].set(ylabel='Missing position (%)');axes[1].legend(frameon=False,ncol=2)
axes[2].bar(x-.17,behavior.run_bouts,width=.34,label='Run >=5 s',color='#0072B2');axes[2].bar(x+.17,behavior.rest_bouts,width=.34,label='Rest >=5 s',color='#D55E00');axes[2].axhline(5,ls=':',color='black',lw=1);axes[2].legend(frameon=False,ncol=2);axes[2].set(ylabel='Bouts',xticks=x,xticklabels=sessions)
for ax in axes:ax.axvline(8.5,color='#999999',ls=':',lw=1);ax.grid(axis='y',alpha=.15)
plt.setp(axes[2].get_xticklabels(),rotation=50,ha='right');fig.subplots_adjust(top=.94,bottom=.22,hspace=.3)
save(fig,'regional_behavior_summary',['regional_behavior_summary.csv'],'Tracking-rate scale, missingness and counts under the revised rules')

track=np.load(OUT/'ec013.157_regional_tracking.npz');bt=read('regional_bouts.csv');bt=bt[bt.session=='ec013.157']
fig,axes=plt.subplots(2,1,figsize=(14,6),sharex=True);t=track['time'];axes[0].plot(t,track['linear_position_cm'],lw=.6,color='#555555');axes[0].axhspan(37.5,212.5,color='#0072B2',alpha=.07);axes[0].set(ylabel='Linear position (cm)',title='ec013.157: tracking-rate speed and qualifying bouts')
axes[1].plot(t,track['speed_cm_s'],lw=.6,color='#555555');axes[1].axhline(6,ls=':',color='black',lw=1);axes[1].set(ylabel='2-D speed (cm/s)',xlabel='Recording time (s)')
for _,r in bt.iterrows():
    color='#0072B2' if r.state=='run' else '#D55E00'
    for ax in axes:ax.axvspan(r.start_time_s,r.stop_exclusive_s,color=color,alpha=.2,lw=0)
axes[1].plot([],[],color='#0072B2',lw=6,alpha=.5,label='Run bout');axes[1].plot([],[],color='#D55E00',lw=6,alpha=.5,label='Rest bout');axes[1].legend(frameon=False,ncol=2)
fig.tight_layout(rect=(0,.1,1,1));save(fig,'regional_tracking_ec013_157',['regional_bouts.csv','regional_behavior_summary.csv'],'Whole-recording tracking trace; blue run, orange rest; PCA center-zone shading')

bout=read('regional_bout_estimates.csv');state=read('regional_state_summary.csv');stats=read('regional_session_statistics.csv');spread=read('regional_within_state_fp_spread.csv');rng=np.random.default_rng(20261022)
for analysis in ['CA1','EC','E1_sensitivity']:
    d=bout[bout.analysis==analysis];ss=sorted(d.session.unique());fig,axes=plt.subplots(2,len(ss),figsize=(max(11,4*len(ss)),7),squeeze=False,sharey='row')
    for j,s in enumerate(ss):
        channel=int(d[d.session==s].channel_index.iloc[0]);region=d[d.session==s].region.iloc[0]
        for k,outcome in enumerate(['fP_hz','ozkurt_mvl']):
            ax=axes[k,j]
            for n,(method,st) in enumerate([('APC-v1.0','run'),('APC-v1.0','rest'),('MVL-Ozkurt','run'),('MVL-Ozkurt','rest')]):
                vals=d[(d.session==s)&(d.method==method)&(d.state==st)][outcome].dropna().to_numpy();color='#0072B2' if method=='APC-v1.0' else '#D55E00'
                ax.scatter(n+rng.uniform(-.13,.13,len(vals)),vals,s=14,alpha=.4,color=color,edgecolors='none')
                r=state[(state.analysis==analysis)&(state.session==s)&(state.method==method)&(state.state==st)&(state.outcome==outcome)].iloc[0]
                ax.errorbar(n,r['mean'],yerr=[[max(0,r['mean']-r.ci_low)],[max(0,r.ci_high-r['mean'])]],fmt='o',color='black',mfc='black' if st=='run' else 'white',capsize=3,zorder=4)
            ax.set(xticks=np.arange(4),xticklabels=['APC\nrun','APC\nrest','Scan\nrun','Scan\nrest']);ax.grid(axis='y',alpha=.15)
            if j==0:ax.set_ylabel('fP (Hz)' if outcome=='fP_hz' else 'Ozkurt-normalized MVL')
            if k==0:ax.set_title(f'{s} | E{channel}, {region}')
    fig.suptitle(analysis+': APC v1.0 and prespecified Ozkurt-max scan',fontsize=14);fig.tight_layout(rect=(0,.09,1,.95))
    save(fig,'regional_'+analysis+'_run_rest',['regional_bout_estimates.csv','regional_state_summary.csv'],'Per-bout scatter and state means with 10,000-resample percentile 95% CIs')

    fig,axes=plt.subplots(1,3,figsize=(14,5),sharey=True)
    for k,outcome in enumerate(['fP_hz','fA_hz','ozkurt_mvl']):
        ax=axes[k]
        for j,s in enumerate(ss):
            for method,offset,color in [('APC-v1.0',-.12,'#0072B2'),('MVL-Ozkurt',.12,'#D55E00')]:
                r=stats[(stats.analysis==analysis)&(stats.session==s)&(stats.method==method)&(stats.outcome==outcome)].iloc[0]
                ax.errorbar(r.mean_difference,j+offset,xerr=[[max(0,r.mean_difference-r.ci_low)],[max(0,r.ci_high-r.mean_difference)]],fmt='o',color=color,capsize=3,label=method if j==0 else None)
        ax.axvline(0,color='#777777',ls=':',lw=1);ax.set(xlabel='Run − rest '+({'fP_hz':'fP (Hz)','fA_hz':'fA (Hz)','ozkurt_mvl':'Ozkurt MVL'}[outcome]),yticks=range(len(ss)),yticklabels=ss);ax.grid(axis='x',alpha=.15)
    axes[0].invert_yaxis();axes[0].legend(frameon=False,fontsize=8);fig.suptitle(analysis+': session-level mean differences and bootstrap 95% CIs');fig.tight_layout(rect=(0,.12,1,.93))
    save(fig,'regional_'+analysis+'_session_differences',['regional_session_statistics.csv'],'Session mean run-minus-rest effects; 10,000-resample percentile CIs')

fig,axes=plt.subplots(1,2,figsize=(12,5),sharey=True)
methods=['APC-v1.0','MVL-raw','MVL-Ozkurt','KLMI','GLM']
for ax,st in zip(axes,['run','rest']):
    for j,analysis in enumerate(['CA1','EC','E1_sensitivity']):
        g=spread[(spread.analysis==analysis)&(spread.state==st)]
        for s in g.session.unique():
            y=g[g.session==s].set_index('method').reindex(methods).fp_sd.to_numpy();ax.plot(np.arange(5)+(j-1)*.06,y,marker='o',lw=.7,ms=4,alpha=.7,color=colors[analysis],label=analysis if s==g.session.unique()[0] else None)
    ax.set(title=st.capitalize(),xticks=range(5),xticklabels=methods,ylabel='Within-session fP SD (Hz)');ax.grid(axis='y',alpha=.15)
axes[0].legend(frameon=False);fig.suptitle('Within-state fP spread; each line is one session');fig.tight_layout(rect=(0,.12,1,.93));save(fig,'regional_within_state_fp_spread',['regional_within_state_fp_spread.csv'],'Within-state sample SDs of APC and all four scans, per included session')
(OUT/'regional_figures.json').write_text(json.dumps(dict(metadata=meta,figures=figures),indent=2),encoding='utf-8')
print(json.dumps(dict(status='COMPLETE',figure_pairs=len(figures))))
