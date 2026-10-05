# APC Brainstorm Process

This repository contains the Brainstorm implementation of amplitude-phase coupling (APC), reproducible scripts for the manuscript benchmarks, and compact derived results and figures. It does not contain raw electrophysiology data, participant identifiers, or manuscript drafts.

## Contents

- `src/`: Brainstorm process and core APC/PAC functions.
- `analysis/`: MATLAB and Python scripts used for the simulation, rodent LFP, sleep-EEG, and operational-validation analyses.
- `results/figures/`: publication-ready main and supplementary figures.
- `results/tables/`: compact derived statistics, confidence intervals, and model summaries.

## Requirements

The analyses were run with MATLAB R2022b Update 2 (9.13.0.2105380), Signal Processing Toolbox 9.1, Statistics and Machine Learning Toolbox 12.4, and Brainstorm 3.230117 (17-Jan-2023; commit `fa0ec3a4d72b66f6d36d4fa2ed6d2ff588fae0f7`). The core process also uses Wavelet Toolbox functionality. Python analysis scripts require standard scientific packages including NumPy, pandas, SciPy, and statsmodels.

## Installation

Copy `src/bst_apc.m`, `src/process_apc.m`, and `src/calc_MI_all_methods.m` to the Brainstorm user-process folder:

- Windows: `%USERPROFILE%/.brainstorm/process`
- macOS/Linux: `$HOME/.brainstorm/process`

Restart Brainstorm or reopen the Process window. APC is available under `Frequency > Amplitude-Phase Coupling (APC)`.

## Reproduction notes

Simulation scripts generate their inputs internally. The rodent LFP and Sleep-EDF scripts require the corresponding external datasets and local paths to be configured before running. The repository provides derived, non-identifiable result tables so reported figures and statistics can be inspected without redistributing those source recordings.

The Sleep-EDF wideband analysis uses the same prespecified 4-30 Hz amplitude-frequency search range for both channels. Its boundary-hit diagnostic is retained in the result tables; recovered amplitude-carrier values should not be interpreted as validated spindle-frequency estimates when those diagnostics are high.

`run_apc_operational_validation.m` is included as a negative quality-control analysis. Its outputs demonstrate that the currently tested APC surrogate calibration and minimum-event rules do not support operational significance thresholds or artifact-rejection claims.

## Data and ethics

No human raw data are included. Sleep-EDF is a publicly available PhysioNet dataset; users must follow its access and reuse terms. The rodent data analysis likewise requires the original source dataset and its applicable terms. This repository distributes only code and derived summary results.

## License

This software is released under the MIT License; see [LICENSE](LICENSE).
