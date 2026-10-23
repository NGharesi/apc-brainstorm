# APC v3.0: aperiodic-corrected Step 2

**v3.0 recommended.** G0-G2 passed. Adoption checks: A1 PASS; A3 PASS; A4 PASS. Phase C completed; ECoG success criterion passed.

## Factual summary

- G0-G2 passed; public freeze `v3.0` = `1cb2056fb16eaf944857c8d3f11a51276d5b7a1f`. Default remains v1.
- A1: HA joint recovery v3 101/450 versus v1 43/450; exact one-sided p=3.469447e-18.
- A2 (key secondary): HA fP recovery v3 368/450 versus SP-raw 440/450; exact two-sided p=2.757789e-18.
- A3 passed all three bounds. A4: false joint v3 72/700 versus v1 45/700; +3.85714 percentage points, within the allowed +5.
- ECoG rest-spectrum criterion passed: v3 13/18, v1 5/18, SP-raw 15/18; required v3 >=9/18.
- ECoG Primary 1: **Not shown**, mean difference -0.002331771, 95% CI [-0.007314731, 0.002822274]. Primary 2: **Opposite**, median SD difference 1.729665 Hz, 95% CI [1.014967, 2.268466].

## Protocol, freeze and provenance

Amendment 1 was public at `c6b669962369cc97e3ab2635e583b48386152472` before the amended method code was written. Protocol SHA-256 `fda66faf93fb29bb8d84bb8fab89a7a051b474165c22b195ef92e24aeb91a8e1` matches. G0-G2 passed; code, gate code and the HA generator were frozen at `1cb2056fb16eaf944857c8d3f11a51276d5b7a1f` (`v3.0`) and pushed before any held-out input was generated. The repository was clean at freeze. No results were committed. MATLAB 9.13.0.2105380 (R2022b) Update 2; full toolbox versions, source hashes and execution conventions: [provenance.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/provenance.json>); [phaseA_implementation.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseA_implementation.json>); [phaseB_implementation.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseB_implementation.json>); [freeze_precheck.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/freeze_precheck.json>).

Default v1 and the v2 path retain their original calculations. The amended helper changes only peak location after unchanged candidate detection: raw-log-power hill climb within the contiguous positive-residual region (`raw_local_max`), otherwise residual refinement of the original candidate (`residual_shoulder`). SP-raw shares the helper. Sigma is sample SD; parabolic displacement is bounded to +/-0.5 bin. [amendment1_peak_location.diff](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/amendment1_peak_location.diff>).

The committed LF endings of `bst_apc.m` were restored without changing its text. Plain `git diff --stat v1.0 -- src/bst_apc.m`: 260 insertions, zero deletions (211 pre-existing v2 additions). Removing v3 additions/version switch restores the pre-v3 source text exactly. [bst_apc_line_endings_and_diff.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/bst_apc_line_endings_and_diff.json>); [source_additions_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/source_additions_verification.json>); [v3_implementation.diff](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/v3_implementation.diff>).

## Attempt 1 (residual-based location)

G0 passed. G1 returned status 0, fP 8.6902612490498399 Hz and fA 121 Hz. The fP error was 0.69026124904983988 Hz, exceeding 0.1 Hz; the fA error was within 8 Hz. The run stopped at G1. G2/G3, freeze and held-out evaluation did not run.

Attempt-1 outputs, STOPPED/status files, logs, implementation diff and source snapshots are preserved unchanged in [attempt1_residual_location](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/attempt1_residual_location>). The uncommitted helper/SP-raw source and `bst_apc.m` diff were also snapshotted before Amendment 1. All archived SHA-256 values were rechecked: [attempt1_archive_manifest.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/attempt1_archive_manifest.json>).

## Phase A gates


| gate | result |
| --- | --- |
| G0 | PASS |
| G1 | PASS |
| G2 | PASS |
| G3 | DESCRIPTIVE_COMPLETE |

G0 canonical tolerance 1e-10:

| metric | expected | observed | absolute_difference |
| --- | --- | --- | --- |
| fP_hz | 7.997923 | 7.997923 | 3.552714e-15 |
| fA_hz | 122 | 122 | 0 |
| raw_MVL | 0.1769078 | 0.1769078 | 1.387779e-16 |
| preferred_phase_deg | 178.5758 | 178.5758 | 3.694822e-13 |

Complete v1 output/runInfo equality against tag v1.0: True; default versus explicit v1: True; complete v2 output/runInfo equality against tag v2.0: True. Full tagged/current results: [G0.mat](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/G0.mat>); [G0.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/G0.json>); [G0_trials.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/G0_trials.csv>).

G1 canonical v3 (required status 0, |fP-8| <=0.1 Hz and |fA-120| <=8 Hz):

| status | fP_hz | fA_hz | score | exponent | offset | peak_height | sigma | location_branch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 7.997923 | 122 | 0.1769078 | 1.355715 | -3.072999 | 3.000331 | 0.3373379 | raw_local_max |

Complete diagnostics and curves: [G1.mat](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/G1.mat>); [G1_curve.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/G1_curve.csv>).

G2: seed 20261031; 20 paired repeats per cell; recovery requires status 0 and |fP-15| <=1 Hz. Every cell requires at least 16/20. Status arrays below are ordered 0,1,2,3,4,5.

| beta | duration_s | repeats | v3_fp_recovery | v1_fp_recovery | v3_status_counts | v1_status_counts | passed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 20 | 19 | 5 | [20,0,0,0,0,0] | [7,0,0,0,13,0] | 1 |
| 1 | 6 | 20 | 20 | 10 | [20,0,0,0,0,0] | [10,0,0,0,10,0] | 1 |
| 2 | 2 | 20 | 19 | 0 | [20,0,0,0,0,0] | [0,0,0,0,20,0] | 1 |
| 2 | 6 | 20 | 20 | 9 | [20,0,0,0,0,0] | [9,0,0,0,11,0] | 1 |

G3: seed 20261031, no-rhythm Poisson bursts; descriptive only. Frequency quantiles use finite returned fP; invalid outputs and status counts are retained.

| beta | duration_s | n | status3 | status3_rate | status0 | finite_fp | fp_min | fp_q25 | fp_median | fp_q75 | fp_max | status_counts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 20 | 1 | 0.05 | 19 | 19 | 3.561905 | 12.51045 | 19.75165 | 24.17951 | 29.63296 | {"0": 19, "3": 1} |
| 1 | 6 | 20 | 0 | 0 | 20 | 20 | 2.386143 | 6.280205 | 11.55862 | 21.72379 | 29.15411 | {"0": 20} |
| 2 | 2 | 20 | 1 | 0.05 | 19 | 19 | 3.565824 | 4.236037 | 15.35857 | 21.85931 | 27.94773 | {"0": 19, "3": 1} |
| 2 | 6 | 20 | 0 | 0 | 20 | 20 | 3.310041 | 3.514251 | 3.71423 | 4.173752 | 23.50648 | {"0": 20} |

Per-trial branch labels (including `not_reached` before location and `not_applicable` for v1/v2), frequencies, diagnostics, status and provenance: [gate_trials.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/gate_trials.csv>); [G0_trials.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/G0_trials.csv>). Branch counts: [gate_location_branch_counts.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/gate_location_branch_counts.csv>). All curves and complete signal/output MAT files are preserved.

## Phase B: held-out evaluation

All 675 regenerated HB cases were bit-identical to the original complete saved cases. Before any held-out v3/SP-raw/scan estimate, all 675 v1 outputs reproduced original unrounded MAT values exactly (fP, fA, score, status and route). [HB_signal_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/HB_signal_verification.json>); [HB_v1_equivalence.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/HB_v1_equivalence.csv>); [HB_VERIFIED.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/HB_VERIFIED.json>).

HA: seed 20261101; 18 cells x 25 coupled trials plus 450 paired timing nulls; fs 1000 Hz. The committed generator uses the development-family power-law construction and 0.18 background-burst recipe. Draw/stream/envelope conventions were fixed before generation in [freeze_precheck.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/freeze_precheck.json>). Independent saved-input audit passed all cell counts, dimensions, finite-signal, unit-SD noise, carrier/rhythm and paired-component checks; maximum pair residual 8.881784197001252e-16. [input_bank_audit.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/input_bank_audit.json>). HB: seed 20261022; original 350 coupled inputs, 250 timing nulls and 75 no-coupled-burst controls. H3 in A4 is all 250 original timing nulls; no-coupled-burst controls are reported separately.

HA APC range [80,150] Hz, defaults otherwise. HB retains the original [80,160] Hz range for exact saved-v1 reproduction, also used for v3. HA scans: phase 3:0.5:30, amplitude 80:4:160, amplitude half-width 30 Hz. HB scans retain phase 3:0.5:14 and amplitude half-width 14 Hz. All phase half-widths 1.5 Hz. Metrics and ties are unchanged; only the HA profile was added to a copy of the SOS scan helper. [comparator_HA_profile.diff](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/comparator_HA_profile.diff>); [HB_generator_wrapper.diff](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/HB_generator_wrapper.diff>).

All 120 unique recorded SOS designs passed pole-radius and centre-gain guards. Maximum pole radius 0.99811790817429558; maximum |centre gain-1| 7.6225331533397167e-06. [filter_guards.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/filter_guards.csv>).

Invalid outputs count as failures. SP-raw estimates fP only; joint/fA entries are NA. Recovery is inclusive +/-1 Hz fP and +/-8 Hz fA; strict joint uses +/-0.5 Hz fP. All proportions have Wilson 95% CIs in the CSVs. Errors describe finite returned estimates; denominators and all status counts are supplied.

## A1-A4 and adoption decision

**v3.0 recommended.**

| criterion | set | n | a_success | b_success | a_only | b_only | p_value | passed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | HA | 450 | 101 | 43 | 58 | 0 | 3.469447e-18 | True |
| A2 (secondary) | HA fP | 450 | 368 | 440 | 4 | 76 | 2.757789e-18 | NA |
| A3 | H1 | 175 | 124 | 120 | 4 | 0 | 0.0625 | True |
| A3 | H2 | 150 | 60 | 63 | 0 | 3 | 1 | True |
| A3 | H4 | 25 | 22 | 22 | 0 | 0 | 1 | True |
| A4 | H3 + HA timing null | 700 | 72 | 45 | 28 | 1 | 1.117587e-07 | True |

A1 uses a one-sided exact binomial McNemar test. A3 requires v3 >= v1 minus 10/175 (H1), 10/150 (H2), and 3/25 (H4), each separately. A4 allows at most +5 percentage points of false joint recovery over the 700 pooled timing nulls. A2 is secondary and does not gate adoption. The A3/A4 p values are descriptive paired comparisons; their decisions use only the fixed count/rate bounds.

### A2: does burst timing add fP information beyond SP-raw?

HA fP recovery: v3 368/450, SP-raw 440/450; v3-only 4, SP-raw-only 76; two-sided exact McNemar p=2.75778872939e-18.

A4 false joint recovery: v3 72/700 (10.285714%), v1 45/700 (6.428571%); difference 3.857143 percentage points.

Complete paired discordance tables/decisions: [criteria_decisions.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/criteria_decisions.csv>); [criteria_decisions.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/criteria_decisions.json>).

## Pooled recovery


| set | method | n | valid | joint | strict_joint | fp | fa | status_counts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HA_coupled | APC-v1.0 | 450 | 109 | 43 | 43 | 97 | 45 | {"0": 109, "4": 341} |
| HA_coupled | APC-v3.0 | 450 | 447 | 101 | 96 | 368 | 111 | {"0": 447, "3": 3} |
| HA_coupled | GLM | 450 | 450 | 216 | 82 | 342 | 276 | {"0": 450} |
| HA_coupled | KLMI | 450 | 450 | 285 | 120 | 301 | 415 | {"0": 450} |
| HA_coupled | MVL-Ozkurt | 450 | 450 | 234 | 94 | 302 | 294 | {"0": 450} |
| HA_coupled | MVL-raw | 450 | 450 | 303 | 125 | 318 | 403 | {"0": 450} |
| HA_coupled | SP-raw | 450 | 446 | NA | NA | 440 | NA | {"0": 446, "3": 4} |
| HA_timing_null | APC-v1.0 | 450 | 90 | 9 | 9 | 77 | 9 | {"0": 90, "2": 1, "4": 359} |
| HA_timing_null | APC-v3.0 | 450 | 449 | 35 | 33 | 346 | 47 | {"0": 449, "2": 1} |
| HA_timing_null | GLM | 450 | 450 | 3 | 1 | 10 | 29 | {"0": 450} |
| HA_timing_null | KLMI | 450 | 450 | 2 | 0 | 3 | 353 | {"0": 450} |
| HA_timing_null | MVL-Ozkurt | 450 | 450 | 3 | 0 | 6 | 36 | {"0": 450} |
| HA_timing_null | MVL-raw | 450 | 450 | 6 | 1 | 8 | 213 | {"0": 450} |
| HA_timing_null | SP-raw | 450 | 446 | NA | NA | 440 | NA | {"0": 446, "3": 4} |
| H1 | APC-v1.0 | 175 | 170 | 120 | 120 | 169 | 120 | {"0": 170, "4": 5} |
| H1 | APC-v3.0 | 175 | 175 | 124 | 124 | 175 | 124 | {"0": 175} |
| H1 | GLM | 175 | 175 | 84 | 29 | 85 | 145 | {"0": 175} |
| H1 | KLMI | 175 | 175 | 75 | 26 | 75 | 142 | {"0": 175} |
| H1 | MVL-Ozkurt | 175 | 175 | 96 | 45 | 97 | 132 | {"0": 175} |
| H1 | MVL-raw | 175 | 175 | 102 | 48 | 102 | 162 | {"0": 175} |
| H1 | SP-raw | 175 | 175 | NA | NA | 175 | NA | {"0": 175} |
| H2 | APC-v1.0 | 150 | 148 | 63 | 61 | 64 | 82 | {"0": 148, "4": 2} |
| H2 | APC-v3.0 | 150 | 150 | 60 | 58 | 61 | 80 | {"0": 150} |
| H2 | GLM | 150 | 150 | 96 | 39 | 103 | 126 | {"0": 150} |
| H2 | KLMI | 150 | 150 | 91 | 38 | 94 | 123 | {"0": 150} |
| H2 | MVL-Ozkurt | 150 | 150 | 73 | 24 | 78 | 109 | {"0": 150} |
| H2 | MVL-raw | 150 | 150 | 78 | 28 | 82 | 123 | {"0": 150} |
| H2 | SP-raw | 150 | 150 | NA | NA | 50 | NA | {"0": 150} |
| H4 | APC-v1.0 | 25 | 25 | 22 | 22 | 25 | 22 | {"0": 25} |
| H4 | APC-v3.0 | 25 | 25 | 22 | 22 | 25 | 22 | {"0": 25} |
| H4 | GLM | 25 | 25 | 24 | 9 | 24 | 25 | {"0": 25} |
| H4 | KLMI | 25 | 25 | 24 | 9 | 24 | 25 | {"0": 25} |
| H4 | MVL-Ozkurt | 25 | 25 | 23 | 6 | 23 | 25 | {"0": 25} |
| H4 | MVL-raw | 25 | 25 | 23 | 6 | 23 | 25 | {"0": 25} |
| H4 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H3_timing_null | APC-v1.0 | 250 | 248 | 36 | 36 | 212 | 44 | {"0": 248, "4": 2} |
| H3_timing_null | APC-v3.0 | 250 | 250 | 37 | 37 | 206 | 46 | {"0": 250} |
| H3_timing_null | GLM | 250 | 250 | 7 | 3 | 28 | 50 | {"0": 250} |
| H3_timing_null | KLMI | 250 | 250 | 3 | 0 | 12 | 65 | {"0": 250} |
| H3_timing_null | MVL-Ozkurt | 250 | 250 | 2 | 0 | 10 | 49 | {"0": 250} |
| H3_timing_null | MVL-raw | 250 | 250 | 2 | 0 | 9 | 99 | {"0": 250} |
| H3_timing_null | SP-raw | 250 | 250 | NA | NA | 200 | NA | {"0": 250} |
| HB_no_coupled_burst | APC-v1.0 | 75 | 74 | 11 | 11 | 74 | 11 | {"0": 74, "4": 1} |
| HB_no_coupled_burst | APC-v3.0 | 75 | 75 | 12 | 12 | 75 | 12 | {"0": 75} |
| HB_no_coupled_burst | GLM | 75 | 75 | 0 | 0 | 3 | 16 | {"0": 75} |
| HB_no_coupled_burst | KLMI | 75 | 75 | 0 | 0 | 0 | 11 | {"0": 75} |
| HB_no_coupled_burst | MVL-Ozkurt | 75 | 75 | 0 | 0 | 1 | 16 | {"0": 75} |
| HB_no_coupled_burst | MVL-raw | 75 | 75 | 0 | 0 | 3 | 19 | {"0": 75} |
| HB_no_coupled_burst | SP-raw | 75 | 75 | NA | NA | 75 | NA | {"0": 75} |

Complete Wilson CIs and finite-error summaries: [pooled_recovery.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/pooled_recovery.csv>).

## HA recovery by cell


