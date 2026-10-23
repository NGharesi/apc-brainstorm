# APC v2 candidate 3 unit results

Final candidate authorized by the user. All ordered unit gates passed. Commit/tag and held-out execution remain conditional on the source attestation.

## Factual summary (8 lines)

1. a=PASS, a2=PASS, b=PASS, c=PASS, d=COMPLETE.

2. Completed unit trial rows: 41; each has BLP/PPC and raw fA-score curves.

3. The five v1 compatibility cases exactly matched the v1.0 reference.

4. Step-2 and event outputs exactly matched candidate 2 on the unchanged unit-(a) signal.

5. Direct BLP/surrogate, PPC, Gaussian FFT formula, diagnostic-isolation and RNG checks passed.

6. The C1-C4 text is unchanged from the original committed protocol.

7. All performance gates passed before any held-out data generation.

8. No further candidate was made.

## Candidate history and fixed method

Candidate 2 failed gate (a) only on fA=115 Hz (error 5 Hz); its fP=7.9996901239320914 Hz passed. The user diagnosed a bimodal Step-4 score from Butterworth band edges. This history and the final authorization are recorded in [PROTOCOL_v2.md](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/PROTOCOL_v2.md>). The prior report is preserved at [RESULTS_v2.md](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_02/RESULTS_v2.md>).

Only Step 4 changes: one-second mirror padding excluding repeated endpoints; FFT; positive-frequency gain 2*exp(-(f-fc)^2/(2*sigma^2)), zero at nonpositive frequencies; sigma=1.5*fP; inverse FFT/crop; raw MVL on the unchanged fP phase. No score smoothing or Gaussian-tail clipping. Select the 1-Hz grid maximum, refine an interior concave maximum by a three-point parabola, and recompute the envelope at refined fA for both raw C_APC and Ozkurt MVL. BLP, both event-test statistics, Steps 1/3 and all inherited profiles/seeds remain unchanged. Gaussian sigma is recorded explicitly; obsolete finite-band widths/edges are NaN.

## Ordered unit gates

| Gate | Criterion | Result |
| --- | --- | --- |
| a | \|fP-8\|<=0.1 Hz and \|fA-120\|<=4 Hz | PASS |
| a2 | Pairs (5.3,95),(6.7,108),(9.4,131),(10.8,142); phase error<=0.1 and amplitude error<=4 | PASS |
| b | Same 8/120 signal + 11-Hz sinusoid at 3x; phase error<=0.5 | PASS |
| c | Poisson: corrected event p>0.05 on at least 8/10 seeds | PASS |
| d | Run first 25 existing level-0 distractor inputs; report without tuning | COMPLETE |

