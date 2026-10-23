"""Record pre-run analysis hashes and provenance; does not touch frozen files."""
from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent
metadata=json.loads((OUT/'diagnosis_runtime.json').read_text(encoding='utf-8'))['metadata']
files={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.suffix in ['.m','.py'] or p.name=='PROTOCOL_followup.md'}
(OUT/'analysis_manifest.json').write_text(json.dumps({'files':files,'metadata':metadata},indent=2),encoding='utf-8')
manifest=json.loads((OUT/'input_source_manifest.json').read_text(encoding='utf-8'))
manifest['metadata']=metadata
source=Path(metadata['paths']['repository'])/'src/bst_apc.m'
lines=source.read_text(encoding='utf-8').splitlines()
manifest['phase_epoch_edge_condition_line']=next(i for i,line in enumerate(lines,1) if i>500 and 'if idx(1) < 1 || idx(end) > numel(signal)' in line)
(OUT/'input_source_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'analysis_files':len(files),'phase_epoch_edge_condition_line':manifest['phase_epoch_edge_condition_line']}))