| dataset | beta | rhythm_amplitude | duration_s | method | n | valid | joint | strict_joint | fp | fa | status_counts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| coupled | 1 | 0.3 | 2 | APC-v1.0 | 25 | 2 | 0 | 0 | 0 | 0 | {"0": 2, "4": 23} |
| coupled | 1 | 0.3 | 2 | APC-v3.0 | 25 | 24 | 2 | 2 | 14 | 4 | {"0": 24, "3": 1} |
| coupled | 1 | 0.3 | 2 | GLM | 25 | 25 | 17 | 11 | 22 | 17 | {"0": 25} |
| coupled | 1 | 0.3 | 2 | KLMI | 25 | 25 | 6 | 3 | 8 | 18 | {"0": 25} |
| coupled | 1 | 0.3 | 2 | MVL-Ozkurt | 25 | 25 | 10 | 4 | 12 | 11 | {"0": 25} |
| coupled | 1 | 0.3 | 2 | MVL-raw | 25 | 25 | 15 | 7 | 15 | 18 | {"0": 25} |
| coupled | 1 | 0.3 | 2 | SP-raw | 25 | 22 | NA | NA | 19 | NA | {"0": 22, "3": 3} |
| coupled | 1 | 0.3 | 6 | APC-v1.0 | 25 | 1 | 1 | 1 | 1 | 1 | {"0": 1, "4": 24} |
| coupled | 1 | 0.3 | 6 | APC-v3.0 | 25 | 25 | 7 | 5 | 18 | 8 | {"0": 25} |
| coupled | 1 | 0.3 | 6 | GLM | 25 | 25 | 21 | 9 | 24 | 22 | {"0": 25} |
| coupled | 1 | 0.3 | 6 | KLMI | 25 | 25 | 22 | 11 | 23 | 23 | {"0": 25} |
| coupled | 1 | 0.3 | 6 | MVL-Ozkurt | 25 | 25 | 20 | 8 | 22 | 21 | {"0": 25} |
| coupled | 1 | 0.3 | 6 | MVL-raw | 25 | 25 | 22 | 8 | 23 | 24 | {"0": 25} |
| coupled | 1 | 0.3 | 6 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| coupled | 1.5 | 0.3 | 2 | APC-v1.0 | 25 | 2 | 0 | 0 | 0 | 1 | {"0": 2, "4": 23} |
| coupled | 1.5 | 0.3 | 2 | APC-v3.0 | 25 | 25 | 3 | 3 | 18 | 4 | {"0": 25} |
| coupled | 1.5 | 0.3 | 2 | GLM | 25 | 25 | 10 | 4 | 15 | 13 | {"0": 25} |
| coupled | 1.5 | 0.3 | 2 | KLMI | 25 | 25 | 10 | 4 | 10 | 22 | {"0": 25} |
| coupled | 1.5 | 0.3 | 2 | MVL-Ozkurt | 25 | 25 | 11 | 5 | 13 | 13 | {"0": 25} |
| coupled | 1.5 | 0.3 | 2 | MVL-raw | 25 | 25 | 14 | 7 | 16 | 18 | {"0": 25} |
| coupled | 1.5 | 0.3 | 2 | SP-raw | 25 | 24 | NA | NA | 22 | NA | {"0": 24, "3": 1} |
| coupled | 1.5 | 0.3 | 6 | APC-v1.0 | 25 | 0 | 0 | 0 | 0 | 0 | {"4": 25} |
| coupled | 1.5 | 0.3 | 6 | APC-v3.0 | 25 | 25 | 10 | 9 | 13 | 11 | {"0": 25} |
| coupled | 1.5 | 0.3 | 6 | GLM | 25 | 25 | 15 | 5 | 23 | 16 | {"0": 25} |
| coupled | 1.5 | 0.3 | 6 | KLMI | 25 | 25 | 21 | 5 | 23 | 23 | {"0": 25} |
| coupled | 1.5 | 0.3 | 6 | MVL-Ozkurt | 25 | 25 | 17 | 6 | 22 | 20 | {"0": 25} |
| coupled | 1.5 | 0.3 | 6 | MVL-raw | 25 | 25 | 22 | 7 | 22 | 25 | {"0": 25} |
| coupled | 1.5 | 0.3 | 6 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| coupled | 2 | 0.3 | 2 | APC-v1.0 | 25 | 0 | 0 | 0 | 0 | 0 | {"4": 25} |
| coupled | 2 | 0.3 | 2 | APC-v3.0 | 25 | 24 | 2 | 2 | 16 | 3 | {"0": 24, "3": 1} |
| coupled | 2 | 0.3 | 2 | GLM | 25 | 25 | 9 | 4 | 13 | 16 | {"0": 25} |
| coupled | 2 | 0.3 | 2 | KLMI | 25 | 25 | 13 | 8 | 13 | 25 | {"0": 25} |
| coupled | 2 | 0.3 | 2 | MVL-Ozkurt | 25 | 25 | 10 | 5 | 13 | 16 | {"0": 25} |
| coupled | 2 | 0.3 | 2 | MVL-raw | 25 | 25 | 14 | 8 | 15 | 24 | {"0": 25} |
| coupled | 2 | 0.3 | 2 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| coupled | 2 | 0.3 | 6 | APC-v1.0 | 25 | 0 | 0 | 0 | 0 | 0 | {"4": 25} |
| coupled | 2 | 0.3 | 6 | APC-v3.0 | 25 | 25 | 6 | 6 | 21 | 7 | {"0": 25} |
| coupled | 2 | 0.3 | 6 | GLM | 25 | 25 | 13 | 5 | 18 | 19 | {"0": 25} |
| coupled | 2 | 0.3 | 6 | KLMI | 25 | 25 | 19 | 6 | 19 | 25 | {"0": 25} |
| coupled | 2 | 0.3 | 6 | MVL-Ozkurt | 25 | 25 | 13 | 3 | 17 | 20 | {"0": 25} |
| coupled | 2 | 0.3 | 6 | MVL-raw | 25 | 25 | 17 | 5 | 17 | 25 | {"0": 25} |
| coupled | 2 | 0.3 | 6 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| coupled | 1 | 0.5 | 2 | APC-v1.0 | 25 | 6 | 1 | 1 | 5 | 1 | {"0": 6, "4": 19} |
| coupled | 1 | 0.5 | 2 | APC-v3.0 | 25 | 24 | 2 | 2 | 14 | 4 | {"0": 24, "3": 1} |
| coupled | 1 | 0.5 | 2 | GLM | 25 | 25 | 7 | 3 | 16 | 11 | {"0": 25} |
| coupled | 1 | 0.5 | 2 | KLMI | 25 | 25 | 7 | 4 | 7 | 21 | {"0": 25} |
| coupled | 1 | 0.5 | 2 | MVL-Ozkurt | 25 | 25 | 6 | 4 | 8 | 10 | {"0": 25} |
| coupled | 1 | 0.5 | 2 | MVL-raw | 25 | 25 | 11 | 6 | 12 | 16 | {"0": 25} |
| coupled | 1 | 0.5 | 2 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| coupled | 1 | 0.5 | 6 | APC-v1.0 | 25 | 9 | 4 | 4 | 8 | 4 | {"0": 9, "4": 16} |
| coupled | 1 | 0.5 | 6 | APC-v3.0 | 25 | 25 | 8 | 8 | 21 | 8 | {"0": 25} |
| coupled | 1 | 0.5 | 6 | GLM | 25 | 25 | 13 | 6 | 21 | 17 | {"0": 25} |
| coupled | 1 | 0.5 | 6 | KLMI | 25 | 25 | 19 | 10 | 21 | 23 | {"0": 25} |
| coupled | 1 | 0.5 | 6 | MVL-Ozkurt | 25 | 25 | 13 | 5 | 19 | 16 | {"0": 25} |
| coupled | 1 | 0.5 | 6 | MVL-raw | 25 | 25 | 18 | 8 | 18 | 23 | {"0": 25} |
| coupled | 1 | 0.5 | 6 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| coupled | 1.5 | 0.5 | 2 | APC-v1.0 | 25 | 2 | 1 | 1 | 1 | 1 | {"0": 2, "4": 23} |
| coupled | 1.5 | 0.5 | 2 | APC-v3.0 | 25 | 25 | 4 | 4 | 21 | 4 | {"0": 25} |
| coupled | 1.5 | 0.5 | 2 | GLM | 25 | 25 | 9 | 1 | 19 | 13 | {"0": 25} |
| coupled | 1.5 | 0.5 | 2 | KLMI | 25 | 25 | 13 | 5 | 16 | 22 | {"0": 25} |
| coupled | 1.5 | 0.5 | 2 | MVL-Ozkurt | 25 | 25 | 11 | 4 | 17 | 14 | {"0": 25} |
| coupled | 1.5 | 0.5 | 2 | MVL-raw | 25 | 25 | 15 | 5 | 16 | 22 | {"0": 25} |
| coupled | 1.5 | 0.5 | 2 | SP-raw | 25 | 25 | NA | NA | 24 | NA | {"0": 25} |
| coupled | 1.5 | 0.5 | 6 | APC-v1.0 | 25 | 3 | 0 | 0 | 2 | 0 | {"0": 3, "4": 22} |
| coupled | 1.5 | 0.5 | 6 | APC-v3.0 | 25 | 25 | 7 | 5 | 23 | 8 | {"0": 25} |
| coupled | 1.5 | 0.5 | 6 | GLM | 25 | 25 | 11 | 3 | 21 | 13 | {"0": 25} |
| coupled | 1.5 | 0.5 | 6 | KLMI | 25 | 25 | 21 | 8 | 21 | 25 | {"0": 25} |
| coupled | 1.5 | 0.5 | 6 | MVL-Ozkurt | 25 | 25 | 16 | 6 | 22 | 17 | {"0": 25} |
| coupled | 1.5 | 0.5 | 6 | MVL-raw | 25 | 25 | 22 | 9 | 22 | 25 | {"0": 25} |
| coupled | 1.5 | 0.5 | 6 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| coupled | 2 | 0.5 | 2 | APC-v1.0 | 25 | 1 | 0 | 0 | 0 | 0 | {"0": 1, "4": 24} |
| coupled | 2 | 0.5 | 2 | APC-v3.0 | 25 | 25 | 2 | 2 | 21 | 2 | {"0": 25} |
| coupled | 2 | 0.5 | 2 | GLM | 25 | 25 | 13 | 1 | 22 | 15 | {"0": 25} |
| coupled | 2 | 0.5 | 2 | KLMI | 25 | 25 | 18 | 9 | 18 | 25 | {"0": 25} |
| coupled | 2 | 0.5 | 2 | MVL-Ozkurt | 25 | 25 | 16 | 7 | 20 | 20 | {"0": 25} |
| coupled | 2 | 0.5 | 2 | MVL-raw | 25 | 25 | 18 | 8 | 21 | 22 | {"0": 25} |
| coupled | 2 | 0.5 | 2 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| coupled | 2 | 0.5 | 6 | APC-v1.0 | 25 | 3 | 0 | 0 | 2 | 1 | {"0": 3, "4": 22} |
| coupled | 2 | 0.5 | 6 | APC-v3.0 | 25 | 25 | 3 | 3 | 22 | 3 | {"0": 25} |
| coupled | 2 | 0.5 | 6 | GLM | 25 | 25 | 14 | 4 | 19 | 18 | {"0": 25} |
| coupled | 2 | 0.5 | 6 | KLMI | 25 | 25 | 19 | 5 | 19 | 25 | {"0": 25} |
| coupled | 2 | 0.5 | 6 | MVL-Ozkurt | 25 | 25 | 17 | 7 | 20 | 22 | {"0": 25} |
| coupled | 2 | 0.5 | 6 | MVL-raw | 25 | 25 | 20 | 8 | 20 | 25 | {"0": 25} |
| coupled | 2 | 0.5 | 6 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| coupled | 1 | 0.8 | 2 | APC-v1.0 | 25 | 15 | 8 | 8 | 14 | 8 | {"0": 15, "4": 10} |
| coupled | 1 | 0.8 | 2 | APC-v3.0 | 25 | 25 | 11 | 11 | 24 | 11 | {"0": 25} |
| coupled | 1 | 0.8 | 2 | GLM | 25 | 25 | 10 | 4 | 16 | 13 | {"0": 25} |
| coupled | 1 | 0.8 | 2 | KLMI | 25 | 25 | 10 | 3 | 13 | 18 | {"0": 25} |
| coupled | 1 | 0.8 | 2 | MVL-Ozkurt | 25 | 25 | 4 | 2 | 5 | 9 | {"0": 25} |
| coupled | 1 | 0.8 | 2 | MVL-raw | 25 | 25 | 5 | 3 | 6 | 20 | {"0": 25} |
| coupled | 1 | 0.8 | 2 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| coupled | 1 | 0.8 | 6 | APC-v1.0 | 25 | 22 | 12 | 12 | 22 | 12 | {"0": 22, "4": 3} |
| coupled | 1 | 0.8 | 6 | APC-v3.0 | 25 | 25 | 12 | 12 | 24 | 12 | {"0": 25} |
| coupled | 1 | 0.8 | 6 | GLM | 25 | 25 | 11 | 4 | 23 | 11 | {"0": 25} |
| coupled | 1 | 0.8 | 6 | KLMI | 25 | 25 | 20 | 10 | 23 | 21 | {"0": 25} |
| coupled | 1 | 0.8 | 6 | MVL-Ozkurt | 25 | 25 | 15 | 6 | 22 | 15 | {"0": 25} |
| coupled | 1 | 0.8 | 6 | MVL-raw | 25 | 25 | 20 | 9 | 22 | 23 | {"0": 25} |
| coupled | 1 | 0.8 | 6 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| coupled | 1.5 | 0.8 | 2 | APC-v1.0 | 25 | 5 | 2 | 2 | 5 | 2 | {"0": 5, "4": 20} |
| coupled | 1.5 | 0.8 | 2 | APC-v3.0 | 25 | 25 | 5 | 5 | 24 | 5 | {"0": 25} |
| coupled | 1.5 | 0.8 | 2 | GLM | 25 | 25 | 9 | 3 | 18 | 12 | {"0": 25} |
| coupled | 1.5 | 0.8 | 2 | KLMI | 25 | 25 | 14 | 5 | 14 | 24 | {"0": 25} |
| coupled | 1.5 | 0.8 | 2 | MVL-Ozkurt | 25 | 25 | 10 | 4 | 15 | 13 | {"0": 25} |
| coupled | 1.5 | 0.8 | 2 | MVL-raw | 25 | 25 | 15 | 6 | 17 | 21 | {"0": 25} |
| coupled | 1.5 | 0.8 | 2 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| coupled | 1.5 | 0.8 | 6 | APC-v1.0 | 25 | 15 | 9 | 9 | 15 | 9 | {"0": 15, "4": 10} |
| coupled | 1.5 | 0.8 | 6 | APC-v3.0 | 25 | 25 | 11 | 11 | 24 | 11 | {"0": 25} |
| coupled | 1.5 | 0.8 | 6 | GLM | 25 | 25 | 9 | 3 | 16 | 16 | {"0": 25} |
| coupled | 1.5 | 0.8 | 6 | KLMI | 25 | 25 | 17 | 6 | 17 | 25 | {"0": 25} |
| coupled | 1.5 | 0.8 | 6 | MVL-Ozkurt | 25 | 25 | 11 | 3 | 16 | 18 | {"0": 25} |
| coupled | 1.5 | 0.8 | 6 | MVL-raw | 25 | 25 | 16 | 4 | 16 | 25 | {"0": 25} |
| coupled | 1.5 | 0.8 | 6 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| coupled | 2 | 0.8 | 2 | APC-v1.0 | 25 | 6 | 0 | 0 | 6 | 0 | {"0": 6, "4": 19} |
| coupled | 2 | 0.8 | 2 | APC-v3.0 | 25 | 25 | 1 | 1 | 25 | 1 | {"0": 25} |
| coupled | 2 | 0.8 | 2 | GLM | 25 | 25 | 10 | 7 | 15 | 16 | {"0": 25} |
| coupled | 2 | 0.8 | 2 | KLMI | 25 | 25 | 14 | 7 | 14 | 25 | {"0": 25} |
| coupled | 2 | 0.8 | 2 | MVL-Ozkurt | 25 | 25 | 14 | 7 | 16 | 18 | {"0": 25} |
| coupled | 2 | 0.8 | 2 | MVL-raw | 25 | 25 | 17 | 8 | 17 | 23 | {"0": 25} |
| coupled | 2 | 0.8 | 2 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| coupled | 2 | 0.8 | 6 | APC-v1.0 | 25 | 17 | 5 | 5 | 16 | 5 | {"0": 17, "4": 8} |
| coupled | 2 | 0.8 | 6 | APC-v3.0 | 25 | 25 | 5 | 5 | 25 | 5 | {"0": 25} |
| coupled | 2 | 0.8 | 6 | GLM | 25 | 25 | 15 | 5 | 21 | 18 | {"0": 25} |
| coupled | 2 | 0.8 | 6 | KLMI | 25 | 25 | 22 | 11 | 22 | 25 | {"0": 25} |
| coupled | 2 | 0.8 | 6 | MVL-Ozkurt | 25 | 25 | 20 | 8 | 23 | 21 | {"0": 25} |
| coupled | 2 | 0.8 | 6 | MVL-raw | 25 | 25 | 22 | 9 | 23 | 24 | {"0": 25} |
| coupled | 2 | 0.8 | 6 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| timing_null | 1 | 0.3 | 2 | APC-v1.0 | 25 | 4 | 0 | 0 | 2 | 0 | {"0": 4, "4": 21} |
| timing_null | 1 | 0.3 | 2 | APC-v3.0 | 25 | 25 | 0 | 0 | 9 | 2 | {"0": 25} |
| timing_null | 1 | 0.3 | 2 | GLM | 25 | 25 | 1 | 1 | 2 | 3 | {"0": 25} |
| timing_null | 1 | 0.3 | 2 | KLMI | 25 | 25 | 0 | 0 | 1 | 14 | {"0": 25} |
| timing_null | 1 | 0.3 | 2 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 1 | 2 | {"0": 25} |
| timing_null | 1 | 0.3 | 2 | MVL-raw | 25 | 25 | 0 | 0 | 1 | 9 | {"0": 25} |
| timing_null | 1 | 0.3 | 2 | SP-raw | 25 | 22 | NA | NA | 19 | NA | {"0": 22, "3": 3} |
| timing_null | 1 | 0.3 | 6 | APC-v1.0 | 25 | 3 | 0 | 0 | 1 | 0 | {"0": 3, "4": 22} |
| timing_null | 1 | 0.3 | 6 | APC-v3.0 | 25 | 25 | 2 | 2 | 15 | 5 | {"0": 25} |
| timing_null | 1 | 0.3 | 6 | GLM | 25 | 25 | 0 | 0 | 0 | 0 | {"0": 25} |
| timing_null | 1 | 0.3 | 6 | KLMI | 25 | 25 | 0 | 0 | 0 | 18 | {"0": 25} |
| timing_null | 1 | 0.3 | 6 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 0 | {"0": 25} |
| timing_null | 1 | 0.3 | 6 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 17 | {"0": 25} |
| timing_null | 1 | 0.3 | 6 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| timing_null | 1.5 | 0.3 | 2 | APC-v1.0 | 25 | 0 | 0 | 0 | 0 | 0 | {"4": 25} |
| timing_null | 1.5 | 0.3 | 2 | APC-v3.0 | 25 | 25 | 1 | 1 | 16 | 3 | {"0": 25} |
| timing_null | 1.5 | 0.3 | 2 | GLM | 25 | 25 | 0 | 0 | 2 | 1 | {"0": 25} |
| timing_null | 1.5 | 0.3 | 2 | KLMI | 25 | 25 | 0 | 0 | 0 | 18 | {"0": 25} |
| timing_null | 1.5 | 0.3 | 2 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 2 | 3 | {"0": 25} |
| timing_null | 1.5 | 0.3 | 2 | MVL-raw | 25 | 25 | 1 | 0 | 2 | 12 | {"0": 25} |
| timing_null | 1.5 | 0.3 | 2 | SP-raw | 25 | 24 | NA | NA | 22 | NA | {"0": 24, "3": 1} |
| timing_null | 1.5 | 0.3 | 6 | APC-v1.0 | 25 | 0 | 0 | 0 | 0 | 0 | {"4": 25} |
| timing_null | 1.5 | 0.3 | 6 | APC-v3.0 | 25 | 25 | 1 | 1 | 14 | 1 | {"0": 25} |
| timing_null | 1.5 | 0.3 | 6 | GLM | 25 | 25 | 1 | 0 | 3 | 5 | {"0": 25} |
| timing_null | 1.5 | 0.3 | 6 | KLMI | 25 | 25 | 0 | 0 | 0 | 23 | {"0": 25} |
| timing_null | 1.5 | 0.3 | 6 | MVL-Ozkurt | 25 | 25 | 1 | 0 | 1 | 8 | {"0": 25} |
| timing_null | 1.5 | 0.3 | 6 | MVL-raw | 25 | 25 | 1 | 0 | 1 | 13 | {"0": 25} |
| timing_null | 1.5 | 0.3 | 6 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| timing_null | 2 | 0.3 | 2 | APC-v1.0 | 25 | 0 | 0 | 0 | 0 | 0 | {"4": 25} |
| timing_null | 2 | 0.3 | 2 | APC-v3.0 | 25 | 25 | 0 | 0 | 18 | 1 | {"0": 25} |
| timing_null | 2 | 0.3 | 2 | GLM | 25 | 25 | 0 | 0 | 0 | 0 | {"0": 25} |
| timing_null | 2 | 0.3 | 2 | KLMI | 25 | 25 | 0 | 0 | 0 | 24 | {"0": 25} |
| timing_null | 2 | 0.3 | 2 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 1 | {"0": 25} |
| timing_null | 2 | 0.3 | 2 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 7 | {"0": 25} |
| timing_null | 2 | 0.3 | 2 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| timing_null | 2 | 0.3 | 6 | APC-v1.0 | 25 | 0 | 0 | 0 | 0 | 0 | {"4": 25} |
| timing_null | 2 | 0.3 | 6 | APC-v3.0 | 25 | 25 | 2 | 2 | 20 | 3 | {"0": 25} |
| timing_null | 2 | 0.3 | 6 | GLM | 25 | 25 | 0 | 0 | 0 | 2 | {"0": 25} |
| timing_null | 2 | 0.3 | 6 | KLMI | 25 | 25 | 0 | 0 | 0 | 25 | {"0": 25} |
| timing_null | 2 | 0.3 | 6 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 2 | {"0": 25} |
| timing_null | 2 | 0.3 | 6 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 9 | {"0": 25} |
| timing_null | 2 | 0.3 | 6 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| timing_null | 1 | 0.5 | 2 | APC-v1.0 | 25 | 2 | 0 | 0 | 2 | 0 | {"0": 2, "4": 23} |
| timing_null | 1 | 0.5 | 2 | APC-v3.0 | 25 | 25 | 3 | 2 | 18 | 4 | {"0": 25} |
| timing_null | 1 | 0.5 | 2 | GLM | 25 | 25 | 0 | 0 | 2 | 0 | {"0": 25} |
| timing_null | 1 | 0.5 | 2 | KLMI | 25 | 25 | 0 | 0 | 0 | 11 | {"0": 25} |
| timing_null | 1 | 0.5 | 2 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 1 | {"0": 25} |
| timing_null | 1 | 0.5 | 2 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 10 | {"0": 25} |
| timing_null | 1 | 0.5 | 2 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| timing_null | 1 | 0.5 | 6 | APC-v1.0 | 25 | 7 | 1 | 1 | 5 | 1 | {"0": 7, "4": 18} |
| timing_null | 1 | 0.5 | 6 | APC-v3.0 | 25 | 25 | 3 | 3 | 21 | 3 | {"0": 25} |
| timing_null | 1 | 0.5 | 6 | GLM | 25 | 25 | 1 | 0 | 1 | 2 | {"0": 25} |
| timing_null | 1 | 0.5 | 6 | KLMI | 25 | 25 | 2 | 0 | 2 | 16 | {"0": 25} |
| timing_null | 1 | 0.5 | 6 | MVL-Ozkurt | 25 | 25 | 1 | 0 | 1 | 4 | {"0": 25} |
| timing_null | 1 | 0.5 | 6 | MVL-raw | 25 | 25 | 1 | 0 | 1 | 10 | {"0": 25} |
| timing_null | 1 | 0.5 | 6 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| timing_null | 1.5 | 0.5 | 2 | APC-v1.0 | 25 | 4 | 0 | 0 | 2 | 0 | {"0": 4, "4": 21} |
| timing_null | 1.5 | 0.5 | 2 | APC-v3.0 | 25 | 25 | 2 | 2 | 18 | 2 | {"0": 25} |
| timing_null | 1.5 | 0.5 | 2 | GLM | 25 | 25 | 0 | 0 | 0 | 1 | {"0": 25} |
| timing_null | 1.5 | 0.5 | 2 | KLMI | 25 | 25 | 0 | 0 | 0 | 19 | {"0": 25} |
| timing_null | 1.5 | 0.5 | 2 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 1 | {"0": 25} |
| timing_null | 1.5 | 0.5 | 2 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 12 | {"0": 25} |
| timing_null | 1.5 | 0.5 | 2 | SP-raw | 25 | 25 | NA | NA | 24 | NA | {"0": 25} |
| timing_null | 1.5 | 0.5 | 6 | APC-v1.0 | 25 | 8 | 0 | 0 | 6 | 0 | {"0": 8, "4": 17} |
| timing_null | 1.5 | 0.5 | 6 | APC-v3.0 | 25 | 25 | 2 | 1 | 23 | 2 | {"0": 25} |
| timing_null | 1.5 | 0.5 | 6 | GLM | 25 | 25 | 0 | 0 | 0 | 1 | {"0": 25} |
| timing_null | 1.5 | 0.5 | 6 | KLMI | 25 | 25 | 0 | 0 | 0 | 20 | {"0": 25} |
| timing_null | 1.5 | 0.5 | 6 | MVL-Ozkurt | 25 | 25 | 1 | 0 | 1 | 2 | {"0": 25} |
| timing_null | 1.5 | 0.5 | 6 | MVL-raw | 25 | 25 | 1 | 0 | 1 | 19 | {"0": 25} |
| timing_null | 1.5 | 0.5 | 6 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| timing_null | 2 | 0.5 | 2 | APC-v1.0 | 25 | 1 | 0 | 0 | 1 | 0 | {"0": 1, "2": 1, "4": 23} |
| timing_null | 2 | 0.5 | 2 | APC-v3.0 | 25 | 24 | 0 | 0 | 17 | 0 | {"0": 24, "2": 1} |
| timing_null | 2 | 0.5 | 2 | GLM | 25 | 25 | 0 | 0 | 0 | 0 | {"0": 25} |
| timing_null | 2 | 0.5 | 2 | KLMI | 25 | 25 | 0 | 0 | 0 | 24 | {"0": 25} |
| timing_null | 2 | 0.5 | 2 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 1 | {"0": 25} |
| timing_null | 2 | 0.5 | 2 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 9 | {"0": 25} |
| timing_null | 2 | 0.5 | 2 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| timing_null | 2 | 0.5 | 6 | APC-v1.0 | 25 | 2 | 0 | 0 | 1 | 0 | {"0": 2, "4": 23} |
| timing_null | 2 | 0.5 | 6 | APC-v3.0 | 25 | 25 | 3 | 3 | 21 | 3 | {"0": 25} |
| timing_null | 2 | 0.5 | 6 | GLM | 25 | 25 | 0 | 0 | 0 | 2 | {"0": 25} |
| timing_null | 2 | 0.5 | 6 | KLMI | 25 | 25 | 0 | 0 | 0 | 25 | {"0": 25} |
| timing_null | 2 | 0.5 | 6 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 2 | {"0": 25} |
| timing_null | 2 | 0.5 | 6 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 11 | {"0": 25} |
| timing_null | 2 | 0.5 | 6 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| timing_null | 1 | 0.8 | 2 | APC-v1.0 | 25 | 12 | 2 | 2 | 12 | 2 | {"0": 12, "4": 13} |
| timing_null | 1 | 0.8 | 2 | APC-v3.0 | 25 | 25 | 3 | 3 | 23 | 4 | {"0": 25} |
| timing_null | 1 | 0.8 | 2 | GLM | 25 | 25 | 0 | 0 | 0 | 1 | {"0": 25} |
| timing_null | 1 | 0.8 | 2 | KLMI | 25 | 25 | 0 | 0 | 0 | 11 | {"0": 25} |
| timing_null | 1 | 0.8 | 2 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 2 | {"0": 25} |
| timing_null | 1 | 0.8 | 2 | MVL-raw | 25 | 25 | 1 | 1 | 1 | 13 | {"0": 25} |
| timing_null | 1 | 0.8 | 2 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| timing_null | 1 | 0.8 | 6 | APC-v1.0 | 25 | 18 | 1 | 1 | 18 | 1 | {"0": 18, "4": 7} |
| timing_null | 1 | 0.8 | 6 | APC-v3.0 | 25 | 25 | 3 | 3 | 24 | 3 | {"0": 25} |
| timing_null | 1 | 0.8 | 6 | GLM | 25 | 25 | 0 | 0 | 0 | 7 | {"0": 25} |
| timing_null | 1 | 0.8 | 6 | KLMI | 25 | 25 | 0 | 0 | 0 | 18 | {"0": 25} |
| timing_null | 1 | 0.8 | 6 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 3 | {"0": 25} |
| timing_null | 1 | 0.8 | 6 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 11 | {"0": 25} |
| timing_null | 1 | 0.8 | 6 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| timing_null | 1.5 | 0.8 | 2 | APC-v1.0 | 25 | 0 | 0 | 0 | 0 | 0 | {"4": 25} |
| timing_null | 1.5 | 0.8 | 2 | APC-v3.0 | 25 | 25 | 3 | 3 | 18 | 4 | {"0": 25} |
| timing_null | 1.5 | 0.8 | 2 | GLM | 25 | 25 | 0 | 0 | 0 | 2 | {"0": 25} |
| timing_null | 1.5 | 0.8 | 2 | KLMI | 25 | 25 | 0 | 0 | 0 | 16 | {"0": 25} |
| timing_null | 1.5 | 0.8 | 2 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 0 | {"0": 25} |
| timing_null | 1.5 | 0.8 | 2 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 14 | {"0": 25} |
| timing_null | 1.5 | 0.8 | 2 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| timing_null | 1.5 | 0.8 | 6 | APC-v1.0 | 25 | 13 | 3 | 3 | 13 | 3 | {"0": 13, "4": 12} |
| timing_null | 1.5 | 0.8 | 6 | APC-v3.0 | 25 | 25 | 4 | 4 | 25 | 4 | {"0": 25} |
| timing_null | 1.5 | 0.8 | 6 | GLM | 25 | 25 | 0 | 0 | 0 | 2 | {"0": 25} |
| timing_null | 1.5 | 0.8 | 6 | KLMI | 25 | 25 | 0 | 0 | 0 | 23 | {"0": 25} |
| timing_null | 1.5 | 0.8 | 6 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 2 | {"0": 25} |
| timing_null | 1.5 | 0.8 | 6 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 15 | {"0": 25} |
| timing_null | 1.5 | 0.8 | 6 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| timing_null | 2 | 0.8 | 2 | APC-v1.0 | 25 | 3 | 0 | 0 | 3 | 0 | {"0": 3, "4": 22} |
| timing_null | 2 | 0.8 | 2 | APC-v3.0 | 25 | 25 | 1 | 1 | 24 | 1 | {"0": 25} |
| timing_null | 2 | 0.8 | 2 | GLM | 25 | 25 | 0 | 0 | 0 | 0 | {"0": 25} |
| timing_null | 2 | 0.8 | 2 | KLMI | 25 | 25 | 0 | 0 | 0 | 23 | {"0": 25} |
| timing_null | 2 | 0.8 | 2 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 0 | {"0": 25} |
| timing_null | 2 | 0.8 | 2 | MVL-raw | 25 | 25 | 1 | 0 | 1 | 13 | {"0": 25} |
| timing_null | 2 | 0.8 | 2 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| timing_null | 2 | 0.8 | 6 | APC-v1.0 | 25 | 13 | 2 | 2 | 11 | 2 | {"0": 13, "4": 12} |
| timing_null | 2 | 0.8 | 6 | APC-v3.0 | 25 | 25 | 2 | 2 | 22 | 2 | {"0": 25} |
| timing_null | 2 | 0.8 | 6 | GLM | 25 | 25 | 0 | 0 | 0 | 0 | {"0": 25} |
| timing_null | 2 | 0.8 | 6 | KLMI | 25 | 25 | 0 | 0 | 0 | 25 | {"0": 25} |
| timing_null | 2 | 0.8 | 6 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 2 | {"0": 25} |
| timing_null | 2 | 0.8 | 6 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 9 | {"0": 25} |
| timing_null | 2 | 0.8 | 6 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |

