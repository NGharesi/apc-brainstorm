function audit_rodent_filters
out='C:\Users\nghare\.brainstorm\process\revision_checks\final';root=fileparts(fileparts(out));
S=load(fullfile(root,'apc_ec013_run_rest_results.mat'),'results');base=S.results;fs=base.fs_hz;
rows=struct([]);i=0;
for f=4:.5:12
 i=i+1;wn=[f-1.5 f+1.5]/(fs/2);[b,a]=butter(4,wn,'bandpass');[z,p,k]=butter(4,wn,'bandpass');[sos,g]=zp2sos(z,p,k);
 bt=base.run.bouts(1,:);x=base.signal_window(bt.start_idx:bt.stop_idx);y=filtfilt(b,a,x(:));ys=filtfilt(sos,g,x(:));
 ww=[2*pi*f/fs 2*pi*f/fs+1e-9];hv=freqz(b,a,ww);hsv=freqz(sos,ww)*g;h=hv(1);hs=hsv(1);
 item=struct('fP_hz',f,'max_pole_ba',max(abs(roots(a))),'max_pole_zpk',max(abs(p)),'center_gain_ba',abs(h),'center_gain_sos',abs(hs),'rms_ba',sqrt(mean(y.^2)),'rms_sos',sqrt(mean(ys.^2)),'relative_L2_difference',norm(y-ys)/norm(ys),'max_abs_ba',max(abs(y)),'max_abs_sos',max(abs(ys)));rows=[rows;item]; %#ok<AGROW>
end
T=struct2table(rows);meta=jsondecode(fileread(fullfile(out,'analysis_provenance.json')));T.provenance_json=repmat(string(jsonencode(meta)),height(T),1);writetable(T,fullfile(out,'rodent_filter_audit.csv'));disp(T(:,1:10));
end