| Test | Trial | True fP | True fA | Recovered fP | Recovered fA | fP error | fA error | C_APC | Ozkurt | Max-event z | Max-event p | Fixed-event z | Fixed-event p | Bursts/usable | Flags | Status | Pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| a | 1 | 8 | 120 | 7.999690124 | 119.9309632 | 0.0003098760679 | 0.06903683588 | 0.1176832549 | 0.2140626659 | 32.63989034 | 0.004975124378 | 25.79496691 | 0.004975124378 | 48/32 | 0 | 0 | 1 |
| a2 | 1 | 5.3 | 95 | 5.299750371 | 94.87151044 | 0.0002496294879 | 0.1284895588 | 0.1420362461 | 0.3332173348 | 25.3130205 | 0.004975124378 | 19.74824808 | 0.004975124378 | 31/21 | 0 | 0 | 1 |
| a2 | 2 | 6.7 | 108 | 6.699982271 | 108.0244096 | 1.7728743e-05 | 0.02440956679 | 0.1347020646 | 0.2728652035 | 35.12116345 | 0.004975124378 | 26.27379946 | 0.004975124378 | 40/27 | 0 | 0 | 1 |
| a2 | 3 | 9.4 | 131 | 9.400296575 | 130.9881122 | 0.0002965746268 | 0.01188781345 | 0.0841901317 | 0.1398685717 | 36.07601306 | 0.004975124378 | 27.5241325 | 0.004975124378 | 56/38 | 0 | 0 | 1 |
| a2 | 4 | 10.8 | 142 | 10.80013371 | 141.4071834 | 0.0001337133928 | 0.5928165696 | 0.05581920924 | 0.08873104374 | 24.9132193 | 0.004975124378 | 19.75808593 | 0.004975124378 | 59/39 | 0 | 0 | 1 |
| b | 1 | 8 | 120 | 8.000358738 | 119.9991156 | 0.0003587384413 | 0.000884391727 | 0.1052879752 | 0.1914599191 | 3.440762781 | 0.01990049751 | 25.56152474 | 0.004975124378 | 47/32 | 0 | 0 | 1 |
| c | 1 | 8 | 120 | 7.991356154 | 121.4887384 | 0.008643846162 | 1.488738385 | 0.005956920365 | 0.01931831202 | 0.1335177605 | 0.2487562189 | 0.4467506416 | 0.2487562189 | 24/16 | 0 | 0 | 1 |
| c | 2 | 8 | 120 | 8.129063052 | 120.5083859 | 0.129063052 | 0.5083858862 | 0.006876521605 | 0.02266220313 | -0.5305527847 | 0.3880597015 | 0.01922607892 | 0.3731343284 | 22/12 | 0 | 0 | 1 |
| c | 3 | 8 | 120 | 28.46850648 | 122.2652278 | 20.46850648 | 2.265227803 | 0.0034168446 | 0.01150298378 | -0.4484035526 | 0.6965174129 | 3.167871001 | 0.01492537313 | 26/19 | 0 | 0 | 1 |
| c | 4 | 8 | 120 | 8.002595036 | 120.8563964 | 0.002595036195 | 0.8563963671 | 0.01525137828 | 0.04580329545 | 0.4136115588 | 0.1791044776 | 0.7224603699 | 0.1791044776 | 25/17 | 0 | 0 | 1 |
| c | 5 | 8 | 120 | 3.177829186 | 119.8727446 | 4.822170814 | 0.1272553629 | 0.01889940034 | 0.06589124594 | -0.4712533952 | 0.8258706468 | 0.8621261488 | 0.1592039801 | 26/19 | 0 | 0 | 1 |
| c | 6 | 8 | 120 | 6.640767969 | 122.1076089 | 1.359232031 | 2.107608886 | 0.002197960776 | 0.008891089728 | -0.5342886952 | 0.8258706468 | 1.105520519 | 0.1393034826 | 27/19 | 0 | 0 | 1 |
| c | 7 | 8 | 120 | 5.73826255 | 114.6870501 | 2.26173745 | 5.312949881 | 0.00515212643 | 0.01696716267 | -0.5649177535 | 0.7313432836 | 2.918772569 | 0.02985074627 | 29/21 | 0 | 0 | 1 |
| c | 8 | 8 | 120 | 7.999749525 | 120.2076177 | 0.0002504754846 | 0.2076177176 | 0.009266218821 | 0.03723445139 | 0.7735803735 | 0.1691542289 | 0.921757512 | 0.1691542289 | 19/13 | 0 | 0 | 1 |
| c | 9 | 8 | 120 | 8.00212754 | 121.499804 | 0.002127539704 | 1.499804006 | 0.005619760652 | 0.01854594225 | 0.3124576716 | 0.223880597 | 0.5823132663 | 0.223880597 | 23/17 | 0 | 0 | 1 |
| c | 10 | 8 | 120 | 5.936323377 | 125.3593009 | 2.063676623 | 5.359300905 | 0.002238789349 | 0.01115596822 | -0.4952172582 | 0.7263681592 | 2.759826714 | 0.02487562189 | 24/15 | 0 | 0 | 1 |
| d | 1 | 8 | 120 | 7.975998143 | 119.6107097 | 0.02400185745 | 0.3892902555 | 0.1046953299 | 0.1698642666 | 3.842118912 | 0.01990049751 | 3.229604175 | 0.01990049751 | 90/62 | 0 | 0 | 1 |
| d | 2 | 8 | 120 | 7.995288197 | 120.5516985 | 0.004711803484 | 0.5516984554 | 0.1009469308 | 0.159723536 | 1.834799514 | 0.07462686567 | 1.790417584 | 0.07462686567 | 90/60 | 0 | 0 | 1 |
| d | 3 | 8 | 120 | 8.005918325 | 122.6106679 | 0.005918324699 | 2.610667869 | 0.09414858598 | 0.1522597091 | 0.6294036348 | 0.1094527363 | 0.9603668126 | 0.1094527363 | 89/59 | 0 | 0 | 1 |
| d | 4 | 8 | 120 | 8.025680038 | 120.6825026 | 0.02568003831 | 0.6825025851 | 0.09163065663 | 0.1495018744 | 0.427921239 | 0.1592039801 | 0.7390269263 | 0.1592039801 | 99/65 | 0 | 0 | 1 |
| d | 5 | 8 | 120 | 7.996230207 | 119.7811756 | 0.003769792616 | 0.2188244466 | 0.1005154239 | 0.1565027576 | 2.530284487 | 0.0447761194 | 2.361210195 | 0.0447761194 | 91/62 | 0 | 0 | 1 |
| d | 6 | 8 | 120 | 8.030684974 | 119.5374792 | 0.03068497377 | 0.462520792 | 0.1118959054 | 0.1790689839 | 0.9971112479 | 0.1094527363 | 1.199852694 | 0.1094527363 | 100/68 | 0 | 0 | 1 |
| d | 7 | 8 | 120 | 8.045288959 | 121.5096629 | 0.04528895949 | 1.509662871 | 0.09430373793 | 0.1455476617 | -0.4294470867 | 0.5323383085 | 0.1072775051 | 0.3532338308 | 96/65 | 0 | 0 | 1 |
| d | 8 | 8 | 120 | 7.989314077 | 120.2518427 | 0.01068592266 | 0.251842727 | 0.08356006318 | 0.1317052649 | 3.412063412 | 0.02487562189 | 2.981013988 | 0.02487562189 | 91/55 | 0 | 0 | 1 |
| d | 9 | 8 | 120 | 8.002384199 | 120.1136835 | 0.002384198942 | 0.1136835448 | 0.1021132277 | 0.1628057795 | 0.6165702137 | 0.144278607 | 0.9657555207 | 0.1393034826 | 97/63 | 0 | 0 | 1 |
| d | 10 | 8 | 120 | 7.995355636 | 118.4146282 | 0.00464436391 | 1.58537183 | 0.1148383736 | 0.1772572869 | 7.8280076 | 0.004975124378 | 6.242643956 | 0.004975124378 | 95/63 | 0 | 0 | 1 |
| d | 11 | 8 | 120 | 8.007212087 | 118.3483285 | 0.007212087128 | 1.651671475 | 0.09954766982 | 0.1643362455 | 1.037096261 | 0.1194029851 | 1.215680494 | 0.1194029851 | 95/68 | 0 | 0 | 1 |
| d | 12 | 8 | 120 | 8.043605679 | 118.9037379 | 0.04360567942 | 1.096262139 | 0.09785920397 | 0.1522114249 | -0.02706299587 | 0.2537313433 | 0.4090155481 | 0.2437810945 | 99/65 | 0 | 0 | 1 |
| d | 13 | 8 | 120 | 7.945605037 | 119.1064201 | 0.05439496287 | 0.8935798505 | 0.1017501008 | 0.1694037386 | 1.536171876 | 0.09452736318 | 1.626881891 | 0.09452736318 | 88/60 | 0 | 0 | 1 |
| d | 14 | 8 | 120 | 8.174098428 | 119.261032 | 0.1740984282 | 0.7389680171 | 0.1027623664 | 0.1682004462 | -0.3308994836 | 0.3482587065 | 0.251446449 | 0.2985074627 | 104/72 | 0 | 0 | 1 |
| d | 15 | 8 | 120 | 8.005920472 | 119.6304657 | 0.005920472264 | 0.36953431 | 0.1137727397 | 0.1851368374 | 1.853795029 | 0.07960199005 | 1.773843709 | 0.07462686567 | 92/63 | 0 | 0 | 1 |
| d | 16 | 8 | 120 | 7.99203634 | 119.8766928 | 0.007963660041 | 0.1233072216 | 0.09979888912 | 0.1632924808 | 2.807608147 | 0.02985074627 | 2.525244647 | 0.02985074627 | 97/65 | 0 | 0 | 1 |
| d | 17 | 8 | 120 | 7.984705019 | 119.2492641 | 0.01529498134 | 0.7507359342 | 0.09561376022 | 0.1563020705 | 2.890683375 | 0.02985074627 | 2.621564905 | 0.02985074627 | 89/62 | 0 | 0 | 1 |
| d | 18 | 8 | 120 | 7.949317009 | 119.6373548 | 0.05068299132 | 0.3626451788 | 0.0920050729 | 0.1392289518 | -0.101103599 | 0.2487562189 | 0.3942677304 | 0.2388059701 | 97/63 | 0 | 0 | 1 |
| d | 19 | 8 | 120 | 7.971594049 | 120.0134573 | 0.02840595092 | 0.01345730197 | 0.08357031168 | 0.1359695746 | 0.473096171 | 0.1890547264 | 0.7658826489 | 0.184079602 | 103/72 | 0 | 0 | 1 |
| d | 20 | 8 | 120 | 7.885017891 | 120.538389 | 0.1149821086 | 0.5383889636 | 0.07624029253 | 0.1199332995 | 1.017352163 | 0.1542288557 | 1.243911014 | 0.1243781095 | 86/54 | 0 | 0 | 1 |
| d | 21 | 8 | 120 | 7.965932892 | 121.1792299 | 0.03406710845 | 1.179229909 | 0.1150628078 | 0.1899614318 | 3.144445565 | 0.01990049751 | 2.817127418 | 0.01492537313 | 89/58 | 0 | 0 | 1 |
| d | 22 | 8 | 120 | 7.98277209 | 121.708523 | 0.01722791027 | 1.708522976 | 0.1044395403 | 0.1647416604 | 2.245119703 | 0.0447761194 | 2.055123534 | 0.0447761194 | 92/60 | 0 | 0 | 1 |
| d | 23 | 8 | 120 | 7.976318587 | 119.7224015 | 0.02368141331 | 0.2775984611 | 0.09978236739 | 0.1586382806 | 3.822783918 | 0.009950248756 | 3.079370123 | 0.009950248756 | 92/58 | 0 | 0 | 1 |
| d | 24 | 8 | 120 | 8.004814449 | 118.0057131 | 0.004814448552 | 1.994286909 | 0.1102809351 | 0.1710774103 | 9.844939737 | 0.004975124378 | 7.520173838 | 0.004975124378 | 90/58 | 0 | 0 | 1 |
| d | 25 | 8 | 120 | 7.998880179 | 119.95182 | 0.001119821235 | 0.04818002427 | 0.09875139761 | 0.1635122178 | 1.680321727 | 0.07960199005 | 1.691946543 | 0.07960199005 | 93/65 | 0 | 0 | 1 |

