"""Prepare POST HOC descriptive overlap using unchanged historical 12/12 reference."""
from pathlib import Path
OUT=Path(__file__).resolve().parent;PARENT=OUT.parent
source=(PARENT/'regional_behavior_checks.py').read_text(encoding='utf-8')
source=source.replace("ROOT=Path(r'C:\\Users\\nghare\\.brainstorm\\process');OUT=ROOT/'revision_checks/rodent_multi'", "ROOT=Path(r'C:\\Users\\nghare\\.brainstorm\\process');OUT=Path(__file__).resolve().parent;PARENT=OUT.parent")
source=source.replace('regional_protocol_record.json','posthoc_2s_provenance.json').replace("stage='tracking-rate QC and descriptive historical overlap; no gate'", "stage='POST HOC 2-s descriptive overlap; no gate'")
source=source.replace("OUT.glob('*_regional_tracking.npz')","PARENT.glob('*_regional_tracking.npz')")
source=source.replace("d=pd.DataFrame(rows);d['provenance_json']", "d=pd.DataFrame(rows);d['analysis_type']=meta['analysis_type'];d['post_hoc']=True;d['minimum_bout_s']=2;d['provenance_json']")
source=source.replace("loadmat(OUT/'behavior_reproduction.mat'", "loadmat(PARENT/'behavior_reproduction.mat'")
source=source.replace("state+'_candidate_intervals_ge_5_s':int((dur>=5).sum())", "state+'_candidate_intervals_ge_2_s':int((dur>=2).sum())")
source=source.replace('regional_behavior_qc.csv','posthoc_2s_behavior_qc.csv').replace('regional_bouts.csv','posthoc_2s_bouts.csv')
source=source.replace('regional_historical_overlap','posthoc_2s_historical_overlap')
(OUT/'posthoc_2s_descriptive.py').write_text('"""POST HOC 2-s descriptive analysis; historical reference remains 12/12."""\n'+source,encoding='utf-8')