## HB recovery by level


| scenario | dataset | level | method | n | valid | joint | strict_joint | fp | fa | status_counts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H1_distractor | coupled | 0 | APC-v1.0 | 25 | 24 | 20 | 20 | 24 | 20 | {"0": 24, "4": 1} |
| H1_distractor | coupled | 0 | APC-v3.0 | 25 | 25 | 20 | 20 | 25 | 20 | {"0": 25} |
| H1_distractor | coupled | 0 | GLM | 25 | 25 | 15 | 8 | 15 | 25 | {"0": 25} |
| H1_distractor | coupled | 0 | KLMI | 25 | 25 | 14 | 7 | 14 | 18 | {"0": 25} |
| H1_distractor | coupled | 0 | MVL-Ozkurt | 25 | 25 | 18 | 11 | 18 | 20 | {"0": 25} |
| H1_distractor | coupled | 0 | MVL-raw | 25 | 25 | 20 | 11 | 20 | 24 | {"0": 25} |
| H1_distractor | coupled | 0 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H1_distractor | coupled | 1.5 | APC-v1.0 | 25 | 22 | 21 | 21 | 22 | 21 | {"0": 22, "4": 3} |
| H1_distractor | coupled | 1.5 | APC-v3.0 | 25 | 25 | 23 | 23 | 25 | 23 | {"0": 25} |
| H1_distractor | coupled | 1.5 | GLM | 25 | 25 | 16 | 4 | 16 | 25 | {"0": 25} |
| H1_distractor | coupled | 1.5 | KLMI | 25 | 25 | 15 | 5 | 15 | 23 | {"0": 25} |
| H1_distractor | coupled | 1.5 | MVL-Ozkurt | 25 | 25 | 17 | 8 | 17 | 22 | {"0": 25} |
| H1_distractor | coupled | 1.5 | MVL-raw | 25 | 25 | 18 | 9 | 18 | 25 | {"0": 25} |
| H1_distractor | coupled | 1.5 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H1_distractor | coupled | 3 | APC-v1.0 | 25 | 24 | 20 | 20 | 23 | 20 | {"0": 24, "4": 1} |
| H1_distractor | coupled | 3 | APC-v3.0 | 25 | 25 | 22 | 22 | 25 | 22 | {"0": 25} |
| H1_distractor | coupled | 3 | GLM | 25 | 25 | 17 | 5 | 17 | 24 | {"0": 25} |
| H1_distractor | coupled | 3 | KLMI | 25 | 25 | 15 | 3 | 15 | 22 | {"0": 25} |
| H1_distractor | coupled | 3 | MVL-Ozkurt | 25 | 25 | 19 | 9 | 19 | 24 | {"0": 25} |
| H1_distractor | coupled | 3 | MVL-raw | 25 | 25 | 17 | 8 | 17 | 23 | {"0": 25} |
| H1_distractor | coupled | 3 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H1_distractor | no_coupled_burst | 3 | APC-v1.0 | 25 | 24 | 8 | 8 | 24 | 8 | {"0": 24, "4": 1} |
| H1_distractor | no_coupled_burst | 3 | APC-v3.0 | 25 | 25 | 9 | 9 | 25 | 9 | {"0": 25} |
| H1_distractor | no_coupled_burst | 3 | GLM | 25 | 25 | 0 | 0 | 2 | 6 | {"0": 25} |
| H1_distractor | no_coupled_burst | 3 | KLMI | 25 | 25 | 0 | 0 | 0 | 1 | {"0": 25} |
| H1_distractor | no_coupled_burst | 3 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 1 | 4 | {"0": 25} |
| H1_distractor | no_coupled_burst | 3 | MVL-raw | 25 | 25 | 0 | 0 | 3 | 0 | {"0": 25} |
| H1_distractor | no_coupled_burst | 3 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H1_distractor | timing_null | 0 | APC-v1.0 | 25 | 25 | 7 | 7 | 25 | 7 | {"0": 25} |
| H1_distractor | timing_null | 0 | APC-v3.0 | 25 | 25 | 7 | 7 | 25 | 7 | {"0": 25} |
| H1_distractor | timing_null | 0 | GLM | 25 | 25 | 0 | 0 | 2 | 5 | {"0": 25} |
| H1_distractor | timing_null | 0 | KLMI | 25 | 25 | 0 | 0 | 0 | 8 | {"0": 25} |
| H1_distractor | timing_null | 0 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 5 | {"0": 25} |
| H1_distractor | timing_null | 0 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 15 | {"0": 25} |
| H1_distractor | timing_null | 0 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H1_distractor | timing_null | 1.5 | APC-v1.0 | 25 | 25 | 4 | 4 | 25 | 4 | {"0": 25} |
| H1_distractor | timing_null | 1.5 | APC-v3.0 | 25 | 25 | 4 | 4 | 25 | 4 | {"0": 25} |
| H1_distractor | timing_null | 1.5 | GLM | 25 | 25 | 0 | 0 | 0 | 3 | {"0": 25} |
| H1_distractor | timing_null | 1.5 | KLMI | 25 | 25 | 0 | 0 | 0 | 6 | {"0": 25} |
| H1_distractor | timing_null | 1.5 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 3 | {"0": 25} |
| H1_distractor | timing_null | 1.5 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 6 | {"0": 25} |
| H1_distractor | timing_null | 1.5 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H1_distractor | timing_null | 3 | APC-v1.0 | 25 | 23 | 4 | 4 | 23 | 4 | {"0": 23, "4": 2} |
| H1_distractor | timing_null | 3 | APC-v3.0 | 25 | 25 | 6 | 6 | 25 | 6 | {"0": 25} |
| H1_distractor | timing_null | 3 | GLM | 25 | 25 | 2 | 2 | 4 | 6 | {"0": 25} |
| H1_distractor | timing_null | 3 | KLMI | 25 | 25 | 0 | 0 | 0 | 3 | {"0": 25} |
| H1_distractor | timing_null | 3 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 1 | 7 | {"0": 25} |
| H1_distractor | timing_null | 3 | MVL-raw | 25 | 25 | 0 | 0 | 3 | 0 | {"0": 25} |
| H1_distractor | timing_null | 3 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H1_sparsity | coupled | 0.15 | APC-v1.0 | 25 | 25 | 8 | 8 | 25 | 8 | {"0": 25} |
| H1_sparsity | coupled | 0.15 | APC-v3.0 | 25 | 25 | 8 | 8 | 25 | 8 | {"0": 25} |
| H1_sparsity | coupled | 0.15 | GLM | 25 | 25 | 1 | 1 | 1 | 10 | {"0": 25} |
| H1_sparsity | coupled | 0.15 | KLMI | 25 | 25 | 0 | 0 | 0 | 18 | {"0": 25} |
| H1_sparsity | coupled | 0.15 | MVL-Ozkurt | 25 | 25 | 3 | 1 | 3 | 11 | {"0": 25} |
| H1_sparsity | coupled | 0.15 | MVL-raw | 25 | 25 | 3 | 1 | 3 | 19 | {"0": 25} |
| H1_sparsity | coupled | 0.15 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H1_sparsity | coupled | 0.25 | APC-v1.0 | 25 | 25 | 9 | 9 | 25 | 9 | {"0": 25} |
| H1_sparsity | coupled | 0.25 | APC-v3.0 | 25 | 25 | 9 | 9 | 25 | 9 | {"0": 25} |
| H1_sparsity | coupled | 0.25 | GLM | 25 | 25 | 7 | 4 | 8 | 14 | {"0": 25} |
| H1_sparsity | coupled | 0.25 | KLMI | 25 | 25 | 7 | 3 | 7 | 19 | {"0": 25} |
| H1_sparsity | coupled | 0.25 | MVL-Ozkurt | 25 | 25 | 7 | 3 | 7 | 15 | {"0": 25} |
| H1_sparsity | coupled | 0.25 | MVL-raw | 25 | 25 | 9 | 3 | 9 | 22 | {"0": 25} |
| H1_sparsity | coupled | 0.25 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H1_sparsity | coupled | 0.55 | APC-v1.0 | 25 | 25 | 21 | 21 | 25 | 21 | {"0": 25} |
| H1_sparsity | coupled | 0.55 | APC-v3.0 | 25 | 25 | 21 | 21 | 25 | 21 | {"0": 25} |
| H1_sparsity | coupled | 0.55 | GLM | 25 | 25 | 15 | 4 | 15 | 23 | {"0": 25} |
| H1_sparsity | coupled | 0.55 | KLMI | 25 | 25 | 11 | 4 | 11 | 21 | {"0": 25} |
| H1_sparsity | coupled | 0.55 | MVL-Ozkurt | 25 | 25 | 16 | 6 | 16 | 19 | {"0": 25} |
| H1_sparsity | coupled | 0.55 | MVL-raw | 25 | 25 | 17 | 7 | 17 | 24 | {"0": 25} |
| H1_sparsity | coupled | 0.55 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H1_sparsity | coupled | 1 | APC-v1.0 | 25 | 25 | 21 | 21 | 25 | 21 | {"0": 25} |
| H1_sparsity | coupled | 1 | APC-v3.0 | 25 | 25 | 21 | 21 | 25 | 21 | {"0": 25} |
| H1_sparsity | coupled | 1 | GLM | 25 | 25 | 13 | 3 | 13 | 24 | {"0": 25} |
| H1_sparsity | coupled | 1 | KLMI | 25 | 25 | 13 | 4 | 13 | 21 | {"0": 25} |
| H1_sparsity | coupled | 1 | MVL-Ozkurt | 25 | 25 | 16 | 7 | 17 | 21 | {"0": 25} |
| H1_sparsity | coupled | 1 | MVL-raw | 25 | 25 | 18 | 9 | 18 | 25 | {"0": 25} |
| H1_sparsity | coupled | 1 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H1_sparsity | no_coupled_burst | 0.15 | APC-v1.0 | 25 | 25 | 1 | 1 | 25 | 1 | {"0": 25} |
| H1_sparsity | no_coupled_burst | 0.15 | APC-v3.0 | 25 | 25 | 1 | 1 | 25 | 1 | {"0": 25} |
| H1_sparsity | no_coupled_burst | 0.15 | GLM | 25 | 25 | 0 | 0 | 1 | 7 | {"0": 25} |
| H1_sparsity | no_coupled_burst | 0.15 | KLMI | 25 | 25 | 0 | 0 | 0 | 8 | {"0": 25} |
| H1_sparsity | no_coupled_burst | 0.15 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 9 | {"0": 25} |
| H1_sparsity | no_coupled_burst | 0.15 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 13 | {"0": 25} |
| H1_sparsity | no_coupled_burst | 0.15 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H1_sparsity | no_coupled_burst | 1 | APC-v1.0 | 25 | 25 | 2 | 2 | 25 | 2 | {"0": 25} |
| H1_sparsity | no_coupled_burst | 1 | APC-v3.0 | 25 | 25 | 2 | 2 | 25 | 2 | {"0": 25} |
| H1_sparsity | no_coupled_burst | 1 | GLM | 25 | 25 | 0 | 0 | 0 | 3 | {"0": 25} |
| H1_sparsity | no_coupled_burst | 1 | KLMI | 25 | 25 | 0 | 0 | 0 | 2 | {"0": 25} |
| H1_sparsity | no_coupled_burst | 1 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 3 | {"0": 25} |
| H1_sparsity | no_coupled_burst | 1 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 6 | {"0": 25} |
| H1_sparsity | no_coupled_burst | 1 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H1_sparsity | timing_null | 0.15 | APC-v1.0 | 25 | 25 | 2 | 2 | 25 | 2 | {"0": 25} |
| H1_sparsity | timing_null | 0.15 | APC-v3.0 | 25 | 25 | 2 | 2 | 25 | 2 | {"0": 25} |
| H1_sparsity | timing_null | 0.15 | GLM | 25 | 25 | 0 | 0 | 1 | 6 | {"0": 25} |
| H1_sparsity | timing_null | 0.15 | KLMI | 25 | 25 | 0 | 0 | 0 | 13 | {"0": 25} |
| H1_sparsity | timing_null | 0.15 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 6 | {"0": 25} |
| H1_sparsity | timing_null | 0.15 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 10 | {"0": 25} |
| H1_sparsity | timing_null | 0.15 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H1_sparsity | timing_null | 0.25 | APC-v1.0 | 25 | 25 | 5 | 5 | 25 | 5 | {"0": 25} |
| H1_sparsity | timing_null | 0.25 | APC-v3.0 | 25 | 25 | 5 | 5 | 25 | 5 | {"0": 25} |
| H1_sparsity | timing_null | 0.25 | GLM | 25 | 25 | 0 | 0 | 1 | 9 | {"0": 25} |
| H1_sparsity | timing_null | 0.25 | KLMI | 25 | 25 | 0 | 0 | 0 | 15 | {"0": 25} |
| H1_sparsity | timing_null | 0.25 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 7 | {"0": 25} |
| H1_sparsity | timing_null | 0.25 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 17 | {"0": 25} |
| H1_sparsity | timing_null | 0.25 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H1_sparsity | timing_null | 0.55 | APC-v1.0 | 25 | 25 | 6 | 6 | 25 | 6 | {"0": 25} |
| H1_sparsity | timing_null | 0.55 | APC-v3.0 | 25 | 25 | 6 | 6 | 25 | 6 | {"0": 25} |
| H1_sparsity | timing_null | 0.55 | GLM | 25 | 25 | 1 | 0 | 1 | 7 | {"0": 25} |
| H1_sparsity | timing_null | 0.55 | KLMI | 25 | 25 | 0 | 0 | 0 | 4 | {"0": 25} |
| H1_sparsity | timing_null | 0.55 | MVL-Ozkurt | 25 | 25 | 1 | 0 | 1 | 6 | {"0": 25} |
| H1_sparsity | timing_null | 0.55 | MVL-raw | 25 | 25 | 1 | 0 | 1 | 17 | {"0": 25} |
| H1_sparsity | timing_null | 0.55 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H1_sparsity | timing_null | 1 | APC-v1.0 | 25 | 25 | 5 | 5 | 25 | 5 | {"0": 25} |
| H1_sparsity | timing_null | 1 | APC-v3.0 | 25 | 25 | 5 | 5 | 25 | 5 | {"0": 25} |
| H1_sparsity | timing_null | 1 | GLM | 25 | 25 | 1 | 1 | 1 | 5 | {"0": 25} |
| H1_sparsity | timing_null | 1 | KLMI | 25 | 25 | 0 | 0 | 0 | 4 | {"0": 25} |
| H1_sparsity | timing_null | 1 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 0 | 5 | {"0": 25} |
| H1_sparsity | timing_null | 1 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 15 | {"0": 25} |
| H1_sparsity | timing_null | 1 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H2 | coupled | 0 | APC-v1.0 | 25 | 25 | 25 | 25 | 25 | 25 | {"0": 25} |
| H2 | coupled | 0 | APC-v3.0 | 25 | 25 | 25 | 25 | 25 | 25 | {"0": 25} |
| H2 | coupled | 0 | GLM | 25 | 25 | 21 | 5 | 21 | 25 | {"0": 25} |
| H2 | coupled | 0 | KLMI | 25 | 25 | 20 | 7 | 20 | 25 | {"0": 25} |
| H2 | coupled | 0 | MVL-Ozkurt | 25 | 25 | 14 | 4 | 14 | 25 | {"0": 25} |
| H2 | coupled | 0 | MVL-raw | 25 | 25 | 14 | 5 | 14 | 25 | {"0": 25} |
| H2 | coupled | 0 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H2 | coupled | 0.5 | APC-v1.0 | 25 | 25 | 24 | 24 | 25 | 24 | {"0": 25} |
| H2 | coupled | 0.5 | APC-v3.0 | 25 | 25 | 24 | 24 | 25 | 24 | {"0": 25} |
| H2 | coupled | 0.5 | GLM | 25 | 25 | 23 | 8 | 23 | 25 | {"0": 25} |
| H2 | coupled | 0.5 | KLMI | 25 | 25 | 21 | 8 | 21 | 25 | {"0": 25} |
| H2 | coupled | 0.5 | MVL-Ozkurt | 25 | 25 | 20 | 7 | 20 | 24 | {"0": 25} |
| H2 | coupled | 0.5 | MVL-raw | 25 | 25 | 21 | 8 | 21 | 25 | {"0": 25} |
| H2 | coupled | 0.5 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H2 | coupled | 1 | APC-v1.0 | 25 | 24 | 13 | 11 | 13 | 17 | {"0": 24, "4": 1} |
| H2 | coupled | 1 | APC-v3.0 | 25 | 25 | 10 | 8 | 10 | 15 | {"0": 25} |
| H2 | coupled | 1 | GLM | 25 | 25 | 17 | 8 | 17 | 25 | {"0": 25} |
| H2 | coupled | 1 | KLMI | 25 | 25 | 18 | 8 | 18 | 25 | {"0": 25} |
| H2 | coupled | 1 | MVL-Ozkurt | 25 | 25 | 15 | 3 | 15 | 23 | {"0": 25} |
| H2 | coupled | 1 | MVL-raw | 25 | 25 | 16 | 4 | 16 | 24 | {"0": 25} |
| H2 | coupled | 1 | SP-raw | 25 | 25 | NA | NA | 0 | NA | {"0": 25} |
| H2 | coupled | 1.5 | APC-v1.0 | 25 | 24 | 1 | 1 | 1 | 7 | {"0": 24, "4": 1} |
| H2 | coupled | 1.5 | APC-v3.0 | 25 | 25 | 1 | 1 | 1 | 7 | {"0": 25} |
| H2 | coupled | 1.5 | GLM | 25 | 25 | 18 | 11 | 18 | 25 | {"0": 25} |
| H2 | coupled | 1.5 | KLMI | 25 | 25 | 16 | 9 | 16 | 24 | {"0": 25} |
| H2 | coupled | 1.5 | MVL-Ozkurt | 25 | 25 | 16 | 9 | 16 | 22 | {"0": 25} |
| H2 | coupled | 1.5 | MVL-raw | 25 | 25 | 16 | 9 | 17 | 24 | {"0": 25} |
| H2 | coupled | 1.5 | SP-raw | 25 | 25 | NA | NA | 0 | NA | {"0": 25} |
| H2 | coupled | 2 | APC-v1.0 | 25 | 25 | 0 | 0 | 0 | 5 | {"0": 25} |
| H2 | coupled | 2 | APC-v3.0 | 25 | 25 | 0 | 0 | 0 | 5 | {"0": 25} |
| H2 | coupled | 2 | GLM | 25 | 25 | 13 | 4 | 16 | 18 | {"0": 25} |
| H2 | coupled | 2 | KLMI | 25 | 25 | 12 | 6 | 13 | 18 | {"0": 25} |
| H2 | coupled | 2 | MVL-Ozkurt | 25 | 25 | 7 | 0 | 9 | 11 | {"0": 25} |
| H2 | coupled | 2 | MVL-raw | 25 | 25 | 9 | 1 | 10 | 17 | {"0": 25} |
| H2 | coupled | 2 | SP-raw | 25 | 25 | NA | NA | 0 | NA | {"0": 25} |
| H2 | coupled | 3 | APC-v1.0 | 25 | 25 | 0 | 0 | 0 | 4 | {"0": 25} |
| H2 | coupled | 3 | APC-v3.0 | 25 | 25 | 0 | 0 | 0 | 4 | {"0": 25} |
| H2 | coupled | 3 | GLM | 25 | 25 | 4 | 3 | 8 | 8 | {"0": 25} |
| H2 | coupled | 3 | KLMI | 25 | 25 | 4 | 0 | 6 | 6 | {"0": 25} |
| H2 | coupled | 3 | MVL-Ozkurt | 25 | 25 | 1 | 1 | 4 | 4 | {"0": 25} |
| H2 | coupled | 3 | MVL-raw | 25 | 25 | 2 | 1 | 4 | 8 | {"0": 25} |
| H2 | coupled | 3 | SP-raw | 25 | 25 | NA | NA | 0 | NA | {"0": 25} |
| H2 | timing_null | 0 | APC-v1.0 | 25 | 25 | 2 | 2 | 25 | 2 | {"0": 25} |
| H2 | timing_null | 0 | APC-v3.0 | 25 | 25 | 2 | 2 | 25 | 2 | {"0": 25} |
| H2 | timing_null | 0 | GLM | 25 | 25 | 1 | 0 | 7 | 4 | {"0": 25} |
| H2 | timing_null | 0 | KLMI | 25 | 25 | 1 | 0 | 4 | 5 | {"0": 25} |
| H2 | timing_null | 0 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 2 | 4 | {"0": 25} |
| H2 | timing_null | 0 | MVL-raw | 25 | 25 | 0 | 0 | 0 | 11 | {"0": 25} |
| H2 | timing_null | 0 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |
| H2 | timing_null | 1 | APC-v1.0 | 25 | 25 | 1 | 1 | 14 | 4 | {"0": 25} |
| H2 | timing_null | 1 | APC-v3.0 | 25 | 25 | 0 | 0 | 6 | 4 | {"0": 25} |
| H2 | timing_null | 1 | GLM | 25 | 25 | 0 | 0 | 5 | 2 | {"0": 25} |
| H2 | timing_null | 1 | KLMI | 25 | 25 | 0 | 0 | 2 | 4 | {"0": 25} |
| H2 | timing_null | 1 | MVL-Ozkurt | 25 | 25 | 0 | 0 | 2 | 4 | {"0": 25} |
| H2 | timing_null | 1 | MVL-raw | 25 | 25 | 0 | 0 | 2 | 6 | {"0": 25} |
| H2 | timing_null | 1 | SP-raw | 25 | 25 | NA | NA | 0 | NA | {"0": 25} |
| H2 | timing_null | 3 | APC-v1.0 | 25 | 25 | 0 | 0 | 0 | 5 | {"0": 25} |
| H2 | timing_null | 3 | APC-v3.0 | 25 | 25 | 0 | 0 | 0 | 5 | {"0": 25} |
| H2 | timing_null | 3 | GLM | 25 | 25 | 2 | 0 | 6 | 3 | {"0": 25} |
| H2 | timing_null | 3 | KLMI | 25 | 25 | 2 | 0 | 6 | 3 | {"0": 25} |
| H2 | timing_null | 3 | MVL-Ozkurt | 25 | 25 | 1 | 0 | 4 | 2 | {"0": 25} |
| H2 | timing_null | 3 | MVL-raw | 25 | 25 | 1 | 0 | 3 | 2 | {"0": 25} |
| H2 | timing_null | 3 | SP-raw | 25 | 25 | NA | NA | 0 | NA | {"0": 25} |
| H4 | coupled | 0 | APC-v1.0 | 25 | 25 | 22 | 22 | 25 | 22 | {"0": 25} |
| H4 | coupled | 0 | APC-v3.0 | 25 | 25 | 22 | 22 | 25 | 22 | {"0": 25} |
| H4 | coupled | 0 | GLM | 25 | 25 | 24 | 9 | 24 | 25 | {"0": 25} |
| H4 | coupled | 0 | KLMI | 25 | 25 | 24 | 9 | 24 | 25 | {"0": 25} |
| H4 | coupled | 0 | MVL-Ozkurt | 25 | 25 | 23 | 6 | 23 | 25 | {"0": 25} |
| H4 | coupled | 0 | MVL-raw | 25 | 25 | 23 | 6 | 23 | 25 | {"0": 25} |
| H4 | coupled | 0 | SP-raw | 25 | 25 | NA | NA | 25 | NA | {"0": 25} |

