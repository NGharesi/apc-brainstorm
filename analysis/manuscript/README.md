# Analysis code and source data for the APC manuscript

All results in the manuscript were produced with the frozen method code tagged in this
repository:

- **APC v1.0** (primary method): tag `v1.0`, commit `71ebc16aed32ca38be73a800738b975e5806b330`
- **APC v2.0** (negative result, Supplementary Note S1): tag `v2.0`, commit `217fd8373759150cdeffe794d231a7cec2225f38`

This folder holds the analysis scripts, protocols, reports and source-data tables. Large
per-trial tables are gzip-compressed (`*.csv.gz`). Binary checkpoints (`.mat`, `.npz`) are
not included; they can be regenerated with the scripts. Absolute Windows paths in the
scripts refer to the original analysis computer.

| Folder | Content | Manuscript |
| --- | --- | --- |
| `repro_diagnosis/` | Reconstruction of the code versions behind earlier draft results | Methods (Development and held-out evaluation) |
| `v1_rerun/` | Freeze of v1.0 and development-suite rerun (main, random fP, nulls) | Supplementary Figure S1 |
| `v1_followup/` | Fixed-width comparators, status-4 diagnosis, slow-rhythm scenario (development) | Methods; Supplement |
| `v2/` | v2 protocol, candidate history, unit gates and held-out evaluation | Supplementary Note S1, Figure S2 |
| `final/` | Second-order-section comparator correction (`final_sos_filter.m`, `sos_comparators.m`), held-out v1.0 vs A2' tables, canonical examples, Figures 1-5 and S1-S2 | Figures 1-5, Table 1 |
| `rodent_multi/` | Regional channel map, tracking-rate behaviour, prespecified 5-s run/rest analysis | Figure 6, Figures S3-S4 |
| `rodent_multi/posthoc_2s/` | Post hoc 2-s sensitivity analysis | Figure 7 |
| `ec013_layout_check/` | Data-driven check of the EC013 channel-to-shank layout | Methods (Rodent recordings) |
| `ieeg_ds004752/` | Prespecified human intracranial analysis (OpenNeuro ds004752): gates, contact selection, both stopped attempts (`attempt1_maintenance_3s/`, Amendment 4 run), stop records. Protocol: `protocol/APC_ieeg_ds004752_protocol.md`. Per-trial checkpoints and preprocessed signals are not included. | Methods and Results (Human intracranial recordings) |
| `ecog_miller_motor/` | Prespecified human ECoG analysis (Miller ECoG library, motor task): inventory, gates, electrode selection, both runs (`attempt1_minphase1/` and the Amendment 1 run), per-bout estimates, statistics and figure. Protocol: `protocol/APC_ecog_miller_motor_protocol.md`. Preprocessed signals (`prep/`) are not included. | Methods and Results (Human electrocorticography), Figure 8 |

Comparator filters: fourth-order Butterworth band-pass, realized as second-order sections
(`[z,p,k]=butter(4,...); [sos,g]=zp2sos(z,p,k); filtfilt(sos,g,x)`), with a pole-radius and
centre-gain guard on every band. The earlier direct-form realization was numerically
inaccurate for narrow low-frequency bands and is superseded.
