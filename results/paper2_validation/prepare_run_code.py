from pathlib import Path
import hashlib,json
O=Path(__file__).resolve().parent;root=O.parent.parent;repo=root/'apc-brainstorm-publish'
src=(root/'revision_checks/v3_aperiodic/generate_v3_hb.m').read_text(encoding='utf-8')
new=src.replace('function generate_v3_hb(out,meta)','function validation_hb_cases(out,meta,seed)',1).replace('20261022','seed')
new=new.replace('new_stream(1)','new_stream(1,seed)').replace('new_stream(2)','new_stream(2,seed)').replace('new_stream(3)','new_stream(3,seed)').replace('function stream=new_stream(sub)','function stream=new_stream(sub,seed)')
new=new.replace('verification_row(n,meta)','verification_row(n,meta,seed)').replace('function r=verification_row(c,meta)','function r=verification_row(c,meta,seed)')
(O/'validation_hb_cases.m').write_text(new,encoding='utf-8')
# Selection computations remain verbatim; only named profile configuration is externalized.
archive=repo/'results/paper2_ablation'
s=(archive/'scan_fa_given_fp.m').read_text(encoding='utf-8')
s=s.replace('function [result,scores,settings]=scan_fa_given_fp','function [result,scores,settings]=validation_scan_fa',1)
start=s.index('if profile=="HA"');end=s.index('\nresult=struct',start)
s=s[:start]+"cfg=validation_settings(profile);settings.amplitude_grid_hz=cfg.amplitude_grid_hz;settings.amplitude_half_width_hz=cfg.amplitude_half_width_hz;"+s[end:]
(O/'validation_scan_fa.m').write_text(s,encoding='utf-8')
s=(archive/'a2_reference_map.m').read_text(encoding='utf-8')
s=s.replace('function [rows,maps]=a2_reference_map','function [rows,maps]=validation_a2_map',1)
start=s.index('if profile=="HA"');end=s.index('\nrows=struct',start)
s=s[:start]+"cfg=validation_settings(profile);faGrid=cfg.amplitude_grid_hz;fpStart=cfg.phase_grid_hz(1);fpStop=cfg.phase_grid_hz(end);"+s[end:]
# Existing A2-prime modes already implement every prespecified half-width.
(O/'validation_a2_map.m').write_text(s,encoding='utf-8')
rec={'generator_adapter':'Only function/seed argument and references to the seed changed from generate_v3_hb.m.',
     'scan_adapter':'Only function name and profile initialization changed; selection/filter/metric/tie body unchanged.',
     'map_adapter':'Only function name and profile initialization changed; score/filter/metric/tie body unchanged.',
     'source_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [root/'revision_checks/v3_aperiodic/generate_v3_hb.m',archive/'scan_fa_given_fp.m',archive/'a2_reference_map.m']}}
(O/'adapter_record.json').write_text(json.dumps(rec,indent=2)+'\n',encoding='utf-8')
