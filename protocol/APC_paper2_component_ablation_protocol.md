# Paper 2, analysis 1: which component of APC adds information? Prespecified component-ablation protocol

Written 2026-10-23, after the APC v3.0 evaluation (protocol/APC_v3_aperiodic_protocol.md, tag v3.0) and before any analysis described here. Committed and pushed before it is run; changes are appended as dated amendments.

## 1. Question

The v3.0 evaluation showed three things:
1. An aperiodic-corrected spectral peak of the raw signal (SP-raw) estimates fP at least as precisely as APC.
2. In aperiodic (1/f) signals, APC's amplitude-carrier step (fA) is weaker than the scans'.
3. APC's false recovery in timing nulls rose with v3.0.

This analysis separates APC into its two estimation stages and tests each against a burst-free alternative on identical signals. No new signals are generated.

- **Stage F (phase frequency), three sources:**
  - F1 = APC v1.0 Step 2;
  - F2 = APC v3.0 Step 2;
  - F3 = SP-raw.
- **Stage A (amplitude carrier given fP), two rules:**
  - A_APC = APC Steps 3-4 at the given fP: trough-locked envelope-waveform cross-correlation, band half-width = fP; burst-anchored through the trough average.
  - A_SCAN = a one-dimensional MVL-Ozkurt scan over the amplitude grid at the fixed fP: phase band fP +/- 1.5 Hz; amplitude half-width 30 Hz in HA and ECoG, 14 Hz in HB, matching the A2' configurations.
- **Pipelines:** six (F1-F3 x A_APC/A_SCAN), plus two references, the full two-dimensional MVL-Ozkurt scan (A2') and APC v1.0/v3.0 as run end-to-end.
- **Coupling** for every pipeline = normalized MVL at its selected pair, computed with the same phase-band rule (fP +/- max(0.5, 0.25 fP)) and the selected amplitude band.

## 2. Data (all existing; identical inputs)

- HA coupled trials and paired timing nulls (seed 20261101; 450 + 450), from `revision_checks/v3_aperiodic`.
- HB: H1, H2, H4 coupled trials, H3 timing nulls and the no-coupled-burst controls (seed 20261022), regenerated bit-identically as in the v3.0 evaluation.
- ECoG: prep files, bouts and electrodes from `revision_checks/ecog_miller_motor` (movement recording, 18 eligible patients; imagery recording as secondary).

## 3. Implementation

- `apc_fa_given_fp.m`:
  - an exact extraction of APC v3.0 Steps 3-4 from `src/bst_apc.m` (tag v3.0), taking fP as input instead of computing it;
  - no other change.
  - **Gate:** at fP = APC's own estimate, it must reproduce APC v1.0 and v3.0 fA, raw MVL and preferred phase to within 1e-10 on the canonical input and on the first 20 HA trials. Stop if not.
- `scan_fa_given_fp.m`:
  - the A2' MVL-Ozkurt computation restricted to one phase band (SOS-guarded filters, unchanged metric and tie rule);
  - **Gate:** at an fP on the A2' grid, it must reproduce the A2' score column for that fP to within 1e-10.

## 4. Endpoints (fixed here)

- **E1 (primary): does burst-anchored fA selection add information?**
  - For each fP source F1-F3, compare A_APC vs A_SCAN on joint recovery (fP within 1 Hz and fA within 8 Hz) in HA and in H1 separately. Paired exact McNemar test (two-sided). Six contrasts; Holm correction within each dataset.
  - **Interpretation:**
    - A_APC significantly better for most fP sources: burst anchoring helps fA;
    - A_SCAN significantly better: it does not;
    - otherwise: no difference shown.
- **E2: fP sources.** fP recovery (within 1 Hz) and strict recovery (within 0.5 Hz) for F1-F3 in HA, H1, H2 and H4, with mean and median absolute error. Paired exact McNemar tests F2 vs F3 and F1 vs F3. Descriptive for H2 and H4.
- **E3: specificity.**
  - False joint recovery in paired timing nulls (HA nulls; H3) for all eight methods.
  - AUC of each method's coupling value, coupled vs its paired null (HA; H1 vs H3 pairs), with bootstrap 95% CIs (10,000 resamples of pairs, seed 20261102).
  - Key comparison: AUC of A_APC vs A_SCAN at each fP source, by paired bootstrap of the AUC difference.
- **E4: ECoG (descriptive).** For the six pipelines and two references:
  - rest-fP agreement with the rest spectral peak (within 2 Hz; count of 18 patients);
  - the movement-minus-rest coupling contrast (patient bootstrap, 10,000, seed 20261024);
  - within-state fP SD.

## 5. Rules

- No signal, setting, grid, tolerance or seed is changed.
- Each reportable run is done once. Tooling fixes are logged, and a defect may be fixed once only if it can be identified without looking at outcomes.
- A failed gate stops the run.
- All results are reported whatever their direction.

## 6. Outputs

`C:\Users\nghare\.brainstorm\process\revision_checks\paper2_ablation\`:
- `RESULTS_ablation.md`;
- per-trial and per-bout CSVs;
- statistics CSV;
- `provenance.json`;
- figures as 300-dpi PNG and SVG, with no titles or footers inside the image:
  - recovery by pipeline for HA and H1;
  - AUC by pipeline;
  - ECoG rest-fP agreement by pipeline.

## Amendment 1 (2026-10-23): method count

Codex flagged that section 1 lists nine methods but sections 2 and 4 say "eight". The correct number is nine: the six F x A pipelines, the full two-dimensional MVL-Ozkurt scan (A2'), APC v1.0 end-to-end and APC v3.0 end-to-end. All nine are reported as separate methods.

F1 x A_APC and F2 x A_APC should equal APC v1.0 and v3.0 end-to-end by construction (gate in section 3). Their agreement is reported as a consistency check: the number of inputs with identical fP, fA and coupling, and any differences. Nothing else changes.
