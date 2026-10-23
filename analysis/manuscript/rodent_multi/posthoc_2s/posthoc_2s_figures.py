"""Separate POST HOC 2-s scientific figures; every title/footer is labelled POST HOC."""
from pathlib import Path
import sys,os,json,hashlib
OUT=Path(__file__).resolve().parent;PARENT=OUT.parent;ROOT=PARENT.parent.parent;sys.path.insert(0,str(ROOT/'pydeps'));os.environ['MPLCONFIGDIR']=str(OUT/'plot_config')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
META=json.loads((OUT/'posthoc_2s_provenance.json').read_text(encoding='utf-8'))|dict(stage='POST HOC 2-s sensitivity figures')
def read(name):return pd.read_csv(OUT/name,encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
figures=[]
plt.rcParams.update({'font.size':9,'font.family':'DejaVu Sans','svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
def save(fig,stem,sources,description):
    provenance=META|dict(description='POST HOC: '+description,sources={str(p):sha(p) for p in sources})
    footer='POST HOC 2-s sensitivity | APC v1.0 '+META['git_commit']+'\nSources: '+', '.join(p.name for p in sources)
    fig.text(.5,.012,footer,ha='center',fontsize=7)
    for ext in ['png','svg']:fig.savefig(OUT/(stem+'.'+ext),dpi=300,metadata={'Description':json.dumps(provenance)})
    plt.close(fig);figures.append(dict(analysis_type=META['analysis_type'],post_hoc=True,stem=stem,description='POST HOC: '+description,png=str(OUT/(stem+'.png')),svg=str(OUT/(stem+'.svg')),sources=[str(p) for p in sources]))
inclusion=read('posthoc_2s_inclusion_comparison.csv');x=np.arange(len(inclusion))
fig,axes=plt.subplots(2,1,figsize=(15,8),sharex=True)
for ax,state in zip(axes,['run','rest']):
    ax.bar(x-.18,inclusion[state+'_bouts_prespecified_5s'],width=.36,color='#777777',label='Prespecified 5-s bouts')
    ax.bar(x+.18,inclusion[state+'_bouts_posthoc_2s'],width=.36,color='#D55E00',label='POST HOC 2-s bouts');ax.axhline(5,color='black',ls=':',lw=1);ax.set(ylabel=state.capitalize()+' bouts');ax.legend(frameon=False,ncol=2)
axes[1].set(xticks=x,xticklabels=inclusion.session);plt.setp(axes[1].get_xticklabels(),rotation=50,ha='right')
fig.suptitle('POST HOC sensitivity: bout counts beside prespecified 5-s results');fig.subplots_adjust(top=.93,bottom=.25,hspace=.25)
save(fig,'posthoc_2s_inclusion_comparison',[OUT/'posthoc_2s_inclusion_comparison.csv',PARENT/'regional_behavior_summary.csv'],'5-s and POST HOC 2-s bout counts; inclusion remains >=5 run and >=5 rest bouts')

comparison=read('posthoc_2s_across_session_comparison.csv');analysis_order=['CA1','EC','E1_sensitivity'];outcomes=['fP_hz','fA_hz','ozkurt_mvl'];labels={'fP_hz':'fP (Hz)','fA_hz':'fA (Hz)','ozkurt_mvl':'Ozkurt MVL'}
fig,axes=plt.subplots(1,3,figsize=(14,5),sharey=True)
for k,outcome in enumerate(outcomes):
    ax=axes[k]
    for j,analysis in enumerate(analysis_order):
        r=comparison[(comparison.analysis==analysis)&(comparison.method=='APC-v1.0')&(comparison.animal_pool=='pooled')&(comparison.outcome==outcome)].iloc[0]
        for suffix,offset,color,label in [('prespecified_5s',-.12,'#777777','Prespecified 5 s'),('posthoc_2s',.12,'#D55E00','POST HOC 2 s')]:
            mean=r['mean_session_difference_'+suffix];lo=r['ci_low_'+suffix];hi=r['ci_high_'+suffix]
            if np.isfinite(mean):ax.errorbar(mean,j+offset,xerr=[[max(0,mean-lo)],[max(0,hi-mean)]],fmt='o',capsize=3,color=color,label=label if j==0 else None)
    ax.axvline(0,ls=':',color='#777777');ax.set(xlabel='Run − rest '+labels[outcome],yticks=range(3),yticklabels=analysis_order)
axes[0].invert_yaxis();axes[0].legend(frameon=False);fig.suptitle('POST HOC sensitivity: pooled session-level APC means and t-based 95% CIs\nEligible sessions differ between the prespecified 5-s and POST HOC 2-s analyses',fontsize=13);fig.tight_layout(rect=(0,.12,1,.9))
save(fig,'posthoc_2s_across_session_comparison',[OUT/'posthoc_2s_across_session_comparison.csv',PARENT/'regional_across_session_statistics.csv'],'Pooled APC effects beside prespecified 5-s results; different eligible-session sets')

bout=read('posthoc_2s_bout_estimates.csv');state=read('posthoc_2s_state_summary.csv');statistics=read('posthoc_2s_session_statistics.csv');spread=read('posthoc_2s_within_state_fp_spread.csv');rng=np.random.default_rng(20261022)
for analysis in analysis_order:
    group=bout[bout.analysis==analysis]
    for animal in sorted(group.animal.unique()):
        data=group[group.animal==animal];sessions=sorted(data.session.unique());ncols=3;nrows=int(np.ceil(len(sessions)/3))
        for outcome in ['fP_hz','ozkurt_mvl']:
            fig,axes=plt.subplots(nrows,ncols,figsize=(13,3.1*nrows+1.1),squeeze=False,sharey=True)
            for ax,session in zip(axes.flat,sessions):
                d=data[data.session==session];channel=int(d.channel_index.iloc[0]);region=d.region.iloc[0]
                for n,(method,st) in enumerate([('APC-v1.0','run'),('APC-v1.0','rest'),('MVL-Ozkurt','run'),('MVL-Ozkurt','rest')]):
                    vals=d[(d.method==method)&(d.state==st)][outcome].dropna().to_numpy();color='#0072B2' if method=='APC-v1.0' else '#D55E00';ax.scatter(n+rng.uniform(-.13,.13,len(vals)),vals,s=10,alpha=.35,color=color,edgecolors='none')
                    r=state[(state.analysis==analysis)&(state.session==session)&(state.method==method)&(state.state==st)&(state.outcome==outcome)].iloc[0]
                    if np.isfinite(r['mean']):ax.errorbar(n,r['mean'],yerr=[[max(0,r['mean']-r.ci_low)],[max(0,r.ci_high-r['mean'])]],fmt='o',color='black',mfc='black' if st=='run' else 'white',capsize=3,zorder=4)
                ax.set(title=f'{session} | E{channel} {region}',xticks=range(4),xticklabels=['APC\nrun','APC\nrest','Scan\nrun','Scan\nrest'],ylabel=labels[outcome]);ax.grid(axis='y',alpha=.15)
            for ax in list(axes.flat)[len(sessions):]:ax.set_visible(False)
            fig.suptitle(f'POST HOC 2-s sensitivity: {analysis}, {animal}, {labels[outcome]}\nAPC v1.0 and prespecified Ozkurt-max scan',fontsize=13);fig.tight_layout(rect=(0,.07,1,.93))
            save(fig,f'posthoc_2s_{analysis}_{animal}_{outcome}_run_rest',[OUT/'posthoc_2s_bout_estimates.csv',OUT/'posthoc_2s_state_summary.csv'],'Per-bout '+analysis+' '+animal+' '+outcome+' with means and 10,000-resample bootstrap 95% CIs')
    sessions=sorted(group.session.unique());fig,axes=plt.subplots(1,3,figsize=(14,max(6,.45*len(sessions)+1)),sharey=True)
    for k,outcome in enumerate(outcomes):
        ax=axes[k]
        for j,session in enumerate(sessions):
            for method,offset,color in [('APC-v1.0',-.12,'#0072B2'),('MVL-Ozkurt',.12,'#D55E00')]:
                r=statistics[(statistics.analysis==analysis)&(statistics.session==session)&(statistics.method==method)&(statistics.outcome==outcome)].iloc[0]
                if np.isfinite(r.mean_difference):ax.errorbar(r.mean_difference,j+offset,xerr=[[max(0,r.mean_difference-r.ci_low)],[max(0,r.ci_high-r.mean_difference)]],fmt='o',color=color,capsize=3,label=method if j==0 else None)
        ax.axvline(0,color='#777777',ls=':');ax.set(xlabel='Run − rest '+labels[outcome],yticks=range(len(sessions)),yticklabels=sessions);ax.grid(axis='x',alpha=.15)
    axes[0].invert_yaxis();axes[0].legend(frameon=False,fontsize=8);fig.suptitle('POST HOC 2-s sensitivity: '+analysis+' session differences and bootstrap 95% CIs');fig.tight_layout(rect=(0,.1,1,.94))
    save(fig,'posthoc_2s_'+analysis+'_session_differences',[OUT/'posthoc_2s_session_statistics.csv'],'Session mean differences with percentile-bootstrap 95% CIs for '+analysis)

fig,axes=plt.subplots(3,2,figsize=(13,12));methods=['APC-v1.0','MVL-raw','MVL-Ozkurt','KLMI','GLM']
for i,analysis in enumerate(analysis_order):
    for j,st in enumerate(['run','rest']):
        ax=axes[i,j];d=spread[(spread.analysis==analysis)&(spread.state==st)];series=[d[d.method==method].fp_sd.dropna().to_numpy() for method in methods]
        ax.boxplot(series,tick_labels=methods,showfliers=False)
        for k,values in enumerate(series):ax.scatter(k+1+rng.uniform(-.12,.12,len(values)),values,s=15,alpha=.6,color='#0072B2')
        ax.set(title='POST HOC '+analysis+' '+st,ylabel='Within-session fP SD (Hz)');plt.setp(ax.get_xticklabels(),rotation=25,ha='right');ax.grid(axis='y',alpha=.15)
fig.suptitle('POST HOC 2-s sensitivity: within-state fP spread',fontsize=14);fig.tight_layout(rect=(0,.07,1,.96));save(fig,'posthoc_2s_within_state_fp_spread',[OUT/'posthoc_2s_within_state_fp_spread.csv'],'Within-session fP SD for all methods; points are sessions')

tracking=np.load(PARENT/'ec013.157_regional_tracking.npz');bb=read('posthoc_2s_bouts.csv');bb=bb[bb.session=='ec013.157'];fig,axes=plt.subplots(2,1,figsize=(14,6),sharex=True)
axes[0].plot(tracking['time'],tracking['linear_position_cm'],lw=.6,color='#555555');axes[0].set(ylabel='Linear position (cm)');axes[0].axhspan(37.5,212.5,color='#0072B2',alpha=.07)
axes[1].plot(tracking['time'],tracking['speed_cm_s'],lw=.6,color='#555555');axes[1].axhline(6,ls=':',color='black');axes[1].set(ylabel='2-D speed (cm/s)',xlabel='Recording time (s)')
for _,r in bb.iterrows():
    for ax in axes:ax.axvspan(r.start_time_s,r.stop_exclusive_s,color='#0072B2' if r.state=='run' else '#D55E00',alpha=.15,lw=0)
axes[1].plot([],[],lw=6,color='#0072B2',alpha=.5,label='POST HOC run >=2 s');axes[1].plot([],[],lw=6,color='#D55E00',alpha=.5,label='POST HOC rest >=2 s');axes[1].legend(frameon=False,ncol=2)
fig.suptitle('POST HOC 2-s sensitivity: ec013.157, unchanged position and speed');fig.tight_layout(rect=(0,.1,1,.94));save(fig,'posthoc_2s_tracking_ec013_157',[OUT/'posthoc_2s_bouts.csv',PARENT/'regional_behavior_summary.csv'],'Unchanged tracking trace with POST HOC >=2-s qualifying bouts; blue run, orange rest')
(OUT/'posthoc_2s_figures.json').write_text(json.dumps(dict(analysis_type=META['analysis_type'],post_hoc=True,metadata=META,figures=figures),indent=2),encoding='utf-8')
print(json.dumps(dict(status='COMPLETE',analysis_type=META['analysis_type'],post_hoc=True,figure_pairs=len(figures))))
