# Amendment 3 execution

Public commit 37c21dbe249881fdc021655a855c000434b3ac54; protocol SHA-256 087c51b1e5b930dca55e3c1ce63af15c891252399a3da1abc68407b27a2df308.

The common preprocessed arrays are reused unchanged from the Amendment-2 stage; only candidate masking/ranking is new. All original source/helper hashes were rechecked.

{
  "welch_window": "hann(2000), MATLAB symmetric default",
  "welch_overlap_samples": 1000,
  "welch_nfft": 2000,
  "welch_fs_hz": 2000,
  "power_integral": "trapz over inclusive 4-8 Hz and 1-4 Hz bins",
  "trial_weights": "equal retained trials pooled across sessions",
  "amplitude_reject": "any abs(x-session_median)>6*1.4826*MAD",
  "difference_reject": "any abs(within-trial diff)>6*1.4826*MAD(diff)",
  "robust_pool": "all maintenance samples of dataset-unflagged trials in the same candidate/session",
  "sensitivity_a": "same selected pair, dataset flags only",
  "sensitivity_b": "same selected pair and final bipolar mask, deeper-contact signal only",
  "sensitivity_c": "primary paired endpoint restricted to native-2000-Hz patients"
}

No candidate spectrum or PAC output preceded this record. Sensitivities retain the primary selected pair; (a) changes only the trial mask to dataset flags, (b) changes only the signal to the deeper contact and uses the selected pair final mask.
