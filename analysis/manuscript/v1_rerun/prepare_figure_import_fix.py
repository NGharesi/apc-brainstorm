from pathlib import Path
import csv,json,hashlib
D=Path(__file__).resolve().parent;R=D.parents[1]/'apc-brainstorm-publish'
for name,expected in [('main',4200),('random_fp',2700),('null',3500)]:
    with (D/(name+'_trials.csv')).open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
    assert len(rows)==expected and all('benchmark' in r and None not in r for r in rows)
old=D/'figures_runtime.json';copy=D/'figures_runtime_tooling_failure.json'
if not copy.exists():copy.write_bytes(old.read_bytes())
source=(R/'analysis/v1_revision/v1_make_figures.m').read_text(encoding='utf-8')
source=source.replace('function v1_make_figures(', 'function render_frozen_figures(',1)
source=source.replace("'TextType','string');", "'TextType','string','Delimiter',',','VariableNamingRule','preserve','Encoding','UTF-8');",1)
target=D/'render_frozen_figures.m';target.write_text(source,encoding='utf-8')
record=json.loads(copy.read_text(encoding='utf-8'));metadata=record['metadata']
metadata['tooling_renderer']={'path':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'change':'explicit CSV delimiter, preserved variable names and UTF-8; plot calculations unchanged'}
(D/'figure_render_metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
deviations=json.loads((D/'tooling_deviations.json').read_text(encoding='utf-8'))
deviations['entries'].append({'category':'figure_csv_import','description':'MATLAB automatic CSV delimiter detection produced no benchmark column after all simulation stages completed. Preserved failed figures runtime; rendered through an external copy with explicit comma delimiter, preserved names and UTF-8. Frozen repository and all trial data unchanged.'})
(D/'tooling_deviations.json').write_text(json.dumps(deviations,indent=2),encoding='utf-8')
print('All 10400 simulation rows have the expected CSV schema; prepared renderer import-only fix.')
