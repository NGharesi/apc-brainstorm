"""Read-only final checks and a new manifest; preserves earlier outputs."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
REPO = ROOT / 'apc-brainstorm-publish'
GIT = Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
sys.path.insert(0, str(ROOT / 'pydeps'))
from PIL import Image


def git(*args):
    return subprocess.check_output([str(GIT), '-C', str(REPO), *args], text=True, encoding='utf-8').strip()


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


with (OUT / 'final_verification.json').open(encoding='utf-8') as f:
    verified = json.load(f)
metadata = verified['metadata']
assert verified['passed']
assert git('rev-parse', 'HEAD') == metadata['git_commit']
assert git('rev-parse', 'v2.0^{commit}') == metadata['git_commit']
assert git('rev-parse', 'HEAD:src/bst_apc.m') == metadata['apc_source_blob']
assert not git('status', '--porcelain')

checked_links = 0
for name in ('RESULTS_v2.md', 'UNIT_RESULTS.md'):
    body = (OUT / name).read_text(encoding='utf-8')
    for target in re.findall(r'\]\((?:<([^>]+)>|([^\s)]+))\)', body):
        link = next(x for x in target if x)
        if link.startswith(('http:', 'https:', '#')):
            continue
        path = Path(link.split('#', 1)[0])
        if not path.is_absolute():
            path = OUT / path
        assert path.exists(), (name, link)
        checked_links += 1

for name in ('joint_recovery_H1.png', 'joint_recovery_H2.png'):
    with Image.open(OUT / name) as im:
        image_metadata = json.loads(im.info['Description'])
        assert image_metadata == metadata, name
        im.verify()

manifest_path = OUT / 'final_output_manifest.json'
assert not manifest_path.exists(), 'Preserve an existing final manifest rather than overwriting it.'
files = []
for path in sorted(OUT.rglob('*')):
    if not path.is_file() or any(part in ('__pycache__', 'plot_config') for part in path.relative_to(OUT).parts):
        continue
    files.append({'path': path.relative_to(OUT).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha256(path)})
manifest = {
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'metadata': metadata,
    'checks': {'passed': True, 'local_report_links_checked': checked_links,
               'figure_metadata_verified': True, 'frozen_tree_clean': True,
               'head_and_tag_match': True, 'earlier_manifest_preserved': True},
    'files': files,
}
with manifest_path.open('w', encoding='utf-8', newline='\n') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=True)
    f.write('\n')
print(json.dumps({'passed': True, 'files': len(files), 'links': checked_links,
                  'commit': metadata['git_commit'], 'manifest': str(manifest_path)}))
