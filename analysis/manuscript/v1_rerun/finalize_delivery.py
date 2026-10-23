from pathlib import Path
import csv,json,re,hashlib,struct,subprocess,datetime,html
D=Path(__file__).resolve().parent;R=D.parents[1]/'apc-brainstorm-publish'
GIT=r'C:\Users\nghare\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe'
def git(*args):return subprocess.check_output([GIT,'-C',str(R),*args],text=True,encoding='utf-8').strip()
metadata=json.loads((D/'result_provenance.json').read_text(encoding='utf-8'));commit=metadata['git_commit']
assert git('rev-parse','HEAD')==git('rev-list','-n','1','v1.0')==commit and not git('status','--porcelain')
report=D/'RESULTS_v1.md';text=report.read_text(encoding='utf-8')
failed=json.loads((D/'figures_runtime_tooling_failure.json').read_text(encoding='utf-8'))
extra=("Additional rendering deviations: the committed figure function's automatic CSV import did not recognize the benchmark column. "
       "An external renderer with an explicit comma-delimited UTF-8 import then resolved the table, but its first launch omitted the frozen v1_options helper path. "
       "The successful renderer adds that helper path and reads the 14 native main MAT tables (4,200 rows), verifies their frozen commit, and uses the unchanged recovery-count and plot calculations. "
       "No benchmark was rerun and no tagged source or trial data was changed. The renderer and launcher are "
       "[render_frozen_figures.m](<"+(D/'render_frozen_figures.m').as_posix()+">) and "
       "[run_fixed_figures.m](<"+(D/'run_fixed_figures.m').as_posix()+">). "
       "Both failed logs are preserved as frozen_suite_matlab.log and fixed_figures_matlab.log; the successful log is fixed_figures2_matlab.log.\n\n"
       f"The runtime total above covers successful frozen stages only. The initial failed figure-import attempt additionally recorded {failed['elapsed_seconds']:.6f} seconds; "
       "the subsequent standalone helper-path failure did not record elapsed computation time. These failed attempts, the earlier pre-commit sanity attempt, and MATLAB startups are excluded from that total.\n\n")
if 'Additional rendering deviations:' not in text:
    text=text.replace('## Full result provenance',extra+'## Full result provenance',1)
svg_note=('SVG metadata deviation: MATLAB exports the closing svg tag across a newline, so the original literal closing-tag replacement did not insert provenance. '
          'Full metadata was inserted before that closing tag with a whitespace-tolerant match; no SVG graphics were changed.\n\n')
if 'SVG metadata deviation:' not in text:
    text=text.replace('## Full result provenance',svg_note+'## Full result provenance',1)
report.write_text(text,encoding='utf-8')
render_metadata=json.loads((D/'figure_render_metadata.json').read_text(encoding='utf-8'))
for bench in ['sparsity','distractor']:
    p=D/f'joint_recovery_{bench}.svg';svg=p.read_text(encoding='utf-8')
    if 'APC-v1-provenance' not in svg:
        payload='<metadata id="APC-v1-provenance">'+html.escape(json.dumps(render_metadata,separators=(',',':')))+' </metadata>\n'
        svg,count=re.subn(r'(?=</svg\s*>\s*$)',lambda match:payload,svg,count=1)
        assert count==1;p.write_text(svg,encoding='utf-8')
deviation_file=D/'tooling_deviations.json';deviations=json.loads(deviation_file.read_text(encoding='utf-8'))
if not any(x['category']=='svg_metadata' for x in deviations['entries']):
    deviations['entries'].append({'category':'svg_metadata','description':'MATLAB split the SVG closing tag across a newline. The literal metadata insertion did not match; inserted full provenance using a whitespace-tolerant closing-tag match without modifying SVG graphics.'})
    deviation_file.write_text(json.dumps(deviations,indent=2),encoding='utf-8')
# Check table structure and required result schemas without changing values.
expected=None;tables=0
for line in text.splitlines():
    if line.startswith('|'):
        count=len(re.split(r'(?<!\\)\|',line))-2
        if expected is None:expected=count;tables+=1
        assert count==expected
    else:expected=None
counts={}
for file,expected_count in [('main_trials.csv',4200),('random_fp_trials.csv',2700),('null_trials.csv',3500),('main_summary.csv',168),('random_fp_summary.csv',108),('null_recovery_summary.csv',140),('null_specificity_auc.csv',140)]:
    with (D/file).open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
    assert len(rows)==expected_count and all(r['git_commit']==commit for r in rows)
    counts[file]=len(rows)
for bench in ['sparsity','distractor']:
    data=(D/f'joint_recovery_{bench}.png').read_bytes();pos=8;found=False
    while pos<len(data):
        n=struct.unpack('>I',data[pos:pos+4])[0];kind=data[pos+4:pos+8];chunk=data[pos+8:pos+8+n]
        if kind==b'tEXt' and chunk.startswith(b'APC_provenance\0'):
            assert json.loads(chunk.split(b'\0',1)[1])['git_commit']==commit;found=True
        pos+=12+n
    assert found
    svg=(D/f'joint_recovery_{bench}.svg').read_text(encoding='utf-8');assert 'APC-v1-provenance' in svg and commit in svg
protected=json.loads((D/'protected_saved_results.json').read_text(encoding='utf-8'))
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==digest for p,digest in protected.items())
assert all(p.read_text(encoding='utf-8').isascii() for p in R.rglob('*.m'))
record={'status':'COMPLETE','git_commit':commit,'git_tag':'v1.0','branch':git('branch','--show-current'),
    'completed_local':datetime.datetime.now().isoformat(),'working_tree_clean':True,'method_unchanged_after_tag':True,
    'row_counts':counts,'markdown_tables_checked':tables,'all_protected_saved_results_unchanged':True,
    'tooling_fixes_recorded':'RESULTS_v1.md and tooling_deviations.json','metadata':metadata}
(D/'RUN_STATUS.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print('Final QA complete:',counts,'; tables:',tables,'; clean tag/commit:',commit)
