from pathlib import Path
import json,subprocess,datetime
D=Path(__file__).resolve().parent;R=D.parents[1]/'apc-brainstorm-publish'
GIT=r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe'
def git(*args):return subprocess.check_output([GIT,'-C',str(R),*args],text=True,encoding='utf-8').strip()
sanity=json.loads((D/'committed_checks/sanity_results.json').read_text(encoding='utf-8'))
smoke=json.loads((D/'committed_checks/smoke_results.json').read_text(encoding='utf-8'))
commit=git('rev-parse','HEAD')
assert sanity['passed'] and smoke['passed']
assert sanity['metadata']['git_commit']==smoke['metadata']['git_commit']==commit
assert not sanity['metadata']['worktree_dirty'] and not smoke['metadata']['worktree_dirty']
assert not git('status','--porcelain')
assert git('branch','--show-current')=='v1.0-revision'
git('tag','-a','v1.0','-m','APC v1.0: committed legacy compatibility and five-trial bandwidth checks passed before full reruns')
assert git('rev-list','-n','1','v1.0')==commit
assert sanity['metadata']['apc_source_git_blob']==git('rev-parse','v1.0:src/bst_apc.m')
metadata=dict(sanity['metadata']);metadata.update(git_tag='v1.0',stage='freeze_attestation')
record=dict(status='FROZEN_AFTER_COMMITTED_CHECKS',git_commit=commit,tag='v1.0',tag_object=git('rev-parse','v1.0'),
    frozen_local=datetime.datetime.now().isoformat(),sanity=sanity['checks'],smoke=smoke,metadata=metadata)
(D/'freeze_attestation.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
entries=[dict(category='encoding',description='Earlier pre-commit Python read used Windows cp1252; UTF-8 right curly quote in build_results.py contained byte 0x9d at original offsets 11611 and 11629. Explicit UTF-8 text I/O applied before commit.'),
 dict(category='source_character_audit',description='All 32 repository MATLAB files were already ASCII; no MATLAB character substitutions were needed.'),
 dict(category='logging',description='MATLAB startup logged missing historical Brainstorm paths. The runner checks that bst_apc resolves to the frozen repository source.'),
 dict(category='git_line_endings',description='Git emitted LF-to-CRLF checkout notices while staging. Checks ran on a clean tree and identify the committed source blob.')]
(D/'tooling_deviations.json').write_text(json.dumps(dict(entries=entries,metadata=metadata),indent=2),encoding='utf-8')
print('Tagged v1.0 at',commit,'after committed compatibility and smoke checks; tree clean.')
