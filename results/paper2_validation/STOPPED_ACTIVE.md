# STOPPED: ECoG saved-result reproduction

Recorded 2026-10-24T16:27:54.138745+00:00. All four workers have exited. No statistics or new figures were run.

Bout: `ca_movement_020`. Error: `Validation:EcogScanReproduction` at `validation_real_worker.m:56`.

| Quantity | Recomputed | Saved ablation reference | Absolute difference |
| --- | ---: | ---: | ---: |
| fP (Hz) | 4.3870772473281363 | 4.3870772473281425 | 6.2172489379008766e-15 |
| fA (Hz) | 116 | 116 | 0 |
| Normalized MVL | 0.061318589373410254 | 0.061318589823546682 | 4.5013642813174215e-10 |

Required absolute tolerance: `1e-10`. The normalized-MVL difference exceeds it. The cause has not been investigated and the tolerance has not been changed. No failing bout has been rerun.

Completed checkpoints: V1 350, V2 900, V3 600, V4 25; rodent 3646; ECoG 39 of 2642. All are retained. The ECoG run and endpoint calculations remain incomplete. `ecog_reproduction_stop/` preserves the automatic stop, source, all four error JSONs and resumed-worker logs. `stop_audit.json` records their hashes.

The original pre-gate `STOPPED.md` is unchanged, as instructed. The new stop is recorded here to preserve that record. HEAD and origin/paper2 are `dbc0d7901091602e146e4d28b22fdadb043daef4`; the working tree is clean. Protocol hash: `7b461e92a09d1a282225f07415d27ca7a4525984d3dab0ca5fc9c444700b6080`. No validation results were committed.
