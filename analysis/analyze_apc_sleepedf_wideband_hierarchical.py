"""Participant-aggregated inference for wideband Sleep-EDF quality control.

Nights are averaged within participant before stage and channel contrasts, so
the inferential unit is participant rather than recording.
"""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "apc_sleepedf_coupling_validation_wideband_signal_level.csv"
RNG = np.random.default_rng(20261004)
N_BOOT = 20_000

def paired_summary(left: np.ndarray, right: np.ndarray) -> dict[str, float]:
    diff = right - left
    n = len(diff)
    boot = diff[RNG.integers(0, n, size=(N_BOOT, n))].mean(axis=1)
    # Exact sign-flip Monte Carlo test; valid without normality assumptions.
    signs = RNG.choice(np.array([-1.0, 1.0]), size=(N_BOOT, n))
    null = (signs * diff).mean(axis=1)
    p = (1 + np.count_nonzero(np.abs(null) >= abs(diff.mean()))) / (N_BOOT + 1)
    dz = diff.mean() / diff.std(ddof=1) if diff.std(ddof=1) > 0 else np.nan
    return {"n_participants": n, "left_median": np.median(left), "left_iqr": np.subtract(*np.percentile(left,[75,25])),
            "right_median": np.median(right), "right_iqr": np.subtract(*np.percentile(right,[75,25])),
            "mean_difference_right_minus_left": diff.mean(), "ci_low": np.quantile(boot,.025), "ci_high": np.quantile(boot,.975),
            "p_two_sided_signflip": p, "cohens_dz": dz}

def main() -> None:
    raw = pd.read_csv(SOURCE)
    apc = raw.loc[raw.apc_status.eq(0)].copy()
    # Aggregate all nights within participant for each channel-stage cell.
    numeric = ["apc_fp_hz","apc_score_z","apc_boundary_hit","apc_fa_hz","detector_spindle_hz"]
    person = apc.groupby(["participant_id","channel","stage"], as_index=False)[numeric].mean()
    rows=[]
    for metric in ["apc_fp_hz","apc_score_z","apc_boundary_hit"]:
        for channel in sorted(person.channel.unique()):
            wide=person.loc[person.channel.eq(channel)].pivot(index="participant_id",columns="stage",values=metric).dropna(subset=["N2","N3"])
            result=paired_summary(wide["N2"].to_numpy(),wide["N3"].to_numpy())
            rows.append({"contrast":"N3 minus N2","channel":channel,"metric":metric,**result})
        for stage in ["N2","N3"]:
            wide=person.loc[person.stage.eq(stage)].pivot(index="participant_id",columns="channel",values=metric).dropna(subset=["EEGFpz_Cz","EEGPz_Oz"])
            result=paired_summary(wide["EEGFpz_Cz"].to_numpy(),wide["EEGPz_Oz"].to_numpy())
            rows.append({"contrast":"posterior minus anterior","channel":stage,"metric":metric,**result})
    out=pd.DataFrame(rows)
    out.to_csv(ROOT / "apc_sleepedf_wideband_participant_level_tests.csv",index=False)
    counts=person.groupby(["channel","stage"]).agg(participants=("participant_id","nunique"),participant_cells=("participant_id","size")).reset_index()
    counts.to_csv(ROOT / "apc_sleepedf_wideband_participant_counts.csv",index=False)
    lines=["Sleep-EDF wideband participant-aggregated analysis", "197 recordings from 100 participants: 97 with two nights and 3 with one night.",
           "Nights were averaged within participant. Contrasts use paired sign-flip tests and percentile bootstrap 95% CIs.",
           "Amplitude-frequency outcomes are quality-control outputs only because boundary-hit rates remain high; they are not interpreted physiologically.", ""]
    for _,r in out.iterrows():
        lines.append(f"{r['contrast']} | {r['channel']} | {r['metric']} | n={int(r.n_participants)} | diff={r.mean_difference_right_minus_left:.4g} | 95% CI [{r.ci_low:.4g}, {r.ci_high:.4g}] | p={r.p_two_sided_signflip:.5g} | dz={r.cohens_dz:.3g}")
    (ROOT / "apc_sleepedf_wideband_participant_level_summary.txt").write_text("\n".join(lines)+"\n")

if __name__ == "__main__": main()
