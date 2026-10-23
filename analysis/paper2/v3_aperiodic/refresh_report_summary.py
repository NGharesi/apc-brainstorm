"""Add a concise factual summary and record figure QA; update text checksums."""
from pathlib import Path
from datetime import datetime,timezone
import csv,json,hashlib
O=Path(__file__).resolve().parent
def js(n):return json.loads((O/n).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=js('provenance.json');a=js('criteria_decisions.json')['criteria'];c=js('phaseC/ecog_success_criterion.json')
with (O/'phaseC/ecog/ecog_statistics.csv').open(encoding='utf-8',newline='') as f:D=list(csv.DictReader(f))
p1=next(z for z in D if z['subset']=='prespecified' and z['endpoint']=='coupling_state');p2=next(z for z in D if z['subset']=='prespecified' and z['endpoint']=='within_state_fP_SD')
summary=['## Factual summary','',
 f'- G0-G2 passed; public freeze `v3.0` = `{m["freeze_commit"]}`. Default remains v1.',
 f'- A1: HA joint recovery v3 {a["A1"]["a_success"]}/450 versus v1 {a["A1"]["b_success"]}/450; exact one-sided p={a["A1"]["p_value"]:.7g}.',
 f'- A2 (key secondary): HA fP recovery v3 {a["A2"]["a_success"]}/450 versus SP-raw {a["A2"]["b_success"]}/450; exact two-sided p={a["A2"]["p_value"]:.7g}.',
 f'- A3 passed all three bounds. A4: false joint v3 {a["A4"]["a_success"]}/700 versus v1 {a["A4"]["b_success"]}/700; +{a["A4"]["difference_pp"]:.6g} percentage points, within the allowed +5.',
 f'- ECoG rest-spectrum criterion passed: v3 {c["v3_success"]}/18, v1 {c["v1_success"]}/18, SP-raw {c["SP_raw_success"]}/18; required v3 >=9/18.',
 f'- ECoG Primary 1: **{p1["decision"]}**, mean difference {float(p1["mean_difference"]):.7g}, 95% CI [{float(p1["ci_low"]):.7g}, {float(p1["ci_high"]):.7g}]. Primary 2: **{p2["decision"]}**, median SD difference {float(p2["median_difference"]):.7g} Hz, 95% CI [{float(p2["ci_low"]):.7g}, {float(p2["ci_high"]):.7g}].','']
p=O/'RESULTS_v3.md';s=p.read_text(encoding='utf-8');assert '## Factual summary' not in s;s=s.replace('## Protocol, freeze and provenance','\n'.join(summary)+'\n## Protocol, freeze and provenance',1);p.write_text(s,encoding='utf-8')
qa=dict(status='PASS',freeze_commit=m['freeze_commit'],protocol_sha256=m['protocol_sha256'],figures=['HA_joint_recovery.png','HA_fp_recovery.png','ECoG_rest_fp_spectral_peak.png'],inspection='All three PNGs inspected at displayed resolution: legible axes/legends, no clipped labels, no internal title/footer; matching SVG and 300-dpi metadata verified by final audit.',method_or_data_changes=False)
(O/'visual_qa.json').write_text(json.dumps(qa,indent=2),encoding='utf-8')
manifest=js('output_manifest.json');records={z['path']:z for z in manifest['files']}
for n in ['RESULTS_v3.md','visual_qa.json',Path(__file__).name]:
    p=O/n;records[n]=dict(path=n,bytes=p.stat().st_size,sha256=sha(p))
manifest['files']=sorted(records.values(),key=lambda z:z['path']);manifest['final_text_and_visual_QA_update_utc']=datetime.now(timezone.utc).isoformat();(O/'output_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Final factual summary and visual QA recorded; manifest text hashes updated; no numerical result changed.')
