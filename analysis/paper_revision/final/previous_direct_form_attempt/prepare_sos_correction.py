from pathlib import Path
import shutil,json,hashlib,datetime
OUT=Path(__file__).resolve().parent
archive=OUT/'previous_direct_form_attempt'
assert not archive.exists()
archive.mkdir()
files=[p for p in OUT.iterdir() if p.is_file()]
for p in files:shutil.copy2(p,archive/p.name)
meta=json.loads((OUT/'analysis_provenance.json').read_text(encoding='utf-8'))
meta['correction']='SOS realization of the same fourth-order Butterworth prototype; no tagged code changes'
meta['filter_guard']={'max_pole_radius':'<1 for zpk and each SOS section','absolute_center_gain_error':'<1e-3 at arithmetic midpoint of realized passband','failure':'stop'}
(OUT/'sos_correction_provenance.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
manifest={'metadata':meta,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[]}
for p in archive.iterdir():manifest['files'].append({'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(OUT/'previous_attempt_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Preserved',len(files),'files')
