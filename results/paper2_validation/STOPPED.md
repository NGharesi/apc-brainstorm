# STOPPED: A_EVENT input-status policy is ambiguous

Recorded 2026-10-24T11:21:13.530989+00:00 before any validation gate, signal generation or method computation.

## Completed housekeeping

- Initial branch paper2, clean tree, HEAD e69a6eeebef2cc9314ad434d8b686d910543b8a0.
- Committed and working-tree validation protocol SHA-256: b33eae54cc93bbbfe3b806e4f785dc7de88501bd0366b3cea1343be33e8a0d94.
- Ablation archive committed and pushed successfully: f66acb513fcc49f5bc4a2d7b426abe095be4dec8.
- All 73 copied source files match their manifest hashes and committed Git blobs.
- Current branch and origin/paper2 both point to the archive commit; working tree clean.
- No matching git processes or .git/*.lock files were found; nothing deleted.

## Exact ambiguity

Protocol section 2 requires A_EVENT to receive a copy of an APC output structure with only fP replaced, with "no other field changed". It defines two APC outputs, v1.0 and v3.0, and an independent F3 spectral source, but does not identify which APC output F3_A_EVENT must copy.

In unchanged src/apc_event_carrier.m, the function reads both status and fP from its input and returns immediately at `if status ~= 0 || ~isfinite(fp), return; end`. Replacing fP alone therefore does not make A_EVENT run after that base APC output failed. Copying v1.0 versus v3.0 can give different eligibility even when F3 supplies the same finite fP. This is a method-relevant choice, not a file or logging defect.

F1/F2 retaining a Step-2 estimate after later failure is explicit. Whether A_EVENT should nevertheless inherit end-to-end APC status, or should run whenever its fP source succeeds, is not explicit. The existing premise script's spectral-input structure uses status 0 and is not a copy of either APC end-to-end output; it does not resolve the new instruction.

## Clarification required before resuming

Specify whether A_EVENT eligibility follows the fP source's success or the copied APC end-to-end status. If it follows end-to-end status, specify which APC version's output F3_A_EVENT copies. The frozen apc_event_carrier.m itself will remain unchanged.

G-gen, G-event and G-abl are not run. V1-V4 are not generated. No primary, secondary, rodent or ECoG validation endpoint has been computed. No Step 2-6 output has been committed. No decision is available.
