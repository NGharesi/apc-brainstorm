# POST HOC sensitivity — minimum bout duration 2 s

Dated 2026-10-22. This sensitivity is POST HOC throughout.

USER REQUEST (verbatim)

POST HOC SENSITIVITY (label it as post hoc everywhere): rerun the regional analysis with the identical pipeline, except that the minimum bout duration is 2 s and inclusion requires >= 5 run and >= 5 rest bouts. Do not change any other rule. Report it beside the prespecified 5-s results, in a separate section, with separate tables and figures. Results go to revision_checks/rodent_multi/posthoc_2s/.

Execution fixed before extraction

The only analysis-rule change is minimum contiguous same-state bout duration
from 5 s to 2 s. Session inclusion remains >=5 run and >=5 rest bouts. Reuse
the saved whole-recording tracking-rate time, position, scale, PCA projection,
Gaussian-smoothed position, 2-D speed and run/rest masks exactly. Re-extract
contiguous >=2-s bouts, retaining the same gaps, central/end position zones,
6-cm/s strict thresholds and first/last 2-s exclusion. Map half-open bout times
to actual LFP timestamps with the same searchsorted convention. Regional
channels, metadata assumptions, auxiliary exclusions and whole-recording
theta/delta ratios are unchanged. Historical overlap remains descriptive only.

Use frozen APC v1.0 (71ebc16a), ampRange 80–150 Hz and all remaining defaults;
the same SOS A2' four metrics/grids/filter guards; identical raw/Ozkurt MVL and
preferred-phase extraction checks. Analyze all newly eligible sessions and
all >=2-s bouts. Recompute method outputs (including >=5-s bouts) from the same
LFP inputs; retained shared >=5-s inputs provide an exact-result consistency
check against the prespecified analysis. Native LFP sampling remains 1250 Hz.

Statistics, 10,000-resample percentile CIs, seed 20261022, session stream scheme,
Welch t, Hedges g, session-level t/Wilcoxon, boundary picks, within-state spread
and random-intercept/random-slope REML models are unchanged. Preserve finite
denominators and nonzero APC statuses. Region-specific models retain animal
when both animals qualify, and omit only a redundant constant animal column
otherwise, as in the prespecified pipeline. Do not simplify random effects.

All new output tables carry analysis_type = POST HOC sensitivity: 2-s minimum
bouts and post_hoc=true in provenance. Every figure title/footer, report section
and figure/table caption says POST HOC. Keep all prespecified CSVs, MAT files,
tracking traces, figures and method source unchanged. Append a separate POST HOC
section to the parent report with side-by-side comparisons and links to the
separate POST HOC report/tables/figures in this folder. Runtime and any tooling
corrections are logged. Stop on a method-relevant failure.
