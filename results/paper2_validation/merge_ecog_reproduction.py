from pathlib import Path
from datetime import datetime, timezone
import json, sys
O = Path(__file__).resolve().parent
sys.path.insert(0, str(O.parent.parent / 'pydeps'))
import pandas as pd

P = json.loads((O / 'provenance.json').read_text(encoding='utf-8'))
d = pd.concat([pd.read_csv(O / f'ecog_reproduction_worker{w}.csv', encoding='utf-8', float_precision='round_trip') for w in range(1, 5)], ignore_index=True)
assert len(d) == 2642 and d.key.is_unique and d.passed.astype(bool).all()
assert (d.git_commit == P['git_head']).all() and (d.protocol_sha256 == P['protocol_sha256']).all()
assert (d.from_completed_checkpoint.astype(bool)).sum() == 39
d = d.sort_values('key').reset_index(drop=True)
d.to_csv(O / 'ecog_reproduction_check.csv', index=False, encoding='utf-8', float_format='%.17g')
cols = ['fp_absolute_difference_hz', 'fp_relative_difference', 'coupling_absolute_difference', 'coupling_relative_difference']
rows = []
for col in cols:
    finite = d[col].notna()
    idx = d.loc[finite, col].idxmax()
    rows.append({'quantity': col, 'maximum': float(d.loc[idx, col]), 'bout_at_maximum': d.loc[idx, 'key'], 'finite_comparisons': int(finite.sum()), 'n_bouts': len(d), 'git_commit': P['git_head'], 'protocol_sha256': P['protocol_sha256'], 'provenance_file': 'provenance.json'})
pd.DataFrame(rows).to_csv(O / 'ecog_reproduction_maxima.csv', index=False, encoding='utf-8', float_format='%.17g')
result = {'status': 'PASS', 'n_bouts': len(d), 'preserved_checkpoint_bouts': 39, 'maxima': rows, 'relative_difference_denominator': 'max(abs(saved), 1e-12) for each quantity', 'git_commit': P['git_head'], 'protocol_sha256': P['protocol_sha256'], 'utc': datetime.now(timezone.utc).isoformat()}
(O / 'ecog_reproduction_summary.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, indent=2))
