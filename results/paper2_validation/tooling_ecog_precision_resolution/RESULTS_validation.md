# Paper-2 validation: stopped during ECoG reproduction

Archive commit pushed: `f66acb513fcc49f5bc4a2d7b426abe095be4dec8`. Protocol Amendment 1 pushed: `dbc0d7901091602e146e4d28b22fdadb043daef4`. Branch `paper2` and origin/paper2 match; working tree clean at the stop. Protocol SHA-256: `7b461e92a09d1a282225f07415d27ca7a4525984d3dab0ca5fc9c444700b6080`.

## Initial stop and Amendment 1 resolution

The pre-gate A_EVENT ambiguity was resolved by Amendment 1 and processing resumed at 2026-10-24T11:27:12.980681+00:00. A_EVENT receives only `struct('status_code', s, 'fp_hz', fP)`, with zero status whenever the source returns finite fP. The original [STOPPED.md](STOPPED.md) remains unchanged. The transfer file `amend1_validation.md` was ignored. Earlier report text is retained in [RESULTS_before_ecog_stop.md](RESULTS_before_ecog_stop.md).

## Gates

| Gate | Result |
| --- | --- |
| G-gen HB | PASS; 675/675 complete cases bit-identical, including H1 |
| G-gen HA | PASS; 900/900 complete cases bit-identical |
| P1 double generation | PASS; repeat 1 in each of six cells, no outcomes computed |
| G-event | PASS; original/minimal/repeated canonical calls agree at 1e-12 |
| G-abl APC | PASS; 42 cases at 1e-10 |
| G-abl scan | PASS; 23 cases at 1e-10 |
| Configuration adapters | PASS; unchanged scan computations reproduced |

Gate details: [all_gate_results.json](all_gate_results.json), [gate_apc.csv](gate_apc.csv), [gate_scan.csv](gate_scan.csv), [adapter_verification.json](adapter_verification.json).

## Execution completed before the stop

| Dataset | Completed inputs | Planned inputs | Rows per input |
| --- | ---: | ---: | ---: |
| V1 | 350 | 350 | 12 |
| V2 | 900 | 900 | 12 |
| V3 | 600 | 600 | 12 |
| V4 | 25 | 25 | 12 |
| Rodent physical inputs | 3646 | 3646 | 4 |
| ECoG bouts | 39 | 2642 | 5 |

All simulation and rodent checkpoints and incremental worker CSVs remain in place. Signals were generated after the protocol push with seeds 20261110/11/12/13, preserving original generator order. Input/source hashes, options and environment are recorded in [provenance.json](provenance.json). No new signal was generated on this resume. Nine simulation pipelines and three references ran per input. Rodent physical inputs map to 3982 regional/bout-set rows, retaining separate prespecified 5-s and POST HOC 2-s datasets.

## Active reproduction stop

Bout: `ca_movement_020`. Error: `Validation:EcogScanReproduction` at `validation_real_worker.m:56`.

| Quantity | Recomputed | Saved ablation reference | Absolute difference |
| --- | ---: | ---: | ---: |
| fP (Hz) | 4.3870772473281363 | 4.3870772473281425 | 6.2172489379008766e-15 |
| fA (Hz) | 116 | 116 | 0 |
| Normalized MVL | 0.061318589373410254 | 0.061318589823546682 | 4.5013642813174215e-10 |

Required absolute tolerance: `1e-10`. The normalized-MVL difference exceeds it. The cause has not been investigated and the tolerance has not been changed. No failing bout has been rerun.



The four workers and workflow controller stopped. The fixed tolerance and all method settings remain unchanged. Details: [STOPPED_ACTIVE.md](STOPPED_ACTIVE.md), [stop_audit.json](stop_audit.json), [preserved evidence](ecog_reproduction_stop).

## Endpoints not evaluated

P-A, P-B and P-C have not been computed; no prespecified decision can be stated. Secondary recovery, errors, AUC, calibrated specificity/power, rodent statistics and ECoG summaries have not been computed. Their prerequisite ECoG run is incomplete. No figures were generated and no final-completion verification was claimed. The statistics controller stopped before invoking `validation_statistics.py`.

## Runtime and deviations

Stop time: 2026-10-24T16:27:54.138745+00:00. Wall time since Amendment-1 resume: 5.011 hours, including interruptions. Gate elapsed 79.889 s. Generation time after its tooling restart is in `generation_complete.json`; individual simulation timers are in `worker1_complete.json` through `worker4_complete.json`. The successful ECoG resume ran until the reproduction assertion; its logs are preserved under `ecog_reproduction_stop/`.

- **GEN_METADATA_SEED_SCOPE**: Seed was parameterized in a local metadata function but omitted from its formal/call arguments. Pass unchanged seed to verification_row; preserve and compare the already-written configuration on resume.

- **SAVED_RODENT_CSV_PRECISION**: Exact deduplication of shared physical inputs incorrectly required equality of rounded raw/phase/coupling CSV fields. Shared physical bounds, fP, fA and status match exactly; raw values were written at different precision. Preserve every original reference row by bout-set and analysis, keep one physical reference for computation, and audit all numeric CSV differences separately.

- **DIAGNOSTIC_STRUCT_CONTAINER**: MATLAB rejected subscripted assignment while building the diagnostic agreement structure. Use a cell container for agreement metadata; no method computations, options or numeric criteria changed.

- **SAVED_BOOLEAN_CSV_PARSE**: MATLAB readtable returns saved True/False valid values as string; logical(string) is unsupported. All four workers stopped at their first ECoG reference row, before saving an ECoG checkpoint. Parse saved true/false and 1/0 explicitly; numeric/logical values retain their original conversion. No estimator, options, reproduction assert or numerical criterion changed.

The saved-boolean parsing fix was identified from the conversion error and code without inspecting numerical outcomes. The later saved-result reproduction failure above is a new stop, not a tooling fix. No protocol, tagged method, seed, grid or tolerance was changed. Validation outputs are uncommitted.
