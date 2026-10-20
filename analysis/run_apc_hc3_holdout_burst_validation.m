function results = run_apc_hc3_holdout_burst_validation(profile)
% RUN_APC_HC3_HOLDOUT_BURST_VALIDATION
% Select APC and raw-spectrum carrier pairs from a training half-window,
% then evaluate high-frequency burst phase concentration on the independent
% held-out half. This tests burst-mode selection without reusing evaluation
% samples for carrier selection. It is not a calibrated coupling test.
%
% Usage: run_apc_hc3_holdout_burst_validation('reviewer')

    if nargin < 1 || isempty(profile), profile = 'reviewer'; end
    cfg = local_config(profile); rows = repmat(local_empty_row(),0,1);
    for iAnimal = 1:numel(cfg.animals)
        animal = cfg.animals{iAnimal}; root = fullfile(cfg.data_root,animal);
        sessions = dir(fullfile(root,'ec*.eeg'));
        for iSession = 1:numel(sessions)
            file = fullfile(sessions(iSession).folder,sessions(iSession).name,'data_block001.mat');
            if ~exist(file,'file'), continue; end
            try
                [signal,time,fs] = local_load(file,cfg.channel_index);
                windows = local_windows(time,fs,cfg);
                for iWindow = 1:height(windows)
                    idx = windows.start_idx(iWindow):windows.stop_idx(iWindow);
                    x = signal(idx); t = time(idx); split = floor(numel(x)/2);
                    train = x(1:split); trainT = t(1:split); test = x(split+1:end);
                    apc = bst_apc(struct('data',train,'time',trainT),cfg.apc_options);
                    [rawFP,rawFA] = local_raw_peaks(train,fs,cfg);
                    rows(end+1,1) = local_row(animal,sessions(iSession).name,iWindow,apc,rawFP,rawFA,test,fs,cfg); %#ok<AGROW>
                end
            catch ME
                warning('Skipping %s: %s',sessions(iSession).name,ME.message);
            end
        end
    end
    T = struct2table(rows); if isempty(T), error('No windows were analyzed.'); end
    S = local_summary(T); outDir=fileparts(mfilename('fullpath')); tag=lower(cfg.profile);
    files.epochs=fullfile(outDir,sprintf('apc_hc3_holdout_burst_validation_%s_epochs.csv',tag));
    files.sessions=fullfile(outDir,sprintf('apc_hc3_holdout_burst_validation_%s_sessions.csv',tag));
    files.summary=fullfile(outDir,sprintf('apc_hc3_holdout_burst_validation_%s_summary.txt',tag));
    files.figure=fullfile(outDir,sprintf('apc_hc3_holdout_burst_validation_%s.png',tag));
    files.mat=fullfile(outDir,sprintf('apc_hc3_holdout_burst_validation_%s.mat',tag));
    writetable(T,files.epochs); writetable(S,files.sessions); results=struct('config',cfg,'epoch_table',T,'session_table',S,'files',files); save(files.mat,'results','-v7.3');
    local_plot(T,files.figure); local_write(results,files.summary);
    fprintf('Saved held-out burst validation: %s\n',files.summary);
end

function cfg=local_config(profile)
    cfg.profile=lower(char(profile)); cfg.data_root='D:\APC_project\RealDatasets\LFP_data\HC3\data';
    cfg.animals={'EC012','EC013'}; cfg.channel_index=1; cfg.window_s=30; cfg.edge_s=10; cfg.windows_per_session=12;
    if strcmp(cfg.profile,'screening'), cfg.windows_per_session=4; elseif ~ismember(cfg.profile,{'reviewer','frozen_reviewer'}), error('Use screening, reviewer or frozen_reviewer.'); end
    cfg.fP_range=[1 30]; cfg.fA_range=[80 150];
    cfg.apc_options=struct('fA',cfg.fA_range,'epoch',[-.6 .6],'decomposition','fft_peak','metric','canolty','diagm',false,'surrogates',false,'num_perm',0,'numPhaseBins',18);
end