Per-trial data: [unit_trials.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_trials.csv>). Gate record: [unit_results.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_results.json>). Checks: [implementation_checks.json](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/implementation_checks.json>).

| BLP/PPC curve | Raw Gaussian fA-score curve |
| --- | --- |
| [unit_a2_01_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_a2_01_curves.csv>) | [unit_a2_01_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_a2_01_fa_scores.csv>) |
| [unit_a2_02_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_a2_02_curves.csv>) | [unit_a2_02_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_a2_02_fa_scores.csv>) |
| [unit_a2_03_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_a2_03_curves.csv>) | [unit_a2_03_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_a2_03_fa_scores.csv>) |
| [unit_a2_04_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_a2_04_curves.csv>) | [unit_a2_04_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_a2_04_fa_scores.csv>) |
| [unit_a_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_a_curves.csv>) | [unit_a_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_a_fa_scores.csv>) |
| [unit_b_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_b_curves.csv>) | [unit_b_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_b_fa_scores.csv>) |
| [unit_c_01_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_01_curves.csv>) | [unit_c_01_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_01_fa_scores.csv>) |
| [unit_c_02_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_02_curves.csv>) | [unit_c_02_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_02_fa_scores.csv>) |
| [unit_c_03_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_03_curves.csv>) | [unit_c_03_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_03_fa_scores.csv>) |
| [unit_c_04_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_04_curves.csv>) | [unit_c_04_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_04_fa_scores.csv>) |
| [unit_c_05_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_05_curves.csv>) | [unit_c_05_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_05_fa_scores.csv>) |
| [unit_c_06_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_06_curves.csv>) | [unit_c_06_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_06_fa_scores.csv>) |
| [unit_c_07_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_07_curves.csv>) | [unit_c_07_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_07_fa_scores.csv>) |
| [unit_c_08_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_08_curves.csv>) | [unit_c_08_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_08_fa_scores.csv>) |
| [unit_c_09_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_09_curves.csv>) | [unit_c_09_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_09_fa_scores.csv>) |
| [unit_c_10_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_10_curves.csv>) | [unit_c_10_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c_10_fa_scores.csv>) |
| [unit_d_01_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_01_curves.csv>) | [unit_d_01_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_01_fa_scores.csv>) |
| [unit_d_02_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_02_curves.csv>) | [unit_d_02_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_02_fa_scores.csv>) |
| [unit_d_03_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_03_curves.csv>) | [unit_d_03_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_03_fa_scores.csv>) |
| [unit_d_04_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_04_curves.csv>) | [unit_d_04_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_04_fa_scores.csv>) |
| [unit_d_05_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_05_curves.csv>) | [unit_d_05_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_05_fa_scores.csv>) |
| [unit_d_06_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_06_curves.csv>) | [unit_d_06_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_06_fa_scores.csv>) |
| [unit_d_07_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_07_curves.csv>) | [unit_d_07_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_07_fa_scores.csv>) |
| [unit_d_08_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_08_curves.csv>) | [unit_d_08_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_08_fa_scores.csv>) |
| [unit_d_09_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_09_curves.csv>) | [unit_d_09_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_09_fa_scores.csv>) |
| [unit_d_10_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_10_curves.csv>) | [unit_d_10_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_10_fa_scores.csv>) |
| [unit_d_11_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_11_curves.csv>) | [unit_d_11_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_11_fa_scores.csv>) |
| [unit_d_12_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_12_curves.csv>) | [unit_d_12_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_12_fa_scores.csv>) |
| [unit_d_13_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_13_curves.csv>) | [unit_d_13_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_13_fa_scores.csv>) |
| [unit_d_14_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_14_curves.csv>) | [unit_d_14_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_14_fa_scores.csv>) |
| [unit_d_15_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_15_curves.csv>) | [unit_d_15_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_15_fa_scores.csv>) |
| [unit_d_16_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_16_curves.csv>) | [unit_d_16_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_16_fa_scores.csv>) |
| [unit_d_17_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_17_curves.csv>) | [unit_d_17_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_17_fa_scores.csv>) |
| [unit_d_18_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_18_curves.csv>) | [unit_d_18_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_18_fa_scores.csv>) |
| [unit_d_19_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_19_curves.csv>) | [unit_d_19_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_19_fa_scores.csv>) |
| [unit_d_20_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_20_curves.csv>) | [unit_d_20_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_20_fa_scores.csv>) |
| [unit_d_21_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_21_curves.csv>) | [unit_d_21_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_21_fa_scores.csv>) |
| [unit_d_22_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_22_curves.csv>) | [unit_d_22_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_22_fa_scores.csv>) |
| [unit_d_23_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_23_curves.csv>) | [unit_d_23_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_23_fa_scores.csv>) |
| [unit_d_24_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_24_curves.csv>) | [unit_d_24_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_24_fa_scores.csv>) |
| [unit_d_25_curves.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_25_curves.csv>) | [unit_d_25_fa_scores.csv](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d_25_fa_scores.csv>) |

