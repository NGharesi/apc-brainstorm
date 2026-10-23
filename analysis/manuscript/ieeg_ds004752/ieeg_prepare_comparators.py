"""Add only the prespecified iEEG profile; prove reversible byte preservation."""
from pathlib import Path
import hashlib,json,difflib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent
source=ROOT/'revision_checks/final/sos_comparators.m';original=source.read_bytes()
edits=[(b'function rows=sos_comparators(',b'function rows=ieeg_comparators('),
       (b'elseif profile=="rodent",faGrid=80:4:148;fpStart=4;fpStop=12;',b'elseif profile=="rodent",faGrid=80:4:148;fpStart=4;fpStop=12;\r\nelseif profile=="ieeg",faGrid=80:4:148;fpStart=2;fpStop=12;'),
       (b'mode=="A2"||mode=="rodent_A2_prime"',b'mode=="A2"||mode=="rodent_A2_prime"||mode=="ieeg_A2_prime"')]
updated=original
for old,new in edits:
    assert updated.count(old)==1
    updated=updated.replace(old,new)
reversed_copy=updated
for old,new in reversed(edits):reversed_copy=reversed_copy.replace(new,old)
assert reversed_copy==original
(OUT/'ieeg_comparators.m').write_bytes(updated)
(OUT/'ieeg_comparators.diff').write_text(''.join(difflib.unified_diff(original.decode('utf-8').splitlines(True),updated.decode('utf-8').splitlines(True),fromfile=str(source),tofile='ieeg_comparators.m')),encoding='utf-8')
meta=json.loads((OUT/'provenance.json').read_text(encoding='utf-8'))
(OUT/'ieeg_comparator_copy_verification.json').write_text(json.dumps(dict(provenance=meta,original_sha256=hashlib.sha256(original).hexdigest(),copy_sha256=hashlib.sha256(updated).hexdigest(),existing_profiles_byte_identical_after_removing_only_added_profile_and_function_rename=True,reverse_edits_exactly_recover_original=True,edits=[dict(before=a.decode('utf-8'),after=b.decode('utf-8')) for a,b in edits]),indent=2),encoding='utf-8')
print('Comparator copy reverse-diff PASS; no dataset estimates computed')