All per-trial estimates/options/generator settings/provenance: [heldout_trial_estimates.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/heldout_trial_estimates.csv>). Full cell statistics, errors and Wilson intervals: [recovery_by_cell.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/recovery_by_cell.csv>). Complete checkpoint MAT files preserve estimator output/diagnostics; no estimator was called during reporting.

## Figures

- [HA_joint_recovery.png](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/HA_joint_recovery.png>) (300 dpi); [HA_joint_recovery.svg](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/HA_joint_recovery.svg>).
- [HA_fp_recovery.png](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/HA_fp_recovery.png>) (300 dpi); [HA_fp_recovery.svg](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/HA_fp_recovery.svg>).

Figures contain no titles or footers. Embedded metadata identifies freeze commit/tag, protocol hash and source CSVs. Best A2′ is descriptive, selected per cell separately for joint/fP recovery in fixed metric tie order [MVL-raw, MVL-Ozkurt, KLMI, GLM]; no method parameter changed. SP-raw is shown only in the fP figure because it does not estimate fA.

## Phase C

A1, A3 and A4 passed. The completed Phase C validation is reported below.

## Runtime and deviations

Amendment-1 Phase-A gate timer: 79.327 s, excluding MATLAB startup. Gates were repeated once under Amendment 1. Each reportable held-out input/method is evaluated once; finished checkpoint outputs are reused, not recomputed.

- generation_runtime.json: 26.005 s (worker timers include the equivalence-release wait).
- worker1_complete.json: 981.790 s (worker timers include the equivalence-release wait).
- worker2_complete.json: 981.499 s (worker timers include the equivalence-release wait).
- worker3_complete.json: 985.705 s (worker timers include the equivalence-release wait).
- worker4_complete.json: 984.377 s (worker timers include the equivalence-release wait).
- Read-only git inspection working directory: One exploratory git diff used the parent process folder and failed to resolve the tag. It was repeated in the repository; no file, code or signal was changed.
- Pre-gate source-verifier line endings: The verifier initially assumed LF but the source checkout uses CRLF. It now detects the original newline, reverses the permitted edits, restores that newline and requires exact original bytes. The v2 block is compared as bytes directly. No method source was altered by this fix and no gate or signal output had been computed. The initial read-only diagnostic also failed before printing the new-source branch; it made no file changes.
- Pre-gate provenance JSON field names: MATLAB jsondecode sanitised filename keys containing dots in the initial provenance struct. The source verifier now compares directly with the preserved baseline bytes and records file hashes as path/sha256 array records, avoiding filename-as-key rewriting. This metadata-reader fix occurred before any gate output; no method code or setting changed.
- Phase-B generator wrapper newline (tooling): A missing newline while copying helper functions concatenated end and function write_json into endfunction. The Poisson helper raised Undefined function endfunction before any input bank or method output was saved. Inserted one newline; original HB signal formulas, draw order and helper source now match the frozen generator exactly. Generation restarts from its fixed streams; no reportable result is recomputed.
- Matplotlib font-cache path (tooling): The initial report-only import could not write its font cache under the user profile due to sandbox permissions. No figure or estimator failed. MPLCONFIGDIR now points inside the work folder; no method or setting changed.
- Wilson error-bar round-off (tooling): Figure export rejected a negative error-bar length caused by floating-point round-off at a zero/one proportion. Plot lengths alone are bounded below by zero. Saved Wilson intervals, recovery counts, criteria and estimates are unchanged. The cached prespecified exact-test results are reused during report/export recovery; no method is rerun.
- MATLAB startup emitted warnings about missing historical Brainstorm paths. Drivers verify repository source precedence and use explicit analysis paths.
- HB retains its original APC [80,160]-Hz amplitude range as required to reproduce the saved suite; HA uses the default [80,150]-Hz range. This execution choice was recorded before held-out generation.

No protocol, tagged method or fixed setting was edited after its run started. Full options/settings are stored with each result/checkpoint and referenced provenance. Archive and source hashes were rechecked while generating this report.


## Phase C: unchanged saved real-data inputs

All saved preprocessing, bouts, channels and scan estimates were reused unchanged. Source/prep/bout/selection hashes were checked before and after the new estimates. The new v3 feature wrapper preserves the original raw-MVL and preferred-phase reconstruction assertions; every valid estimate passed them. [provenance.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/provenance.json>); [v3_feature_wrapper.diff](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/v3_feature_wrapper.diff>).

There were 3,646 unique physical rodent windows and 3,982 analysis rows across the prespecified 5-s and explicitly **POST HOC 2-s** analyses. Identical channel/start/stop windows are estimated once and reused. ECoG contains the original 2,648 analysed movement/imagery bouts, including the originally ineligible patient for status reporting; the primary eligibility remains the fixed 18 patients. APC v3 uses fA [80,150], minPhaseHz 1, maxPhaseHz 30 and all other defaults. The saved ECoG v1 reference is its Amendment-1 6-30-Hz run; v3 uses 1-30 Hz with its automatic 7/T feasibility bound, as specified for Phase C. The reused ECoG scans retain 6-30 Hz. No scan or preprocessing step was rerun.

The original regional statistics and seeds were reused, including 10,000 bout-bootstrap resamples and region-specific REML mixed models. ECoG statistics retain the original patient-bootstrap scheme (10,000, seed 20261024), restricted to the v3 protocol's endpoints. Original v1 fits/results are shown alongside. Full execution/statistical source diffs are stored with the copied scripts. [phaseC_analysis_plan.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC_analysis_plan.json>).

### Prespecified rodent: 5-s bouts

Per-session run minus rest differences (same fixed sessions and selected channels):

| analysis | animal | session | method | outcome | n_run | n_rest | mean_difference | welch_t | welch_p | hedges_g | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | EC013 | ec013.156 | APC-v1.0 | fP_hz | 9 | 43 | 1.33752 | 13.1584 | 9.11751e-15 | 2.78814 | 1.14915 | 1.53166 |
| CA1 | EC013 | ec013.156 | APC-v1.0 | fA_hz | 9 | 43 | 0.333333 | 0.047496 | 0.962931 | 0.0172553 | -12.7652 | 13.1037 |
| CA1 | EC013 | ec013.156 | APC-v1.0 | ozkurt_mvl | 9 | 43 | 0.00649848 | 1.51471 | 0.139763 | 0.326324 | -0.00164768 | 0.014682 |
| CA1 | EC013 | ec013.156 | APC-v3.0 | fP_hz | 9 | 43 | 1.33752 | 13.1584 | 9.11751e-15 | 2.78814 | 1.14915 | 1.53166 |
| CA1 | EC013 | ec013.156 | APC-v3.0 | fA_hz | 9 | 43 | 0.333333 | 0.047496 | 0.962931 | 0.0172553 | -12.7652 | 13.1037 |
| CA1 | EC013 | ec013.156 | APC-v3.0 | ozkurt_mvl | 9 | 43 | 0.00649848 | 1.51471 | 0.139763 | 0.326324 | -0.00164768 | 0.014682 |
| CA1 | EC013 | ec013.157 | APC-v1.0 | fP_hz | 6 | 14 | 1.34726 | 7.29177 | 1.6736e-06 | 2.73736 | 0.99851 | 1.68063 |
| CA1 | EC013 | ec013.157 | APC-v1.0 | fA_hz | 6 | 14 | 2.2381 | 0.272164 | 0.789953 | 0.113819 | -12.5476 | 17.4617 |
| CA1 | EC013 | ec013.157 | APC-v1.0 | ozkurt_mvl | 6 | 14 | 0.0166006 | 2.5592 | 0.0204366 | 0.942287 | 0.00415899 | 0.0282318 |
| CA1 | EC013 | ec013.157 | APC-v3.0 | fP_hz | 6 | 15 | 0.899299 | 1.86627 | 0.0807484 | 0.553957 | -0.164424 | 1.59888 |
| CA1 | EC013 | ec013.157 | APC-v3.0 | fA_hz | 6 | 15 | 1.46667 | 0.182765 | 0.858072 | 0.0760719 | -12.9008 | 16.2333 |
| CA1 | EC013 | ec013.157 | APC-v3.0 | ozkurt_mvl | 6 | 15 | 0.0170119 | 2.72905 | 0.0144819 | 0.991013 | 0.00507586 | 0.0281119 |
| CA1 | EC013 | ec013.375 | APC-v1.0 | fP_hz | 5 | 33 | -0.56722 | -0.286433 | 0.780017 | -0.0801911 | -4.02213 | 3.13666 |
| CA1 | EC013 | ec013.375 | APC-v1.0 | fA_hz | 5 | 33 | -3.63636 | -0.462856 | 0.659458 | -0.182559 | -17.3549 | 10.6488 |
| CA1 | EC013 | ec013.375 | APC-v1.0 | ozkurt_mvl | 5 | 33 | 0.0224492 | 2.17107 | 0.0863325 | 1.31571 | 0.00486727 | 0.0408901 |
| CA1 | EC013 | ec013.375 | APC-v3.0 | fP_hz | 5 | 33 | -2.06032 | -1.04509 | 0.319372 | -0.294449 | -5.45796 | 1.63871 |
| CA1 | EC013 | ec013.375 | APC-v3.0 | fA_hz | 5 | 33 | -1.45455 | -0.183091 | 0.860397 | -0.0693963 | -15.3516 | 13.0067 |
| CA1 | EC013 | ec013.375 | APC-v3.0 | ozkurt_mvl | 5 | 33 | 0.0229411 | 2.1866 | 0.0814448 | 1.16501 | 0.00507717 | 0.0415406 |
| E1_sensitivity | EC013 | ec013.156 | APC-v1.0 | fP_hz | 9 | 43 | 1.17204 | 16.7826 | 2.42646e-12 | 4.50743 | 1.04491 | 1.30237 |
| E1_sensitivity | EC013 | ec013.156 | APC-v1.0 | fA_hz | 9 | 43 | 6.46512 | 1.08269 | 0.297207 | 0.333708 | -4.50407 | 17.2196 |
| E1_sensitivity | EC013 | ec013.156 | APC-v1.0 | ozkurt_mvl | 9 | 43 | 0.0254384 | 3.77682 | 0.00259411 | 1.30731 | 0.0126484 | 0.0376025 |
| E1_sensitivity | EC013 | ec013.156 | APC-v3.0 | fP_hz | 9 | 43 | 1.17204 | 16.7826 | 2.42646e-12 | 4.50743 | 1.04491 | 1.30237 |
| E1_sensitivity | EC013 | ec013.156 | APC-v3.0 | fA_hz | 9 | 43 | 6.46512 | 1.08269 | 0.297207 | 0.333708 | -4.50407 | 17.2196 |
| E1_sensitivity | EC013 | ec013.156 | APC-v3.0 | ozkurt_mvl | 9 | 43 | 0.0254384 | 3.77682 | 0.00259411 | 1.30731 | 0.0126484 | 0.0376025 |
| E1_sensitivity | EC013 | ec013.157 | APC-v1.0 | fP_hz | 6 | 15 | 1.09313 | 7.13043 | 1.17552e-06 | 2.47849 | 0.794612 | 1.3613 |
| E1_sensitivity | EC013 | ec013.157 | APC-v1.0 | fA_hz | 6 | 15 | 8.3 | 1.03253 | 0.321326 | 0.42014 | -7.16667 | 22.3333 |
| E1_sensitivity | EC013 | ec013.157 | APC-v1.0 | ozkurt_mvl | 6 | 15 | 0.0464304 | 3.92338 | 0.00458792 | 1.99139 | 0.0263703 | 0.0684509 |
| E1_sensitivity | EC013 | ec013.157 | APC-v3.0 | fP_hz | 6 | 15 | 1.09313 | 7.13043 | 1.17552e-06 | 2.47849 | 0.794612 | 1.3613 |
| E1_sensitivity | EC013 | ec013.157 | APC-v3.0 | fA_hz | 6 | 15 | 8.3 | 1.03253 | 0.321326 | 0.42014 | -7.16667 | 22.3333 |
| E1_sensitivity | EC013 | ec013.157 | APC-v3.0 | ozkurt_mvl | 6 | 15 | 0.0464304 | 3.92338 | 0.00458792 | 1.99139 | 0.0263703 | 0.0684509 |
| E1_sensitivity | EC013 | ec013.375 | APC-v1.0 | fP_hz | 5 | 33 | 1.27199 | 4.02273 | 0.000292556 | 0.794194 | 0.710368 | 1.90598 |
| E1_sensitivity | EC013 | ec013.375 | APC-v1.0 | fA_hz | 5 | 33 | -15.1576 | -3.11825 | 0.0123065 | -0.941908 | -23.8911 | -6.49091 |
| E1_sensitivity | EC013 | ec013.375 | APC-v1.0 | ozkurt_mvl | 5 | 33 | 0.0459779 | 4.22352 | 0.00544228 | 1.68677 | 0.0270436 | 0.0657096 |
| E1_sensitivity | EC013 | ec013.375 | APC-v3.0 | fP_hz | 5 | 34 | 0.828485 | 4.40168 | 0.000450062 | 1.0625 | 0.47885 | 1.16849 |
| E1_sensitivity | EC013 | ec013.375 | APC-v3.0 | fA_hz | 5 | 34 | -14.9882 | -3.04579 | 0.0131464 | -0.887172 | -23.9001 | -6.14103 |
| E1_sensitivity | EC013 | ec013.375 | APC-v3.0 | ozkurt_mvl | 5 | 34 | 0.0492059 | 4.6549 | 0.00458039 | 2.09822 | 0.0311102 | 0.0682946 |
| EC | EC013 | ec013.156 | APC-v1.0 | fP_hz | 9 | 43 | 1.14035 | 16.6354 | 2.48661e-13 | 4.19601 | 1.01428 | 1.27076 |
| EC | EC013 | ec013.156 | APC-v1.0 | fA_hz | 9 | 43 | 8.51421 | 1.15417 | 0.272271 | 0.428637 | -5.39541 | 21.9922 |
| EC | EC013 | ec013.156 | APC-v1.0 | ozkurt_mvl | 9 | 43 | 0.0196201 | 2.6564 | 0.023569 | 1.11099 | 0.00542844 | 0.0330601 |
| EC | EC013 | ec013.156 | APC-v3.0 | fP_hz | 9 | 43 | 1.14035 | 16.6354 | 2.48661e-13 | 4.19601 | 1.01428 | 1.27076 |
| EC | EC013 | ec013.156 | APC-v3.0 | fA_hz | 9 | 43 | 8.51421 | 1.15417 | 0.272271 | 0.428637 | -5.39541 | 21.9922 |
| EC | EC013 | ec013.156 | APC-v3.0 | ozkurt_mvl | 9 | 43 | 0.0196201 | 2.6564 | 0.023569 | 1.11099 | 0.00542844 | 0.0330601 |
| EC | EC013 | ec013.157 | APC-v1.0 | fP_hz | 6 | 15 | 1.05281 | 7.38744 | 5.69039e-07 | 2.48445 | 0.77832 | 1.30741 |
| EC | EC013 | ec013.157 | APC-v1.0 | fA_hz | 6 | 15 | -4.03333 | -0.398614 | 0.698401 | -0.176839 | -23.2333 | 13.8667 |
| EC | EC013 | ec013.157 | APC-v1.0 | ozkurt_mvl | 6 | 15 | 0.0272217 | 1.90281 | 0.107044 | 1.20407 | -0.000309521 | 0.0505737 |
| EC | EC013 | ec013.157 | APC-v3.0 | fP_hz | 6 | 15 | 1.05281 | 7.38744 | 5.69039e-07 | 2.48445 | 0.77832 | 1.30741 |
| EC | EC013 | ec013.157 | APC-v3.0 | fA_hz | 6 | 15 | -4.03333 | -0.398614 | 0.698401 | -0.176839 | -23.2333 | 13.8667 |
| EC | EC013 | ec013.157 | APC-v3.0 | ozkurt_mvl | 6 | 15 | 0.0272217 | 1.90281 | 0.107044 | 1.20407 | -0.000309521 | 0.0505737 |
| EC | EC013 | ec013.375 | APC-v1.0 | fP_hz | 5 | 34 | 1.33736 | 4.0679 | 0.000242448 | 0.780428 | 0.758837 | 2.01488 |
| EC | EC013 | ec013.375 | APC-v1.0 | fA_hz | 5 | 34 | -9.92941 | -2.00534 | 0.0730702 | -0.572185 | -18.8826 | -1.27044 |
| EC | EC013 | ec013.375 | APC-v1.0 | ozkurt_mvl | 5 | 34 | 0.0370946 | 3.60268 | 0.00921224 | 1.28305 | 0.0183604 | 0.0553621 |
| EC | EC013 | ec013.375 | APC-v3.0 | fP_hz | 5 | 34 | 0.764096 | 3.36569 | 0.00231743 | 0.712637 | 0.361159 | 1.22488 |
| EC | EC013 | ec013.375 | APC-v3.0 | fA_hz | 5 | 34 | -11.1059 | -2.25724 | 0.0484702 | -0.650637 | -20.0471 | -2.38809 |
| EC | EC013 | ec013.375 | APC-v3.0 | ozkurt_mvl | 5 | 34 | 0.0433191 | 4.41346 | 0.00523554 | 1.88159 | 0.0260071 | 0.0606905 |

