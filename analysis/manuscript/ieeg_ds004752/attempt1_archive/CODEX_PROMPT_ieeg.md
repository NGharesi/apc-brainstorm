GOAL: Run the prespecified human intracranial analysis of APC on OpenNeuro ds004752. Follow the protocol exactly:
C:\Users\nghare\.brainstorm\process\apc-brainstorm-publish\protocol\APC_ieeg_ds004752_protocol.md
(committed in 8183594 on branch neuroimage-submission; SHA-256 8c613b0f8d8ea61fb2a922fbfb58531907d37f278c596ea946a165f75837a804).

Do not edit that protocol, anything under src\, or any tagged code. Put all new code and outputs in:
C:\Users\nghare\.brainstorm\process\revision_checks\ieeg_ds004752\
Fix and log tooling errors (file reading, paths, memory). Stop and report on anything method-relevant.

STEP 0. Provenance
- Confirm the repository is on branch neuroimage-submission with a clean working tree.
- Confirm the protocol's SHA-256 matches the value above.
- Record in provenance.json: git HEAD, MATLAB version, toolbox versions, and the SHA-256 of src\bst_apc.m, src\calc_MI_all_methods.m, revision_checks\rodent_multi\v1_bout_features.m, revision_checks\final\sos_comparators.m and revision_checks\final\final_sos_filter.m.

STEP 1. Gates (protocol 3.1, 3.2, 4.1). All must pass before any APC or scan output is computed on ds004752.
a) APC equivalence gate:
   - addpath the repo's src\ first. Check that which('bst_apc') is the repo copy, not revision_checks\final\frozen_v1.
   - Run bst_apc on revision_checks\final\burst_coupled_input.csv (fs 500 Hz) with struct('fA',[80 150]).
   - Reproduce fP 7.99792313403792, fA 122, raw MVL 0.176907779165945 and preferred phase 178.575795410875 to within 1e-10.
b) EDF reading checks for every iEEG file: channel order vs channels.tsv, sample count vs events.tsv, fs = 2000, no NaN, non-zero variance, microvolt range.
   - The earlier screening of this dataset returned NaN. Find and report the cause in a sentence.
c) Trial-timeline check (protocol 3.2):
   - Use the papers cited in the dataset README.
   - Plot the grand-average occipital scalp-EEG evoked response over all trials, with expected onsets at 1 s and 6 s, and report the peak latencies.
   - Stop if the timeline 0-1 fixation / 1-3 encoding / 3-6 maintenance / 6+ probe is not confirmed.

STEP 2. Fixed choices made before any APC or scan output (protocol 3.3-3.5)
- Notch filtering.
- Bipolar hippocampal pair per patient by the 4-8/1-4 Hz power-ratio rule.
- Trial exclusion (dataset artifact flag plus the robust 6-SD rules).
- Session eligibility (>= 20 trials) and patient eligibility (>= 2 sessions).
Write contacts.csv and trial_inclusion.csv before Step 3.

STEP 3. Per-trial estimates (protocol 4) on the 3-s maintenance windows
- APC: through v1_bout_features.m, using the repo's src\bst_apc.m with default options plus fA [80 150].
- Scans: ieeg_comparators.m, a copy of sos_comparators.m with the added "ieeg" profile (phase 2:0.5:12, half-width 1.5; amplitude 80:4:148, mode "ieeg_A2_prime" with half-width 12). Leave the existing profiles byte-identical; verify by diffing the copy against the original.
- Log every filter guard (pole radius, centre gain) to filter_guards.csv.
- Save ieeg_trial_estimates.csv incrementally, so the run can resume after an interruption without recomputing finished trials.

STEP 4. Statistics (protocol 5): primary, secondary 1-6, exploratory load model, sensitivity analyses (a) and (b).
- Use the seeds in the protocol.
- State the primary decision in exactly one of the three prespecified forms.

STEP 5. Outputs (protocol 7)
- RESULTS_ieeg.md with: gate results, timeline plot and latencies, the NaN cause, contacts per patient, trial counts per exclusion rule, all endpoint tables (with n patients, n sessions and n trials), boundary-hit and failure rates, and a list of every deviation with its reason.
- Figure: four panels, 300-dpi PNG and SVG, no titles or footers inside the image.
- CSV files and provenance.json as listed in the protocol.
- Do not commit. I will review the results first.

STOP RULES: as in protocol section 6. Each reportable run is done once. If a method-relevant problem appears (equivalence gate fails, timeline not confirmed, most trials invalid for a method, a needed change to any fixed setting), stop, write STOPPED.md explaining it, and report back without working around it.
