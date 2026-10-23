# APC v3 aperiodic correction: stopped at G1

**Prespecified gate G1 failed.** Canonical v3: status 0, fP 8.6902612490498399 Hz, fA 121 Hz; |fP-8|=0.69026124904983988 Hz and |fA-120|=1 Hz. Required: status 0, <=0.1-Hz fP error and <=8-Hz fA error. The phase stopped with no redesign, freeze, held-out generation or real-data evaluation. [STOPPED.md](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/STOPPED.md>).

## Public protocol and implementation provenance

Clean `neuroimage-submission` HEAD `8cabe20538b55f5185a20630f19fd7162b9bb269` was pushed before v3 implementation. Protocol SHA-256 `c2d8ede3fb994d6ef90f9757abbd993ed33e8e0a082288cb7501458d64a1bbb7` matches. The protocol was not edited. MATLAB 9.13.0.2105380 (R2022b) Update 2; complete toolbox versions and baseline source hashes: [provenance.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/provenance.json>). The gate-tested source is uncommitted and identified by SHA-256 in [phaseA_implementation.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseA_implementation.json>) and preserved in `phaseA_source_snapshot/`. No results were committed.

v3 is an explicit version selection; default v1 remains unchanged. The implementation shares v1 Steps 1, 3 and 4, and substitutes the two-pass aperiodic residual peak rule only for v3 Step 2. SP-raw uses the same fitting/peak helper on its specified raw-signal Hann/50%-overlap Welch spectrum. T=N/fs; residual sigma uses sample SD; the parabolic delta is clipped to +/-0.5 bin. Complete pre-gate numerical/generator conventions are in [phaseA_implementation.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/phaseA_implementation.json>).

The new delta reverses byte-for-byte to the pre-implementation source, preserving the v2 block and metric helper. This branch already contained v2 additions relative to v1.0: those are separately preserved in [preexisting_v1_tag_diff.patch](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/preexisting_v1_tag_diff.patch>). The newly introduced diff contains the v3 additions/version switch only. [source_additions_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/source_additions_verification.json>); [v3_implementation.diff](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/v3_implementation.diff>).

## Gate decisions


| gate | result |
| --- | --- |
| G0 | PASS |
| G1 | FAIL |
| G2 | NOT_RUN |
| G3 | NOT_RUN |

## G0: default/v1 and v2 regression

Canonical tolerance: 1e-10. The reference numbers and observed default-v1 outputs are:

| metric | expected | observed | absolute_difference |
| --- | --- | --- | --- |
| fP_hz | 7.99792313404 | 7.99792313404 | 3.5527136788e-15 |
| fA_hz | 122 | 122 | 0 |
| raw_MVL | 0.176907779166 | 0.176907779166 | 1.38777878078e-16 |
| preferred_phase_deg | 178.575795411 | 178.575795411 | 3.69482222595e-13 |

Complete v1 output/runInfo equality against tag v1.0: True. Default versus explicit version=v1 equality: True. Complete v2 output/runInfo equality against tag v2.0: True.


| source | phase_frequency_hz | amplitude_frequency_hz | pac_strength | preferred_phase_deg | status_code |
| --- | --- | --- | --- | --- | --- |
| referenceV2 | 7.99910518273 | 120.003982644 | 0.262898816036 | 177.123364829 | 0 |
| currentV2 | 7.99910518273 | 120.003982644 | 0.262898816036 | 177.123364829 | 0 |

Tagged reference outputs and complete structures: [G0.mat](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/G0.mat>); checks [G0.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/G0.json>); [G0_v2_reproduction.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/G0_v2_reproduction.csv>).

## G1: canonical v3

Canonical v3: status 0, fP 8.6902612490498399 Hz, fA 121 Hz; |fP-8|=0.69026124904983988 Hz and |fA-120|=1 Hz. Required: status 0, <=0.1-Hz fP error and <=8-Hz fA error.


| method | status | fP_hz | fA_hz | score | n_bursts | exponent | offset | peak_height | sigma | f_lo_hz |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APC-v3.0 | 0 | 8.69026124905 | 121 | 0.196770683265 | 182 | 1.35571458693 | -3.07299921649 | 3.02580281103 | 0.337337868733 | 1 |

Saved complete canonical v3 result/diagnostics: [G1.mat](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/G1.mat>). Welch, fit and residual curve: [G1_curve.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/G1_curve.csv>). No diagnostic estimator rerun was needed.

## G2: development cells

Prespecified design: beta={1,2}, T={2,6} s, fs=1000 Hz, unit-SD development-family 1/f^beta noise; 15-Hz sine amplitude 0.6; 110-Hz bursts with 10-ms Gaussian sigma and amplitude 1.5; Bernoulli 55% cycle retention and 5-ms Gaussian timing jitter; 20 paired v3/v1 repeats per cell, seed 20261031. Pass requires >=16/20 v3 fP estimates within 1 Hz of 15 Hz in every cell. Invalid outputs count as failures.

G2 was not run because an earlier gate failed. No G2 signal was generated.

## G3, freeze and later phases

G3 was not run after the required-gate failure. Its status-3 rate and fP distribution are therefore unavailable. No freeze commit or v3.0 tag was created or pushed. The HA held-out generator was not written, and neither HA nor regenerated HB signals were generated.

A1, A2 (v3 versus SP-raw), A3 and A4 were not evaluated. No adoption decision based on these criteria is available. Phase C rodent/ECoG analyses did not run. The HA and ECoG evaluation figures were not generated because their phases did not run. No empty result/figure placeholders are supplied.

## A2: v3 versus SP-raw (not evaluated)

The prespecified key secondary comparison is unavailable because G1 failed before the held-out phase. No claim about added information from burst timing is made.

## Runtime and deviations

Phase-A gate timer: 48.909 s, excluding MATLAB startup. Tagged reference and modified-source calls were each run once as specified; no completed gate was repeated and no method was tuned after an outcome.

- Read-only git inspection working directory: One exploratory git diff used the parent process folder and failed to resolve the tag. It was repeated in the repository; no file, code or signal was changed.
- Pre-gate source-verifier line endings: The verifier initially assumed LF but the source checkout uses CRLF. It now detects the original newline, reverses the permitted edits, restores that newline and requires exact original bytes. The v2 block is compared as bytes directly. No method source was altered by this fix and no gate or signal output had been computed. The initial read-only diagnostic also failed before printing the new-source branch; it made no file changes.
- Pre-gate provenance JSON field names: MATLAB jsondecode sanitised filename keys containing dots in the initial provenance struct. The source verifier now compares directly with the preserved baseline bytes and records file hashes as path/sha256 array records, avoiding filename-as-key rewriting. This metadata-reader fix occurred before any gate output; no method code or setting changed.
- Existing MATLAB startup warnings refer to missing historical Brainstorm paths; the gate driver explicitly verifies repository/reference source precedence.

Final verification: [final_verification.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/final_verification.json>). File inventory: [output_manifest.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v3_aperiodic/output_manifest.json>).
