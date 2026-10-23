# STOPPED: most completed inputs invalid for APC v1.0

The run stopped under protocol section 6.4 after Amendment 3. At the first stop check, 325/422 completed unique trial-signal inputs (77.0%) returned status 4. After already-running work finished, 326/425 (76.7%) returned status 4; 99 returned status 0. These are partial-run rates.

The partial run covers 2 patients and 6 sessions; only 3 sessions completed all planned inputs. It contains 3165 method rows and 425 unique input checkpoints. All four comparators returned valid status/finite scores on these completed inputs.

All three workers stopped. The incremental CSV and checkpoints are preserved. No dataset method was rerun and no method setting was changed. No null analysis, primary/secondary endpoint, sensitivity endpoint test, exploratory model or final endpoint figure was computed. No primary decision is stated from a partial run.

Status 4 has two return conditions in the unchanged source: empty detected troughs, or empty phase-locked average/TF output. The saved status does not distinguish those conditions; no diagnostic rerun was made.

Protocol commit `37c21dbe249881fdc021655a855c000434b3ac54`; SHA-256 `087c51b1e5b930dca55e3c1ce63af15c891252399a3da1abc68407b27a2df308`. Protocol, src and tagged method code remain untouched. No results were committed.

Full gate/contact/mask/partial-run report: [RESULTS_ieeg.md](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/RESULTS_ieeg.md>). First stop snapshot: [method_failure_first_snapshot.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/method_failure_first_snapshot.json>). Final counts: [STATUS.json](<C:/Users/nghare/.brainstorm/process/revision_checks/ieeg_ds004752/STATUS.json>).
