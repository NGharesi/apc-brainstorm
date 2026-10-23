"""Create verified local EDF copies with valid wall-clock header syntax only."""
from pathlib import Path
import hashlib,json,shutil,difflib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent
meta=json.loads((OUT/'provenance.json').read_text(encoding='utf-8'));data=Path(meta['data_root'])
def sha(p,start=0):
    h=hashlib.sha256()
    with p.open('rb') as f:
        f.seek(start)
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()
records=[]
for p in sorted(list(data.glob('sub-*/ses-*/ieeg/*_ieeg.edf'))+list(data.glob('sub-*/ses-*/eeg/*_eeg.edf'))):
    with p.open('rb') as f:head=f.read(256)
    text=head[176:184].decode('ascii');a,b,c=map(int,text.split('.'))
    if a<24 and b<60 and c<60:continue
    assert 0<=a<24 and 0<=b<60 and c==60
    elapsed=(a*3600+b*60+c)%(24*3600);new=f'{elapsed//3600:02d}.{elapsed//60%60:02d}.{elapsed%60:02d}'
    target=OUT/'edf_header_copies'/p.relative_to(data);target.parent.mkdir(parents=True,exist_ok=True);assert not target.exists()
    shutil.copyfile(p,target)
    with target.open('r+b') as f:f.seek(176);f.write(new.encode('ascii'))
    with target.open('rb') as f:copyhead=f.read(256)
    assert copyhead[:176]==head[:176] and copyhead[184:]==head[184:]
    original_payload=sha(p,256);copy_payload=sha(target,256);assert original_payload==copy_payload
    records.append(dict(original_path=str(p),read_path=str(target),old_start_time=text,new_start_time=new,original_sha256=sha(p),copy_sha256=sha(target),payload_from_byte_256_sha256=original_payload,payload_byte_identical=True,changed_byte_range_zero_based=[176,184]))
assert len(records)==2
# Store path/hash records as an array: MATLAB jsondecode cannot preserve path keys.
paths=[ROOT/'apc-brainstorm-publish/src/bst_apc.m',ROOT/'apc-brainstorm-publish/src/calc_MI_all_methods.m',ROOT/'revision_checks/rodent_multi/v1_bout_features.m',ROOT/'revision_checks/final/sos_comparators.m',ROOT/'revision_checks/final/final_sos_filter.m',ROOT/'apc-brainstorm-publish/protocol/APC_ieeg_ds004752_protocol.md']
meta['file_sha256_records']=[dict(path=str(p),sha256=sha(p)) for p in paths]
meta['file_sha256']={str(p):sha(p) for p in paths}
eq=json.loads((OUT/'equivalence_gate.json').read_text(encoding='utf-8'));meta['apc_options']=eq['options']
meta['edf_header_copy_manifest']='edf_header_copies.json'
(OUT/'provenance.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
(OUT/'edf_header_copies.json').write_text(json.dumps(dict(provenance=meta,files=records),indent=2),encoding='utf-8')
for name in ['reading_gates_matlab.log','reading_gate_failure.json','edf_channel_checks.csv','edf_file_checks.csv']:
    shutil.copyfile(OUT/name,OUT/('before_header_time_fix_'+name))
d=json.loads((OUT/'deviations.json').read_text(encoding='utf-8'));d['deviations'] += [dict(type='resolved EDF wall-clock header syntax',reason='MATLAB rejects seconds=60. Two local analysis-folder copies carry the minute (10.28.60 to 10.29.00; 14.23.60 to 14.24.00). Only header bytes 176:184 changed; all bytes from offset 256 onward are SHA-256 identical. Originals remain untouched. Analysis uses events.tsv sample indices, not EDF wall-clock times.',identified_without_method_outcomes=True,manifest='edf_header_copies.json',rerun='EDF/scalp gates once after this header compatibility fix'),dict(type='resolved JSON provenance serialization',reason='MATLAB jsondecode sanitizes object keys containing full paths. Full path/hash records are additionally stored as an array; values and source files are unchanged.')]
(OUT/'deviations.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
print(json.dumps(dict(header_copies=len(records),payloads_identical=True)))