Across-session primary summaries:

| analysis | animal_pool | method | outcome | n_sessions | mean_session_difference | ci_low | ci_high | one_sample_p | wilcoxon_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | EC012 | APC-v1.0 | fA_hz | 0 | NA | NA | NA | NA | NA |
| CA1 | EC013 | APC-v1.0 | fA_hz | 3 | -0.354978 | -7.8002 | 7.09025 | 0.856443 | 1 |
| CA1 | pooled | APC-v1.0 | fA_hz | 3 | -0.354978 | -7.8002 | 7.09025 | 0.856443 | 1 |
| CA1 | EC012 | APC-v1.0 | fP_hz | 0 | NA | NA | NA | NA | NA |
| CA1 | EC013 | APC-v1.0 | fP_hz | 3 | 0.705852 | -2.03297 | 3.44467 | 0.382964 | 0.5 |
| CA1 | pooled | APC-v1.0 | fP_hz | 3 | 0.705852 | -2.03297 | 3.44467 | 0.382964 | 0.5 |
| CA1 | EC012 | APC-v1.0 | ozkurt_mvl | 0 | NA | NA | NA | NA | NA |
| CA1 | EC013 | APC-v1.0 | ozkurt_mvl | 3 | 0.0151827 | -0.00486253 | 0.035228 | 0.0826512 | 0.25 |
| CA1 | pooled | APC-v1.0 | ozkurt_mvl | 3 | 0.0151827 | -0.00486253 | 0.035228 | 0.0826512 | 0.25 |
| CA1 | EC012 | APC-v3.0 | fA_hz | 0 | NA | NA | NA | NA | NA |
| CA1 | EC013 | APC-v3.0 | fA_hz | 3 | 0.115152 | -3.54343 | 3.77373 | 0.904677 | 0.75 |
| CA1 | pooled | APC-v3.0 | fA_hz | 3 | 0.115152 | -3.54343 | 3.77373 | 0.904677 | 0.75 |
| CA1 | EC012 | APC-v3.0 | fP_hz | 0 | NA | NA | NA | NA | NA |
| CA1 | EC013 | APC-v3.0 | fP_hz | 3 | 0.0588326 | -4.53253 | 4.65019 | 0.961045 | 1 |
| CA1 | pooled | APC-v3.0 | fP_hz | 3 | 0.0588326 | -4.53253 | 4.65019 | 0.961045 | 1 |
| CA1 | EC012 | APC-v3.0 | ozkurt_mvl | 0 | NA | NA | NA | NA | NA |
| CA1 | EC013 | APC-v3.0 | ozkurt_mvl | 3 | 0.0154838 | -0.00520195 | 0.0361696 | 0.0843844 | 0.25 |
| CA1 | pooled | APC-v3.0 | ozkurt_mvl | 3 | 0.0154838 | -0.00520195 | 0.0361696 | 0.0843844 | 0.25 |
| E1_sensitivity | EC012 | APC-v1.0 | fA_hz | 0 | NA | NA | NA | NA | NA |
| E1_sensitivity | EC013 | APC-v1.0 | fA_hz | 3 | -0.13082 | -32.5385 | 32.2769 | 0.98772 | 1 |
| E1_sensitivity | pooled | APC-v1.0 | fA_hz | 3 | -0.13082 | -32.5385 | 32.2769 | 0.98772 | 1 |
| E1_sensitivity | EC012 | APC-v1.0 | fP_hz | 0 | NA | NA | NA | NA | NA |
| E1_sensitivity | EC013 | APC-v1.0 | fP_hz | 3 | 1.17905 | 0.95638 | 1.40172 | 0.00192103 | 0.25 |
| E1_sensitivity | pooled | APC-v1.0 | fP_hz | 3 | 1.17905 | 0.95638 | 1.40172 | 0.00192103 | 0.25 |
| E1_sensitivity | EC012 | APC-v1.0 | ozkurt_mvl | 0 | NA | NA | NA | NA | NA |
| E1_sensitivity | EC013 | APC-v1.0 | ozkurt_mvl | 3 | 0.0392822 | 0.00949425 | 0.0690702 | 0.029685 | 0.25 |
| E1_sensitivity | pooled | APC-v1.0 | ozkurt_mvl | 3 | 0.0392822 | 0.00949425 | 0.0690702 | 0.029685 | 0.25 |
| E1_sensitivity | EC012 | APC-v3.0 | fA_hz | 0 | NA | NA | NA | NA | NA |
| E1_sensitivity | EC013 | APC-v3.0 | fA_hz | 3 | -0.074373 | -32.2398 | 32.0911 | 0.992965 | 1 |
| E1_sensitivity | pooled | APC-v3.0 | fA_hz | 3 | -0.074373 | -32.2398 | 32.0911 | 0.992965 | 1 |
| E1_sensitivity | EC012 | APC-v3.0 | fP_hz | 0 | NA | NA | NA | NA | NA |
| E1_sensitivity | EC013 | APC-v3.0 | fP_hz | 3 | 1.03122 | 0.584197 | 1.47823 | 0.00999834 | 0.25 |
| E1_sensitivity | pooled | APC-v3.0 | fP_hz | 3 | 1.03122 | 0.584197 | 1.47823 | 0.00999834 | 0.25 |
| E1_sensitivity | EC012 | APC-v3.0 | ozkurt_mvl | 0 | NA | NA | NA | NA | NA |
| E1_sensitivity | EC013 | APC-v3.0 | ozkurt_mvl | 3 | 0.0403582 | 0.00807613 | 0.0726403 | 0.0328667 | 0.25 |
| E1_sensitivity | pooled | APC-v3.0 | ozkurt_mvl | 3 | 0.0403582 | 0.00807613 | 0.0726403 | 0.0328667 | 0.25 |
| EC | EC012 | APC-v1.0 | fA_hz | 0 | NA | NA | NA | NA | NA |
| EC | EC013 | APC-v1.0 | fA_hz | 3 | -1.81618 | -25.2157 | 21.5834 | 0.770179 | 0.75 |
| EC | pooled | APC-v1.0 | fA_hz | 3 | -1.81618 | -25.2157 | 21.5834 | 0.770179 | 0.75 |
| EC | EC012 | APC-v1.0 | fP_hz | 0 | NA | NA | NA | NA | NA |
| EC | EC013 | APC-v1.0 | fP_hz | 3 | 1.17684 | 0.814791 | 1.53889 | 0.0050736 | 0.25 |
| EC | pooled | APC-v1.0 | fP_hz | 3 | 1.17684 | 0.814791 | 1.53889 | 0.0050736 | 0.25 |
| EC | EC012 | APC-v1.0 | ozkurt_mvl | 0 | NA | NA | NA | NA | NA |
| EC | EC013 | APC-v1.0 | ozkurt_mvl | 3 | 0.0279788 | 0.00621326 | 0.0497443 | 0.0311692 | 0.25 |
| EC | pooled | APC-v1.0 | ozkurt_mvl | 3 | 0.0279788 | 0.00621326 | 0.0497443 | 0.0311692 | 0.25 |
| EC | EC012 | APC-v3.0 | fA_hz | 0 | NA | NA | NA | NA | NA |
| EC | EC013 | APC-v3.0 | fA_hz | 3 | -2.20833 | -26.8921 | 22.4754 | 0.737364 | 0.75 |
| EC | pooled | APC-v3.0 | fA_hz | 3 | -2.20833 | -26.8921 | 22.4754 | 0.737364 | 0.75 |
| EC | EC012 | APC-v3.0 | fP_hz | 0 | NA | NA | NA | NA | NA |
| EC | EC013 | APC-v3.0 | fP_hz | 3 | 0.985752 | 0.496656 | 1.47485 | 0.0130383 | 0.25 |
| EC | pooled | APC-v3.0 | fP_hz | 3 | 0.985752 | 0.496656 | 1.47485 | 0.0130383 | 0.25 |
| EC | EC012 | APC-v3.0 | ozkurt_mvl | 0 | NA | NA | NA | NA | NA |
| EC | EC013 | APC-v3.0 | ozkurt_mvl | 3 | 0.0300536 | -6.00377e-06 | 0.0601133 | 0.0500185 | 0.25 |
| EC | pooled | APC-v3.0 | ozkurt_mvl | 3 | 0.0300536 | -6.00377e-06 | 0.0601133 | 0.0500185 | 0.25 |

Full session tables, all scan rows and within-state SD/IQR/MAD:
- [regional_session_statistics.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/rodent5s/regional_session_statistics.csv>).
- [regional_across_session_statistics.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/rodent5s/regional_across_session_statistics.csv>).
- [regional_within_state_fp_spread.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/rodent5s/regional_within_state_fp_spread.csv>); [regional_across_session_spread_comparisons.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/rodent5s/regional_across_session_spread_comparisons.csv>).
- [v1_v3_mixed_coefficients.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/rodent5s/v1_v3_mixed_coefficients.csv>); v3 convergence/covariance diagnostics [regional_mixed_models.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/rodent5s/regional_mixed_models.json>).

Mixed-model state coefficients:

| analysis | method | outcome | Estimate | SE | tStat | DF | pValue | Lower | Upper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | APC-v1.0 | fP_hz | 0.646746 | 1.19 | 0.543486 | 108 | 0.587916 | -1.71203 | 3.00552 |
| CA1 | APC-v1.0 | ozkurt_mvl | 0.0148146 | 0.00596592 | 2.48321 | 108 | 0.0145582 | 0.00298916 | 0.0266401 |
| EC | APC-v1.0 | fP_hz | 1.20543 | 0.261901 | 4.60262 | 110 | 1.12481e-05 | 0.686406 | 1.72446 |
| EC | APC-v1.0 | ozkurt_mvl | 0.0264026 | 0.00685976 | 3.84891 | 110 | 0.000199522 | 0.0128081 | 0.039997 |
| E1_sensitivity | APC-v1.0 | fP_hz | 1.20765 | 0.236793 | 5.10001 | 109 | 1.44387e-06 | 0.73833 | 1.67696 |
| E1_sensitivity | APC-v1.0 | ozkurt_mvl | 0.0378455 | 0.007588 | 4.98754 | 109 | 2.32533e-06 | 0.0228063 | 0.0528847 |
| CA1 | APC-v3.0 | fP_hz | 0.038438 | 1.46261 | 0.0262804 | 109 | 0.979082 | -2.8604 | 2.93728 |
| CA1 | APC-v3.0 | ozkurt_mvl | 0.0150854 | 0.00618667 | 2.43837 | 109 | 0.0163693 | 0.00282359 | 0.0273471 |
| EC | APC-v3.0 | fP_hz | 1.01875 | 0.162928 | 6.25272 | 110 | 7.87947e-09 | 0.69586 | 1.34163 |
| EC | APC-v3.0 | ozkurt_mvl | 0.0284235 | 0.00759139 | 3.74417 | 110 | 0.000289738 | 0.0133791 | 0.0434678 |
| E1_sensitivity | APC-v3.0 | fP_hz | 1.05635 | 0.125858 | 8.39323 | 110 | 1.80342e-13 | 0.806932 | 1.30577 |
| E1_sensitivity | APC-v3.0 | ozkurt_mvl | 0.039409 | 0.00804697 | 4.89737 | 110 | 3.35881e-06 | 0.0234618 | 0.0553562 |

### POST HOC rodent sensitivity: 2-s bouts

Per-session run minus rest differences (same fixed sessions and selected channels):

