from pathlib import Path
import sys,json,hashlib,csv,xml.etree.ElementTree as ET
ROOT=Path(r'C:\Users\nghare\.brainstorm\process');OUT=ROOT/'revision_checks/rodent_multi';sys.path.insert(0,str(ROOT/'pydeps'))
import numpy as np
import pandas as pd
BASE=Path(r'D:\APC_project\Previous_Computer\RealData');PAPER=BASE/'tPACPaper'
XML=BASE/'ec012ec.14/ec012ec.269/ec012ec.269.xml'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
meta=json.loads((OUT/'regional_protocol_record.json').read_text(encoding='utf-8'))
meta=meta|dict(stage='metadata and regional selection',sources={str(p):sha(p) for p in [XML,PAPER/'ElePosition.txt',PAPER/'hc3-session.csv',OUT/'channel_ratios.csv']})
groups=[[int(c.text) for c in g.findall('channel')] for g in ET.parse(XML).findall('./anatomicalDescription/channelGroups/group')]
passed=groups==[list(range(i,i+8)) for i in range(0,32,8)]+[[32]]
evidence=dict(metadata=meta,anatomical_groups_zero_based=groups,contiguous_eight_channel_blocks=passed,auxiliary_raw_channel=32,
              one_based_electrode_groups=[[i+1 for i in g] for g in groups])
(OUT/'regional_xml_grouping.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
assert passed,'METHOD-RELEVANT STOP: XML anatomical groups are not contiguous 8-channel blocks'
with (PAPER/'hc3-session.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.reader(f))
session_rows={r[2]:r for r in rows if len(r)>=6}
electrodes={}
for n,line in enumerate((PAPER/'ElePosition.txt').read_text(encoding='utf-8').splitlines(),1):
    f=line.split();electrodes[f[0]]=dict(regions=f[4:],source_line=n,source_text=line)
ratios=pd.read_csv(OUT/'channel_ratios.csv',encoding='utf-8');mapped=[];selected=[];sessions=[]
for session,g in ratios.groupby('session',sort=False):
    r=session_rows[session];assert r[3]=='linear',f'METHOD-RELEVANT STOP: {session} behavior {r[3]}'
    animal=g.animal.iloc[0];directory=r[1];e=electrodes[directory];regions=e['regions'];assert len(regions)==(8 if animal=='EC013' else 4)
    assumption='assumed contiguous, verified on ec012ec.269' if animal=='EC013' else ('verified in session XML' if session=='ec012ec.269' else 'contiguous mapping applied from ec012ec.269 as prespecified')
    one=[]
    for _,x in g.iterrows():
        ch=int(x.channel_index);aux=ch>(64 if animal=='EC013' else 32);shank=(ch-1)//8+1 if not aux else np.nan;region=regions[int(shank)-1] if not aux else 'auxiliary'
        row=dict(animal=animal,session=session,top_directory=directory,channel_index=ch,channel_name=x.channel_name,shank=shank,region=region,auxiliary=aux,
                 theta_delta_ratio=x.theta_delta_ratio,source_channel_flag=x.source_channel_flag,source_file=x.source_file,mapping_evidence=assumption,
                 session_metadata_row=','.join(r),eleposition_line=e['source_line'],eleposition_source_text=e['source_text'])
        one.append(row);mapped.append(row)
    frame=pd.DataFrame(one)
    analyses=['EC']+(['CA1','E1_sensitivity'] if animal=='EC013' else [])
    for analysis in analyses:
        eligible=frame[frame.channel_index==1] if analysis=='E1_sensitivity' else frame[(~frame.auxiliary)&(frame.region.str.startswith('EC') if analysis=='EC' else frame.region.eq('CA1'))]
        eligible=eligible[np.isfinite(eligible.theta_delta_ratio)].sort_values('channel_index');assert len(eligible)>0
        best=eligible.loc[eligible.theta_delta_ratio.idxmax()].to_dict();selected.append(best|{'analysis':analysis})
    sessions.append(dict(animal=animal,session=session,top_directory=directory,behavior=r[3],metadata_duration_s=float(r[5]),shank_regions=';'.join(regions),mapping_evidence=assumption))
for values,name in [(mapped,'regional_channel_map.csv'),(selected,'regional_selected_channels.csv'),(sessions,'regional_session_metadata.csv')]:
    d=pd.DataFrame(values);d['git_commit']=meta['git_commit'];d['provenance_json']=json.dumps(meta,separators=(',',':'));d.to_csv(OUT/name,index=False,encoding='utf-8')
print(json.dumps(dict(status='PASS',sessions=len(sessions),channel_map_rows=len(mapped),selections=len(selected),groups=groups)))
