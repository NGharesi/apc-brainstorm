# Paper 2, analysis 3: confirmatory test of the polarity-alignment effect

Written 2026-10-24, after the exploratory no-flip analysis (protocol/APC_paper2_exploratory_noflip.md; results in revision_checks/paper2_noflip). That analysis was post hoc. This protocol tests its main finding on fresh signals, generated only after this file is committed and pushed. Changes are appended as dated amendments.

## 1. Hypothesis (from the exploratory analysis)

APC's polarity alignment (`flipTroughs = true`) makes the burst-triggered average follow the dominant rhythm whether or not it is coupled. In the exploratory run, disabling the flip:
- raised coupled-rhythm fP recovery in the non-dominant two-rhythm cells from 0 to 79 of 400 (v1.0) and from 3 to 135 of 400 (v3.0);
- cut the BTA power at the dominant frequency about 25-fold;
- reduced false joint recovery in uncoupled and timing-null signals.

It also lowered recovery in V1 coupled trials (v3.0: 120 to 106 of 175).

## 2. Data (fresh; generated only after this protocol is pushed)

- **W3 (two-rhythm), seed 20261120.** Generator and design identical to V3 of the validation protocol: P1 generator, 500 Hz, 8 s, six cells, 100 repeats per cell (600 trials).
- **W1 (original regime), seed 20261121.** Generator and design identical to V1 (H1 coupled design and H3 paired timing nulls; 175 + 175).

## 3. Methods (identical signals)

- APC v1.0 and APC v3.0, each with `flipTroughs = true` (default) and `flipTroughs = false`. Step-2 fP and end-to-end. All other options are exactly as in the validation.
- F3 x A_SCAN (spectral peak + 1-D scan) and the A2' two-dimensional scan, as in the validation.
- **New combination, secondary only:** v3.0 no-flip Step-2 fP x A_SCAN (written F2nf x A_SCAN). This uses `scan_fa_given_fp.m` unchanged.
- `src` is not modified.

## 4. Endpoints (fixed here)

Recovery definitions as in the validation: fP within 1 Hz; joint adds fA within 8 Hz; strict uses fP within 0.5 Hz. Invalid outputs count as failures. Exact two-sided McNemar tests; Wilson 95% CIs.

### Primary
In W3, coupled-rhythm fP recovery pooled over the four non-dominant cells (n = 400):
- **C1:** v3.0 no-flip vs v3.0 flip;
- **C2:** v1.0 no-flip vs v1.0 flip.

Holm correction over C1 and C2.

**Decision:**
- If no-flip is significantly better in C1 or C2: "polarity alignment suppresses recovery of a coupled non-dominant rhythm (confirmed)".
- If flip is significantly better in either: "not confirmed; reversed".
- Otherwise: "not confirmed".

### Key secondary
1. W3 non-dominant cells, joint recovery: v3.0 no-flip end-to-end vs A2', and F2nf x A_SCAN vs A2'.
2. W3 N_uncoupled: false joint recovery, flip vs no-flip, for v1.0 and v3.0.
3. W1:
   - joint and strict recovery in coupled trials, flip vs no-flip (the cost where the coupled rhythm is dominant);
   - false joint recovery in timing nulls;
   - F2nf x A_SCAN vs F3 x A_SCAN.
4. Per-cell W3 counts, including dominant-rhythm picks, for every method.
5. v3.0 BTA power at the coupled and dominant frequencies in the non-dominant cells, flip vs no-flip, read from APC's returned spectrum as in the exploratory analysis.

## 5. Rules

- No signal is generated before this protocol is pushed.
- **Generator check:** regenerate the first repeat of each V3 cell (seed 20261112) and the first V1 trial (seed 20261110), and confirm they are bit-identical to the saved validation inputs.
- Each run is done once. Tooling defects may be fixed once, only if identifiable without looking at outcomes, and are logged.
- Every result is reported whatever its direction.

## 6. Outputs

`revision_checks\paper2_noflip_confirm\`:
- `RESULTS_confirm.md`, with the decision stated in exactly one of the forms above;
- per-trial CSV;
- statistics CSV;
- `provenance.json`;
- one figure: W3 per-cell coupled-rhythm recovery and dominant picks for all methods, plus W1 joint recovery; 300-dpi PNG and SVG; no titles or footers inside the image.