| analysis | animal | session | method | outcome | n_run | n_rest | mean_difference | welch_t | welch_p | hedges_g | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | EC013 | ec013.156 | APC-v1.0 | fP_hz | 56 | 54 | 1.12282 | 9.15846 | 3.81932e-13 | 1.76129 | 0.880403 | 1.36336 |
| CA1 | EC013 | ec013.156 | APC-v1.0 | fA_hz | 56 | 54 | -6.60384 | -1.95897 | 0.0527211 | -0.371473 | -13.1027 | -0.0825081 |
| CA1 | EC013 | ec013.156 | APC-v1.0 | ozkurt_mvl | 56 | 54 | 0.0192118 | 3.64044 | 0.000426603 | 0.691629 | 0.00895873 | 0.0293029 |
| CA1 | EC013 | ec013.156 | APC-v3.0 | fP_hz | 56 | 56 | 0.3317 | 0.644803 | 0.521711 | 0.121023 | -0.803358 | 1.15672 |
| CA1 | EC013 | ec013.156 | APC-v3.0 | fA_hz | 56 | 56 | -7.625 | -2.26519 | 0.0254726 | -0.425155 | -14.0179 | -1.14241 |
| CA1 | EC013 | ec013.156 | APC-v3.0 | ozkurt_mvl | 56 | 56 | 0.0224324 | 4.62447 | 1.03128e-05 | 0.867969 | 0.0131261 | 0.0318249 |
| CA1 | EC013 | ec013.157 | APC-v1.0 | fP_hz | 23 | 31 | 1.57604 | 8.34812 | 7.62719e-10 | 1.98126 | 1.22549 | 1.97312 |
| CA1 | EC013 | ec013.157 | APC-v1.0 | fA_hz | 23 | 31 | 4.29313 | 0.729698 | 0.468918 | 0.193222 | -6.81258 | 15.5218 |
| CA1 | EC013 | ec013.157 | APC-v1.0 | ozkurt_mvl | 23 | 31 | 0.00253418 | 0.383725 | 0.702811 | 0.0968168 | -0.0104391 | 0.0149411 |
| CA1 | EC013 | ec013.157 | APC-v3.0 | fP_hz | 23 | 33 | 1.31303 | 5.12576 | 1.11089e-05 | 1.15587 | 0.752878 | 1.75526 |
| CA1 | EC013 | ec013.157 | APC-v3.0 | fA_hz | 23 | 33 | 3.95784 | 0.688722 | 0.494097 | 0.179745 | -7.05537 | 14.8816 |
| CA1 | EC013 | ec013.157 | APC-v3.0 | ozkurt_mvl | 23 | 33 | 0.00556936 | 0.965515 | 0.338595 | 0.243775 | -0.00542331 | 0.0166904 |
| CA1 | EC013 | ec013.205 | APC-v1.0 | fP_hz | 8 | 9 | 1.3283 | 10.2172 | 4.46708e-08 | 4.63596 | 1.10038 | 1.58372 |
| CA1 | EC013 | ec013.205 | APC-v1.0 | fA_hz | 8 | 9 | 2.30556 | 0.281839 | 0.782545 | 0.132315 | -13.1392 | 17.1951 |
| CA1 | EC013 | ec013.205 | APC-v1.0 | ozkurt_mvl | 8 | 9 | -0.00828765 | -0.640358 | 0.531607 | -0.293443 | -0.0321791 | 0.0153993 |
| CA1 | EC013 | ec013.205 | APC-v3.0 | fP_hz | 8 | 9 | 1.3283 | 10.2172 | 4.46708e-08 | 4.63596 | 1.10038 | 1.58372 |
| CA1 | EC013 | ec013.205 | APC-v3.0 | fA_hz | 8 | 9 | 2.30556 | 0.281839 | 0.782545 | 0.132315 | -13.1392 | 17.1951 |
| CA1 | EC013 | ec013.205 | APC-v3.0 | ozkurt_mvl | 8 | 9 | -0.00828765 | -0.640358 | 0.531607 | -0.293443 | -0.0321791 | 0.0153993 |
| CA1 | EC013 | ec013.206 | APC-v1.0 | fP_hz | 58 | 59 | 1.1579 | 12.0829 | 3.33814e-18 | 2.20249 | 0.967793 | 1.34008 |
| CA1 | EC013 | ec013.206 | APC-v1.0 | fA_hz | 58 | 59 | 3.4661 | 0.962419 | 0.337867 | 0.176867 | -3.42904 | 10.483 |
| CA1 | EC013 | ec013.206 | APC-v1.0 | ozkurt_mvl | 58 | 59 | 0.0137364 | 2.82453 | 0.00561436 | 0.519627 | 0.00431815 | 0.0232598 |
| CA1 | EC013 | ec013.206 | APC-v3.0 | fP_hz | 58 | 61 | 0.487603 | 1.06677 | 0.290329 | 0.189527 | -0.535786 | 1.20445 |
| CA1 | EC013 | ec013.206 | APC-v3.0 | fA_hz | 58 | 61 | 4.35246 | 1.22051 | 0.224752 | 0.222694 | -2.44914 | 11.3691 |
| CA1 | EC013 | ec013.206 | APC-v3.0 | ozkurt_mvl | 58 | 61 | 0.0148327 | 3.05386 | 0.00282232 | 0.558711 | 0.00536261 | 0.0242376 |
| CA1 | EC013 | ec013.208 | APC-v1.0 | fP_hz | 43 | 48 | 1.17762 | 1.16161 | 0.248534 | 0.238991 | -0.820137 | 3.11641 |
| CA1 | EC013 | ec013.208 | APC-v1.0 | fA_hz | 43 | 48 | 0.52907 | 0.129679 | 0.897114 | 0.0269273 | -7.48043 | 8.52548 |
| CA1 | EC013 | ec013.208 | APC-v1.0 | ozkurt_mvl | 43 | 48 | -0.0134289 | -1.8265 | 0.0711946 | -0.37505 | -0.0280145 | 9.27372e-05 |
| CA1 | EC013 | ec013.208 | APC-v3.0 | fP_hz | 44 | 53 | -1.11245 | -0.773571 | 0.441121 | -0.155103 | -3.82159 | 1.63471 |
| CA1 | EC013 | ec013.208 | APC-v3.0 | fA_hz | 44 | 53 | 0.599057 | 0.155876 | 0.876467 | 0.0313767 | -6.90408 | 8.09611 |
| CA1 | EC013 | ec013.208 | APC-v3.0 | ozkurt_mvl | 44 | 53 | -0.00474972 | -0.854161 | 0.395178 | -0.171098 | -0.0154674 | 0.0059942 |
| CA1 | EC013 | ec013.251 | APC-v1.0 | fP_hz | 54 | 60 | 1.02718 | 7.20385 | 5.6266e-10 | 1.28262 | 0.744606 | 1.29815 |
| CA1 | EC013 | ec013.251 | APC-v1.0 | fA_hz | 54 | 60 | -5.00926 | -1.31981 | 0.189598 | -0.245189 | -12.3871 | 2.26456 |
| CA1 | EC013 | ec013.251 | APC-v1.0 | ozkurt_mvl | 54 | 60 | 0.00433012 | 0.909111 | 0.365247 | 0.168104 | -0.00497246 | 0.0137427 |
| CA1 | EC013 | ec013.251 | APC-v3.0 | fP_hz | 54 | 65 | 0.687059 | 2.48381 | 0.0155148 | 0.41525 | 0.0700301 | 1.14328 |
| CA1 | EC013 | ec013.251 | APC-v3.0 | fA_hz | 54 | 65 | -4.00285 | -1.0648 | 0.289188 | -0.193434 | -11.2998 | 3.1816 |
| CA1 | EC013 | ec013.251 | APC-v3.0 | ozkurt_mvl | 54 | 65 | 0.00423334 | 0.862866 | 0.38998 | 0.154473 | -0.00512942 | 0.014017 |
| CA1 | EC013 | ec013.252 | APC-v1.0 | fP_hz | 32 | 60 | 1.23368 | 7.69663 | 3.51399e-11 | 1.29499 | 0.925024 | 1.55344 |
| CA1 | EC013 | ec013.252 | APC-v1.0 | fA_hz | 32 | 60 | -4.9375 | -1.1861 | 0.240156 | -0.26046 | -12.7617 | 3.01115 |
| CA1 | EC013 | ec013.252 | APC-v1.0 | ozkurt_mvl | 32 | 60 | 0.00431873 | 0.715444 | 0.476916 | 0.154339 | -0.00736468 | 0.0163009 |
| CA1 | EC013 | ec013.252 | APC-v3.0 | fP_hz | 32 | 64 | -0.188406 | -0.349564 | 0.727799 | -0.0532359 | -1.35735 | 0.748878 |
| CA1 | EC013 | ec013.252 | APC-v3.0 | fA_hz | 32 | 64 | -4.71875 | -1.1556 | 0.252536 | -0.253763 | -12.4062 | 3.10938 |
| CA1 | EC013 | ec013.252 | APC-v3.0 | ozkurt_mvl | 32 | 64 | 0.00364731 | 0.619753 | 0.537733 | 0.134105 | -0.00776705 | 0.0152938 |
| CA1 | EC013 | ec013.374 | APC-v1.0 | fP_hz | 88 | 76 | 1.03554 | 8.00041 | 5.74451e-12 | 1.32865 | 0.789315 | 1.2894 |
| CA1 | EC013 | ec013.374 | APC-v1.0 | fA_hz | 88 | 76 | 0.809809 | 0.273614 | 0.784739 | 0.0427121 | -4.78849 | 6.63805 |
| CA1 | EC013 | ec013.374 | APC-v1.0 | ozkurt_mvl | 88 | 76 | 0.00460918 | 1.18686 | 0.237115 | 0.186212 | -0.0032059 | 0.0119531 |
| CA1 | EC013 | ec013.374 | APC-v3.0 | fP_hz | 88 | 77 | 0.676478 | 2.36836 | 0.019929 | 0.387356 | 0.070298 | 1.15624 |
| CA1 | EC013 | ec013.374 | APC-v3.0 | fA_hz | 88 | 77 | 1.78247 | 0.597011 | 0.551348 | 0.0928585 | -3.81015 | 7.65771 |
| CA1 | EC013 | ec013.374 | APC-v3.0 | ozkurt_mvl | 88 | 77 | 0.00523777 | 1.34408 | 0.180888 | 0.210084 | -0.00268962 | 0.0125891 |
| CA1 | EC013 | ec013.375 | APC-v1.0 | fP_hz | 61 | 120 | -0.746984 | -0.876504 | 0.382055 | -0.122465 | -2.3895 | 0.898993 |
| CA1 | EC013 | ec013.375 | APC-v1.0 | fA_hz | 61 | 120 | -0.621175 | -0.196735 | 0.844371 | -0.0310001 | -6.85271 | 5.47072 |
| CA1 | EC013 | ec013.375 | APC-v1.0 | ozkurt_mvl | 61 | 120 | 0.0054233 | 1.05106 | 0.295311 | 0.164067 | -0.0045681 | 0.015669 |
| CA1 | EC013 | ec013.375 | APC-v3.0 | fP_hz | 68 | 135 | -0.853808 | -0.750541 | 0.454206 | -0.110095 | -3.06498 | 1.37454 |
| CA1 | EC013 | ec013.375 | APC-v3.0 | fA_hz | 68 | 135 | -2.928 | -0.929881 | 0.354059 | -0.136514 | -9.01095 | 3.202 |
| CA1 | EC013 | ec013.375 | APC-v3.0 | ozkurt_mvl | 68 | 135 | 0.00527357 | 1.13871 | 0.257046 | 0.174757 | -0.00355695 | 0.0144025 |
| E1_sensitivity | EC013 | ec013.156 | APC-v1.0 | fP_hz | 56 | 56 | 0.982409 | 11.6486 | 6.5879e-19 | 2.18632 | 0.818501 | 1.14102 |
| E1_sensitivity | EC013 | ec013.156 | APC-v1.0 | fA_hz | 56 | 56 | 2.82143 | 0.796401 | 0.427523 | 0.149477 | -4.07143 | 9.66071 |
| E1_sensitivity | EC013 | ec013.156 | APC-v1.0 | ozkurt_mvl | 56 | 56 | 0.0380728 | 8.74547 | 2.88354e-14 | 1.64144 | 0.0293812 | 0.0466367 |
| E1_sensitivity | EC013 | ec013.156 | APC-v3.0 | fP_hz | 56 | 56 | 0.850096 | 6.23744 | 4.01159e-08 | 1.17071 | 0.557916 | 1.07906 |
| E1_sensitivity | EC013 | ec013.156 | APC-v3.0 | fA_hz | 56 | 56 | 3.625 | 1.03598 | 0.302491 | 0.194443 | -3.19643 | 10.3933 |
| E1_sensitivity | EC013 | ec013.156 | APC-v3.0 | ozkurt_mvl | 56 | 56 | 0.0377071 | 8.70964 | 3.47617e-14 | 1.63471 | 0.0290057 | 0.0462046 |
| E1_sensitivity | EC013 | ec013.157 | APC-v1.0 | fP_hz | 23 | 33 | 1.14265 | 6.77905 | 3.60573e-08 | 1.56253 | 0.827226 | 1.4786 |
| E1_sensitivity | EC013 | ec013.157 | APC-v1.0 | fA_hz | 23 | 33 | 4.45718 | 0.984578 | 0.329275 | 0.251885 | -4.14499 | 13.1344 |
| E1_sensitivity | EC013 | ec013.157 | APC-v1.0 | ozkurt_mvl | 23 | 33 | 0.0221082 | 2.59302 | 0.0126102 | 0.694635 | 0.00558307 | 0.0382455 |
| E1_sensitivity | EC013 | ec013.157 | APC-v3.0 | fP_hz | 23 | 33 | 0.67451 | 2.0394 | 0.0492209 | 0.458573 | -0.0583597 | 1.17316 |
| E1_sensitivity | EC013 | ec013.157 | APC-v3.0 | fA_hz | 23 | 33 | 1.30567 | 0.275571 | 0.78393 | 0.0695478 | -7.56265 | 10.697 |
| E1_sensitivity | EC013 | ec013.157 | APC-v3.0 | ozkurt_mvl | 23 | 33 | 0.0222247 | 2.61192 | 0.0120281 | 0.700322 | 0.00563962 | 0.038359 |
| E1_sensitivity | EC013 | ec013.205 | APC-v1.0 | fP_hz | 8 | 9 | 1.40038 | 9.34705 | 2.94062e-07 | 4.1901 | 1.1374 | 1.68031 |
| E1_sensitivity | EC013 | ec013.205 | APC-v1.0 | fA_hz | 8 | 9 | -2.25 | -0.325883 | 0.749146 | -0.147547 | -15.0698 | 10.2639 |
| E1_sensitivity | EC013 | ec013.205 | APC-v1.0 | ozkurt_mvl | 8 | 9 | 0.0339532 | 2.28615 | 0.0406011 | 1.01742 | 0.00586542 | 0.0598343 |
| E1_sensitivity | EC013 | ec013.205 | APC-v3.0 | fP_hz | 8 | 9 | 1.40038 | 9.34705 | 2.94062e-07 | 4.1901 | 1.1374 | 1.68031 |
| E1_sensitivity | EC013 | ec013.205 | APC-v3.0 | fA_hz | 8 | 9 | -2.25 | -0.325883 | 0.749146 | -0.147547 | -15.0698 | 10.2639 |
| E1_sensitivity | EC013 | ec013.205 | APC-v3.0 | ozkurt_mvl | 8 | 9 | 0.0339532 | 2.28615 | 0.0406011 | 1.01742 | 0.00586542 | 0.0598343 |
| E1_sensitivity | EC013 | ec013.206 | APC-v1.0 | fP_hz | 58 | 60 | 1.05167 | 14.9552 | 1.19828e-23 | 2.69805 | 0.909023 | 1.18206 |
| E1_sensitivity | EC013 | ec013.206 | APC-v1.0 | fA_hz | 58 | 60 | 1.09023 | 0.364092 | 0.716461 | 0.0664365 | -4.81132 | 6.78531 |
| E1_sensitivity | EC013 | ec013.206 | APC-v1.0 | ozkurt_mvl | 58 | 60 | 0.0270488 | 5.85411 | 4.7964e-08 | 1.06733 | 0.0180806 | 0.0360125 |
| E1_sensitivity | EC013 | ec013.206 | APC-v3.0 | fP_hz | 58 | 61 | 1.04189 | 14.8936 | 9.63625e-24 | 2.65801 | 0.900015 | 1.17293 |
| E1_sensitivity | EC013 | ec013.206 | APC-v3.0 | fA_hz | 58 | 61 | 0.526569 | 0.174392 | 0.861863 | 0.0316368 | -5.40533 | 6.3078 |
| E1_sensitivity | EC013 | ec013.206 | APC-v3.0 | ozkurt_mvl | 58 | 61 | 0.027823 | 5.99577 | 2.43962e-08 | 1.08657 | 0.0187822 | 0.0368009 |
| E1_sensitivity | EC013 | ec013.208 | APC-v1.0 | fP_hz | 44 | 53 | 1.11814 | 8.0317 | 2.5278e-11 | 1.50694 | 0.861554 | 1.39982 |
| E1_sensitivity | EC013 | ec013.208 | APC-v1.0 | fA_hz | 44 | 53 | -2.11321 | -0.668149 | 0.505672 | -0.131781 | -8.31279 | 4.26117 |
| E1_sensitivity | EC013 | ec013.208 | APC-v1.0 | ozkurt_mvl | 44 | 53 | 0.03345 | 6.46275 | 5.75831e-09 | 1.25073 | 0.0234502 | 0.0433982 |
| E1_sensitivity | EC013 | ec013.208 | APC-v3.0 | fP_hz | 44 | 53 | 0.972028 | 9.69061 | 4.78838e-15 | 1.85072 | 0.774843 | 1.1589 |
| E1_sensitivity | EC013 | ec013.208 | APC-v3.0 | fA_hz | 44 | 53 | -1.79245 | -0.549434 | 0.584022 | -0.107892 | -8.19431 | 4.71775 |
| E1_sensitivity | EC013 | ec013.208 | APC-v3.0 | ozkurt_mvl | 44 | 53 | 0.0319991 | 6.17652 | 2.05021e-08 | 1.19522 | 0.0218922 | 0.0418593 |
| E1_sensitivity | EC013 | ec013.251 | APC-v1.0 | fP_hz | 54 | 61 | 1.27468 | 10.6445 | 1.65016e-16 | 1.8785 | 1.04487 | 1.51784 |
| E1_sensitivity | EC013 | ec013.251 | APC-v1.0 | fA_hz | 54 | 61 | -2.45871 | -0.726036 | 0.469366 | -0.132315 | -9.07811 | 4.09279 |
| E1_sensitivity | EC013 | ec013.251 | APC-v1.0 | ozkurt_mvl | 54 | 61 | 0.0389383 | 6.4798 | 2.53891e-09 | 1.20014 | 0.0274793 | 0.0505821 |
| E1_sensitivity | EC013 | ec013.251 | APC-v3.0 | fP_hz | 54 | 65 | 0.72842 | 2.07461 | 0.0419563 | 0.346315 | -0.0677211 | 1.24675 |
| E1_sensitivity | EC013 | ec013.251 | APC-v3.0 | fA_hz | 54 | 65 | -2.50285 | -0.74477 | 0.457932 | -0.132308 | -9.23147 | 3.99699 |
| E1_sensitivity | EC013 | ec013.251 | APC-v3.0 | ozkurt_mvl | 54 | 65 | 0.042509 | 7.1603 | 8.27461e-11 | 1.30496 | 0.0312477 | 0.0540587 |
| E1_sensitivity | EC013 | ec013.252 | APC-v1.0 | fP_hz | 32 | 60 | 1.09468 | 9.65989 | 1.72953e-15 | 1.70906 | 0.873206 | 1.32033 |
| E1_sensitivity | EC013 | ec013.252 | APC-v1.0 | fA_hz | 32 | 60 | -1.92708 | -0.614062 | 0.540897 | -0.121609 | -7.99198 | 4.09594 |
| E1_sensitivity | EC013 | ec013.252 | APC-v1.0 | ozkurt_mvl | 32 | 60 | 0.0311074 | 5.15128 | 1.71499e-06 | 1.00803 | 0.0195413 | 0.0429918 |
| E1_sensitivity | EC013 | ec013.252 | APC-v3.0 | fP_hz | 32 | 64 | 0.211276 | 0.413103 | 0.680896 | 0.0628973 | -0.897289 | 1.08125 |
| E1_sensitivity | EC013 | ec013.252 | APC-v3.0 | fA_hz | 32 | 64 | -2.28125 | -0.728769 | 0.468209 | -0.140382 | -8.3125 | 3.73477 |
| E1_sensitivity | EC013 | ec013.252 | APC-v3.0 | ozkurt_mvl | 32 | 64 | 0.0351991 | 5.79012 | 1.13078e-07 | 1.09523 | 0.0235508 | 0.0470609 |
| E1_sensitivity | EC013 | ec013.374 | APC-v1.0 | fP_hz | 88 | 75 | 0.970139 | 8.94094 | 6.20077e-14 | 1.4938 | 0.766943 | 1.19015 |
| E1_sensitivity | EC013 | ec013.374 | APC-v1.0 | fA_hz | 88 | 75 | -0.557727 | -0.21592 | 0.829337 | -0.0339383 | -5.59096 | 4.57244 |
| E1_sensitivity | EC013 | ec013.374 | APC-v1.0 | ozkurt_mvl | 88 | 75 | 0.0309664 | 7.25301 | 1.8764e-11 | 1.13988 | 0.0227308 | 0.0393287 |
| E1_sensitivity | EC013 | ec013.374 | APC-v3.0 | fP_hz | 88 | 77 | 0.942409 | 8.30752 | 1.11548e-12 | 1.36517 | 0.722387 | 1.16527 |
| E1_sensitivity | EC013 | ec013.374 | APC-v3.0 | fA_hz | 88 | 77 | -0.423701 | -0.166105 | 0.868287 | -0.0258898 | -5.40584 | 4.62179 |
| E1_sensitivity | EC013 | ec013.374 | APC-v3.0 | ozkurt_mvl | 88 | 77 | 0.0316794 | 7.4333 | 6.48866e-12 | 1.15994 | 0.0234087 | 0.0400593 |
| E1_sensitivity | EC013 | ec013.375 | APC-v1.0 | fP_hz | 68 | 128 | 1.42036 | 10.4033 | 1.58405e-19 | 1.17634 | 1.16327 | 1.69485 |
| E1_sensitivity | EC013 | ec013.375 | APC-v1.0 | fA_hz | 68 | 128 | -3.56296 | -1.49823 | 0.135926 | -0.206473 | -8.17969 | 1.067 |
| E1_sensitivity | EC013 | ec013.375 | APC-v1.0 | ozkurt_mvl | 68 | 128 | 0.0302318 | 7.5619 | 1.93166e-12 | 1.01358 | 0.0223483 | 0.0380005 |
| E1_sensitivity | EC013 | ec013.375 | APC-v3.0 | fP_hz | 68 | 137 | 0.395227 | 1.49894 | 0.136086 | 0.157525 | -0.167381 | 0.868584 |
| E1_sensitivity | EC013 | ec013.375 | APC-v3.0 | fA_hz | 68 | 137 | -4.25451 | -1.80962 | 0.0721148 | -0.243833 | -8.75766 | 0.278564 |
| E1_sensitivity | EC013 | ec013.375 | APC-v3.0 | ozkurt_mvl | 68 | 137 | 0.0335075 | 8.54937 | 5.03931e-15 | 1.12219 | 0.0258743 | 0.0412181 |
| EC | EC012 | ec012ec.239 | APC-v1.0 | fP_hz | 47 | 33 | 2.43447 | 13.123 | 1.13688e-14 | 3.50116 | 2.10267 | 2.81082 |
| EC | EC012 | ec012ec.239 | APC-v1.0 | fA_hz | 47 | 33 | -13.6389 | -3.3923 | 0.00118834 | -0.776674 | -21.1382 | -5.67567 |
| EC | EC012 | ec012ec.239 | APC-v1.0 | ozkurt_mvl | 47 | 33 | 0.0163365 | 2.38718 | 0.0201793 | 0.557282 | 0.00294183 | 0.0299206 |
| EC | EC012 | ec012ec.239 | APC-v3.0 | fP_hz | 47 | 34 | 2.22315 | 13.9471 | 9.32435e-16 | 3.62717 | 1.91171 | 2.52236 |
| EC | EC012 | ec012ec.239 | APC-v3.0 | fA_hz | 47 | 34 | -12.8805 | -3.22311 | 0.00196484 | -0.731175 | -20.3978 | -4.96558 |
| EC | EC012 | ec012ec.239 | APC-v3.0 | ozkurt_mvl | 47 | 34 | 0.0179156 | 2.6156 | 0.0112119 | 0.605033 | 0.00455782 | 0.0314833 |
| EC | EC012 | ec012ec.240 | APC-v1.0 | fP_hz | 66 | 15 | 2.60691 | 6.11908 | 2.52843e-05 | 3.53104 | 1.90124 | 3.48305 |
| EC | EC012 | ec012ec.240 | APC-v1.0 | fA_hz | 66 | 15 | 1.3303 | 0.209652 | 0.836278 | 0.0692059 | -10.9136 | 13.0697 |
| EC | EC012 | ec012ec.240 | APC-v1.0 | ozkurt_mvl | 66 | 15 | 0.00220546 | 0.242981 | 0.810738 | 0.0797823 | -0.0169566 | 0.0176425 |
| EC | EC012 | ec012ec.240 | APC-v3.0 | fP_hz | 66 | 17 | 1.18504 | 1.67829 | 0.112634 | 0.894038 | -0.332441 | 2.07809 |
| EC | EC012 | ec012ec.240 | APC-v3.0 | fA_hz | 66 | 17 | 5.17736 | 0.891711 | 0.382277 | 0.270873 | -6.16814 | 15.818 |
| EC | EC012 | ec012ec.240 | APC-v3.0 | ozkurt_mvl | 66 | 17 | 0.0104286 | 1.51755 | 0.141358 | 0.399663 | -0.0028362 | 0.0238143 |
| EC | EC012 | ec012ec.269 | APC-v1.0 | fP_hz | 38 | 45 | 2.95476 | 15.738 | 4.37671e-20 | 3.16256 | 2.59873 | 3.33576 |
| EC | EC012 | ec012ec.269 | APC-v1.0 | fA_hz | 38 | 45 | -1.89357 | -0.452089 | 0.652438 | -0.0984325 | -9.92959 | 6.03921 |
| EC | EC012 | ec012ec.269 | APC-v1.0 | ozkurt_mvl | 38 | 45 | 0.0159988 | 2.3857 | 0.0194109 | 0.508473 | 0.00250822 | 0.0288772 |
| EC | EC012 | ec012ec.269 | APC-v3.0 | fP_hz | 38 | 48 | 2.62312 | 17.0651 | 1.88784e-22 | 3.2815 | 2.33052 | 2.9268 |
| EC | EC012 | ec012ec.269 | APC-v3.0 | fA_hz | 38 | 48 | -3.41996 | -0.814674 | 0.41763 | -0.173959 | -11.4978 | 4.69751 |
| EC | EC012 | ec012ec.269 | APC-v3.0 | ozkurt_mvl | 38 | 48 | 0.0190221 | 3.09914 | 0.00264479 | 0.654524 | 0.00669204 | 0.0306126 |
| EC | EC012 | ec012ec.270 | APC-v1.0 | fP_hz | 24 | 40 | 2.79716 | 16.6527 | 2.04629e-20 | 3.3364 | 2.49371 | 3.14341 |
| EC | EC012 | ec012ec.270 | APC-v1.0 | fA_hz | 24 | 40 | 2.875 | 0.566577 | 0.573443 | 0.141394 | -6.82151 | 12.7021 |
| EC | EC012 | ec012ec.270 | APC-v1.0 | ozkurt_mvl | 24 | 40 | 0.00050725 | 0.0704622 | 0.944074 | 0.0170234 | -0.0132576 | 0.0145367 |
| EC | EC012 | ec012ec.270 | APC-v3.0 | fP_hz | 24 | 49 | 2.29345 | 10.7327 | 1.05693e-14 | 1.86823 | 1.85589 | 2.66824 |
| EC | EC012 | ec012ec.270 | APC-v3.0 | fA_hz | 24 | 49 | 2.04337 | 0.418314 | 0.677519 | 0.0999297 | -7.28318 | 11.3742 |
| EC | EC012 | ec012ec.270 | APC-v3.0 | ozkurt_mvl | 24 | 49 | 0.00318845 | 0.490072 | 0.626262 | 0.11757 | -0.00910171 | 0.0158752 |
| EC | EC012 | ec012ec.271 | APC-v1.0 | fP_hz | 35 | 16 | 2.67884 | 6.56162 | 7.90524e-06 | 2.84571 | 1.95444 | 3.49734 |
| EC | EC012 | ec012ec.271 | APC-v1.0 | fA_hz | 35 | 16 | -2.30536 | -0.315453 | 0.755037 | -0.100281 | -15.987 | 11.6957 |
| EC | EC012 | ec012ec.271 | APC-v1.0 | ozkurt_mvl | 35 | 16 | 0.00164739 | 0.12628 | 0.900941 | 0.0490658 | -0.0257154 | 0.0244639 |
| EC | EC012 | ec012ec.271 | APC-v3.0 | fP_hz | 35 | 21 | 1.0289 | 1.41565 | 0.172137 | 0.498616 | -0.571842 | 2.10679 |
| EC | EC012 | ec012ec.271 | APC-v3.0 | fA_hz | 35 | 21 | -2.3619 | -0.383838 | 0.70314 | -0.10642 | -13.7721 | 9.2381 |
| EC | EC012 | ec012ec.271 | APC-v3.0 | ozkurt_mvl | 35 | 21 | 0.00920694 | 1.17547 | 0.248679 | 0.351292 | -0.00624524 | 0.0243296 |
| EC | EC012 | ec012ec.356 | APC-v1.0 | fP_hz | 40 | 46 | 3.06318 | 19.7346 | 8.71834e-25 | 3.95757 | 2.78215 | 3.37731 |
| EC | EC012 | ec012ec.356 | APC-v1.0 | fA_hz | 40 | 46 | 1.275 | 0.329421 | 0.742659 | 0.0700669 | -6.21035 | 8.82057 |
| EC | EC012 | ec012ec.356 | APC-v1.0 | ozkurt_mvl | 40 | 46 | 0.0222163 | 3.37018 | 0.00113921 | 0.718758 | 0.00945757 | 0.0347934 |
| EC | EC012 | ec012ec.356 | APC-v3.0 | fP_hz | 40 | 50 | 2.50194 | 7.09945 | 4.32787e-09 | 1.33571 | 1.69772 | 3.05768 |
| EC | EC012 | ec012ec.356 | APC-v3.0 | fA_hz | 40 | 50 | 2.035 | 0.537038 | 0.592617 | 0.111646 | -5.3555 | 9.38513 |
| EC | EC012 | ec012ec.356 | APC-v3.0 | ozkurt_mvl | 40 | 50 | 0.0234871 | 3.59592 | 0.00053752 | 0.748832 | 0.010899 | 0.0360184 |
| EC | EC012 | ec012ec.357 | APC-v1.0 | fP_hz | 38 | 34 | 2.15776 | 12.0858 | 1.28745e-14 | 2.95921 | 1.8237 | 2.50947 |
| EC | EC012 | ec012ec.357 | APC-v1.0 | fA_hz | 38 | 34 | -15.2337 | -3.75359 | 0.000365276 | -0.880662 | -22.9057 | -7.35756 |
| EC | EC012 | ec012ec.357 | APC-v1.0 | ozkurt_mvl | 38 | 34 | 0.00433956 | 0.627427 | 0.532886 | 0.14964 | -0.00919696 | 0.017524 |
| EC | EC012 | ec012ec.357 | APC-v3.0 | fP_hz | 38 | 36 | 1.39558 | 2.21345 | 0.0334006 | 0.523405 | 0.00609797 | 2.23382 |
| EC | EC012 | ec012ec.357 | APC-v3.0 | fA_hz | 38 | 36 | -14.8187 | -3.54509 | 0.000710822 | -0.8195 | -22.7842 | -6.51996 |
| EC | EC012 | ec012ec.357 | APC-v3.0 | ozkurt_mvl | 38 | 36 | 0.00772903 | 1.15474 | 0.252652 | 0.268379 | -0.00536542 | 0.0207776 |
| EC | EC012 | ec012ec.375 | APC-v1.0 | fP_hz | 37 | 31 | 2.07598 | 16.8318 | 1.12142e-18 | 4.34671 | 1.84572 | 2.32158 |
| EC | EC012 | ec012ec.375 | APC-v1.0 | fA_hz | 37 | 31 | -9.1456 | -2.03753 | 0.0461476 | -0.498795 | -18.0064 | -0.455991 |
| EC | EC012 | ec012ec.375 | APC-v1.0 | ozkurt_mvl | 37 | 31 | 0.0308151 | 4.09148 | 0.000119011 | 0.970902 | 0.0165604 | 0.0451492 |
| EC | EC012 | ec012ec.375 | APC-v3.0 | fP_hz | 37 | 32 | 1.64458 | 3.67321 | 0.000884635 | 0.942746 | 0.651622 | 2.25029 |
| EC | EC012 | ec012ec.375 | APC-v3.0 | fA_hz | 37 | 32 | -9.17483 | -2.08588 | 0.041189 | -0.504244 | -17.866 | -0.654392 |
| EC | EC012 | ec012ec.375 | APC-v3.0 | ozkurt_mvl | 37 | 32 | 0.0305937 | 4.12047 | 0.000106309 | 0.971007 | 0.0165275 | 0.0447015 |
| EC | EC012 | ec012ec.444 | APC-v1.0 | fP_hz | 30 | 40 | 2.61056 | 15.8933 | 2.71808e-19 | 3.30592 | 2.31498 | 2.94404 |
| EC | EC012 | ec012ec.444 | APC-v1.0 | fA_hz | 30 | 40 | -1.4 | -0.319666 | 0.7503 | -0.07662 | -9.80729 | 7.055 |
| EC | EC012 | ec012ec.444 | APC-v1.0 | ozkurt_mvl | 30 | 40 | 0.019894 | 2.84552 | 0.00589164 | 0.666442 | 0.00665533 | 0.0332326 |
| EC | EC012 | ec012ec.444 | APC-v3.0 | fP_hz | 30 | 46 | 2.15834 | 11.8021 | 1.00923e-15 | 2.22616 | 1.79808 | 2.51095 |
| EC | EC012 | ec012ec.444 | APC-v3.0 | fA_hz | 30 | 46 | -3.37826 | -0.801502 | 0.426014 | -0.188244 | -11.2928 | 4.84786 |
| EC | EC012 | ec012ec.444 | APC-v3.0 | ozkurt_mvl | 30 | 46 | 0.0211874 | 3.15181 | 0.00242185 | 0.713175 | 0.00843695 | 0.0341577 |
| EC | EC013 | ec013.156 | APC-v1.0 | fP_hz | 56 | 55 | 0.857135 | 7.82757 | 6.42744e-11 | 1.48684 | 0.624125 | 1.04918 |
| EC | EC013 | ec013.156 | APC-v1.0 | fA_hz | 56 | 55 | 4.38377 | 1.27251 | 0.205941 | 0.240131 | -2.30294 | 11.1527 |
| EC | EC013 | ec013.156 | APC-v1.0 | ozkurt_mvl | 56 | 55 | 0.0330491 | 7.34773 | 4.32767e-11 | 1.38303 | 0.024418 | 0.0420508 |
| EC | EC013 | ec013.156 | APC-v3.0 | fP_hz | 56 | 56 | 0.847789 | 7.84228 | 5.2769e-11 | 1.47192 | 0.618305 | 1.03971 |
| EC | EC013 | ec013.156 | APC-v3.0 | fA_hz | 56 | 56 | 3.92857 | 1.14175 | 0.256068 | 0.214295 | -2.69687 | 10.7679 |
| EC | EC013 | ec013.156 | APC-v3.0 | ozkurt_mvl | 56 | 56 | 0.0324888 | 7.22069 | 7.91089e-11 | 1.35525 | 0.0239028 | 0.0414675 |
| EC | EC013 | ec013.157 | APC-v1.0 | fP_hz | 23 | 33 | 1.0953 | 6.03144 | 4.28443e-07 | 1.38749 | 0.763439 | 1.45808 |
| EC | EC013 | ec013.157 | APC-v1.0 | fA_hz | 23 | 33 | -4.19895 | -0.884247 | 0.380598 | -0.228617 | -13.3084 | 4.9447 |
| EC | EC013 | ec013.157 | APC-v1.0 | ozkurt_mvl | 23 | 33 | 0.0165181 | 2.18593 | 0.0341357 | 0.595983 | 0.00206991 | 0.0314695 |
| EC | EC013 | ec013.157 | APC-v3.0 | fP_hz | 23 | 33 | 0.490568 | 0.652006 | 0.517572 | 0.154419 | -1.19227 | 1.71947 |
| EC | EC013 | ec013.157 | APC-v3.0 | fA_hz | 23 | 33 | -3.21212 | -0.675627 | 0.502191 | -0.172639 | -12.3136 | 5.84078 |
| EC | EC013 | ec013.157 | APC-v3.0 | ozkurt_mvl | 23 | 33 | 0.017929 | 2.32578 | 0.0245093 | 0.628971 | 0.00295349 | 0.0329567 |
| EC | EC013 | ec013.205 | APC-v1.0 | fP_hz | 8 | 9 | 1.43033 | 9.84539 | 2.32042e-07 | 4.39589 | 1.17523 | 1.70363 |
| EC | EC013 | ec013.205 | APC-v1.0 | fA_hz | 8 | 9 | 2.56944 | 0.339767 | 0.738777 | 0.156294 | -11.2229 | 16.4448 |
| EC | EC013 | ec013.205 | APC-v1.0 | ozkurt_mvl | 8 | 9 | 0.0352096 | 2.19327 | 0.0478378 | 0.976941 | 0.00386892 | 0.062675 |
| EC | EC013 | ec013.205 | APC-v3.0 | fP_hz | 8 | 9 | 1.43033 | 9.84539 | 2.32042e-07 | 4.39589 | 1.17523 | 1.70363 |
| EC | EC013 | ec013.205 | APC-v3.0 | fA_hz | 8 | 9 | 2.56944 | 0.339767 | 0.738777 | 0.156294 | -11.2229 | 16.4448 |
| EC | EC013 | ec013.205 | APC-v3.0 | ozkurt_mvl | 8 | 9 | 0.0352096 | 2.19327 | 0.0478378 | 0.976941 | 0.00386892 | 0.062675 |
| EC | EC013 | ec013.206 | APC-v1.0 | fP_hz | 58 | 61 | 1.055 | 14.649 | 2.61755e-23 | 2.61409 | 0.911805 | 1.18982 |
| EC | EC013 | ec013.206 | APC-v1.0 | fA_hz | 58 | 61 | 3.23516 | 1.08447 | 0.280388 | 0.197261 | -2.50368 | 9.01139 |
| EC | EC013 | ec013.206 | APC-v1.0 | ozkurt_mvl | 58 | 61 | 0.0204776 | 4.2829 | 3.81051e-05 | 0.78062 | 0.0112101 | 0.0295551 |
| EC | EC013 | ec013.206 | APC-v3.0 | fP_hz | 58 | 61 | 1.055 | 14.649 | 2.61755e-23 | 2.61409 | 0.911805 | 1.18982 |
| EC | EC013 | ec013.206 | APC-v3.0 | fA_hz | 58 | 61 | 3.23516 | 1.08447 | 0.280388 | 0.197261 | -2.50368 | 9.01139 |
| EC | EC013 | ec013.206 | APC-v3.0 | ozkurt_mvl | 58 | 61 | 0.0204776 | 4.2829 | 3.81051e-05 | 0.78062 | 0.0112101 | 0.0295551 |
| EC | EC013 | ec013.208 | APC-v1.0 | fP_hz | 44 | 52 | 1.0586 | 9.31434 | 6.56656e-14 | 1.78356 | 0.844102 | 1.2932 |
| EC | EC013 | ec013.208 | APC-v1.0 | fA_hz | 44 | 52 | 0.795455 | 0.24612 | 0.806132 | 0.048882 | -5.49665 | 7.19784 |
| EC | EC013 | ec013.208 | APC-v1.0 | ozkurt_mvl | 44 | 52 | 0.0317053 | 6.31611 | 8.85279e-09 | 1.26302 | 0.0217066 | 0.0413351 |
| EC | EC013 | ec013.208 | APC-v3.0 | fP_hz | 44 | 53 | 1.05605 | 9.43844 | 2.99911e-14 | 1.78836 | 0.844568 | 1.28737 |
| EC | EC013 | ec013.208 | APC-v3.0 | fA_hz | 44 | 53 | 1.19168 | 0.370099 | 0.712139 | 0.0729838 | -5.07133 | 7.53949 |
| EC | EC013 | ec013.208 | APC-v3.0 | ozkurt_mvl | 44 | 53 | 0.0318982 | 6.41722 | 5.41079e-09 | 1.27643 | 0.0219837 | 0.0414074 |
| EC | EC013 | ec013.251 | APC-v1.0 | fP_hz | 54 | 59 | 1.19065 | 11.6165 | 1.80353e-18 | 2.10123 | 0.992035 | 1.39086 |
| EC | EC013 | ec013.251 | APC-v1.0 | fA_hz | 54 | 59 | -2.2806 | -0.662799 | 0.508863 | -0.12269 | -8.85284 | 4.44387 |
| EC | EC013 | ec013.251 | APC-v1.0 | ozkurt_mvl | 54 | 59 | 0.040046 | 6.59662 | 1.54042e-09 | 1.22288 | 0.0281543 | 0.0519403 |
| EC | EC013 | ec013.251 | APC-v3.0 | fP_hz | 54 | 65 | 0.760992 | 2.1056 | 0.0390836 | 0.351443 | -0.0260331 | 1.28427 |
| EC | EC013 | ec013.251 | APC-v3.0 | fA_hz | 54 | 65 | -3.58803 | -1.06534 | 0.288924 | -0.190492 | -10.0701 | 3.09501 |
| EC | EC013 | ec013.251 | APC-v3.0 | ozkurt_mvl | 54 | 65 | 0.0434603 | 7.31656 | 3.46996e-11 | 1.31244 | 0.0317613 | 0.0551629 |
| EC | EC013 | ec013.252 | APC-v1.0 | fP_hz | 32 | 59 | 1.10398 | 9.90582 | 6.15156e-16 | 1.76954 | 0.888606 | 1.32231 |
| EC | EC013 | ec013.252 | APC-v1.0 | fA_hz | 32 | 59 | -0.113347 | -0.0319304 | 0.974613 | -0.00657876 | -6.87509 | 6.79423 |
| EC | EC013 | ec013.252 | APC-v1.0 | ozkurt_mvl | 32 | 59 | 0.0215421 | 3.55284 | 0.000625226 | 0.690023 | 0.00959764 | 0.0333085 |
| EC | EC013 | ec013.252 | APC-v3.0 | fP_hz | 32 | 64 | 0.144375 | 0.269176 | 0.788653 | 0.0409579 | -1.01901 | 1.05881 |
| EC | EC013 | ec013.252 | APC-v3.0 | fA_hz | 32 | 64 | -0.546875 | -0.157662 | 0.875162 | -0.0319742 | -7.17188 | 6.20312 |
| EC | EC013 | ec013.252 | APC-v3.0 | ozkurt_mvl | 32 | 64 | 0.0239041 | 3.8981 | 0.000187832 | 0.723681 | 0.0118053 | 0.0356645 |
| EC | EC013 | ec013.374 | APC-v1.0 | fP_hz | 88 | 75 | 0.943491 | 9.9788 | 2.41293e-16 | 1.65707 | 0.766423 | 1.13157 |
| EC | EC013 | ec013.374 | APC-v1.0 | fA_hz | 88 | 75 | -2.21394 | -0.791342 | 0.430099 | -0.126277 | -7.72455 | 3.27229 |
| EC | EC013 | ec013.374 | APC-v1.0 | ozkurt_mvl | 88 | 75 | 0.0383784 | 8.79402 | 2.93805e-15 | 1.38502 | 0.0296418 | 0.0468113 |
| EC | EC013 | ec013.374 | APC-v3.0 | fP_hz | 88 | 77 | 0.852875 | 9.36333 | 3.31375e-15 | 1.52754 | 0.675937 | 1.02818 |
| EC | EC013 | ec013.374 | APC-v3.0 | fA_hz | 88 | 77 | -1.83766 | -0.667702 | 0.505396 | -0.105378 | -7.23401 | 3.53742 |
| EC | EC013 | ec013.374 | APC-v3.0 | ozkurt_mvl | 88 | 77 | 0.0374472 | 8.76344 | 2.91268e-15 | 1.36687 | 0.0288747 | 0.0457608 |
| EC | EC013 | ec013.375 | APC-v1.0 | fP_hz | 68 | 130 | 1.27638 | 9.83479 | 4.31707e-18 | 1.103 | 1.03256 | 1.53744 |
| EC | EC013 | ec013.375 | APC-v1.0 | fA_hz | 68 | 130 | -1.61199 | -0.641156 | 0.522326 | -0.0896495 | -6.44272 | 3.29378 |
| EC | EC013 | ec013.375 | APC-v1.0 | ozkurt_mvl | 68 | 130 | 0.0256416 | 5.93234 | 1.69745e-08 | 0.823054 | 0.0169965 | 0.033633 |
| EC | EC013 | ec013.375 | APC-v3.0 | fP_hz | 68 | 137 | 0.686113 | 3.59896 | 0.000433604 | 0.381484 | 0.295832 | 1.03131 |
| EC | EC013 | ec013.375 | APC-v3.0 | fA_hz | 68 | 137 | -1.72681 | -0.699593 | 0.485207 | -0.097028 | -6.47492 | 3.10947 |
| EC | EC013 | ec013.375 | APC-v3.0 | ozkurt_mvl | 68 | 137 | 0.0274189 | 6.45144 | 1.21415e-09 | 0.885872 | 0.0188209 | 0.0353936 |

