function [T,detail]=validation_estimate(x,t,profile,base,m,shifts)
% Frozen sources/rules evaluated at the prespecified configuration.
cfg=validation_settings(profile);opt1=cfg.apc_options_v1;opt3=cfg.apc_options_v3;fs=1/median(diff(t));
[r1,i1]=bst_apc(struct('data',x(:).','time',t(:).'),opt1);[r3,i3]=bst_apc(struct('data',x(:).','time',t(:).'),opt3);
refs={r1,r3};infos={i1,i3};fp=nan(1,3);sourceStatus=nan(1,3);sourceDetails=cell(1,3);
for k=1:2
 fp(k)=refs{k}.phase_frequency_hz.Value;sourceStatus(k)=refs{k}.status_code.Value;
 if ~isfinite(fp(k))
  opt=opt1;v='v1';if k==2,opt=opt3;v='v3';end
  [z,d]=apc_fp_source(x,t,v,opt);fp(k)=z.phase_frequency_hz;sourceStatus(k)=z.status_code;sourceDetails{k}=struct('metrics',z,'diagnostics',d);
 end
 if isfinite(fp(k)),sourceStatus(k)=0;end
end
[fp(3),sp,sourceStatus(3)]=sp_raw_fp(x,fs,opt3);sourceDetails{3}=sp;if isfinite(fp(3)),sourceStatus(3)=0;end
rows={};amplitudeDetails=cell(3,3);agreement=cell(1,2);
for k=1:3
 opt=opt1;if k>=2,opt=opt3;end
 later=k<=2&&isfinite(fp(k))&&refs{k}.status_code.Value~=0;
 [z,d,o]=apc_fa_given_fp(x,t,fp(k),opt);
 a=struct('fp',z.phase_frequency_hz,'fa',z.amplitude_frequency_hz,'raw',z.pac_strength,'pref',z.preferred_phase_deg,'coupling',z.normalized_mvl,'status',z.status_code,'band',z.final_band_hz,'route',string(z.route),'selection_score',nan);
 if ~isfinite(fp(k)),a.status=sourceStatus(k);end
 if k<=2
  expected=[refs{k}.phase_frequency_hz.Value,refs{k}.amplitude_frequency_hz.Value,refs{k}.pac_strength.Value,refs{k}.preferred_phase_deg.Value];observed=[a.fp,a.fa,a.raw,a.pref];
  mask=isfinite(expected)&isfinite(observed);delta=0;if any(mask),delta=max(abs(expected(mask)-observed(mask)));end
  pattern=isequal(isnan(expected),isnan(observed));statusSame=(a.status==refs{k}.status_code.Value);
  % A failed Step-1 source may expose a more specific source status; all finite-source outputs must agree.
  pass=pattern&&delta<=1e-10&&(statusSame||~isfinite(fp(k)));
  assert(pass,'Validation:APCAgreement','%s source%d extraction/reference mismatch; observed%s expected%s statuses[%g %g]',base.key,k,mat2str(observed,17),mat2str(expected,17),a.status,refs{k}.status_code.Value);
  agreement{k}=struct('source',k,'max_abs_error',delta,'nan_pattern_equal',pattern,'status_equal',statusSame,'pass',pass); %#ok<AGROW>
 end
 rows{end+1}=pack("F"+k+"_A_APC",k,"A_APC",a,fp(k),sourceStatus(k),later,opt,cfg); %#ok<AGROW>
 amplitudeDetails{k,1}=struct('metrics',z,'diagnostics',d,'options',o);
 [s,curve,settings]=validation_scan_fa(x,fs,fp(k),profile);
 a=selected(s.fp,s.fa,s.status,s.amplitude_band_hz,"SCAN",s.selection_score);
 if ~isfinite(fp(k)),a.status=sourceStatus(k);end
 rows{end+1}=pack("F"+k+"_A_SCAN",k,"A_SCAN",a,fp(k),sourceStatus(k),later,opt,settings); %#ok<AGROW>
 amplitudeDetails{k,2}=struct('selected',s,'scores',curve,'settings',settings);
 % Amendment 1: source success alone controls event-rule eligibility.
 input=struct('status_code',sourceStatus(k),'fp_hz',fp(k));if isfinite(fp(k)),input.status_code=0;end
 ev=apc_event_carrier(x,fs,input,cfg.amplitude_grid_hz,6,1.5,.020);
 a=selected(ev.fp_hz,ev.fa_hz,ev.status_code,[ev.fa_hz-6,ev.fa_hz+6],"APC",ev.score);
 rows{end+1}=pack("F"+k+"_A_EVENT",k,"A_EVENT",a,fp(k),sourceStatus(k),later,opt,struct('amplitude_grid_hz',cfg.amplitude_grid_hz,'amplitude_half_width_hz',6,'phase_half_width_hz',1.5,'min_separation_s',.020,'threshold_sd',.75,'prominence_sd',.25)); %#ok<AGROW>
 amplitudeDetails{k,3}=struct('source_input',input,'output',ev);
