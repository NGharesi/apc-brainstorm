"""Separate POST HOC 2-s report and an appended POST HOC section beside prespecified 5-s results."""
from pathlib import Path
import sys,json,hashlib
OUT=Path(__file__).resolve().parent;PARENT=OUT.parent;ROOT=PARENT.parent.parent;sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
import pandas as pd
META=json.loads((OUT/'posthoc_2s_provenance.json').read_text(encoding='utf-8'))
def js(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def read(name):return pd.read_csv(OUT/name,encoding='utf-8')
def link(p,label=None):
    p=Path(p);p=p if p.is_absolute() else OUT/p
    return f'[{label or p.name}](<{p.as_posix()}>)'
def table(d,cols):
    def fmt(x):
        if x is None or isinstance(x,(float,np.floating)) and not np.isfinite(x):return 'NA'
        return f'{x:.6g}' if isinstance(x,(float,np.floating)) else str(x).replace('|','/').replace('\n',' ')
    return '| '+' | '.join(cols)+' |\n| '+' | '.join('---' for _ in cols)+' |\n'+'\n'.join('| '+' | '.join(fmt(r[c]) for c in cols)+' |' for _,r in d.iterrows())+'\n'
runtime=js('posthoc_2s_bouts_runtime.json');assert runtime['status']=='COMPLETE' and runtime['shared_prespecified_outputs_exact']
statistics_runtime=js('posthoc_2s_statistics_runtime.json');models=js('posthoc_2s_mixed_models.json');assert models['status']=='COMPLETE'
bouts=read('posthoc_2s_bout_estimates.csv');behavior=read('posthoc_2s_behavior_summary.csv');eligible=read('posthoc_2s_session_eligibility.csv')
session=read('posthoc_2s_session_statistics.csv');across=read('posthoc_2s_across_session_statistics.csv');spread=read('posthoc_2s_within_state_fp_spread.csv');boundaries=read('posthoc_2s_boundary_counts.csv');counts=read('posthoc_2s_status_counts.csv')
comparison=read('posthoc_2s_across_session_comparison.csv');inclusion=read('posthoc_2s_inclusion_comparison.csv');coef=read('posthoc_2s_mixed_model_coefficients.csv');mixedcomp=read('posthoc_2s_mixed_model_comparison.csv')
figures=js('posthoc_2s_figures.json')['figures'];deviations=js('posthoc_2s_deviations.json')['deviations'];warnings=read('posthoc_2s_statistics_warnings.csv')
primary=comparison[(comparison.method=='APC-v1.0')&(comparison.animal_pool=='pooled')]
diagnostics=[]
for m in models['models']:
    cov=np.asarray(m['random_effect_covariance']);diagnostics.append(dict(analysis=m['analysis'],outcome=m['outcome'],sessions=m['sessions'],observations=m['observations'],animal_term_omitted=m['constant_animal_term_omitted'],formula=m['formula'],
        var_intercept=cov[0,0],cov_intercept_state=cov[0,1],var_state=cov[1,1],residual_variance=m['residual_variance'],covariance_rank=m['random_effect_numerical_rank'],optimizer_nonconvergence_warning=m['optimizer_nonconvergence_warning'],warning=m['last_warning'] or 'none'))
diag=pd.DataFrame(diagnostics);diag['analysis_type']=META['analysis_type'];diag['post_hoc']=True;diag['provenance_json']=json.dumps(META);diag.to_csv(OUT/'posthoc_2s_mixed_model_diagnostics.csv',index=False,encoding='utf-8')
title='# POST HOC sensitivity — 2-s minimum bout duration'
lines=[title,'','**POST HOC analysis.** Minimum contiguous same-state bout duration is 2 s. Inclusion remains >=5 run and >=5 rest bouts. All other rules, source inputs, regional channels, frozen APC v1.0 options, SOS comparator settings, statistical estimators and seed scheme are unchanged. The prespecified 5-s analysis is retained separately.','',
    '## POST HOC scope and provenance','',
    'The POST HOC protocol was saved before new bout extraction: '+link('PROTOCOL_posthoc_2s.md')+'. Frozen method commit `'+META['git_commit']+'`; seed 20261022. Full POST HOC provenance: '+link('posthoc_2s_provenance.json')+'. All parent numerical results, method code, tracking traces and figures are checked against the prespecified manifest: '+link('posthoc_2s_prespecified_manifest.json')+'.','',
    'The identical saved tracking time, position, LED validity, short-gap interpolation, PCA projection/scale, Gaussian smoothing, 2-D speed and strict run/rest masks were reused. Only the duration cutoff changed. All 202 bouts in the original all-session 5-s extraction retained identical tracking/LFP boundaries. All method outputs, including shared >=5-s inputs, were recomputed. The 1,680 method rows shared with the prespecified analysis match exactly: '+link('posthoc_2s_shared_5s_exact_comparison.csv')+'.','',
    '## POST HOC inclusion beside prespecified 5-s results','',
    'POST HOC: all 18 sessions qualify (9 EC013 and 9 EC012). CA1 uses 9 EC013 sessions; EC uses all 18; E1 sensitivity uses 9 EC013. Prespecified 5-s: 3 EC013 sessions qualify in each analysis, with no EC012 sessions. Different eligible-session sets are therefore used in the side-by-side pooled summaries.','',
    'POST HOC table — duration/inclusion comparison:',
    table(inclusion,['animal','session','run_bouts_prespecified_5s','rest_bouts_prespecified_5s','included_prespecified_5s','run_bouts_posthoc_2s','rest_bouts_posthoc_2s','included_posthoc_2s']),
    'POST HOC table — regional channel choices (unchanged from prespecified regional choices):',
    table(eligible,['animal','session','analysis','channel_name','shank','region','theta_delta_ratio','source_channel_flag','included']),
    'POST HOC table — behaviour summaries and durations:',
    table(behavior,['session','cm_per_unit','raw_missing_fraction','missing_after_short_interpolation_fraction','run_bouts','rest_bouts','run_total_duration_s','run_mean_duration_s','run_median_duration_s','rest_total_duration_s','rest_mean_duration_s','rest_median_duration_s']),
    'Every POST HOC bout duration, tracking/LFP boundary and source trace hash is in '+link('posthoc_2s_bouts.csv')+'. Complete POST HOC behaviour summaries include min/max durations: '+link('posthoc_2s_behavior_summary.csv')+'.','',
    '## POST HOC APC summaries beside prespecified 5-s summaries','',
    'POST HOC comparison table — session-level mean run-minus-rest differences. CIs are t intervals across sessions. Counts refer to finite session differences for each outcome; session sets differ between analyses. The complete comparison includes every comparator, outcome and animal pool: '+link('posthoc_2s_across_session_comparison.csv')+'.','',
    table(primary,['analysis','outcome','n_sessions_prespecified_5s','mean_session_difference_prespecified_5s','ci_low_prespecified_5s','ci_high_prespecified_5s','n_sessions_posthoc_2s','mean_session_difference_posthoc_2s','ci_low_posthoc_2s','ci_high_posthoc_2s','one_sample_p_posthoc_2s','wilcoxon_p_posthoc_2s']),
    'POST HOC comparisons for the three sessions also eligible at 5 s, for every method/outcome: '+link('posthoc_2s_shared_session_comparison.csv')+'. These retain the original 5-s estimates beside the POST HOC 2-s estimates without restricting the full POST HOC analysis.','',
    '## POST HOC per-bout outputs and statuses','',
    f'POST HOC: {runtime["unique_input_checkpoints"]} channel/bout inputs and {len(bouts)} method rows. Frozen APC v1.0 uses amplitude 80–150 Hz and all other defaults. A2\' uses phase 4:0.5:12 Hz, half-width 1.5; amplitude 80:4:148 Hz, half-width 12; MVL-raw, MVL-Ozkurt, KLMI and GLM. SOS filter pole/gain guards and the raw-MVL/preferred-phase extraction checks are unchanged.','',
    'POST HOC per-bout fP/fA, raw/Ozkurt MVL, preferred phase, status, route and complete settings: '+link('posthoc_2s_bout_estimates.csv')+'. Nonzero frozen APC statuses are retained; finite-value denominators are reported. POST HOC status table:',
    table(counts,['analysis','animal','method','state','status','bouts']),
    '## POST HOC per-session and across-session statistics','',
    'POST HOC estimators are identical: run-minus-rest means, unequal-variance Welch t, pooled-SD Hedges g with exact gamma correction, 10,000 percentile-bootstrap resamples with seed 20261022 and the same deterministic group stream scheme; session-level one-sample t and Wilcoxon signed rank, zero differences recorded, no multiplicity correction. Shared bout-index draws across methods within each analysis/session are retained. Bootstrap finite-resample counts and all test outputs are in the POST HOC CSVs.','']
for analysis in ['CA1','EC','E1_sensitivity']:
    lines+=['### POST HOC '+analysis+' statistics','',
        'POST HOC per-session table:',table(session[session.analysis==analysis],['animal','session','method','outcome','n_run','n_rest','run_mean','rest_mean','mean_difference','welch_t','welch_p','hedges_g','ci_low','ci_high']),
        'POST HOC across-session table:',table(across[across.analysis==analysis],['animal_pool','method','outcome','n_sessions','mean_session_difference','median_session_difference','ci_low','ci_high','one_sample_t','one_sample_p','wilcoxon_statistic','wilcoxon_p','zero_differences'])]
lines+=['## POST HOC region-specific mixed models','',
    'POST HOC REML models retain the same session random intercept and state slope. EC now has both animals and uses `outcome ~ state_run + animal + (1 + state_run | session)`, EC012 reference. CA1/E1 sensitivity contain EC013 only and omit the redundant constant animal term, as in the prespecified pipeline. No random-effects simplification is applied. POST HOC coefficient table:',
    table(coef,['analysis','outcome','Name','Estimate','SE','tStat','DF','pValue','Lower','Upper']),
    'POST HOC covariance and optimizer-warning table:',
    table(diag,['analysis','outcome','sessions','observations','animal_term_omitted','var_intercept','cov_intercept_state','var_state','residual_variance','covariance_rank','optimizer_nonconvergence_warning','warning']),
    'POST HOC versus prespecified mixed-model coefficient table:',
    table(mixedcomp,['analysis','outcome','Name','Estimate_prespecified_5s','Lower_prespecified_5s','Upper_prespecified_5s','Estimate_posthoc_2s','Lower_posthoc_2s','Upper_posthoc_2s','pValue_posthoc_2s']),
    'Full POST HOC model objects, covariance eigenvalues and fit logs are retained in this folder; '+link('posthoc_2s_mixed_models.json')+'.','',
    '## POST HOC boundary picks and within-state spread','',
    'POST HOC exact boundary counts (fP=4 or 12 Hz) and sample SD/IQR/unscaled MAD of within-state fP are reported below. Frozen APC can estimate outside the scan phase range. POST HOC boundary table:',
    table(boundaries,['analysis','animal','session','method','state','n_bouts','n_valid','boundary_fp_4','boundary_fp_12']),
    'POST HOC fP spread table:',
    table(spread,['analysis','animal','session','method','state','n_valid','fp_sd','fp_iqr','fp_mad']),
    'POST HOC paired APC-minus-scan session spread differences: '+link('posthoc_2s_within_state_spread_comparisons.csv')+'. POST HOC across-session spread tests: '+link('posthoc_2s_across_session_spread_comparisons.csv')+'.','',
    '## POST HOC descriptive historical overlap','',
    'POST HOC descriptive comparison only, with the same original ec013.157 12/12 >=5-s historical reference and [32.6392,298.0)-s window. No overlap gate. POST HOC overlap table:',
    table(read('posthoc_2s_historical_overlap_summary.csv'),['state','historical_bouts','new_bouts_whole_recording','new_bouts_intersecting_original_interval','historical_bouts_with_any_same_state_overlap','same_state_intersection_s','jaccard']),
    'POST HOC per-historical-bout and cross-state overlaps: '+link('posthoc_2s_historical_overlap_bouts.csv')+'; '+link('posthoc_2s_historical_overlap_cross_state.csv')+'.','',
    '## POST HOC figures','',
    'Every POST HOC figure is separately exported as 300-dpi PNG and SVG, visibly labelled POST HOC and embedding commit/settings/source-CSV hashes. The displayed comparison scan remains the prespecified Ozkurt-max scan; every scan is retained in the POST HOC tables.','']
for f in figures:lines.append('- '+f['description']+': '+link(f['png'],'POST HOC PNG')+'; '+link(f['svg'],'POST HOC SVG')+'.')
lines+=['','## POST HOC runtime and deviations','',
    'POST HOC behaviour extraction: '+f"{js('posthoc_2s_behavior_runtime.json')['elapsed_seconds']:.3f} s. POST HOC method-worker seconds (parallel): "+', '.join(f'{s:.3f}' for s in runtime['worker_compute_seconds'])+f"; sum {runtime['worker_compute_seconds_sum']:.3f} s, longest worker {runtime['maximum_worker_compute_seconds']:.3f} s. POST HOC statistics: {statistics_runtime['elapsed_seconds']:.3f} s. POST HOC mixed models: {models['elapsed_seconds']:.3f} s. Startup, the approval-service interruption and report/figure packaging are excluded from stage compute timings.",
    '',f'POST HOC statistical warning records: {len(warnings)}; '+link('posthoc_2s_statistics_warnings.csv')+'. Test outputs are retained with warning context; estimators and data were not adjusted.','']
for d in deviations:lines.append('- POST HOC '+d['type']+': '+d['detail'])
lines+=['- POST HOC execution uses three independent session partitions with one MATLAB computational thread per worker; numerical code/settings are unchanged.',
    '- POST HOC nonzero APC statuses and covariance/optimizer warnings are reported as method/statistical outputs using the same handling as the prespecified pipeline.',
    '- POST HOC regional mapping assumptions and the ec013.157 equivalent source remain unchanged and documented in the prespecified report.',
    '', 'POST HOC verification: '+link('posthoc_2s_verification.json')+'. POST HOC output manifest: '+link('posthoc_2s_output_manifest.json')+'.','']
(OUT/'RESULTS_posthoc_2s.md').write_text('\n'.join(lines),encoding='utf-8')
base=(OUT/'posthoc_2s_prespecified_report_snapshot.md').read_text(encoding='utf-8')
append=['','## POST HOC sensitivity — 2-s minimum bout duration','',
    '**POST HOC analysis; separate from all prespecified 5-s results above.** Only minimum bout duration changes from 5 s to 2 s; inclusion remains >=5 run/>=5 rest bouts. All tracking, channel, frozen APC, SOS comparator and statistical rules remain identical.','',
    'POST HOC: all 18 sessions qualify (CA1 9 EC013; EC 18 including both animals; E1 sensitivity 9 EC013), compared with 3 EC013 sessions in each prespecified 5-s analysis. Shared >=5-s method outputs reproduce all 1,680 original rows exactly. Pooled comparisons below have different eligible-session sets.','',
    'POST HOC inclusion comparison table:',table(inclusion,['animal','session','run_bouts_prespecified_5s','rest_bouts_prespecified_5s','run_bouts_posthoc_2s','rest_bouts_posthoc_2s','included_posthoc_2s']),
    'POST HOC session-level APC comparison table:',table(primary,['analysis','outcome','n_sessions_prespecified_5s','mean_session_difference_prespecified_5s','ci_low_prespecified_5s','ci_high_prespecified_5s','n_sessions_posthoc_2s','mean_session_difference_posthoc_2s','ci_low_posthoc_2s','ci_high_posthoc_2s','one_sample_p_posthoc_2s','wilcoxon_p_posthoc_2s']),
    'The separate '+link('RESULTS_posthoc_2s.md','POST HOC report')+' contains all POST HOC tables, statuses, mixed models, comparisons, historical overlap, runtime and deviations. Separate POST HOC CSVs: '+link('posthoc_2s_bout_estimates.csv')+', '+link('posthoc_2s_session_statistics.csv')+', '+link('posthoc_2s_across_session_statistics.csv')+', '+link('posthoc_2s_mixed_model_comparison.csv')+'.','',
    'POST HOC figures (additional per-session figures and spread figures are listed in the separate POST HOC report):','']
for name in ['posthoc_2s_inclusion_comparison','posthoc_2s_across_session_comparison']:
    f=next(f for f in figures if f['stem']==name);append.append('- '+f['description']+': '+link(f['png'],'POST HOC PNG')+'; '+link(f['svg'],'POST HOC SVG')+'.')
(PARENT/'RESULTS_rodent.md').write_bytes((OUT/'posthoc_2s_prespecified_report_snapshot.md').read_bytes()+('\n'.join(append)+'\n').encode('utf-8'))
(OUT/'posthoc_2s_STATUS.json').write_text(json.dumps(dict(status='COMPLETE',analysis_type=META['analysis_type'],post_hoc=True,metadata=META,method_rows=len(bouts),figures=len(figures),included_sessions=18),indent=2),encoding='utf-8')
print(json.dumps(dict(status='COMPLETE',analysis_type=META['analysis_type'],post_hoc=True,report=str(OUT/'RESULTS_posthoc_2s.md'),method_rows=len(bouts),figure_pairs=len(figures))))
