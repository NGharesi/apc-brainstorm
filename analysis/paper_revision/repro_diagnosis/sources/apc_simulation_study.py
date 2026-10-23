from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd


OUTDIR = Path(__file__).with_name("apc_simulation_outputs")
OUTDIR.mkdir(exist_ok=True)


@dataclass
class SimParams:
    fs: float = 500.0
    duration: float = 20.0
    true_fp: float = 8.0
    true_fa: float = 120.0
    phase_offset_rad: float = -np.pi / 2
    burst_sigma_s: float = 0.03
    burst_amp: float = 1.8
    low_amp: float = 1.0
    hf_base_amp: float = 0.15
    noise_sd: float = 0.8
    jitter_sd_s: float = 0.0
    broad_fa_range: tuple[float, float] = (80.0, 150.0)


def analytic_signal(x: np.ndarray) -> np.ndarray:
    n = x.size
    x_fft = np.fft.fft(x)
    h = np.zeros(n)
    if n % 2 == 0:
        h[0] = 1
        h[n // 2] = 1
        h[1 : n // 2] = 2
    else:
        h[0] = 1
        h[1 : (n + 1) // 2] = 2
    return np.fft.ifft(x_fft * h)


def bandpass_fft(x: np.ndarray, fs: float, low: float, high: float) -> np.ndarray:
    if high <= low:
        return np.zeros_like(x)
    n = x.size
    freqs = np.fft.fftfreq(n, d=1.0 / fs)
    x_fft = np.fft.fft(x)
    mask = (np.abs(freqs) >= low) & (np.abs(freqs) <= high)
    return np.real(np.fft.ifft(x_fft * mask))


def smooth(x: np.ndarray, win: int) -> np.ndarray:
    if win <= 1:
        return x
    kernel = np.ones(win) / win
    return np.convolve(x, kernel, mode="same")


def find_local_peaks(x: np.ndarray, min_distance: int, threshold: float) -> np.ndarray:
    idx = np.where((x[1:-1] > x[:-2]) & (x[1:-1] >= x[2:]) & (x[1:-1] >= threshold))[0] + 1
    if idx.size == 0:
        return idx
    selected = [int(idx[0])]
    for i in idx[1:]:
        if i - selected[-1] >= min_distance:
            selected.append(int(i))
        elif x[i] > x[selected[-1]]:
            selected[-1] = int(i)
    return np.array(selected, dtype=int)


def circular_diff_deg(a_deg: np.ndarray, b_deg: float) -> np.ndarray:
    return ((a_deg - b_deg + 180.0) % 360.0) - 180.0


def canolty_mi(phi: np.ndarray, amp: np.ndarray) -> tuple[float, float]:
    z = amp * np.exp(1j * phi)
    mean_vec = np.mean(z)
    return float(np.abs(mean_vec)), float(np.degrees(np.angle(mean_vec)))


def surrogate_canolty(phi: np.ndarray, amp: np.ndarray, n_perm: int, rng: np.random.Generator) -> tuple[float, float, np.ndarray]:
    raw_mi, pref = canolty_mi(phi, amp)
    n = amp.size
    surrogate = np.empty(n_perm, dtype=float)
    low = max(1, int(0.10 * n))
    high = max(low + 1, int(0.90 * n))
    for i in range(n_perm):
        shift = int(rng.integers(low, high))
        surrogate[i], _ = canolty_mi(phi, np.roll(amp, shift))
    mu = surrogate.mean()
    sd = surrogate.std()
    z = (raw_mi - mu) / sd if sd > 0 else raw_mi - mu
    return float(z), pref, surrogate


def estimate_fp_from_average(avg_signal: np.ndarray, fs: float, fp_max: float = 30.0, fp_min: float = 1.0) -> float:
    x = avg_signal - avg_signal.mean()
    n = max(256, int(2 ** np.ceil(np.log2(x.size))))
    spec = np.abs(np.fft.rfft(x, n=n)) ** 2
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    valid = (freqs >= fp_min) & (freqs <= fp_max)
    if not np.any(valid):
        return np.nan
    f_valid = freqs[valid]
    s_valid = spec[valid]
    return float(f_valid[np.argmax(s_valid)])


def extract_epochs(x: np.ndarray, event_idx: np.ndarray, win_idx: np.ndarray, flip_center: bool = False) -> np.ndarray:
    epochs = []
    center = int(-win_idx[0])
    for ev in event_idx:
        idx = ev + win_idx
        if idx[0] < 0 or idx[-1] >= x.size:
            continue
        ep = x[idx].copy()
        if flip_center:
            local = ep[max(0, center - 1) : min(ep.size, center + 2)]
            if np.abs(local.min()) > np.abs(local.max()):
                ep = -ep
        epochs.append(ep)
    if not epochs:
        return np.empty((0, win_idx.size))
    return np.vstack(epochs)


def detect_troughs(x: np.ndarray, fs: float, fp: float) -> np.ndarray:
    min_dist = max(1, int(round(0.8 * fs / max(fp, 1e-6))))
    thr = np.mean(-x) + 0.25 * np.std(x)
    return find_local_peaks(-x, min_dist, thr)


def estimate_fa_from_trough_locked(
    raw_signal: np.ndarray,
    trough_idx: np.ndarray,
    avg_waveform: np.ndarray,
    fs: float,
    fp: float,
    fa_range: tuple[float, float],
) -> float:
    if trough_idx.size == 0:
        return np.nan
    half_cycles = int(round(3 * fs / max(fp, 1e-6)))
    win_idx = np.arange(-half_cycles, half_cycles + 1)
    max_lag = max(1, int(round(0.8 * fs / max(fp, 1e-6))))
    candidate_freqs = np.arange(fa_range[0], fa_range[1] + 0.1, 4.0)
    best_score = -np.inf
    best_freq = np.nan
    for freq in candidate_freqs:
        band = bandpass_fft(raw_signal, fs, max(1.0, freq - 6.0), min(fs / 2 - 1.0, freq + 6.0))
        env = np.abs(analytic_signal(band))
        env_epochs = extract_epochs(env, trough_idx, win_idx, flip_center=False)
        if env_epochs.shape[0] == 0:
            continue
        avg_env = env_epochs.mean(axis=0)
        xc = np.correlate(avg_env - avg_env.mean(), avg_waveform - avg_waveform.mean(), mode="full")
        center = xc.size // 2
        local = xc[center - max_lag : center + max_lag + 1]
        score = float(np.max(np.abs(local)))
        if score > best_score:
            best_score = score
            best_freq = float(freq)
    return best_freq


def run_apc(signal: np.ndarray, params: SimParams, rng: np.random.Generator, use_surrogates: bool = False) -> dict:
    fs = params.fs
    signal = signal - signal.mean()

    hf = bandpass_fft(signal, fs, params.broad_fa_range[0], params.broad_fa_range[1])
    burst_trace = smooth(np.abs(analytic_signal(hf)), int(round(0.02 * fs)))
    threshold = burst_trace.mean() + 0.5 * burst_trace.std()
    min_dist = max(1, int(round(0.9 * fs / params.broad_fa_range[0])))
    burst_idx = find_local_peaks(burst_trace, min_dist, threshold)

    epoch_win = np.arange(int(round(-0.6 * fs)), int(round(0.6 * fs)) + 1)
    burst_epochs = extract_epochs(signal, burst_idx, epoch_win, flip_center=True)
    if burst_epochs.shape[0] == 0:
        return {"status_code": 2}

    burst_avg = burst_epochs.mean(axis=0)
    fp = estimate_fp_from_average(burst_avg, fs, fp_max=min(30.0, params.broad_fa_range[0] - 1.0))
    if not np.isfinite(fp) or fp < 1.0 or fp >= params.broad_fa_range[0]:
        return {"status_code": 3, "n_bursts": int(burst_epochs.shape[0])}

    phase_band = (max(0.5, fp - max(0.5, 0.25 * fp)), min(params.broad_fa_range[0] - 0.5, fp + max(0.5, 0.25 * fp)))
    phase_signal = bandpass_fft(signal, fs, phase_band[0], phase_band[1])
    trough_idx = detect_troughs(phase_signal, fs, fp)
    if trough_idx.size == 0:
        return {"status_code": 4, "n_bursts": int(burst_epochs.shape[0]), "phase_frequency_hz": fp}

    half_cycles = int(round(3 * fs / fp))
    trough_win = np.arange(-half_cycles, half_cycles + 1)
    trough_epochs = extract_epochs(signal, trough_idx, trough_win, flip_center=False)
    if trough_epochs.shape[0] == 0:
        return {"status_code": 4, "n_bursts": int(burst_epochs.shape[0]), "phase_frequency_hz": fp}
    trough_avg = trough_epochs.mean(axis=0)

    fa = estimate_fa_from_trough_locked(signal, trough_idx, trough_avg, fs, fp, params.broad_fa_range)
    if not np.isfinite(fa):
        return {
            "status_code": 5,
            "n_bursts": int(burst_epochs.shape[0]),
            "n_phase_events": int(trough_epochs.shape[0]),
            "phase_frequency_hz": fp,
        }

    amp_signal = bandpass_fft(signal, fs, max(1.0, fa - 6.0), min(fs / 2 - 1.0, fa + 6.0))
    amp_env = np.abs(analytic_signal(amp_signal))
    phi = np.angle(analytic_signal(phase_signal))

    if use_surrogates:
        pac_strength, pref_phase, _ = surrogate_canolty(phi, amp_env, 100, rng)
    else:
        pac_strength, pref_phase = canolty_mi(phi, amp_env)

    return {
        "status_code": 0,
        "n_bursts": int(burst_epochs.shape[0]),
        "n_phase_events": int(trough_epochs.shape[0]),
        "phase_frequency_hz": float(fp),
        "amplitude_frequency_hz": float(fa),
        "preferred_phase_deg": float(pref_phase),
        "pac_strength": float(pac_strength),
    }


def standard_pac_known_bands(signal: np.ndarray, params: SimParams, rng: np.random.Generator) -> dict:
    low = bandpass_fft(signal, params.fs, max(0.5, params.true_fp - 1.5), params.true_fp + 1.5)
    high = bandpass_fft(signal, params.fs, params.true_fa - 8.0, params.true_fa + 8.0)
    phi = np.angle(analytic_signal(low))
    amp = np.abs(analytic_signal(high))
    raw, pref = canolty_mi(phi, amp)
    z, _, _ = surrogate_canolty(phi, amp, 100, rng)
    return {"standard_pac_raw": float(raw), "standard_pac_z": float(z), "standard_pref_phase_deg": float(pref)}


def low_signal_component(t: np.ndarray, params: SimParams, asymmetric: bool = False) -> np.ndarray:
    base = params.low_amp * np.sin(2 * np.pi * params.true_fp * t)
    if asymmetric:
        base = base + 0.35 * np.sin(2 * np.pi * 2 * params.true_fp * t + 0.3)
    return base


def burst_train_signal(
    t: np.ndarray,
    params: SimParams,
    rng: np.random.Generator,
    coupled: bool = True,
    jitter_sd_s: float | None = None,
    amplitude_scale: float = 1.0,
    asymmetric_low: bool = False,
) -> tuple[np.ndarray, np.ndarray]:
    lf = low_signal_component(t, params, asymmetric=asymmetric_low)
    cycle_times = (params.phase_offset_rad / (2 * np.pi * params.true_fp)) + np.arange(0, params.duration * params.true_fp + 2) / params.true_fp
    cycle_times = cycle_times[(cycle_times > 0.5) & (cycle_times < params.duration - 0.5)]
    if coupled:
        event_times = cycle_times.copy()
    else:
        event_times = np.sort(rng.uniform(0.5, params.duration - 0.5, size=cycle_times.size))
    if jitter_sd_s is None:
        jitter_sd_s = params.jitter_sd_s
    if jitter_sd_s > 0:
        event_times = event_times + rng.normal(0.0, jitter_sd_s, size=event_times.size)
        event_times = event_times[(event_times > 0.5) & (event_times < params.duration - 0.5)]

    burst = np.zeros_like(t)
    for ev in event_times:
        env = np.exp(-0.5 * ((t - ev) / params.burst_sigma_s) ** 2)
        burst += amplitude_scale * params.burst_amp * env * np.sin(2 * np.pi * params.true_fa * (t - ev))
    background_hf = params.hf_base_amp * np.sin(2 * np.pi * params.true_fa * t + rng.uniform(0, 2 * np.pi))
    noise = rng.normal(0.0, params.noise_sd, size=t.size)
    signal = lf + burst + background_hf + noise
    return signal, event_times


def continuous_pac_signal(t: np.ndarray, params: SimParams, rng: np.random.Generator) -> np.ndarray:
    lf = low_signal_component(t, params, asymmetric=False)
    phase = 2 * np.pi * params.true_fp * t + params.phase_offset_rad
    mod = 0.5 * (1 + np.sin(phase))
    hf_amp = 0.5 + 1.1 * mod
    hf = hf_amp * np.sin(2 * np.pi * params.true_fa * t + rng.uniform(0, 2 * np.pi))
    noise = rng.normal(0.0, params.noise_sd, size=t.size)
    return lf + hf + noise


def circular_mean_deg(phases_deg: np.ndarray) -> float:
    phases_rad = np.radians(phases_deg)
    return float(np.degrees(np.angle(np.mean(np.exp(1j * phases_rad)))))


def target_phase_from_events(t: np.ndarray, params: SimParams, event_times: np.ndarray, asymmetric_low: bool = False) -> float:
    low = low_signal_component(t, params, asymmetric=asymmetric_low)
    phi = np.degrees(np.angle(analytic_signal(low)))
    idx = np.clip(np.round(event_times * params.fs).astype(int), 0, t.size - 1)
    return circular_mean_deg(phi[idx])


def run_scenario(
    scenario_name: str,
    generator: Callable[[np.ndarray, SimParams, np.random.Generator], np.ndarray | tuple[np.ndarray, np.ndarray]],
    params: SimParams,
    n_rep: int,
    seed: int,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    t = np.arange(0, params.duration, 1 / params.fs)
    rows = []
    for rep in range(n_rep):
        out = generator(t, params, rng)
        if isinstance(out, tuple):
            signal, event_times = out
        else:
            signal = out
            event_times = np.array([], dtype=float)
        apc = run_apc(signal, params, rng)
        std = standard_pac_known_bands(signal, params, rng)
        target_phase = float(np.degrees(params.phase_offset_rad))
        if event_times.size:
            target_phase = target_phase_from_events(t, params, event_times, asymmetric_low=("asymmetric" in scenario_name))
        row = {
            "scenario": scenario_name,
            "replicate": rep,
            "true_fp": params.true_fp,
            "true_fa": params.true_fa,
            "target_phase_deg": target_phase,
            **apc,
            **std,
        }
        rows.append(row)
    return pd.DataFrame(rows)


def summarize_results(df: pd.DataFrame) -> pd.DataFrame:
    summaries = []
    for scenario, grp in df.groupby("scenario"):
        valid = grp[grp["status_code"] == 0].copy()
        summary = {
            "scenario": scenario,
            "n": int(grp.shape[0]),
            "valid_rate": float((grp["status_code"] == 0).mean()),
            "median_apc_raw": float(valid["pac_strength"].median()) if not valid.empty else np.nan,
            "median_standard_pac_raw": float(valid["standard_pac_raw"].median()) if not valid.empty else np.nan,
            "median_standard_pac_z": float(valid["standard_pac_z"].median()) if not valid.empty else np.nan,
            "median_fp_hz": float(valid["phase_frequency_hz"].median()) if "phase_frequency_hz" in valid else np.nan,
            "median_fa_hz": float(valid["amplitude_frequency_hz"].median()) if "amplitude_frequency_hz" in valid else np.nan,
            "median_phase_error_deg": float(np.median(np.abs(circular_diff_deg(valid["preferred_phase_deg"].to_numpy(), valid["target_phase_deg"].iloc[0])))) if not valid.empty else np.nan,
            "median_bursts": float(valid["n_bursts"].median()) if "n_bursts" in valid else np.nan,
            "median_phase_events": float(valid["n_phase_events"].median()) if "n_phase_events" in valid else np.nan,
        }
        summaries.append(summary)
    return pd.DataFrame(summaries).sort_values("scenario")


def main() -> None:
    base = SimParams()
    n_rep = 40
    all_frames = []

    all_frames.append(
        run_scenario(
            "burst_coupled",
            lambda t, p, rng: burst_train_signal(t, p, rng, coupled=True),
            base,
            n_rep,
            101,
        )
    )

    all_frames.append(
        run_scenario(
            "burst_null",
            lambda t, p, rng: burst_train_signal(t, p, rng, coupled=False),
            base,
            n_rep,
            102,
        )
    )

    for noise_sd, seed in [(0.4, 103), (0.8, 104), (1.2, 105)]:
        p = SimParams(noise_sd=noise_sd)
        all_frames.append(
            run_scenario(
                f"burst_coupled_snr_{noise_sd:.1f}",
                lambda t, pp, rng: burst_train_signal(t, pp, rng, coupled=True),
                p,
                n_rep,
                seed,
            )
        )

    for jitter_sd, seed in [(0.0, 106), (0.01, 107), (0.02, 108), (0.04, 109)]:
        p = SimParams(jitter_sd_s=jitter_sd)
        all_frames.append(
            run_scenario(
                f"burst_coupled_jitter_{jitter_sd:.2f}",
                lambda t, pp, rng: burst_train_signal(t, pp, rng, coupled=True, jitter_sd_s=pp.jitter_sd_s),
                p,
                n_rep,
                seed,
            )
        )

    all_frames.append(
        run_scenario(
            "continuous_pac",
            continuous_pac_signal,
            base,
            n_rep,
            110,
        )
    )

    all_frames.append(
        run_scenario(
            "burst_coupled_asymmetric_low",
            lambda t, p, rng: burst_train_signal(t, p, rng, coupled=True, asymmetric_low=True),
            base,
            n_rep,
            111,
        )
    )

    df = pd.concat(all_frames, ignore_index=True)
    summary = summarize_results(df)

    df.to_csv(OUTDIR / "apc_simulation_runs.csv", index=False)
    summary.to_csv(OUTDIR / "apc_simulation_summary.csv", index=False)

    report = {
        "base_parameters": {
            "fs": base.fs,
            "duration": base.duration,
            "true_fp_hz": base.true_fp,
            "true_fa_hz": base.true_fa,
            "preferred_phase_deg": float(np.degrees(base.phase_offset_rad)),
            "burst_sigma_s": base.burst_sigma_s,
            "burst_amp": base.burst_amp,
            "noise_sd": base.noise_sd,
            "replicates_per_condition": n_rep,
        },
        "summary_records": summary.to_dict(orient="records"),
    }
    (OUTDIR / "apc_simulation_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
