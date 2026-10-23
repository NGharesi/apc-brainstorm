from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
s=(ROOT/'revision_checks/v1_followup/fu_slow_generator.m').read_text(encoding='utf-8')
s=s.replace('function varargout=fu_slow_generator(', 'function varargout=v2_unit_generator(',1)
s=s.replace("cfg=local_get_profile('reviewer_control');cfg.true_fp_hz=6;", "cfg=local_get_profile('reviewer_control');cfg.true_fp_hz=8;cfg.snr_db=20;cfg.broad_fa_band_hz=[80 160];",1)
s=s.replace('cfg.slow_distractor_hz=10;cfg.slow_amplitude_ratios=[0 .5 1 1.5 2 3];', 'cfg.slow_distractor_hz=11;cfg.slow_amplitude_ratios=[0 3];',1)
target=ROOT/'apc-brainstorm-publish/analysis/v2_revision/v2_unit_generator.m'
assert not target.exists()
target.write_text(s,encoding='utf-8')
print('Prepared the predeclared unit generator; no inputs generated.')