end
mode="A2_prime";if cfg.amplitude_half_width_hz==30,mode="HA_A2_prime";elseif cfg.amplitude_half_width_hz==12,mode="rodent_A2_prime";end
[scans,maps]=validation_a2_map(x,fs,profile,mode,.5);s=scans(string({scans.method})=="MVL-Ozkurt");assert(isscalar(s));
a=selected(s.fp,s.fa,s.status,[max(1,s.fa-cfg.amplitude_half_width_hz),min(fs/2-1,s.fa+cfg.amplitude_half_width_hz)],"SCAN",s.score);
rows{end+1}=pack("A2_prime_2D",0,"A_SCAN",a,s.fp,s.status,false,opt3,cfg);
for k=1:2
 a=rows{(k-1)*3+1};a.method="APC-v1.0";if k==2,a.method="APC-v3.0";end;a.f_source="end_to_end";
 % End-to-end reference status is retained, including Step-1/2 failures.
 a.status=refs{k}.status_code.Value;a.valid=a.status==0&&all(isfinite([a.recovered_fp_hz a.recovered_fa_hz a.coupling]));rows{end+1}=a; %#ok<AGROW>
end
calibration=validation_calibration(x,fs,fp(3),cfg,shifts);
T=struct2table(vertcat(rows{:}));detail=struct('r1',r1,'i1',i1,'r3',r3,'i3',i3,'source_fp_hz',fp,'source_status',sourceStatus,'source_details',{sourceDetails},'amplitude_details',{amplitudeDetails},'agreement',{agreement},'a2_map',{maps},'calibration',calibration,'provenance',m);
 function a=selected(f,fa,status,band,family,score)
  a=struct('fp',f,'fa',fa,'raw',nan,'pref',nan,'coupling',nan,'status',status,'band',band,'route',"not_applicable",'selection_score',score);
  if status==0&&all(isfinite([f fa band]))
   c=paper2_coupling_at_pair(x,t,f,fa,band,family);a.raw=c.raw_mvl;a.pref=c.preferred_phase_deg;a.coupling=c.normalized_mvl;a.status=c.status;
  end
 end
 function row=pack(method,k,rule,a,sourcefp,ss,later,opt,settings)
  row=base;row.method=method;row.f_source="F"+k;row.a_rule=rule;row.source_fp_hz=sourcefp;row.source_status=ss;row.step2_fp_later_apc_failed=later;
  row.recovered_fp_hz=a.fp;row.recovered_fa_hz=a.fa;row.raw_mvl=a.raw;row.coupling=a.coupling;row.preferred_phase_deg=a.pref;row.status=a.status;row.valid=a.status==0&&all(isfinite([a.fp a.fa a.coupling]));row.selection_score=a.selection_score;row.amplitude_band_low_hz=a.band(1);row.amplitude_band_high_hz=a.band(2);row.route=a.route;
  row.git_commit=string(m.git_head);row.protocol_sha256=string(m.protocol_sha256);row.matlab_version=string(version);row.options_json=string(jsonencode(opt));row.comparator_settings_json=string(jsonencode(settings));row.provenance_file="provenance.json";
 end
end
