"""Fix a concatenated helper declaration; preserve failed tooling unchanged."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,difflib
O=Path(__file__).resolve().parent;repo=O.parent.parent/'apc-brainstorm-publish'
A=O/'tooling_generation_attempt1';assert not A.exists();A.mkdir()
assert not (O/'HA_inputs.mat').exists() and not (O/'HB_inputs.mat').exists()
records=[]
for n in ['generate_v3_hb.m','phaseB_generate_matlab.log','prepare_phaseB.py','HB_generator_wrapper.diff']:
    p=O/n;shutil.copy2(p,A/n);records.append(dict(path=n,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
p=O/'generate_v3_hb.m';s=p.read_text(encoding='utf-8');assert s.count('endfunction write_json')==1;s=s.replace('endfunction write_json','end\nfunction write_json');p.write_text(s,encoding='utf-8')
p=O/'prepare_phaseB.py';s=p.read_text(encoding='utf-8');s=s.replace("old.index('\\nfunction s=git')]+old[", "old.index('\\nfunction s=git')]+'\\n'+old[");p.write_text(s,encoding='utf-8')
old=(repo/'analysis/v2_revision/run_v2_heldout.m').read_text(encoding='utf-8')
body=old[old.index('function generate_inputs(out,meta)'):old.index('\nfunction analyze_worker')]
actual=(O/'generate_v3_hb.m').read_text(encoding='utf-8')
expected=body.replace('function generate_inputs(out,meta)','function generate_v3_hb(out,meta)').replace("'heldout_inputs.mat'","'HB_inputs.mat'").replace("'heldout_frequency_draws.csv'","'HB_frequency_draws.csv'").replace("'heldout_null_pair_verification.csv'","'HB_null_pair_verification.csv'").replace("'heldout_input_manifest.json'","'HB_input_manifest.json'")
tail=old[old.index('function r=verification_row'):old.index('\nfunction s=git')]+'\n'+old[old.index('function write_json'):old.index('\nfunction restore')]
assert actual==expected+'\n'+tail
(O/'HB_generator_wrapper.diff').write_text(''.join(difflib.unified_diff(body.splitlines(True),expected.splitlines(True),fromfile='frozen v2 generate_inputs',tofile='v3 HB output-name wrapper')),encoding='utf-8')
record=dict(recorded_utc=datetime.now(timezone.utc).isoformat(),reason='A missing newline while copying helper functions concatenated end and function write_json into endfunction. The Poisson helper raised Undefined function endfunction before any input bank or method output was saved. Inserted one newline; original HB signal formulas, draw order and helper source now match the frozen generator exactly. Generation restarts from its fixed streams; no reportable result is recomputed.',method_source_changed=False,heldout_bank_saved_before_error=False,files=records)
(A/'manifest.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
d=json.loads((O/'deviations.json').read_text(encoding='utf-8'));d['deviations'].append(dict(type='Phase-B generator wrapper newline (tooling)',reason=record['reason']));(O/'deviations.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
print('Fixed one wrapper newline; unchanged HB generator body/helpers verified; failed tooling archived.')