MAT checkpoints, including inputs, intermediate arrays, both surrogate-statistic vectors and full provenance: [unit_a.mat](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_a.mat>), [unit_a2.mat](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_a2.mat>), [unit_b.mat](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_b.mat>), [unit_c.mat](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_c.mat>), [unit_d.mat](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/unit_d.mat>).

## Freeze state and held-out decisions

These gates were run on working sources before the conditional commit. Recorded git_commit is the candidate-1 base commit `7848af05ada722971769da856e970d0737820169`; exact tested method blob is `7fc5e8c2f0ad32a79df652beb824e6d14b46d67e`. Source snapshot: [bst_apc.m](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01/source_snapshot/bst_apc.m>). This source remained unchanged during the gates. Candidate-1/2 snapshots remain available.

| Criterion | Status |
| --- | --- |
| C1 | Pending frozen held-out execution |
| C2 | Pending frozen held-out execution |
| C3 | Pending frozen held-out execution |
| C4 | Pending frozen held-out execution |

## Runtime, deviations and preservation

Unit-driver runtime=167.733939 seconds, excluding MATLAB startup. One computation thread; MATLAB 9.13.0.2105380 (R2022b) Update 2. [unit_attempt_01_matlab.log](<C:/Users/nghare/.brainstorm/process/revision_checks/v2/candidate_03/unit_attempt_01_matlab.log>).

