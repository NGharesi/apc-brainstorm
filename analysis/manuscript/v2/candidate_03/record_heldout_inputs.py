from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent
meta=json.loads((OUT/'generate_runtime.json').read_text(encoding='utf-8'))['metadata']
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
names=['heldout_inputs.mat','heldout_frequency_draws.csv','heldout_null_pair_verification.csv']
result={'recorded_before_analysis':True,'files':{str(OUT/n):sha(OUT/n) for n in names},'metadata':meta}
target=OUT/'heldout_inputs_sha256.json';assert not target.exists()
target.write_text(json.dumps(result,indent=2),encoding='utf-8')
print('Input hashes recorded before analysis.')
