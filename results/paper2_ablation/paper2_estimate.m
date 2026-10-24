function [T,detail]=paper2_estimate(x,t,profile,opt1,opt3,ref1,ref3,spfp,spstatus,sp,scanRef,m,base)
% Frozen end-to-end coordinates reused; only missing stages are computed.
fp=[ref1.fp,ref3.fp,spfp];sourceStatus=[ref1.status,ref3.status,spstatus];sourceDetails=cell(1,3);
for k=1:2
 if isfinite(fp(k)),sourceStatus(k)=0;continue;end
 options=opt1;v='v1';if k==2,options=opt3;v='v3';end
 [f,d]=apc_fp_source(x,t,v,options);fp(k)=f.phase_frequency_hz;sourceStatus(k)=f.status_code;sourceDetails{k}=struct('metrics',f,'diagnostics',d);
end
sourceDetails{3}=sp;refs={ref1,ref3};rows={};aa=cell(1,3);as=cell(1,3);scanSettings=cell(1,3);
for k=1:3
 paper2_error_context('context',base.key,k);
 options=opt1;if k>=2,options=opt3;end
 % At its own fP, the first two A_APC results equal the saved end-to-end run.
 if k<=2
  a=refs{k};a.source_fp=fp(k);a.normalized_mvl=nan;
  if a.status==0
   c=paper2_coupling_at_pair(x,t,a.fp,a.fa,a.band,"APC");paper2_assert(c.status==0,'Paper2:Coupling','APC reference coupling invalid',c.status,0,k,base.key);
   paper2_assert(abs(c.raw_mvl-a.raw)<=1e-10,'Paper2:ReferenceMVL','Saved APC raw MVL reconstruction mismatch',c.raw_mvl,a.raw,k,base.key);
   if isfield(a,'normalized_saved')&&isfinite(a.normalized_saved),paper2_assert(abs(c.normalized_mvl-a.normalized_saved)<=1e-10,'Paper2:ReferenceNormalized','Saved APC normalized MVL mismatch',c.normalized_mvl,a.normalized_saved,k,base.key);end
   a.normalized_mvl=c.normalized_mvl;
  end
 else
  [z,d,o]=apc_fa_given_fp(x,t,fp(k),options);a=struct('source_fp',fp(k),'fp',z.phase_frequency_hz,'fa',z.amplitude_frequency_hz,'raw',z.pac_strength,'pref',z.preferred_phase_deg,'normalized_mvl',z.normalized_mvl,'status',z.status_code,'band',z.final_band_hz,'route',string(z.route));aa{k}=struct('metrics',z,'diagnostics',d,'options',o);
 end
 if sourceStatus(k)~=0,a.fp=nan;a.fa=nan;a.raw=nan;a.pref=nan;a.normalized_mvl=nan;a.status=sourceStatus(k);end
 endFailed=k<=2&&isfinite(fp(k))&&refs{k}.status~=0;
 rows{end+1}=pack("F"+k+"_A_APC","F"+k,"A_APC",a,fp(k),sourceStatus(k),endFailed,options,[]); %#ok<AGROW>
 [s,curve,settings]=scan_fa_given_fp(x,1/median(diff(t)),fp(k),profile);scanSettings{k}=settings;
 b=struct('fp',s.fp,'fa',s.fa,'raw',nan,'pref',nan,'normalized_mvl',nan,'status',s.status,'band',s.amplitude_band_hz,'route',"not_applicable");
 if sourceStatus(k)~=0,b.fp=nan;b.fa=nan;b.status=sourceStatus(k);
 elseif b.status==0
  c=paper2_coupling_at_pair(x,t,b.fp,b.fa,b.band,"SCAN");b.raw=c.raw_mvl;b.pref=c.preferred_phase_deg;b.normalized_mvl=c.normalized_mvl;b.status=c.status;
 end
 as{k}=struct('selected',s,'scores',curve,'common_coupling',b,'settings',settings);
 rows{end+1}=pack("F"+k+"_A_SCAN","F"+k,"A_SCAN",b,fp(k),sourceStatus(k),endFailed,options,settings); %#ok<AGROW>
end
half=14;if profile=="HA"||profile=="ecog",half=30;end
band=[max(1,scanRef.fa-half),min(1/median(diff(t))/2-1,scanRef.fa+half)];c=paper2_coupling_at_pair(x,t,scanRef.fp,scanRef.fa,band,"SCAN");
b=struct('fp',scanRef.fp,'fa',scanRef.fa,'raw',c.raw_mvl,'pref',c.preferred_phase_deg,'normalized_mvl',c.normalized_mvl,'status',c.status,'band',band,'route',"not_applicable");
rows{end+1}=pack("A2_prime_2D","2D","A_SCAN",b,b.fp,0,false,opt3,struct('profile',profile,'amplitude_half_width_hz',half,'original_selection_score',scanRef.score));
% Separate references are intentionally retained under Amendment 1.
for k=1:2
 a=rows{2*k-1};a.method="APC-v1.0";if k==2,a.method="APC-v3.0";end;a.f_source="end_to_end";rows{end+1}=a; %#ok<AGROW>
end
T=struct2table(vertcat(rows{:}));detail=struct('source_fp_hz',fp,'source_status',sourceStatus,'source_details',{sourceDetails},'apc_new',{aa},'scan',{as},'ref1',ref1,'ref3',ref3,'scan_reference',scanRef,'provenance',m);
 function row=pack(method,source,rule,a,sourcefp,sourcestatus,laterfailed,options,settings)
  fulloptions=paper2_options(options);fulloptions.version='v1';if isfield(options,'version'),fulloptions.version=options.version;end
  row=base;row.method=method;row.f_source=source;row.a_rule=rule;row.source_fp_hz=sourcefp;row.source_status=sourcestatus;row.step2_fp_later_apc_failed=laterfailed;row.recovered_fp_hz=a.fp;row.recovered_fa_hz=a.fa;row.raw_mvl=a.raw;row.coupling=a.normalized_mvl;row.preferred_phase_deg=a.pref;row.status=a.status;row.valid=a.status==0&&all(isfinite([a.fp a.fa a.normalized_mvl]));row.amplitude_band_low_hz=a.band(1);row.amplitude_band_high_hz=a.band(2);row.route=string(a.route);row.git_commit=string(m.git_head);row.protocol_sha256=string(m.protocol_sha256);row.matlab_version=string(version);row.options_json=string(jsonencode(fulloptions));row.comparator_settings_json=string(jsonencode(settings));row.provenance_file="provenance.json";
 end
end