Across-session primary summaries:

| analysis | animal_pool | method | outcome | n_sessions | mean_session_difference | ci_low | ci_high | one_sample_p | wilcoxon_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | EC012 | APC-v1.0 | fA_hz | 0 | NA | NA | NA | NA | NA |
| CA1 | EC013 | APC-v1.0 | fA_hz | 9 | -0.640901 | -3.69711 | 2.41531 | 0.641643 | 0.734375 |
| CA1 | pooled | APC-v1.0 | fA_hz | 9 | -0.640901 | -3.69711 | 2.41531 | 0.641643 | 0.734375 |
| CA1 | EC012 | APC-v1.0 | fP_hz | 0 | NA | NA | NA | NA | NA |
| CA1 | EC013 | APC-v1.0 | fP_hz | 9 | 0.990233 | 0.473246 | 1.50722 | 0.00223572 | 0.0078125 |
| CA1 | pooled | APC-v1.0 | fP_hz | 9 | 0.990233 | 0.473246 | 1.50722 | 0.00223572 | 0.0078125 |
| CA1 | EC012 | APC-v1.0 | ozkurt_mvl | 0 | NA | NA | NA | NA | NA |
| CA1 | EC013 | APC-v1.0 | ozkurt_mvl | 9 | 0.00360524 | -0.00400565 | 0.0112161 | 0.306483 | 0.300781 |
| CA1 | pooled | APC-v1.0 | ozkurt_mvl | 9 | 0.00360524 | -0.00400565 | 0.0112161 | 0.306483 | 0.300781 |
| CA1 | EC012 | APC-v3.0 | fA_hz | 0 | NA | NA | NA | NA | NA |
| CA1 | EC013 | APC-v3.0 | fA_hz | 9 | -0.697469 | -3.95961 | 2.56468 | 0.635232 | 0.652344 |
| CA1 | pooled | APC-v3.0 | fA_hz | 9 | -0.697469 | -3.95961 | 2.56468 | 0.635232 | 0.652344 |
| CA1 | EC012 | APC-v3.0 | fP_hz | 0 | NA | NA | NA | NA | NA |
| CA1 | EC013 | APC-v3.0 | fP_hz | 9 | 0.296611 | -0.367748 | 0.96097 | 0.333344 | 0.359375 |
| CA1 | pooled | APC-v3.0 | fP_hz | 9 | 0.296611 | -0.367748 | 0.96097 | 0.333344 | 0.359375 |
| CA1 | EC012 | APC-v3.0 | ozkurt_mvl | 0 | NA | NA | NA | NA | NA |
| CA1 | EC013 | APC-v3.0 | ozkurt_mvl | 9 | 0.00535435 | -0.00170074 | 0.0124094 | 0.118214 | 0.164062 |
| CA1 | pooled | APC-v3.0 | ozkurt_mvl | 9 | 0.00535435 | -0.00170074 | 0.0124094 | 0.118214 | 0.164062 |
| E1_sensitivity | EC012 | APC-v1.0 | fA_hz | 0 | NA | NA | NA | NA | NA |
| E1_sensitivity | EC013 | APC-v1.0 | fA_hz | 9 | -0.500095 | -2.58858 | 1.58839 | 0.59591 | 0.652344 |
| E1_sensitivity | pooled | APC-v1.0 | fA_hz | 9 | -0.500095 | -2.58858 | 1.58839 | 0.59591 | 0.652344 |
| E1_sensitivity | EC012 | APC-v1.0 | fP_hz | 0 | NA | NA | NA | NA | NA |
| E1_sensitivity | EC013 | APC-v1.0 | fP_hz | 9 | 1.16168 | 1.03296 | 1.2904 | 2.97972e-08 | 0.00390625 |
| E1_sensitivity | pooled | APC-v1.0 | fP_hz | 9 | 1.16168 | 1.03296 | 1.2904 | 2.97972e-08 | 0.00390625 |
| E1_sensitivity | EC012 | APC-v1.0 | ozkurt_mvl | 0 | NA | NA | NA | NA | NA |
| E1_sensitivity | EC013 | APC-v1.0 | ozkurt_mvl | 9 | 0.0317641 | 0.0277535 | 0.0357747 | 8.30787e-08 | 0.00390625 |
| E1_sensitivity | pooled | APC-v1.0 | ozkurt_mvl | 9 | 0.0317641 | 0.0277535 | 0.0357747 | 8.30787e-08 | 0.00390625 |
| E1_sensitivity | EC012 | APC-v3.0 | fA_hz | 0 | NA | NA | NA | NA | NA |
| E1_sensitivity | EC013 | APC-v3.0 | fA_hz | 9 | -0.89417 | -2.73639 | 0.948048 | 0.295498 | 0.300781 |
| E1_sensitivity | pooled | APC-v3.0 | fA_hz | 9 | -0.89417 | -2.73639 | 0.948048 | 0.295498 | 0.300781 |
| E1_sensitivity | EC012 | APC-v3.0 | fP_hz | 0 | NA | NA | NA | NA | NA |
| E1_sensitivity | EC013 | APC-v3.0 | fP_hz | 9 | 0.801805 | 0.529682 | 1.07393 | 0.000138585 | 0.00390625 |
| E1_sensitivity | pooled | APC-v3.0 | fP_hz | 9 | 0.801805 | 0.529682 | 1.07393 | 0.000138585 | 0.00390625 |
| E1_sensitivity | EC012 | APC-v3.0 | ozkurt_mvl | 0 | NA | NA | NA | NA | NA |
| E1_sensitivity | EC013 | APC-v3.0 | ozkurt_mvl | 9 | 0.0329558 | 0.0285383 | 0.0373733 | 1.32609e-07 | 0.00390625 |
| E1_sensitivity | pooled | APC-v3.0 | ozkurt_mvl | 9 | 0.0329558 | 0.0285383 | 0.0373733 | 1.32609e-07 | 0.00390625 |
| EC | EC012 | APC-v1.0 | fA_hz | 9 | -4.23743 | -9.41275 | 0.937879 | 0.0957045 | 0.128906 |
| EC | EC013 | APC-v1.0 | fA_hz | 9 | 0.0627778 | -2.1655 | 2.29106 | 0.949794 | 0.910156 |
| EC | pooled | APC-v1.0 | fA_hz | 18 | -2.08733 | -4.81933 | 0.64467 | 0.125379 | 0.28373 |
| EC | EC012 | APC-v1.0 | fP_hz | 9 | 2.59773 | 2.34234 | 2.85313 | 1.16072e-08 | 0.00390625 |
| EC | EC013 | APC-v1.0 | fP_hz | 9 | 1.11232 | 0.980762 | 1.24388 | 4.97577e-08 | 0.00390625 |
| EC | pooled | APC-v1.0 | fP_hz | 18 | 1.85503 | 1.45416 | 2.25589 | 2.19699e-08 | 7.62939e-06 |
| EC | EC012 | APC-v1.0 | ozkurt_mvl | 9 | 0.0126623 | 0.00430612 | 0.0210184 | 0.00814637 | 0.00390625 |
| EC | EC013 | APC-v1.0 | ozkurt_mvl | 9 | 0.0291742 | 0.0227013 | 0.0356471 | 6.35868e-06 | 0.00390625 |
| EC | pooled | APC-v1.0 | ozkurt_mvl | 18 | 0.0209182 | 0.0146053 | 0.0272311 | 2.1738e-06 | 7.62939e-06 |
| EC | EC012 | APC-v3.0 | fA_hz | 9 | -4.08649 | -9.40638 | 1.2334 | 0.114448 | 0.128906 |
| EC | EC013 | APC-v3.0 | fA_hz | 9 | 0.00148346 | -2.16876 | 2.17172 | 0.998781 | 1 |
| EC | pooled | APC-v3.0 | fA_hz | 18 | -2.0425 | -4.79856 | 0.713554 | 0.13634 | 0.28373 |
| EC | EC012 | APC-v3.0 | fP_hz | 9 | 1.8949 | 1.4401 | 2.3497 | 1.14338e-05 | 0.00390625 |
| EC | EC013 | APC-v3.0 | fP_hz | 9 | 0.813789 | 0.532494 | 1.09508 | 0.000157301 | 0.00390625 |
| EC | pooled | APC-v3.0 | fP_hz | 18 | 1.35434 | 0.989878 | 1.71881 | 4.80026e-07 | 7.62939e-06 |
| EC | EC012 | APC-v3.0 | ozkurt_mvl | 9 | 0.0158621 | 0.00910446 | 0.0226197 | 0.000636195 | 0.00390625 |
| EC | EC013 | APC-v3.0 | ozkurt_mvl | 9 | 0.030026 | 0.0236306 | 0.0364213 | 4.67712e-06 | 0.00390625 |
| EC | pooled | APC-v3.0 | ozkurt_mvl | 18 | 0.022944 | 0.0174502 | 0.0284379 | 9.56544e-08 | 7.62939e-06 |

