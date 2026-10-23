# iEEG attempt 2 execution notes

Both committed amendments were pushed before resumed dataset signal reads.
Current public protocol: 2b2bb08ff17fd96b1e520f9125e46655cd69786b;
SHA-256 6f457fd2a2ca714abec723728e1a6617ef23b938f3da03bd025030642d63ad58.

The second synthetic equivalence run passed. All 68 iEEG files passed their
amended native-rate, sample, variance, unit/range and per-trial resampling
checks. All 68 scalp files passed their 200-Hz trialwise resampling checks.
The scalp timing gate passed: 160-ms encoding and 200-ms probe peaks, at
5-ms resolution, across all 3353 trials. No dataset PAC outcome exists.

Common preprocessing, before any candidate ranking or inclusion decision:

- Read candidate contacts from the original BIDS files (using the two
  previously verified header-only compatibility copies where necessary).
- Cut each native 8-s trial separately; apply the committed resample ratios
  to produce exactly 16000 samples at 2000 Hz.
- Form each candidate bipolar k minus k+1; retain the deeper contact signal
  separately for the prespecified referential sensitivity.
- Remove the mean of each full trial. Apply zero-phase 50/100/150-Hz
  Butterworth bandstops, half-width 1 Hz, as SOS. The specified fourth-order
  digital bandstop is realized with butter prototype order 2 (four poles),
  then filtfilt. Assert four poles and maximum pole radius below one.
- Retain samples 6001:12000, corresponding to [3,6) s at 2000 Hz.
- Save double-precision maintenance arrays and metadata for every candidate;
  no spectrum, contact choice, rejection mask, APC or scan is computed here.
- Resume by verified per-session cache rather than recomputing finished
  inputs. Original source and tagged files remain unchanged.

The required contact-ranking/rejection order is pending the user's answer
to the clarification referencing protocol sections 3.3 and 3.5. No candidate
power ratio or fixed contact selection will be computed before that answer.

APC will continue through the original v1_bout_features helper, without
editing it. A separate diagnostic-only copy of frozen Step 1 computes the
burst count that the helper does not expose; its count is checked against
the saved synthetic gate output without an additional APC estimator call.