Implementation bug fixes after unit execution: none.

Tooling deviations during unit execution: none. The existing protocol mirror and separate candidate output folder preserve earlier records. Pre-existing missing Brainstorm startup paths may appear in the log. All Python text I/O explicitly uses UTF-8.

Candidate-2 saved-file hashes verified unchanged: 16. Source checks confirm unchanged v1 calculations, Steps 1/2/3 and the entire candidate-2 event-test block. No further candidate was made.

## Full unit provenance

```json
{
  "candidate": 3,
  "git_commit": "7848af05ada722971769da856e970d0737820169",
  "git_worktree_status": "M analysis/v2_revision/PROTOCOL_v2.md\n M analysis/v2_revision/run_v2_units.m\n M src/bst_apc.m\n?? analysis/v2_revision/build_candidate2_results.py",
  "source_committed": false,
  "tag": "not_created",
  "matlab_version": "9.13.0.2105380 (R2022b) Update 2",
  "signal_seed": 20260618.0,
  "heldout_seed": 20261022.0,
  "heldout_generated": false,
  "apc_options": {
    "fA": [
      80,
      160
    ],
    "epoch": [
      -0.6,
      0.6
    ],
    "decomposition": "fft_peak",
    "metric": "canolty",
    "diagm": false,
    "surrogates": false,
    "num_perm": 0,
    "numPhaseBins": 18,
    "burstTimeBandwidth": 5,
    "phaseTimeBandwidth": 20,
    "phaseEpochCycles": 3,
    "minPhaseHz": 1,
    "maxPhaseHz": 30,
    "flipTroughs": true,
    "burstProminenceScale": 0.75,
    "surrogateMethod": "circular_shift",
    "amplitudeBandWidthHz": 4,
    "stepFourMode": "v1",
    "fPRefine": true,
    "fPMaxBinSpacingHz": 0.05,
    "version": "v2",
    "eventSurrogateSeed": 20260619.0,
    "eventSurrogateSubstream": 2
  },
  "comparator_settings": {
    "phase_grid_hz": [
      3,
      3.5,
      4,
      4.5,
      5,
      5.5,
      6,
      6.5,
      7,
      7.5,
      8,
      8.5,
      9,
      9.5,
      10,
      10.5,
      11,
      11.5,
      12,
      12.5,
      13,
      13.5,
      14
    ],
    "phase_half_width_hz": 1.5,
    "amplitude_grid_hz": [
      80,
      84,
      88,
      92,
      96,
      100,
      104,
      108,
      112,
      116,
      120,
      124,
      128,
      132,
      136,
      140,
      144,
      148,
      152,
      156,
      160
    ],
    "A2_prime_half_width_hz": 14,
    "A1_prime_half_width": "candidate fP",
    "metrics": [
      "MVL-raw",
      "MVL-Ozkurt",
      "KLMI",
      "GLM"
    ]
  },
  "base_tag": "v1.0",
  "base_commit": "71ebc16aed32ca38be73a800738b975e5806b330",
  "apc_source_blob": "7fc5e8c2f0ad32a79df652beb824e6d14b46d67e",
  "protocol_git_blob": "acbf9e2a19bd3d34a9ece8186a109c036fbc8a28",
  "unit_profile": {
    "profile_name": "reviewer_control",
    "random_seed": 20260618.0,
    "fs_hz": 500,
    "duration_s": 6,
    "true_fp_hz": 8,
    "true_fa_hz": 120,
    "distractor_fa_hz": 96,
    "phase_offset_deg": 180,
    "low_amp": 1,
    "true_high_amp": 1.3,
    "distractor_base_amp": 0,
    "base_hf_amp": 0.08,
    "burst_sigma_s": 0.028,
    "coupling_level": 0.6,
    "burst_phase_jitter_s": 0.01,
    "snr_db": 20,
    "broad_fa_band_hz": [
      80,
      160
    ],
    "phase_scan_hz": [
      4,
      5,
      6,
      7,
      8,
      9,
      10,
      11,
      12
    ],
    "amplitude_scan_hz": [
      80,
      88,
      96,
      104,
      112,
      120,
      128,
      136,
      144,
      152
    ],
    "phase_band_half_width_hz": 1.5,
    "amplitude_band_half_width_hz": 6,
    "metric": "canolty",
    "fa_tolerance_hz": 8,
    "fp_tolerance_hz": 1,
    "oracle_control_distractor_scale": 0,
    "n_repeats": 25,
    "distractor_scale_values": [
      0,
      0.5,
      1,
      1.5,
      2,
      2.5,
      3
    ],
    "slow_distractor_hz": 11,
    "slow_amplitude_ratios": [
      0,
      3
    ],
    "slow_distractor_phase_rad": 0,
    "slow_amplitude_ratio": 0,
    "high_frequency_distractor_present": false
  },
  "surrogate_generator": "mrg32k3a",
  "surrogate_seed": 20260619.0,
  "surrogate_substream": 2,
  "unit_poisson_seeds": [
    20260618.0,
    20260619.0,
    20260620.0,
    20260621.0,
    20260622.0,
    20260623.0,
    20260624.0,
    20260625.0,
    20260626.0,
    20260627.0
  ],
  "unit_poisson_generator": "mrg32k3a",
  "unit_poisson_substream": 3,
  "uncoupled_phase_seed": 20260619.0,
  "uncoupled_phase_generator": "mrg32k3a",
  "uncoupled_phase_substream": 1,
  "repository": "C:\\Users\\nghare\\.brainstorm\\process\\apc-brainstorm-publish"
}
```
