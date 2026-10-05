"""Exact Figure 5 APC run/rest statistics from saved EC013 bout results."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "apc_ec013_run_rest_summary.csv"
N_BOOT = 20_000


def _betacf(a: float, b: float, x: float) -> float:
    """Continued fraction for the regularized incomplete beta function."""
    max_iter, eps, fpmin = 200, 3e-14, 1e-300
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / max(abs(d), fpmin) * (1 if d >= 0 else -1)
    h = d
    for m in range(1, max_iter + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d; d = 1.0 / max(abs(d), fpmin) * (1 if d >= 0 else -1)
        c = 1.0 + aa / c; c = c if abs(c) > fpmin else fpmin
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d; d = 1.0 / max(abs(d), fpmin) * (1 if d >= 0 else -1)
        c = 1.0 + aa / c; c = c if abs(c) > fpmin else fpmin
        delta = d * c; h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def regularized_beta(x: float, a: float, b: float) -> float:
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    front = np.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * np.log(x) + b * np.log1p(-x))
    if x < (a + 1) / (a + b + 2):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1 - x) / b


def welch_two_sided_p(t_stat: float, df: float) -> float:
    if not np.isfinite(t_stat): return np.nan
    return regularized_beta(df / (df + t_stat**2), df / 2, 0.5)


def welch_summary(run: np.ndarray, rest: np.ndarray, rng: np.random.Generator) -> dict[str, float]:
    n1, n2 = len(run), len(rest)
    mean_diff = float(run.mean() - rest.mean())
    var1, var2 = run.var(ddof=1), rest.var(ddof=1)
    se2 = var1 / n1 + var2 / n2
    df = se2**2 / ((var1 / n1) ** 2 / (n1 - 1) + (var2 / n2) ** 2 / (n2 - 1))
    t_stat = mean_diff / np.sqrt(se2) if se2 > 0 else np.nan
    p = welch_two_sided_p(t_stat, df)
    pooled = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    d = mean_diff / pooled if pooled > 0 else np.nan
    correction = 1 - 3 / (4 * (n1 + n2) - 9)
    g = d * correction if np.isfinite(d) else np.nan
    boot = (run[rng.integers(n1, size=(N_BOOT, n1))].mean(axis=1) -
            rest[rng.integers(n2, size=(N_BOOT, n2))].mean(axis=1))
    return {"mean_difference_run_minus_rest": mean_diff, "welch_t": t_stat, "welch_df": df,
            "welch_p_two_sided": p, "hedges_g": g,
            "bootstrap_ci_low": float(np.quantile(boot, .025)), "bootstrap_ci_high": float(np.quantile(boot, .975))}


def main() -> None:
    data = pd.read_csv(SOURCE)
    data = data.loc[data.segment.isin(["run", "rest"])].copy()
    rng = np.random.default_rng(20261004)
    rows: list[dict[str, float | str | int]] = []
    for metric in ["pac_strength", "phase_frequency_hz", "amplitude_frequency_hz", "duration_s"]:
        run = data.loc[data.segment.eq("run"), metric].to_numpy(float)
        rest = data.loc[data.segment.eq("rest"), metric].to_numpy(float)
        row: dict[str, float | str | int] = {
            "metric": metric, "n_run": len(run), "n_rest": len(rest),
            "run_mean": run.mean(), "run_median": np.median(run),
            "rest_mean": rest.mean(), "rest_median": np.median(rest),
        }
        row.update(welch_summary(run, rest, rng))
        rows.append(row)
    table = pd.DataFrame(rows)
    table.to_csv(ROOT / "apc_ec013_figure5_exact_stats.csv", index=False)
    lines = [
        "Figure 5 exact APC run/rest statistics (EC013 R2)",
        "Primary inferential unit: one unweighted observation per bout (12 run and 12 rest bouts).",
        "Welch two-sample t tests are two-sided; Hedges g is signed as run minus rest.",
        "Unequal bout durations were retained; duration-weighted means are provided separately in apc_ec013_lfp_apc_vs_pac_state_method_summary.csv as a sensitivity analysis.",
        "",
    ]
    for row in rows:
        lines.extend([
            f"{row['metric']}: run mean/median={row['run_mean']:.6g}/{row['run_median']:.6g}; "
            f"rest mean/median={row['rest_mean']:.6g}/{row['rest_median']:.6g}",
            f"  Welch t({row['welch_df']:.2f})={row['welch_t']:.3f}, p={row['welch_p_two_sided']:.4g}, "
            f"Hedges g={row['hedges_g']:.3f}, mean difference={row['mean_difference_run_minus_rest']:.6g}, "
            f"bootstrap 95% CI=[{row['bootstrap_ci_low']:.6g}, {row['bootstrap_ci_high']:.6g}]",
        ])
    (ROOT / "apc_ec013_figure5_exact_stats.txt").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
