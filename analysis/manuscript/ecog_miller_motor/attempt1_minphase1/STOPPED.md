# STOPPED: protocol rule 9.4 (APC invalid in more than half of bouts)

Stopped 2026-10-23 ~11:33 local, after the first combined check at 200 bouts: APC v1.0 returned status 4 (no complete trough epochs) in 127 of 200 bouts. At the moment all four workers halted, 225 bouts were complete: 149 status 4, 76 valid (movement 36/143 valid, rest 40/82 valid; patients bp, ca, cc, de, gf).

All gates passed before the run: protocol public on origin before download (230ec14), state coding documented (0 rest, 11 tongue, 12 hand; codes 13 in gf and 15 in zt undocumented and not analysed), APC equivalence (max difference 3.69e-13), comparator copy verified (only the "ecog" profile added).

Valid APC fP values were bimodal: about 3-6 Hz and about 13-17 Hz (beta); medians 6.1 Hz (rest) and 7.8 Hz (movement). The four scans (phase grid 6-30 Hz) returned estimates for every bout; the MVL-Ozkurt scan selected the lower grid edge (6 Hz) in 40 of 225 bouts.

Interpretation (not tested): APC searches phase frequencies from 1 Hz (default), whereas the scans start at 6 Hz. In 2-s bouts, Step 2 is drawn to slow components (including the 1-2 Hz repetitive movement during movement blocks); at those frequencies the +/-3-cycle trough epochs of Step 3 do not fit in the bout, giving status 4.

No endpoint was computed. Partial estimates (estimates_w1-4.csv), prep files, inventory, electrodes and bouts are preserved. No setting was changed.
