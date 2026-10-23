from pathlib import Path
import difflib,json
O=Path(__file__).resolve().parent;R=O.parent.parent
s=(R/'revision_checks/rodent_multi/v1_bout_features.m').read_text(encoding='utf-8')
t=s.replace('function [row,info]=v1_bout_features','function [row,info]=v3_bout_features',1).replace("struct('fA',[80 150])","struct('fA',[80 150],'version','v3','minPhaseHz',1,'maxPhaseHz',30)",1).replace('APC-v1.0','APC-v3.0',1)
t=t.replace('if row.status~=0,return;end','row.n_bursts=s.n_bursts.Value;\nif row.status~=0,return;end',1)
(O/'v3_bout_features.m').write_text(t,encoding='utf-8');(O/'phaseC/v3_feature_wrapper.diff').write_text(''.join(difflib.unified_diff(s.splitlines(True),t.splitlines(True),fromfile='unchanged v1_bout_features.m',tofile='v3 version/options wrapper')),encoding='utf-8')
p=O/'deviations.json';d=json.loads(p.read_text(encoding='utf-8'));d['deviations'].append(dict(type='Phase-C wrapper setup quoting (tooling)',reason='A PowerShell parsing error rejected an inline Python wrapper-copy command before it executed. The same literal replacement is performed by this saved UTF-8 Python script. No input, method source, option or estimate was changed by the failed command.'));p.write_text(json.dumps(d,indent=2),encoding='utf-8')
