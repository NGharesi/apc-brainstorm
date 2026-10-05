"""Compute exact uncertainty summaries for the Figure 3 reviewer-control run."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
RUNS = ROOT / "apc_distractor_frequency_runs_reviewer_control.csv"
ORACLE = ROOT / "apc_distractor_frequency_oracle_runs_reviewer_control.csv"
N_BOOTSTRAP = 10_000
RNG = np.random.default_rng(20261004)


def wilson_interval(successes: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n == 0:
        return np.nan, np.nan
    proportion = successes / n
    denominator = 1 + z**2 / n
    center = (proportion + z**2 / (2 * n)) / denominator
    half_width = z * np.sqrt(proportion * (1 - proportion) / n + z**2 / (4 * n**2)) / denominator
    return center - half_width, center + half_width


def paired_bootstrap_ci(values: np.ndarray) -> tuple[float, float, float]:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if values.size == 0:
        return np.nan, np.nan, np.nan
    sampled_indices = RNG.integers(0, values.size, size=(N_BOOTSTRAP, values.size))
    means = values[sampled_indices].mean(axis=1)
    lower, upper = np.quantile(means, [0.025, 0.975])
    return values.mean(), lower, upper


def bootstrap_auc_ci(coupled: np.ndarray, null: np.ndarray) -> tuple[float, float, float]:
    coupled = np.asarray(coupled, dtype=float)
    null = np.asarray(null, dtype=float)
    coupled = coupled[np.isfinite(coupled)]
    null = null[np.isfinite(null)]
    if coupled.size == 0 or null.size == 0:
        return np.nan, np.nan, np.nan

    def auc(x: np.ndarray, y: np.ndarray) -> float:
        return (np.greater(x[:, None], y[None, :]).mean() +
                0.5 * np.equal(x[:, None], y[None, :]).mean())

    observed = auc(coupled, null)
    bootstrap = np.empty(N_BOOTSTRAP)
    for index in range(N_BOOTSTRAP):
        x = coupled[RNG.integers(0, coupled.size, coupled.size)]
        y = null[RNG.integers(0, null.size, null.size)]
        bootstrap[index] = auc(x, y)
    lower, upper = np.quantile(bootstrap, [0.025, 0.975])
    return observed, lower, upper


def main() -> None:
    runs = pd.read_csv(RUNS)
    oracle = pd.read_csv(ORACLE, keep_default_na=False)
    methods = ["APC", "MVL-scan", "KLMI-scan", "GLM-scan"]
    scales = sorted(runs["distractor_scale"].unique())

    recovery_rows = []
    paired_rows = []
    for scale in scales:
        scale_data = runs[runs["distractor_scale"] == scale]
        apc = scale_data[scale_data["method"] == "APC"].set_index("repeat_index")
        for method in methods:
            sub = scale_data[scale_data["method"] == method]
            successes = int(sub["pair_correct"].sum())
            n = len(sub)
            lower, upper = wilson_interval(successes, n)
            recovery_rows.append({
                "distractor_amplitude_scale": scale,
                "method": method,
                "n": n,
                "joint_pair_recovery_count": successes,
                "joint_pair_recovery_proportion": successes / n,
                "wilson_95_ci_lower": lower,
                "wilson_95_ci_upper": upper,
            })
            if method != "APC":
                comparator = sub.set_index("repeat_index").loc[apc.index]
                for outcome in ["pair_correct", "fa_abs_error_hz", "fp_abs_error_hz"]:
                    difference = apc[outcome].to_numpy() - comparator[outcome].to_numpy()
                    mean_difference, ci_lower, ci_upper = paired_bootstrap_ci(difference)
                    paired_rows.append({
                        "distractor_amplitude_scale": scale,
                        "comparison": f"APC minus {method}",
                        "outcome": outcome,
                        "n_pairs": len(difference),
                        "mean_paired_difference": mean_difference,
                        "bootstrap_95_ci_lower": ci_lower,
                        "bootstrap_95_ci_upper": ci_upper,
                    })

    oracle_rows = []
    for method in sorted(oracle["method"].unique()):
        for scale in sorted(oracle["distractor_scale"].unique()):
            sub = oracle[(oracle["method"] == method) & (oracle["distractor_scale"] == scale)]
            coupled = sub.loc[sub["signal_condition"] == "coupled", "score"].to_numpy()
            null = sub.loc[sub["signal_condition"] == "null", "score"].to_numpy()
            auc, lower, upper = bootstrap_auc_ci(coupled, null)
            oracle_rows.append({
                "distractor_amplitude_scale": scale,
                "method": method,
                "n_coupled": len(coupled),
                "n_null": len(null),
                "auc_coupled_vs_null": auc,
                "bootstrap_95_ci_lower": lower,
                "bootstrap_95_ci_upper": upper,
            })

    recovery = pd.DataFrame(recovery_rows)
    paired = pd.DataFrame(paired_rows)
    oracle_summary = pd.DataFrame(oracle_rows)
    recovery.to_csv(ROOT / "apc_distractor_frequency_reviewer_control_recovery_intervals.csv", index=False)
    paired.to_csv(ROOT / "apc_distractor_frequency_reviewer_control_paired_intervals.csv", index=False)
    oracle_summary.to_csv(ROOT / "apc_distractor_frequency_reviewer_control_oracle_intervals.csv", index=False)

    lines = [
        "Figure 3 reviewer-control inferential summary",
        "",
        "Recovery proportions use Wilson 95% confidence intervals (n = 25 per method and scale).",
        "Paired APC-minus-comparator differences and oracle AUC intervals use 10,000 percentile bootstrap samples.",
        "",
        "Known-pair positive control: MVL and GLM reliably distinguish coupled from null trials; KLMI is weaker.",
    ]
    (ROOT / "apc_distractor_frequency_reviewer_control_inference_summary.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print("Wrote Figure 3 interval summaries.")


if __name__ == "__main__":
    main()
