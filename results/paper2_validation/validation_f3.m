function [rows,detail]=validation_f3(x,t,profile)
cfg=validation_settings(profile);fs=1/median(diff(t));[fp,sp,status]=sp_raw_fp(x,fs,cfg.apc_options_v3);if isfinite(fp),status=0;end
[s,scores,settings]=validation_scan_fa(x,fs,fp,profile);a=one("F3_A_SCAN",s.fp,s.fa,s.status,s.amplitude_band_hz,"SCAN",s.selection_score);
input=struct('status_code',status,'fp_hz',fp);ev=apc_event_carrier(x,fs,input,cfg.amplitude_grid_hz,6,1.5,.020);b=one("F3_A_EVENT",ev.fp_hz,ev.fa_hz,ev.status_code,[ev.fa_hz-6 ev.fa_hz+6],"APC",ev.score);
rows=[a;b];detail=struct('source_fp_hz',fp,'source_status',status,'sp',sp,'scan',s,'scan_scores',scores,'scan_settings',settings,'event_input',input,'event',ev);
 function row=one(method,f,fa,ss,band,family,score)
  row=struct('method',method,'source_fp_hz',fp,'source_status',status,'recovered_fp_hz',f,'recovered_fa_hz',fa,'raw_mvl',nan,'coupling',nan,'preferred_phase_deg',nan,'status',ss,'valid',false,'selection_score',score,'amplitude_band_low_hz',band(1),'amplitude_band_high_hz',band(2));
  if ss==0&&all(isfinite([f fa band]))
   c=paper2_coupling_at_pair(x,t,f,fa,band,family);row.raw_mvl=c.raw_mvl;row.coupling=c.normalized_mvl;row.preferred_phase_deg=c.preferred_phase_deg;row.status=c.status;row.valid=c.status==0&&isfinite(c.normalized_mvl);
  end
 end
end
