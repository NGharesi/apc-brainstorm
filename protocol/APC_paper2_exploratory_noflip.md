# Paper 2, exploratory analysis E-NF: does polarity alignment make APC follow the dominant rhythm?

Written 2026-10-24, after the validation results (protocol/APC_paper2_validation_protocol.md, Amendment 1) were seen. This analysis is **post hoc and exploratory**. It was motivated by P-C: APC v1.0's burst-triggered fP returned the stronger uncoupled rhythm in 395 of 400 non-dominant two-rhythm trials. It is reported as exploratory in any paper, whatever it shows, and it cannot change any validation decision.

## Hypothesis

APC Step 1 flips trough-centred epochs (`flipTroughs = true`, the default) so the burst-triggered average (BTA) has consistent polarity. If the flip decision follows the sign of the largest low-frequency deflection, flipping can make an uncoupled but stronger rhythm average coherently. The coupled rhythm is then suppressed in the BTA spectrum. If this is the mechanism, APC with `flipTroughs = false` should recover the coupled rhythm in the non-dominant cells far more often than with the default.

## Data and methods

- Saved inputs only; nothing is regenerated:
  - V3, all six cells (600 trials) — main;
  - V1 coupled trials and timing nulls (350);
  - V2 coupled trials and timing nulls (900);
  - V4 (25).
- Methods, all with the settings used in the validation, varying only `flipTroughs`:
  - APC v1.0, Step-2 fP and end-to-end, with `flipTroughs = false` (new);
  - APC v3.0, Step-2 fP and end-to-end, with `flipTroughs = false` (new);
  - the saved default (`flipTroughs = true`) results are reused for comparison.
- No other option, grid, seed or tolerance changes. `src/bst_apc.m` is not modified (the option already exists).

## Outcomes (descriptive)

1. **V3 non-dominant cells (n = 400, and per cell):**
   - coupled-rhythm fP recovery (within 1 Hz);
   - dominant-rhythm picks;
   - joint recovery;
   - for each, flip vs no-flip, with exact McNemar p-values labelled exploratory.
2. **V3 single coupled rhythm and uncoupled control:** the same counts, and false joint recovery in N_uncoupled.
3. **V1, V2 and V4:** joint and strict recovery, plus false joint recovery in the timing nulls, flip vs no-flip. This shows what the polarity flip buys where the coupled rhythm is also the spectral peak.
4. **Mechanism diagnostics, from APC's outputs where available:**
   - number of detected bursts;
   - fraction of epochs flipped;
   - in V3 non-dominant cells, the BTA spectral power at the coupled vs the dominant frequency, with and without the flip.

   Items that `bst_apc` does not output are reported as not available; no code is added to `src` to expose them.

## Rules

- Each run is done once. Tooling defects may be fixed once, only if identifiable without looking at outcomes, and are logged.
- All results are reported whatever their direction, under the heading "exploratory".
- Outputs go to `revision_checks\paper2_noflip\`:
  - `RESULTS_noflip.md`;
  - per-trial CSV;
  - `provenance.json`;
  - one figure (V3 per-cell coupled-rhythm recovery and dominant picks, flip vs no-flip; 300-dpi PNG and SVG; no titles or footers inside the image).
