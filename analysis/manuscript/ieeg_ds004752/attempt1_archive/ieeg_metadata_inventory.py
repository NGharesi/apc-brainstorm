"""Read BIDS metadata only; do not choose contacts or compute PAC."""
from pathlib import Path
import json,sys,re,hashlib,difflib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent;sys.path.insert(0,str(ROOT/'pydeps'))
import pandas as pd
meta=json.loads((OUT/'provenance.json').read_text(encoding='utf-8'));data=Path(meta['data_root']);rows=[];pairs=[]
for subject in sorted(data.glob('sub-*')):
    sessions=[]
    for f in sorted(subject.glob('ses-*/ieeg/*_ieeg.edf')):
        base=str(f)[:-len('_ieeg.edf')];c=pd.read_csv(base+'_channels.tsv',sep='\t',encoding='utf-8');e=pd.read_csv(base+'_events.tsv',sep='\t',encoding='utf-8');a=pd.read_csv(base+'_electrodes.tsv',sep='\t',encoding='utf-8')
        labels=dict(zip(a.name,a.AnatomicalLocation));sessions.append((f,c,e,labels))
        rows.append(dict(patient=subject.name,session=f.parent.parent.name,edf_file=str(f),channels=len(c),trials=len(e),artifact_flag_trials=int((e.Artifact==1).sum()),last_end_sample=int(e.endSample.iloc[-1]),edf_bytes=f.stat().st_size,channels_tsv_sha256=hashlib.sha256(Path(base+'_channels.tsv').read_bytes()).hexdigest(),events_tsv_sha256=hashlib.sha256(Path(base+'_events.tsv').read_bytes()).hexdigest(),electrodes_tsv_sha256=hashlib.sha256(Path(base+'_electrodes.tsv').read_bytes()).hexdigest()))
    common=set.intersection(*(set(c.name) for _,c,_,_ in sessions))
    for name in sorted(common):
        m=re.fullmatch(r'(.+?)(\d+)',name)
        if not m:continue
        prefix,k=m[1],int(m[2]);other=prefix+str(k+1)
        if other not in common:continue
        anatomy=[(str(labels.get(name,'')),str(labels.get(other,''))) for _,_,_,labels in sessions]
        if not all(a.startswith('Hipp') or b.startswith('Hipp') for a,b in anatomy):continue
        pairs.append(dict(patient=subject.name,deeper_contact=name,adjacent_contact=other,prefix=prefix,k=k,sessions=len(sessions),deeper_labels=';'.join(sorted({a for a,b in anatomy})),adjacent_labels=';'.join(sorted({b for a,b in anatomy}))))
for values,name in [(rows,'metadata_file_inventory.csv'),(pairs,'metadata_candidate_pairs.csv')]:
    d=pd.DataFrame(values);d['provenance_json']=json.dumps(meta,separators=(',',':'));d.to_csv(OUT/name,index=False,encoding='utf-8')
# Save the explicit source diff for the header-compatibility reader correction.
after=(OUT/'ieeg_reading_gates.m').read_text(encoding='utf-8');before=after.replace("readPath=compatible_path(path,out);I=edfinfo(readPath);","I=edfinfo(path);").replace('TT=edfread(readPath);','TT=edfread(path);').replace("TT=edfread(readPath,'SelectedSignals'","TT=edfread(path,'SelectedSignals'")
before=before[:before.index('function value=compatible_path(path,out)')]
(OUT/'header_time_reader_fix.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='before_header_time_fix',tofile='ieeg_reading_gates.m')),encoding='utf-8')
print(json.dumps(dict(files=len(rows),patients=len({r['patient'] for r in rows}),candidate_pairs=len(pairs),candidate_patients=len({r['patient'] for r in pairs}))))