Full session tables, all scan rows and within-state SD/IQR/MAD:
- [posthoc_2s_session_statistics.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/POST_HOC_rodent2s/posthoc_2s_session_statistics.csv>).
- [posthoc_2s_across_session_statistics.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/POST_HOC_rodent2s/posthoc_2s_across_session_statistics.csv>).
- [posthoc_2s_within_state_fp_spread.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/POST_HOC_rodent2s/posthoc_2s_within_state_fp_spread.csv>); [posthoc_2s_across_session_spread_comparisons.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/POST_HOC_rodent2s/posthoc_2s_across_session_spread_comparisons.csv>).
- [v1_v3_mixed_coefficients.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/POST_HOC_rodent2s/v1_v3_mixed_coefficients.csv>); v3 convergence/covariance diagnostics [posthoc_2s_mixed_models.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/POST_HOC_rodent2s/posthoc_2s_mixed_models.json>).

Mixed-model state coefficients:

| analysis | method | outcome | Estimate | SE | tStat | DF | pValue | Lower | Upper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CA1 | APC-v1.0 | fP_hz | 0.898049 | 0.296683 | 3.02697 | 938 | 0.00253767 | 0.315811 | 1.48029 |
| CA1 | APC-v1.0 | ozkurt_mvl | 0.00489009 | 0.00317267 | 1.54132 | 938 | 0.123576 | -0.00133626 | 0.0111164 |
| EC | APC-v1.0 | fP_hz | 1.84202 | 0.190275 | 9.68083 | 1616 | 1.38427e-21 | 1.46881 | 2.21523 |
| EC | APC-v1.0 | ozkurt_mvl | 0.0215187 | 0.00301053 | 7.14779 | 1616 | 1.33007e-12 | 0.0156137 | 0.0274236 |
| E1_sensitivity | APC-v1.0 | fP_hz | 1.13639 | 0.0652058 | 17.4277 | 964 | 2.43046e-59 | 1.00843 | 1.26435 |
| E1_sensitivity | APC-v1.0 | ozkurt_mvl | 0.0319893 | 0.00184632 | 17.3259 | 964 | 9.38596e-59 | 0.028366 | 0.0356126 |
| CA1 | APC-v3.0 | fP_hz | 0.220689 | 0.370768 | 0.595221 | 982 | 0.551833 | -0.506899 | 0.948277 |
| CA1 | APC-v3.0 | ozkurt_mvl | 0.00664866 | 0.00282105 | 2.3568 | 982 | 0.0186286 | 0.00111268 | 0.0121846 |
| EC | APC-v3.0 | fP_hz | 1.3124 | 0.185304 | 7.08243 | 1671 | 2.07903e-12 | 0.94895 | 1.67585 |
| EC | APC-v3.0 | ozkurt_mvl | 0.0234287 | 0.0027189 | 8.61697 | 1671 | 1.56538e-17 | 0.0180959 | 0.0287615 |
| E1_sensitivity | APC-v3.0 | fP_hz | 0.726596 | 0.143246 | 5.07238 | 984 | 4.69424e-07 | 0.445494 | 1.0077 |
| E1_sensitivity | APC-v3.0 | ozkurt_mvl | 0.0335041 | 0.00185016 | 18.1088 | 984 | 1.7666e-63 | 0.0298734 | 0.0371349 |

### Rodent status and feasibility-bound counts


| bout_set | analysis | animal | state | n | valid | status3 | fp_near_flo | status_counts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| POST_HOC_2s | CA1 | EC013 | rest | 555 | 553 | 2 | 0 | {"0": 553, "3": 2} |
| POST_HOC_2s | CA1 | EC013 | run | 431 | 431 | 0 | 0 | {"0": 431} |
| POST_HOC_2s | E1_sensitivity | EC013 | rest | 555 | 555 | 0 | 0 | {"0": 555} |
| POST_HOC_2s | E1_sensitivity | EC013 | run | 431 | 431 | 0 | 0 | {"0": 431} |
| POST_HOC_2s | EC | EC012 | rest | 333 | 333 | 0 | 0 | {"0": 333} |
| POST_HOC_2s | EC | EC012 | run | 355 | 355 | 0 | 0 | {"0": 355} |
| POST_HOC_2s | EC | EC013 | rest | 555 | 555 | 0 | 0 | {"0": 555} |
| POST_HOC_2s | EC | EC013 | run | 431 | 431 | 0 | 0 | {"0": 431} |
| prespecified_5s | CA1 | EC013 | rest | 92 | 91 | 1 | 0 | {"0": 91, "3": 1} |
| prespecified_5s | CA1 | EC013 | run | 20 | 20 | 0 | 0 | {"0": 20} |
| prespecified_5s | E1_sensitivity | EC013 | rest | 92 | 92 | 0 | 0 | {"0": 92} |
| prespecified_5s | E1_sensitivity | EC013 | run | 20 | 20 | 0 | 0 | {"0": 20} |
| prespecified_5s | EC | EC013 | rest | 92 | 92 | 0 | 0 | {"0": 92} |
| prespecified_5s | EC | EC013 | run | 20 | 20 | 0 | 0 | {"0": 20} |

## ECoG: fixed eligible patients and primary endpoints


| subset | primary | method | n_patients | n_bouts | mean_difference | median_difference | t_p_two_sided | wilcoxon_p_two_sided | ci_low | ci_high | decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| prespecified | Primary 1 | APC-v1.0 | 18 | 1809 | 0.00245947 | 0.00214055 | 0.299498 | 0.392738 | -0.00190419 | 0.00671545 | Not shown |
| prespecified | Primary 2 | APC-v1.0 minus MVL-Ozkurt | 18 | 1809 | -1.06129 | -0.28749 | NA | 0.0538559 | -2.35289 | 0.0566456 | Not shown |
| sensitivity_a | Primary 1 | APC-v1.0 | 7 | 833 | -0.00259347 | -0.00176796 | 0.526077 | 0.46875 | -0.00960933 | 0.0044438 | Not shown |
| sensitivity_a | Primary 2 | APC-v1.0 minus MVL-Ozkurt | 7 | 833 | -2.12991 | -2.35289 | NA | 0.046875 | -4.17528 | -0.297347 | Supported |
| prespecified | Primary 1 | APC-v3.0 | 18 | 1809 | -0.00233177 | -0.0038289 | 0.39715 | 0.34655 | -0.00731473 | 0.00282227 | Not shown |
| prespecified | Primary 2 | APC-v3.0 minus MVL-Ozkurt | 18 | 1809 | 1.60793 | 1.72967 | NA | 7.62939e-05 | 1.01497 | 2.26847 | Opposite |
| sensitivity_a | Primary 1 | APC-v3.0 | 7 | 833 | -0.00367234 | -0.00542059 | 0.0758331 | 0.109375 | -0.00625961 | -0.000322455 | Supported |
| sensitivity_a | Primary 2 | APC-v3.0 minus MVL-Ozkurt | 7 | 833 | 1.30154 | 1.49438 | NA | 0.046875 | 0.0910884 | 2.23013 | Opposite |

Primary 1 uses the mean movement minus rest normalized-MVL difference. Primary 2 uses the median patient-level difference in mean within-state fP SD (APC minus MVL-Ozkurt scan). Decisions use the original bootstrap CI rules and labels. Sensitivity (a) excludes the same 11 flagged eligible patients.

- prespecified, Primary 1: **Not shown**.
- prespecified, Primary 2: **Opposite**.
- sensitivity_a, Primary 1: **Supported**.
- sensitivity_a, Primary 2: **Opposite**.

The unchanged eligible-patient inventory: [patient_eligibility.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/ecog/patient_eligibility.csv>). Patient/state means, medians, SD and finite-bout denominators: [ecog_patient_summary.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/ecog/ecog_patient_summary.csv>). New primary endpoint tables: [ecog_statistics.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/ecog/ecog_statistics.csv>).

Mixed model (original ML/default fitlme specification, rest reference): outcome ~ state + (1 + state | patient). [mixed_model_coefficients.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/ecog/mixed_model_coefficients.csv>); [mixed_model_runtime.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/ecog/mixed_model_runtime.json>).

### ECoG secondary 1 and prespecified success criterion

**ECoG success criterion: PASS.** v3 median rest fP was within 2 Hz of the unchanged rest spectral peak in 13/18 patients (required >=9/18); v1: 5/18; SP-raw: 15/18. Missing medians count as failures. The original analysed-rest spectrum uses its unchanged 8-30-Hz residual-peak rule.


| patient | n_rest | n_v3_valid | spectral_peak_hz | v1_median_fp_hz | v3_median_fp_hz | SP_raw_median_fp_hz | scan_median_fp_hz | v3_within_2_hz | paired_fraction_within_1_hz |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bp | 59 | 59 | 15 | 14.107 | 15.5333 | 16.221 | 8.5 | True | 0.542373 |
| ca | 29 | 29 | 16 | 6.01196 | 17.3552 | 16.1546 | 8.5 | True | 0.344828 |
| cc | 14 | 13 | 15 | 6.01196 | 14.1176 | 13.3885 | 9.75 | True | 0.230769 |
| de | 29 | 29 | 18 | 6.01196 | 16.8612 | 16.5479 | 9.5 | True | 0.310345 |
| fp | 59 | 59 | 8 | 6.01196 | 8.30219 | 7.49509 | 9 | True | 0.305085 |
| gc | 29 | 29 | 15 | 14.3906 | 15.4571 | 15.5773 | 9 | True | 0.551724 |
| gf | 45 | 45 | 8 | 6.01196 | 7.67844 | 7.42538 | 8 | True | 0.444444 |
| hh | 59 | 59 | 16 | 6.01196 | 14.7757 | 16.6356 | 9 | True | 0.322034 |
| hl | 29 | 29 | 22 | 8.70853 | 18.2003 | 19.8567 | 8 | False | 0.517241 |
| jc | 59 | 57 | 18 | 6.01196 | 17.5477 | 17.0752 | 10 | True | 0.421053 |
| jm | 59 | 58 | 20 | 6.01196 | 10.6974 | 16.1384 | 8.5 | False | 0.206897 |
| jp | 18 | 18 | 13 | 6.01196 | 12.9174 | 12.8733 | 8.75 | True | 0.666667 |
| jt | 29 | 29 | 18 | 6.01196 | 13.5414 | 18.0464 | 8.5 | False | 0.310345 |
| rh | 59 | 57 | 19 | 6.01196 | 18.0775 | 18.3185 | 9.5 | True | 0.526316 |
| rr | 59 | 59 | 14 | 13.6913 | 13.8276 | 14.4389 | 9.5 | True | 0.677966 |
| ug | 44 | 44 | 18 | 13.72 | 15.7315 | 14.8474 | 7.75 | False | 0.409091 |
| wc | 29 | 28 | 13 | 8.20981 | 17.326 | 14.5612 | 9.5 | False | 0.357143 |
| zt | 44 | 44 | 16 | 12.3546 | 15.3931 | 16.4895 | 9 | True | 0.454545 |

All per-patient medians, counts within 12-20 Hz, spectrum agreement, paired SP-raw agreement and finite denominators: [ecog_rest_frequencies.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/ecog_rest_frequencies.csv>).


| method | n_patients | median_in_12_20 | within_2_hz_spectrum |
| --- | --- | --- | --- |
| v1 | 18 | 5 | 5 |
| v3 | 18 | 15 | 13 |
| scan | 18 | 0 | 2 |
| SP_raw | 18 | 16 | 15 |

### ECoG status-3 rates and fP near f_lo


| patient | recording | state | eligible | n | n_valid | status3 | status3_rate | status4 | fp_near_flo | fp_near_flo_rate_all | fp_near_flo_rate_valid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bp | imagery | move | True | 60 | 59 | 1 | 0.0166667 | 0 | 0 | 0 | 0 |
| bp | imagery | rest | True | 59 | 58 | 1 | 0.0169492 | 0 | 0 | 0 | 0 |
| bp | movement | move | True | 60 | 56 | 4 | 0.0666667 | 0 | 0 | 0 | 0 |
| bp | movement | rest | True | 59 | 59 | 0 | 0 | 0 | 0 | 0 | 0 |
| ca | movement | move | True | 60 | 60 | 0 | 0 | 0 | 0 | 0 | 0 |
| ca | movement | rest | True | 29 | 29 | 0 | 0 | 0 | 0 | 0 | 0 |
| cc | movement | move | True | 30 | 30 | 0 | 0 | 0 | 0 | 0 | 0 |
| cc | movement | rest | True | 14 | 13 | 1 | 0.0714286 | 0 | 0 | 0 | 0 |
| de | movement | move | True | 60 | 60 | 0 | 0 | 0 | 0 | 0 | 0 |
| de | movement | rest | True | 29 | 29 | 0 | 0 | 0 | 0 | 0 | 0 |
| fp | imagery | move | True | 60 | 60 | 0 | 0 | 0 | 0 | 0 | 0 |
| fp | imagery | rest | True | 59 | 59 | 0 | 0 | 0 | 0 | 0 | 0 |
| fp | movement | move | True | 60 | 60 | 0 | 0 | 0 | 0 | 0 | 0 |
| fp | movement | rest | True | 59 | 59 | 0 | 0 | 0 | 0 | 0 | 0 |
| gc | movement | move | True | 60 | 60 | 0 | 0 | 0 | 0 | 0 | 0 |
| gc | movement | rest | True | 29 | 29 | 0 | 0 | 0 | 0 | 0 | 0 |
| gf | movement | move | True | 60 | 60 | 0 | 0 | 0 | 0 | 0 | 0 |
| gf | movement | rest | True | 45 | 45 | 0 | 0 | 0 | 0 | 0 | 0 |
| hh | imagery | move | True | 60 | 60 | 0 | 0 | 0 | 0 | 0 | 0 |
| hh | imagery | rest | True | 59 | 59 | 0 | 0 | 0 | 0 | 0 | 0 |
| hh | movement | move | True | 60 | 60 | 0 | 0 | 0 | 0 | 0 | 0 |
| hh | movement | rest | True | 59 | 59 | 0 | 0 | 0 | 0 | 0 | 0 |
| hl | movement | move | True | 60 | 59 | 1 | 0.0166667 | 0 | 1 | 0.0166667 | 0.0169492 |
| hl | movement | rest | True | 29 | 29 | 0 | 0 | 0 | 0 | 0 | 0 |
| jc | imagery | move | True | 60 | 60 | 0 | 0 | 0 | 0 | 0 | 0 |
| jc | imagery | rest | True | 59 | 59 | 0 | 0 | 0 | 1 | 0.0169492 | 0.0169492 |
| jc | movement | move | True | 60 | 57 | 3 | 0.05 | 0 | 0 | 0 | 0 |
| jc | movement | rest | True | 59 | 57 | 2 | 0.0338983 | 0 | 0 | 0 | 0 |
| jf | movement | rest | False | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| jm | imagery | move | True | 60 | 59 | 1 | 0.0166667 | 0 | 0 | 0 | 0 |
| jm | imagery | rest | True | 59 | 57 | 2 | 0.0338983 | 0 | 0 | 0 | 0 |
| jm | movement | move | True | 60 | 60 | 0 | 0 | 0 | 0 | 0 | 0 |
| jm | movement | rest | True | 59 | 58 | 1 | 0.0169492 | 0 | 0 | 0 | 0 |
| jp | movement | move | True | 37 | 37 | 0 | 0 | 0 | 0 | 0 | 0 |
| jp | movement | rest | True | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 |
| jt | movement | move | True | 60 | 60 | 0 | 0 | 0 | 0 | 0 | 0 |
| jt | movement | rest | True | 29 | 29 | 0 | 0 | 0 | 0 | 0 | 0 |
| rh | imagery | move | True | 60 | 60 | 0 | 0 | 0 | 0 | 0 | 0 |
| rh | imagery | rest | True | 59 | 58 | 1 | 0.0169492 | 0 | 0 | 0 | 0 |
| rh | movement | move | True | 60 | 59 | 0 | 0 | 1 | 0 | 0 | 0 |
| rh | movement | rest | True | 59 | 57 | 2 | 0.0338983 | 0 | 0 | 0 | 0 |
| rr | imagery | move | True | 60 | 59 | 1 | 0.0166667 | 0 | 0 | 0 | 0 |
| rr | imagery | rest | True | 59 | 59 | 0 | 0 | 0 | 0 | 0 | 0 |
| rr | movement | move | True | 60 | 60 | 0 | 0 | 0 | 0 | 0 | 0 |
| rr | movement | rest | True | 59 | 59 | 0 | 0 | 0 | 0 | 0 | 0 |
| ug | movement | move | True | 90 | 89 | 1 | 0.0111111 | 0 | 0 | 0 | 0 |
| ug | movement | rest | True | 44 | 44 | 0 | 0 | 0 | 0 | 0 | 0 |
| wc | movement | move | True | 60 | 57 | 3 | 0.05 | 0 | 0 | 0 | 0 |
| wc | movement | rest | True | 29 | 28 | 1 | 0.0344828 | 0 | 0 | 0 | 0 |
| zt | movement | move | True | 60 | 57 | 3 | 0.05 | 0 | 0 | 0 | 0 |
| zt | movement | rest | True | 44 | 44 | 0 | 0 | 0 | 0 | 0 | 0 |

f_lo = max(1, 7/T); near means within 0.05 Hz. Full status counts and denominators: [ecog_status_floor_rates.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/ecog_status_floor_rates.csv>). Original scan/v1 boundary flags and new v3 boundary flags are retained in [status_boundary_rates.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseC/ecog/status_boundary_rates.csv>).

### Phase C figure

[ECoG_rest_fp_spectral_peak.png](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/ECoG_rest_fp_spectral_peak.png>) (300 dpi); [ECoG_rest_fp_spectral_peak.svg](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/ECoG_rest_fp_spectral_peak.svg>). No title/footer inside the figure; source CSV and commit/hash are embedded in metadata. Shading marks +/-2 Hz.

### Phase C runtime and deviations

- Worker 1: 720.390 s (ECoG and rodent).
- Worker 2: 429.889 s (ECoG and rodent).
- Worker 3: 561.228 s (ECoG and rodent).
- Worker 4: 425.288 s (ECoG and rodent).
- Read-only git inspection working directory: One exploratory git diff used the parent process folder and failed to resolve the tag. It was repeated in the repository; no file, code or signal was changed.
- Pre-gate source-verifier line endings: The verifier initially assumed LF but the source checkout uses CRLF. It now detects the original newline, reverses the permitted edits, restores that newline and requires exact original bytes. The v2 block is compared as bytes directly. No method source was altered by this fix and no gate or signal output had been computed. The initial read-only diagnostic also failed before printing the new-source branch; it made no file changes.
- Pre-gate provenance JSON field names: MATLAB jsondecode sanitised filename keys containing dots in the initial provenance struct. The source verifier now compares directly with the preserved baseline bytes and records file hashes as path/sha256 array records, avoiding filename-as-key rewriting. This metadata-reader fix occurred before any gate output; no method code or setting changed.
- Phase-B generator wrapper newline (tooling): A missing newline while copying helper functions concatenated end and function write_json into endfunction. The Poisson helper raised Undefined function endfunction before any input bank or method output was saved. Inserted one newline; original HB signal formulas, draw order and helper source now match the frozen generator exactly. Generation restarts from its fixed streams; no reportable result is recomputed.
- Matplotlib font-cache path (tooling): The initial report-only import could not write its font cache under the user profile due to sandbox permissions. No figure or estimator failed. MPLCONFIGDIR now points inside the work folder; no method or setting changed.
- Wilson error-bar round-off (tooling): Figure export rejected a negative error-bar length caused by floating-point round-off at a zero/one proportion. Plot lengths alone are bounded below by zero. Saved Wilson intervals, recovery counts, criteria and estimates are unchanged. The cached prespecified exact-test results are reused during report/export recovery; no method is rerun.
- Phase-C wrapper setup quoting (tooling): A PowerShell parsing error rejected an inline Python wrapper-copy command before it executed. The same literal replacement is performed by this saved UTF-8 Python script. No input, method source, option or estimate was changed by the failed command.
- ECoG copied Primary-2 label (tooling): The copied statistics code computed the v3-minus-scan SD difference correctly but retained the literal v1-minus-scan output label. Verified all saved patient differences against the v3 patient SD table, archived original labelled files with hashes, and replaced only that full label in the script/CSV/JSON. No number, bootstrap or method output was recomputed.
- Post-hoc CSV metadata dtype warning: Pandas emitted a mixed-type warning for metadata-only columns that are missing on the reused old rows and strings on new v3 rows. The numeric analysis columns were unaffected; the statistics completed once with unchanged formulas. No retry or setting change was made.
- Parallel workers emitted a harmless directory-already-exists warning while creating the shared checkpoint directory; each output filename belongs to one worker.

All protocol/source/prep hashes remain unchanged. No result was committed. Complete normalized-feature assertions, diagnostics and provenance are retained per unique input in `phaseC/checkpoints/`.

## Final verification

Saved-output audit: [final_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/final_verification.json>). Source, protocol, dependency and archive hashes match. The repository is clean; no result was committed. File checksums: [output_manifest.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/output_manifest.json>).
