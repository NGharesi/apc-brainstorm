"""Record public freeze and build execution wrappers without generating signals."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,difflib
O=Path(__file__).resolve().parent;R=O.parent.parent;repo=R/'apc-brainstorm-publish'
git=Path(r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
def g(*a):return subprocess.check_output([str(git),'-C',str(repo),*a],text=True,encoding='utf-8').strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(n):return json.loads((O/n).read_text(encoding='utf-8'))
head=g('rev-parse','HEAD');assert head==g('rev-parse','origin/neuroimage-submission')==g('rev-list','-n','1','v3.0')
assert not g('status','--porcelain');assert g('branch','--show-current')=='neuroimage-submission'
pre=js('freeze_precheck.json');m=js('provenance.json')
assert sha(repo/'protocol/APC_v3_aperiodic_protocol.md')==m['protocol_sha256']
for r in pre['files']:assert sha(repo/r['path'])==r['sha256']
for r in js('attempt1_archive_manifest.json')['moved_files']:assert sha(O/r['archived_path'])==r['sha256']
m.update(status='V3_FROZEN_PUBLIC_BEFORE_HELDOUT',git_head=head,freeze_commit=head,git_tag='v3.0',freeze_public_verified_utc=datetime.now(timezone.utc).isoformat(),git_clean_at_freeze=True,source_committed=True,results_committed=False,heldout_generated=False,gate_base_commit=pre['git_head'],freeze_precheck='freeze_precheck.json',HA_conventions=pre['HA_conventions'],HB_conventions=pre['HB_conventions'],phaseB_seed_HA=20261101,phaseB_seed_HB=20261022)
m['evaluation_dependencies_sha256']=[dict(path=str(p),sha256=sha(p)) for p in [R/'revision_checks/final/sos_comparators.m',R/'revision_checks/final/final_sos_filter.m',repo/'analysis/v2_revision/v2_heldout_generator.m',repo/'analysis/v2_revision/v2_unit_generator.m',repo/'analysis/v1_revision/v1_sparsity_generator.m',repo/'analysis/v1_revision/v1_distractor_generator.m',repo/'analysis/v1_revision/v1_options.m',repo/'src/calc_MI_all_methods.m']]
for n in ['provenance.json','phaseB_implementation.json']:(O/n).write_text(json.dumps(m,indent=2),encoding='utf-8')
# Exact old held-out generation body; only output names and metadata wrapper change.
old=(repo/'analysis/v2_revision/run_v2_heldout.m').read_text(encoding='utf-8')
body=old[old.index('function generate_inputs(out,meta)'):old.index('\nfunction analyze_worker')]
body=body.replace('function generate_inputs(out,meta)','function generate_v3_hb(out,meta)').replace("'heldout_inputs.mat'","'HB_inputs.mat'").replace("'heldout_frequency_draws.csv'","'HB_frequency_draws.csv'").replace("'heldout_null_pair_verification.csv'","'HB_null_pair_verification.csv'").replace("'heldout_input_manifest.json'","'HB_input_manifest.json'")
tail=old[old.index('function r=verification_row'):old.index('\nfunction s=git')]+'\n'+old[old.index('function write_json'):old.index('\nfunction restore')]
assert not (O/'generate_v3_hb.m').exists()
(O/'generate_v3_hb.m').write_text(body+'\n'+tail,encoding='utf-8')
(O/'HB_generator_wrapper.diff').write_text(''.join(difflib.unified_diff(old[old.index('function generate_inputs(out,meta)'):old.index('\nfunction analyze_worker')].splitlines(True),body.splitlines(True),fromfile='frozen v2 generate_inputs',tofile='v3 HB output-name wrapper')),encoding='utf-8')
# Preserve comparator implementation; add HA profile/half-width only.
src=(R/'revision_checks/final/sos_comparators.m').read_text(encoding='utf-8')
dst=src.replace('function rows=sos_comparators','function rows=v3_comparators',1).replace('if profile=="heldout",','if profile=="HA",faGrid=80:4:160;fpStart=3;fpStop=30;\nelseif profile=="heldout",',1).replace('elseif mode=="A2_prime",half=14;end','elseif mode=="A2_prime",half=14;elseif mode=="HA_A2_prime",half=30;end',1)
(O/'v3_comparators.m').write_text(dst,encoding='utf-8')
(O/'comparator_HA_profile.diff').write_text(''.join(difflib.unified_diff(src.splitlines(True),dst.splitlines(True),fromfile='sos_comparators.m',tofile='v3_comparators.m')),encoding='utf-8')
print(head, 'public; clean; frozen hashes verified; no held-out signal generated',flush=True)
