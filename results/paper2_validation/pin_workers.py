from pathlib import Path
import json,hashlib,datetime,sys,subprocess
O=Path(__file__).resolve().parent;R=O.parent.parent;sys.path.insert(0,str(R/'pydeps'))
import pandas as pd
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
P=json.loads((O/'provenance.json').read_text(encoding='utf-8'))
assert json.loads((O/'all_gate_results.json').read_text(encoding='utf-8'))['status']=='PASS'
assert json.loads((O/'generation_complete.json').read_text(encoding='utf-8'))['status']=='COMPLETE'
assert not list(O.glob('worker*_complete.json'))
P.update(status='READY_FOR_METHODS',gates_started=True,gates_passed=True,new_signal_generated=True,
         method_output_computed=False,environment=json.loads((O/'environment.json').read_text(encoding='utf-8')),
         configuration=json.loads((O/'configuration.json').read_text(encoding='utf-8')),
         input_banks=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(O.glob('V*_inputs.mat'))],
         real_inputs=json.loads((O/'real_input_provenance.json').read_text(encoding='utf-8')),
         implementation_files=[dict(path=str(p),sha256=sha(p)) for p in sorted(O.glob('*.m'))],
         calibration_shift_rule=json.loads((O/'generation_complete.json').read_text(encoding='utf-8'))['shift_rule'],
         coupling_rule='Unchanged ablation common APC phase-band rule. APC/event use fourth-order amplitude band, scan uses original guarded SOS band; event half-width 6 Hz.',
         reference_policy='Saved real-data selected pairs; ECoG ablation common coupling reused. Rodent saved A2 pairs are remeasured with common ablation phase rule; APC saved coupling retained.',
         method_start_prepared_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(O/'provenance.json').write_text(json.dumps(P,indent=2)+'\n',encoding='utf-8')
d=json.loads((O/'deviations.json').read_text(encoding='utf-8'))
Q=pd.read_csv(O/'rodent_saved_csv_precision_differences.csv',encoding='utf-8')
d['deviations'].append(dict(code='SAVED_RODENT_CSV_PRECISION',reason='Exact deduplication of shared physical inputs incorrectly required equality of rounded raw/phase/coupling CSV fields. Shared physical bounds, fP, fA and status match exactly; raw values were written at different precision.',fix='Preserve every original reference row by bout-set and analysis, keep one physical reference for computation, and audit all numeric CSV differences separately.',identified_without_new_outcomes=True,n_differences=len(Q),max_absolute_difference=float(abs(Q.difference).max()),audit_file='rodent_saved_csv_precision_differences.csv'))
(O/'deviations.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
with (O/'RESULTS_validation.md').open('a',encoding='utf-8') as f:
 f.write('\n## Gates and generation completed\n\nG-gen PASS: all 675 HB and 900 HA complete cases bit-identical; six P1 repeat-1 double-generation checks identical, no outcomes. G-event PASS at 1e-12. G-abl PASS: 42 APC cases and 23 scan cases.\n\nV1: 350 inputs (175 coupled, 175 paired timing nulls); V2: 900 (450 + 450); V3: 600 (six cells x 100); V4: 25. Original HB stream order was retained by generating its full sequence and selecting only the prespecified H1/H3 or H4 inputs. No methods run on unused source-sequence inputs.\n')
print(json.dumps({'status':P['status'],'input_banks':len(P['input_banks']),'rodent_inputs':P['real_inputs']['rodent_physical_inputs'],'ecog_inputs':P['real_inputs']['ecog_bouts']},indent=2))
