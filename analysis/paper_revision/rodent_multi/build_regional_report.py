from pathlib import Path
import sys,json,hashlib,platform,datetime
ROOT=Path(r'C:\Users\nghare\.brainstorm\process');OUT=ROOT/'revision_checks/rodent_multi';sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
import pandas as pd
import scipy
def js(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def read(name):return pd.read_csv(OUT/name,encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def link(name,label=None):return f'[{label or name}](<{(OUT/name).as_posix()}>)'
def table(d,columns):
    def fmt(x):
        if x is None or (isinstance(x,(float,np.floating)) and not np.isfinite(x)):return 'NA'
        if isinstance(x,(float,np.floating)):return f'{x:.6g}'
        return str(x).replace('|','/').replace('\n',' ')
    return '| '+' | '.join(columns)+' |\n| '+' | '.join('---' for _ in columns)+' |\n'+'\n'.join('| '+' | '.join(fmt(r[c]) for c in columns)+' |' for _,r in d.iterrows())+'\n'

runtime=js('regional_bouts_runtime.json');assert runtime['status']=='COMPLETE'
models=js('regional_mixed_models.json');assert models['status']=='COMPLETE'
meta=js('regional_protocol_record.json');bouts=read('regional_bout_estimates.csv');first=json.loads(bouts.provenance_json.iloc[0])
provenance=meta|dict(stage='completed regional rodent report',python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,scipy=scipy.__version__,
    matlab_version=first['matlab_version'],apc_options=first['apc_options'],comparators=first['comparators'],
    frozen_source_sha256={n:sha(ROOT/'revision_checks/final/frozen_v1'/n) for n in ['bst_apc.m','calc_MI_all_methods.m']},
    reported_behavior='revised tracking-rate procedure only',historical_behavior_role='archival 12/12 and requested descriptive overlap only')
(OUT/'regional_analysis_provenance.json').write_text(json.dumps(provenance,indent=2),encoding='utf-8')
behavior=read('regional_behavior_summary.csv');selected=read('regional_session_eligibility.csv');mapping=read('mapping_checks.csv');sessionmeta=read('regional_session_metadata.csv');channels=read('regional_channel_map.csv')
sessionstats=read('regional_session_statistics.csv');across=read('regional_across_session_statistics.csv');state=read('regional_state_summary.csv');spread=read('regional_within_state_fp_spread.csv');spreadcomp=read('regional_across_session_spread_comparisons.csv')
overlap=read('regional_historical_overlap_summary.csv');detail=read('regional_historical_overlap_bouts.csv');qc=read('regional_behavior_qc.csv');coef=read('regional_mixed_model_coefficients.csv')
figures=js('regional_figures.json')['figures'];tooling=js('regional_tooling_deviations.json')['deviations']
guard=read('regional_comparator_filter_guards.csv');assert guard.guard_passed.astype(bool).all()
status=bouts.groupby(['analysis','method','state','status'],dropna=False).size().reset_index(name='bouts');status['provenance_json']=json.dumps(provenance);status.to_csv(OUT/'regional_status_counts.csv',index=False,encoding='utf-8')
boundaries=state[state.outcome=='fP_hz'][['analysis','animal','session','method','state','n_bouts','n_valid','boundary_fp_4','boundary_fp_12']].copy();boundaries['provenance_json']=json.dumps(provenance);boundaries.to_csv(OUT/'regional_boundary_counts.csv',index=False,encoding='utf-8')
modelrows=[]
for m in models['models']:
    cov=np.asarray(m['random_effect_covariance']);modelrows.append(dict(analysis=m['analysis'],outcome=m['outcome'],sessions=m['sessions'],observations=m['observations'],animal_term_omitted=m['constant_animal_term_omitted'],
        var_intercept=cov[0,0],cov_intercept_state=cov[0,1],var_state=cov[1,1],residual_variance=m['residual_variance'],covariance_rank=m['random_effect_numerical_rank'],
        optimizer_nonconvergence_warning=m['optimizer_nonconvergence_warning'],warning=m['last_warning'] or 'none'))
modeltable=pd.DataFrame(modelrows);modeltable['provenance_json']=json.dumps(provenance);modeltable.to_csv(OUT/'regional_mixed_model_diagnostics.csv',index=False,encoding='utf-8')

included=behavior[behavior.included];checks=js('regional_xml_grouping.json');dirs=sessionmeta[['animal','top_directory','shank_regions','mapping_evidence']].drop_duplicates()
lines=['# Regional rodent replication','',
    '**Status: completed under the dated revised behaviour/channel plan.** Three sessions meet the five-run/five-rest criterion in both CA1 and EC: ec013.156, ec013.157 and ec013.375. All are EC013. No EC012 session qualifies. E1 sensitivity uses the same three sessions and bouts.','',
    'Frozen APC `v1.0`, commit `'+meta['git_commit']+'`. Tagged method code is unchanged. '+link('regional_analysis_provenance.json','Full settings and provenance')+'.','',
    'Primary APC summaries below use the three session-level run-minus-rest differences; CIs are t intervals across sessions. Pooled and EC013 summaries coincide. Per-bout mixed-model estimates are reported separately.','',
    table(across[(across.method=='APC-v1.0')&(across.animal_pool=='pooled')&(across.analysis.isin(['CA1','EC']))],['analysis','outcome','n_sessions','mean_session_difference','ci_low','ci_high','one_sample_p','wilcoxon_p']),
    '## Dated amendment and historical record','',
    'The 2026-10-22 amendment in '+link('PROTOCOL_rodent.md')+' supersedes the chunked historical-speed plan and its gate. It records the user-supplied rationale that historical x1-only trenddecomp speed, retaining -1 sentinels and raw units, changes about 12% of labels under a 2.5-s window shift. That shift claim was not independently rerun here. All regional outcomes use the revised tracking-rate method. The exact historical **12 run/12 rest** reproduction is retained solely as an original-analysis record and for the requested descriptive overlap: '+link('behavior_reproduction.json')+'. The superseded stopped report is '+link('RESULTS_rodent_chunk_plan_stopped.md')+'.','',
    'The amendment was recorded before regional mapping/behaviour/PAC: '+link('regional_protocol_record.json')+'. Protocol SHA-256: `'+meta['protocol_sha256']+'`. Operational details, including Gaussian boundaries, quantiles and bout timestamps, were recorded in '+link('EXECUTION_rodent.md')+'.','',
    '## Channel-to-region map','',
    'The ec012ec.269 XML contains zero-based anatomical groups 0–7, 8–15, 16–23, 24–31 and singleton 32. Thus E1–E8 = shank 1, E9–E16 = shank 2, E17–E24 = shank 3, E25–E32 = shank 4. E33 is auxiliary. The prespecified extension to EC013 gives eight 8-channel shanks through E64, with E65 auxiliary. EC013 is explicitly labelled **“assumed contiguous, verified on ec012ec.269.”** The XML check passed: '+link('regional_xml_grouping.json')+'.','',
    'Region labels come from the exact top-directory rows in ElePosition.txt, joined through hc3-session.csv. All 18 session metadata rows specify `linear`. The per-channel map includes all 882 imported channel rows, region, shank, auxiliary exclusion, source ratio/flag and evidence: '+link('regional_channel_map.csv')+'. Source rows/hashes: '+link('regional_session_metadata.csv')+'.','',
    table(dirs,['animal','top_directory','shank_regions','mapping_evidence']),
    'EC013 shanks 1/2/3–4/5–8 are EC3/EC4/EC5/CA1, respectively; EC012 shanks 1–2/3–4 are EC3/EC5. E1 sensitivity is EC3 in every EC013 session. These are metadata region labels; no additional anatomical inference was applied.','',
    '## Regional channel selection','',
    'Existing whole-recording theta(6–10)/delta(1–4) Welch ratios were reused. Select the first finite maximum within the requested CA1 or EC mask; exclude auxiliary E33/E65. Selection is separate from behaviour eligibility and PAC outcomes. Source channel flags are reported alongside the regional choices. '+link('regional_selected_channels.csv')+'.','',
    table(selected,['animal','session','analysis','channel_name','shank','region','theta_delta_ratio','source_channel_flag','included']),
    '## Mapping and tracking-rate behaviour','',
    'All 18 tracking/LFP duration ratios pass the unchanged 5% mapping check. The ec013.157 missing requested path is supplied by the previously verified equivalent full recording; all timestamps and the saved multichannel crop matched exactly. '+link('mapping_checks.csv')+'; '+link('ec013_157_source_recovery.json')+'.','',
    table(mapping,['animal','session','tracking_array','lfp_duration_s','tracking_to_lfp_duration_ratio']),
    'At 39.0625 Hz, combine valid LED positions, interpolate bounded missing gaps <=0.5 s, fit PC1 to valid positions, and use 250 cm divided by the 99.5th–0.5th percentile span. State position uses the unsmoothed projection. End zones include the extreme percentile tails. Smooth x/y within each finite segment with a normalized Gaussian (SD 0.2 s, radius 32 samples, reflected boundaries), then central-difference 2-D speed in cm/s. Long gaps remain unclassified and split bouts. RUN requires >6 cm/s in the central 70%; REST requires <6 cm/s in either outer 15%; exactly 6 is unclassified. Keep contiguous >=5-s bouts after excluding first/last 2 s. Half-open tracking bout times map to actual 1250-Hz LFP timestamps.','',
    'Raw missing fraction means neither LED is valid; after interpolation means positions still missing. Complete per-bout durations and both tracking/LFP indices: '+link('regional_bouts.csv')+'. Whole-session traces and masks are in the 18 `*_regional_tracking.npz` files.','',
    table(behavior,['animal','session','cm_per_unit','raw_missing_fraction','missing_after_short_interpolation_fraction','short_gap_samples_interpolated','run_bouts','rest_bouts','included']),
    table(behavior,['session','run_total_duration_s','run_mean_duration_s','run_median_duration_s','run_min_duration_s','run_max_duration_s','rest_total_duration_s','rest_mean_duration_s','rest_median_duration_s','rest_min_duration_s','rest_max_duration_s']),
    'Before the 5-s criterion, all EC012 run candidate intervals are shorter than 5 s. Candidate counts, maximum durations and speed quantiles are in '+link('regional_behavior_qc.csv')+'. Eligibility is identical across regional channels because each session uses one behaviour trace. Included: ec013.156 (9 run/43 rest), ec013.157 (6/15), ec013.375 (5/34). The other 15 sessions fail the >=5/5 criterion; '+link('regional_session_eligibility.csv')+' provides every regional inclusion/exclusion row.','',
    '## Descriptive overlap with original ec013.157 bouts','',
    'No overlap gate was applied. Comparisons below clip the new bout sets to the original interval [32.6392,298.0) s. Jaccard is same-state intersection divided by union; whole-recording new bouts outside that interval are not added to the denominator.','',
    table(overlap,['state','historical_bouts','new_bouts_whole_recording','new_bouts_intersecting_original_interval','historical_bouts_with_any_same_state_overlap','historical_duration_s','new_duration_in_original_interval_s','same_state_intersection_s','jaccard']),
    table(detail,['state','historical_bout','historical_start_s','historical_stop_exclusive_s','new_same_state_overlap_s','fraction_historical_bout_covered','new_bouts_overlapping']),
    'Cross-state intersections: '+link('regional_historical_overlap_cross_state.csv')+'.','',
    '## Per-bout analysis and status','',
    'APC uses the byte-verified frozen source with ampRange 80–150 Hz and all other defaults. Additional raw/Ozkurt MVL and preferred phase use the exact frozen selected bands/filter designs; raw MVL and preferred phase are checked against the frozen output on every successful bout. A2\' uses phase 4:0.5:12 Hz, half-width 1.5 Hz; amplitude 80:4:148 Hz, fixed half-width 12 Hz; MVL-raw, MVL-Ozkurt, KLMI and GLM, each at its own grid maximum. Comparator filtering is the corrected `butter(4)` zpk→SOS/filtfilt realization, with pole radius <1 and centre-gain error <1e-3 guards.','',
    f'{runtime["unique_input_checkpoints"]} unique channel/bout inputs; {len(bouts)} method rows across CA1, EC and E1 sensitivity. Full fP, fA, raw/Ozkurt MVL, preferred phase, status, route and provenance: '+link('regional_bout_estimates.csv')+'. Full normalized APC options and comparator settings are stored per row/checkpoint. Guard table: '+link('regional_comparator_filter_guards.csv')+f' ({len(guard)} band/fs entries, all passed).','',
    table(status,['analysis','method','state','status','bouts']),
    '## Per-session and across-session statistics','',
    'Per-session run-minus-rest: Welch unequal-variance t, pooled-SD Hedges g with exact gamma correction, and 10,000 percentile bootstrap resamples (seed 20261022, deterministic session streams; indices shared across methods within each analysis/session). Finite-value denominators are shown. Across sessions: session-level differences, two-sided one-sample t and Wilcoxon signed-rank tests, zero differences recorded, no multiplicity correction. EC012 n=0 rows are unavailable; pooled results equal EC013 because only EC013 qualifies.','',
    'Full CSVs: '+link('regional_session_statistics.csv')+'; '+link('regional_across_session_statistics.csv')+'; '+link('regional_state_summary.csv')+'. One SciPy precision-loss warning was returned for the CA1 ec013.157 KLMI fP Welch comparison (nearly identical values). The original test output is retained with its warning; no estimator or data adjustment was applied. Warning/context: '+link('regional_statistics_warnings.csv')+'.','']
for analysis in ['CA1','EC','E1_sensitivity']:
    lines+=['### '+analysis,'',table(sessionstats[sessionstats.analysis==analysis],['session','method','outcome','n_run','n_rest','run_mean','rest_mean','mean_difference','welch_t','welch_df','welch_p','hedges_g','ci_low','ci_high']),
        table(across[across.analysis==analysis],['animal_pool','method','outcome','n_sessions','mean_session_difference','median_session_difference','ci_low','ci_high','one_sample_t','one_sample_p','wilcoxon_statistic','wilcoxon_p','zero_differences'])]
lines+=['## Region-specific mixed models','',
    'Specified session random intercept and state slope retained throughout, fitted by REML. With only EC013 represented, the constant animal fixed effect is redundant; all fitted formulas are `outcome ~ state_run + (1 + state_run | session)`. This constant-animal handling was recorded before PAC analysis. State is 0=rest, 1=run. The optimizer nonconvergence warning was enabled/captured; its exit code is not a public property in this MATLAB version. Covariance eigenvalues/rank and full fit logs are retained.','',
    table(coef,['analysis','outcome','Name','Estimate','SE','tStat','DF','pValue','Lower','Upper']),
    table(modeltable,['analysis','outcome','sessions','observations','var_intercept','cov_intercept_state','var_state','residual_variance','covariance_rank','optimizer_nonconvergence_warning','warning']),
    'Model diagnostics: '+link('regional_mixed_models.json')+'; saved models and individual `regional_mixed_*_fit.txt` logs preserve each fit.','',
    '## Boundary picks and within-state fP spread','',
    'Boundary counts refer to exact fP=4 or 12 Hz. APC uses its frozen default continuous phase search; its estimates can lie outside the scan range. Spread is sample SD, linear-quantile IQR and unscaled median absolute deviation.','',
    table(boundaries,['analysis','session','method','state','n_bouts','n_valid','boundary_fp_4','boundary_fp_12']),
    table(spread,['analysis','session','method','state','n_valid','fp_sd','fp_iqr','fp_mad']),
    'Paired session APC-minus-scan spread values: '+link('regional_within_state_spread_comparisons.csv')+'. Across-session spread summaries/tests for every scan, state, region and animal pool: '+link('regional_across_session_spread_comparisons.csv')+'.','',
    '## Figures','',
    'Every figure is exported as 300-dpi PNG and SVG, with commit and source CSV(s) printed and source hashes embedded. The displayed comparison scan is the prespecified Ozkurt-max scan; all four scan metrics remain in the tables.','']
for f in figures:lines.append('- '+f['description']+': '+link(Path(f['png']).name,'PNG')+'; '+link(Path(f['svg']).name,'SVG')+'.')
lines+=['','## Runtime, deviations and limits','',
    f'Tracking-rate behaviour: {js("regional_behavior_runtime.json")["elapsed_seconds"]:.3f} s. Successful PAC/comparator runner: {runtime["elapsed_seconds"]:.3f} s. Statistics: {js("regional_statistics_runtime.json")["elapsed_seconds"]:.3f} s. Mixed models: {models["elapsed_seconds"]:.3f} s. MATLAB startup and failed tooling launches are excluded from these stage timings.','',
    'Three sessions from one animal qualify; no between-animal coefficient or EC012 session-level test is estimable. Source anatomical mapping for EC013 is the explicitly requested assumption. All source channel flags remain visible in the selection table. The historical speed/chunk results are superseded and not used in regional inference.','']
for d in tooling:lines.append('- '+d['type']+': '+d['detail'])
lines+=['- Existing MATLAB startup warnings refer to old missing Brainstorm directories; no installation change was made.',
    '- Source path recovery for ec013.157 is the previously verified local equivalent, documented above. No input or tagged method file was modified.',
    '- Constant-animal mixed-model handling and tracking endpoint/quantile conventions are recorded in the execution amendment; the random-effects structure was retained.',
    '', 'Full current provenance: '+link('regional_analysis_provenance.json')+'. Current status: '+link('STATUS.json')+'. Output manifest: '+link('output_manifest.json')+'.','']
(OUT/'RESULTS_rodent.md').write_text('\n'.join(lines),encoding='utf-8')
(OUT/'deviations.json').write_text(json.dumps(dict(metadata=provenance,deviations=tooling+[
    dict(type='metadata assumption',detail='EC013 contiguous 8-channel mapping is assumed as explicitly requested, verified on ec012ec.269.'),
    dict(type='constant animal',detail='Only EC013 eligible; redundant animal fixed-effect term omitted as prespecified before outcome analysis; random intercept/slope retained.'),
    dict(type='statistical warning',detail='SciPy precision-loss warning for CA1 ec013.157 KLMI fP Welch comparison; unchanged test output and warning context retained in regional_statistics_warnings.csv.'),
    dict(type='source recovery',detail='ec013.157 uses previously verified equivalent full local recording.'),
    dict(type='startup tooling',detail='Pre-existing missing Brainstorm-directory warnings retained in MATLAB logs.')]),indent=2),encoding='utf-8')
(OUT/'STATUS.json').write_text(json.dumps(dict(status='COMPLETE_REGIONAL_PLAN',metadata=provenance,included_sessions=included.session.tolist(),regional_analyses=['CA1','EC','E1_sensitivity'],method_rows=len(bouts),historical_speed_used_for_primary_results=False),indent=2),encoding='utf-8')
print(json.dumps(dict(status='COMPLETE',report=str(OUT/'RESULTS_rodent.md'),method_rows=len(bouts),figure_pairs=len(figures))))