function [x,t,fs]=local_load(file,ch)
    S=load(file); F=double(S.F); t=double(S.Time(:).'); if size(F,2)~=numel(t), F=F.'; end
    x=F(ch,:); fs=1/median(diff(t));
end

function W=local_windows(t,fs,cfg)
    n=round(cfg.window_s*fs); a=round(cfg.edge_s*fs)+1; b=numel(t)-round(cfg.edge_s*fs)-n+1;
    if b<a,error('Recording too short.');end
    s=unique(round(linspace(a,b,cfg.windows_per_session))); W=table((1:numel(s)).',s(:),s(:)+n-1,'VariableNames',{'window_index','start_idx','stop_idx'});
end

function [fp,fa]=local_raw_peaks(x,fs,cfg)
    [p,f]=pwelch(double(x(:)),[],[],max(256,2^nextpow2(numel(x))),fs);
    fp=local_peak(f,p,cfg.fP_range); fa=local_peak(f,p,cfg.fA_range);
end

function value=local_peak(f,p,range)
    keep=f>=range(1)&f<=range(2); ff=f(keep); pp=p(keep); [~,i]=max(pp); value=ff(i);
end

function row=local_empty_row()
    row=struct('animal',"",'session',"",'window_index',NaN,'apc_valid',false,'apc_fp_hz',NaN,'apc_fa_hz',NaN,'raw_fp_hz',NaN,'raw_fa_hz',NaN,'apc_test_event_plv',NaN,'raw_test_event_plv',NaN,'apc_test_event_count',NaN,'raw_test_event_count',NaN,'plv_difference',NaN);
end

function row=local_row(animal,session,iWindow,apc,rawFP,rawFA,test,fs,cfg)
    row=local_empty_row(); row.animal=string(animal); row.session=string(session); row.window_index=iWindow; row.raw_fp_hz=rawFP; row.raw_fa_hz=rawFA;
    row.apc_valid=apc.status_code.Value(1)==0;
    if row.apc_valid, row.apc_fp_hz=apc.phase_frequency_hz.Value(1); row.apc_fa_hz=apc.amplitude_frequency_hz.Value(1); end
    [row.apc_test_event_plv,row.apc_test_event_count]=local_event_plv(test,fs,row.apc_fp_hz,row.apc_fa_hz);
    [row.raw_test_event_plv,row.raw_test_event_count]=local_event_plv(test,fs,rawFP,rawFA);
    row.plv_difference=row.apc_test_event_plv-row.raw_test_event_plv;
end

function [plv,n]=local_event_plv(x,fs,fp,fa)
    if ~isfinite(fp)||~isfinite(fa)||fp<=0||fa<=0,plv=NaN;n=0;return;end
    low=local_bandpass(x,fs,max(.5,fp-max(.5,.25*fp)),fp+max(.5,.25*fp));
    high=local_bandpass(x,fs,fa-6,fa+6); phase=angle(hilbert(low)); env=abs(hilbert(high));
    [~,loc]=findpeaks(env,'MinPeakProminence',.25*std(env),'MinPeakDistance',max(1,round(.020*fs)));
    loc=loc(env(loc)>=median(env)+.75*std(env)); n=numel(loc);
    if n==0,plv=NaN;else,plv=abs(mean(exp(1i*phase(loc))));end
end

function y=local_bandpass(x,fs,lo,hi)
    lo=max(lo,.1); hi=min(hi,fs/2-1); [b,a]=butter(4,[lo hi]/(fs/2),'bandpass'); y=filtfilt(b,a,double(x(:)));
end

function S=local_summary(T)
    S=groupsummary(T,{'animal','session'},{'mean','median'},{'plv_difference','apc_test_event_plv','raw_test_event_plv'});
end

function local_plot(T,file)
    figure('Color','w','Position',[100 100 720 380]); hold on; x=[ones(height(T),1);2*ones(height(T),1)]; y=[T.raw_test_event_plv;T.apc_test_event_plv];
    scatter(x+.08*randn(size(x)),y,16,[.25 .25 .25],'filled','MarkerFaceAlpha',.35); plot([1 2],[T.raw_test_event_plv T.apc_test_event_plv]','-','Color',[.75 .75 .75]);
    plot([.8 1.2],[median(T.raw_test_event_plv,'omitnan') median(T.raw_test_event_plv,'omitnan')],'LineWidth',3,'Color',[.1 .4 .8]);
    plot([1.8 2.2],[median(T.apc_test_event_plv,'omitnan') median(T.apc_test_event_plv,'omitnan')],'LineWidth',3,'Color',[.85 .35 0]);
    xlim([.5 2.5]); xticks([1 2]); xticklabels({'Raw-spectrum pair','APC-selected pair'}); ylabel('Held-out event-phase concentration'); title('Held-out burst-locking comparison'); grid off; box off; exportgraphics(gcf,file,'Resolution',300);close(gcf);
end

function local_write(results,file)
    T=results.epoch_table; fid=fopen(file,'w'); fprintf(fid,'Held-out burst validation\nWindows: %d\n',height(T));
    fprintf(fid,'Median APC-minus-raw held-out event PLV: %.6f\n',median(T.plv_difference,'omitnan'));
    fprintf(fid,'Positive differences: %d/%d\n',sum(T.plv_difference>0),sum(isfinite(T.plv_difference))); fprintf(fid,'Selection and evaluation use separate half-windows; this is not calibrated coupling detection.\n'); fclose(fid);
end
