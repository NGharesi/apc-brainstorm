"""Create reviewer-facing Figure 4 source-data and inference tables.

This uses the existing full benchmark trial CSV; it does not rerun simulations.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
RUNS = ROOT / "apc_burst_sparsity_runs_full.csv"
N_BOOT = 10_000
SEED = 20261004
METHODS = ["APC", "MVL-scan", "KLMI-scan", "GLM-scan"]


def wilson(k: int, n: int) -> tuple[float, float]:
    z = 1.959963984540054
    p = k / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    half = z / denom * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return max(0.0, center - half), min(1.0, center + half)


def quantile_ci(values: np.ndarray) -> tuple[float, float]:
    return tuple(np.quantile(values, [0.025, 0.975]).tolist())


def main() -> None:
    runs = pd.read_csv(RUNS)
    rng = np.random.default_rng(SEED)
    summaries: list[dict[str, object]] = []
    paired: list[dict[str, object]] = []

    for keep_rate in sorted(runs.burst_keep_rate.unique()):
        condition = runs.loc[runs.burst_keep_rate.eq(keep_rate)]
        apc = condition.loc[condition.method.eq("APC")].sort_values("repeat_index")
        for method in METHODS:
            sub = condition.loc[condition.method.eq(method)].sort_values("repeat_index")
            n = len(sub)
            row: dict[str, object] = {
                "burst_keep_rate": keep_rate,
                "method": method,
                "n": n,
            }
            for field, label in [
                ("pair_correct", "pair_recovery"),
                ("fa_correct", "fa_recovery"),
                ("fp_correct", "fp_recovery"),
            ]:
                k = int(sub[field].sum())
                lo, hi = wilson(k, n)
                row.update({f"{label}_count": k, f"{label}_proportion": k / n,
                            f"{label}_ci_low": lo, f"{label}_ci_high": hi})
            for field, label in [
                ("fa_abs_error_hz", "fa_error"),
                ("fp_abs_error_hz", "fp_error"),
            ]:
                values = sub[field].to_numpy(float)
                means = values[rng.integers(0, n, size=(N_BOOT, n))].mean(axis=1)
                lo, hi = quantile_ci(means)
                row.update({
                    f"{label}_mean_hz": values.mean(),
                    f"{label}_mean_ci_low": lo,
                    f"{label}_mean_ci_high": hi,
                    f"{label}_median_hz": np.median(values),
                    f"{label}_q1_hz": np.quantile(values, 0.25),
                    f"{label}_q3_hz": np.quantile(values, 0.75),
                    f"{label}_zero_count": int(np.count_nonzero(values == 0)),
                    f"{label}_zero_proportion": np.mean(values == 0),
                })
            summaries.append(row)

            if method == "APC":
                continue
            other = sub.set_index("repeat_index").loc[apc.repeat_index]
            for field, label in [("pair_correct", "pair_recovery"),
                                 ("fa_correct", "fa_recovery"),
                                 ("fp_abs_error_hz", "fp_error"),
                                 ("fa_abs_error_hz", "fa_error")]:
                diff = apc[field].to_numpy(float) - other[field].to_numpy(float)
                estimates = diff[rng.integers(0, n, size=(N_BOOT, n))].mean(axis=1)
                lo, hi = quantile_ci(estimates)
                paired.append({
                    "burst_keep_rate": keep_rate,
                    "comparison": f"APC minus {method}",
                    "outcome": label,
                    "n_paired": n,
                    "difference": diff.mean(),
                    "ci_low": lo,
                    "ci_high": hi,
                })

    summary = pd.DataFrame(summaries)
    paired_table = pd.DataFrame(paired)
    summary.to_csv(ROOT / "apc_burst_sparsity_reviewer_summary.csv", index=False)
    paired_table.to_csv(ROOT / "apc_burst_sparsity_reviewer_paired_intervals.csv", index=False)

    sparse = summary.loc[summary.burst_keep_rate.eq(summary.burst_keep_rate.min())]
    dense = summary.loc[summary.burst_keep_rate.eq(summary.burst_keep_rate.max())]
    lines = [
        "Figure 4 reviewer-control inference summary",
        "All conditions contain n = 25 paired simulation repeats per method.",
        "Recovery intervals are two-sided 95% Wilson binomial intervals.",
        "Mean-error and paired-difference intervals are percentile 95% bootstrap intervals (10,000 resamples).",
        "",
        "Sparsest keep rate (0.15):",
    ]
    for _, row in sparse.iterrows():
        lines.append(
            f"{row.method}: pair {row.pair_recovery_count}/{row.n} "
            f"({row.pair_recovery_proportion:.2f}; {row.pair_recovery_ci_low:.2f}-{row.pair_recovery_ci_high:.2f}); "
            f"fA {row.fa_recovery_count}/{row.n}; fP zero error {row.fp_error_zero_count}/{row.n}."
        )
    lines.extend(["", "Densest keep rate (1.00):"])
    for _, row in dense.iterrows():
        lines.append(
            f"{row.method}: pair {row.pair_recovery_count}/{row.n} "
            f"({row.pair_recovery_proportion:.2f}; {row.pair_recovery_ci_low:.2f}-{row.pair_recovery_ci_high:.2f}); "
            f"fA mean error {row.fa_error_mean_hz:.2f} Hz "
            f"[{row.fa_error_mean_ci_low:.2f}, {row.fa_error_mean_ci_high:.2f}]."
        )
    (ROOT / "apc_burst_sparsity_reviewer_inference_summary.txt").write_text("\n".join(lines) + "\n",encoding="utf-8")


if __name__ == "__main__":
    main()
