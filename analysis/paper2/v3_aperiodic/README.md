# Archived APC v3.0 evaluation

Snapshot of the completed v3 evaluation, copied on branch `paper2` before paper-2 component-ablation analysis. Original files remain unchanged in `revision_checks/v3_aperiodic/` outside the repository.

- Frozen method: tag `v3.0`, commit `1cb2056fb16eaf944857c8d3f11a51276d5b7a1f`.
- Paper-2 protocol base: `815ac24154385a3b4e7e5acbe9daf65c941adfb7`.
- Entry point: `RESULTS_v3.md`; current state/provenance: `STATUS.json`, `provenance.json`, `final_verification.json`.
- Includes Phase A gates and curves, the failed residual-location attempt, HA/HB evaluation tables, Phase C rodent/ECoG tables, figures (PNG/SVG), MATLAB/Python scripts, source diffs, model-fit text logs and execution logs.
- CSVs larger than 2,000,000 bytes are stored as deterministic `.csv.gz` files. Decompression recovers the exact original bytes. Other included files are byte-identical copies. Diff `.patch` files and model `_fit.txt` logs are included alongside `.diff` and `.log` files.
- MAT checkpoints, generated signal banks, runtime caches and other binary data are omitted. Original report links/provenance paths are preserved; some point to local inputs/checkpoints that are not in this archive.
- `archive_manifest.json` lists every archived path, original/archive sizes and SHA-256 values; original full-run manifests may also list omitted local MAT files.

## File counts by original suffix

| Suffix | Files |
| --- | --- |
| .csv | 255 |
| .diff | 15 |
| .json | 64 |
| .log | 14 |
| .m | 34 |
| .md | 3 |
| .patch | 2 |
| .png | 3 |
| .py | 27 |
| .svg | 3 |
| .txt | 12 |

Total archived source files: 432; compressed CSVs: 26. No `.mat` file is included.
