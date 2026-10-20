function results = run_apc_comparator_fairness_benchmark(profileName)
% RUN_APC_COMPARATOR_FAIRNESS_BENCHMARK Matched-grid comparator control.
%
% All scanned methods use the same 1-30 Hz phase range and 80-152 Hz
% amplitude range. The comparator set includes raw Canolty MVL, Ozkurt's
% amplitude-normalized MVL, KLMI, GLM, and an event-triggered phase-locking
% scan. Fixed-pair controls at the known 8-Hz/120-Hz simulated pair verify
% that every comparator detects the injected coupling without selection.
%
% Usage:
%   run_apc_comparator_fairness_benchmark('fast')      % 5 repeats/level
%   run_apc_comparator_fairness_benchmark('reviewer')  % 15 repeats/level
%   run_apc_comparator_fairness_benchmark('full')      % 25 repeats/level
%   run_apc_comparator_fairness_benchmark('narrow_reproduction')
%       % 25 repeats/level, original 4-12 Hz and 80:8:152 Hz centers
%       % evaluated through this same six-method implementation.
%   run_apc_comparator_fairness_benchmark('phase_qc_development')
%       % Same seeds as the reviewer profile for repair development only.
%   run_apc_comparator_fairness_benchmark('phase_qc_holdout')
%       % New seeds and 100 repeats/level for frozen validation.
%   run_apc_comparator_fairness_benchmark('phase_qc_detrend_development')
%       % Development-only test of detrended burst-average phase selection.
%   run_apc_comparator_fairness_benchmark('phase_qc_3cycle_development')
%       % Development-only test of the three-cycle spectral-support rule.
%   run_apc_comparator_fairness_benchmark('stable_filter_smoke')
%       % One-repeat implementation check after the comparator filter fix.
%   run_apc_comparator_fairness_benchmark('stable_filter_holdout')
%       % Independent matched-filter validation on new random seeds.

    if nargin < 1 || isempty(profileName), profileName = 'reviewer'; end
    cfg = local_config(profileName); rng(cfg.randomSeed, 'twister');
    rows = {}; fixedRows = {};
    for iScale = 1:numel(cfg.distractorScales)
        for iRepeat = 1:cfg.nRepeats
            fprintf('[%s] distractor %.1f, repeat %d/%d\n', cfg.profileName, ...
                cfg.distractorScales(iScale), iRepeat, cfg.nRepeats);
            [coupled, null] = local_signals(cfg, cfg.distractorScales(iScale));
            scan = local_scan_all(coupled, cfg);
            for iMethod = 1:numel(scan.methods)
                rows{end+1} = local_row(scan.methods(iMethod), cfg.distractorScales(iScale), iRepeat, scan, iMethod, cfg); %#ok<AGROW>
            end
            for iMethod = 1:numel(scan.methods(2:end))
                method = scan.methods(iMethod+1);
                coupledScore = local_fixed_pair(coupled, cfg, method);
                nullScore = local_fixed_pair(null, cfg, method);
                fixedRows{end+1} = local_fixed_row(method, "coupled", cfg.distractorScales(iScale), iRepeat, coupledScore); %#ok<AGROW>
                fixedRows{end+1} = local_fixed_row(method, "null", cfg.distractorScales(iScale), iRepeat, nullScore); %#ok<AGROW>
            end
        end
    end
    runTable = struct2table([rows{:}]); fixedTable = struct2table([fixedRows{:}]);
    summaryTable = local_summary(runTable, cfg); fixedSummary = local_fixed_summary(fixedTable);
    baseDir = fileparts(mfilename('fullpath')); tag = lower(cfg.profileName);
    files.mat = fullfile(baseDir, sprintf('apc_comparator_fairness_%s.mat', tag));
    files.runs = fullfile(baseDir, sprintf('apc_comparator_fairness_runs_%s.csv', tag));
    files.summary = fullfile(baseDir, sprintf('apc_comparator_fairness_summary_%s.csv', tag));
    files.fixed = fullfile(baseDir, sprintf('apc_comparator_fairness_fixed_%s.csv', tag));
    files.fixedSummary = fullfile(baseDir, sprintf('apc_comparator_fairness_fixed_summary_%s.csv', tag));
    files.png = fullfile(baseDir, sprintf('apc_comparator_fairness_%s.png', tag));
    files.pdf = fullfile(baseDir, sprintf('apc_comparator_fairness_%s.pdf', tag));
    files.fig = fullfile(baseDir, sprintf('apc_comparator_fairness_%s.fig', tag));
    writetable(runTable, files.runs); writetable(summaryTable, files.summary);
    writetable(fixedTable, files.fixed); writetable(fixedSummary, files.fixedSummary);
    save(files.mat, 'cfg', 'runTable', 'fixedTable', 'summaryTable', 'fixedSummary', '-v7.3');
    fig = local_plot(summaryTable, fixedSummary, cfg);
    exportgraphics(fig, files.png, 'Resolution', 300); exportgraphics(fig, files.pdf, 'ContentType', 'vector'); savefig(fig, files.fig); close(fig);
    fprintf('\nSaved comparator-fairness outputs:\n  %s\n  %s\n  %s\n', files.mat, files.summary, files.png);
    results = struct('config',cfg,'run_table',runTable,'fixed_table',fixedTable, ...
        'summary_table',summaryTable,'fixed_summary',fixedSummary,'files',files);
end

function cfg = local_config(profileName)
    cfg.profileName = char(lower(string(profileName))); cfg.randomSeed = 20261006;
    cfg.fs = 500; cfg.durationSec = 6; cfg.fP = 8; cfg.fA = 120; cfg.distractorFA = 96;
    cfg.phaseGrid = 1:1:30; cfg.amplitudeGrid = 88:4:148; cfg.commonFA = [80 152];
    cfg.phaseHalfWidth = 1.5; cfg.amplitudeHalfWidth = 6; cfg.distractorScales = 0:.5:3;
    cfg.fpTolerance = 1; cfg.faTolerance = 8; cfg.snrDb = -3; cfg.minPhaseCycles = 3;
    switch lower(string(profileName))
        case "fast", cfg.nRepeats = 5;
        case "reviewer", cfg.nRepeats = 15;
        case "full", cfg.nRepeats = 25;
        case "narrow_reproduction"
            % This is not a fairness control. It isolates whether the Figure 3
            % shift is caused by grid/repeat choices or by implementation.
            cfg.nRepeats = 25;
            cfg.phaseGrid = 4:1:12;
            cfg.amplitudeGrid = 80:8:152;
        case "phase_qc_development"
            cfg.nRepeats = 15;
        case "phase_qc_holdout"
            cfg.nRepeats = 100;
            cfg.randomSeed = 20261014;
        case "phase_qc_detrend_development"
            cfg.nRepeats = 15;
        case "phase_qc_3cycle_development"
            cfg.nRepeats = 15;
        case "stable_filter_smoke"
            cfg.nRepeats = 1;
            cfg.randomSeed = 20261020;
            cfg.distractorScales = 1.5;
        case "stable_filter_holdout"
            cfg.nRepeats = 100;
            cfg.randomSeed = 20261020;
        otherwise
            error(['Use ''fast'', ''reviewer'', ''full'', ''narrow_reproduction'', ', ...
                '''phase_qc_development'', ''phase_qc_detrend_development'', ', ...
                '''phase_qc_3cycle_development'', ''stable_filter_smoke'', ', ...
                'or ''stable_filter_holdout''.']);
    end
end

function [coupled, null] = local_signals(cfg, scale)
    t = 0:1/cfg.fs:(cfg.durationSec-1/cfg.fs); low = sin(2*pi*cfg.fP*t);
    cycles = (0:ceil(cfg.durationSec*cfg.fP))./cfg.fP + .75/cfg.fP;
    cycles = cycles(cycles > 0 & cycles < cfg.durationSec);
    coupledEnv = local_envelope(t, cycles + .010*randn(size(cycles)));
    nullEnv = local_envelope(t, rand(size(cycles))*cfg.durationSec);
    distractorEnv = local_envelope(t, rand(size(cycles))*cfg.durationSec);
    trueCoupled = (.08 + 1.3*.60*coupledEnv).*sin(2*pi*cfg.fA*t);
    trueNull = (.08 + 1.3*.60*nullEnv).*sin(2*pi*cfg.fA*t);
    distractor = (.08 + .6*scale*distractorEnv).*sin(2*pi*cfg.distractorFA*t + 2*pi*rand());
    coupled = local_noise(low + trueCoupled + distractor, cfg.snrDb);
    null = local_noise(low + trueNull + distractor, cfg.snrDb);
end

function env = local_envelope(t, centers)
    env = zeros(size(t));
    for i = 1:numel(centers), env = env + exp(-.5*((t-centers(i))/.028).^2); end
    env = env ./ max(max(env), eps);
end

function y = local_noise(x, snrDb)
    pink = cumsum(randn(size(x))); pink = (pink-mean(pink))/std(pink);
    white = randn(size(x)); noise = pink+.5*white; noise = noise/std(noise);
    y = x + sqrt(mean(x.^2)/(10^(snrDb/10)))*noise;
end

function scan = local_scan_all(signal, cfg)
    t = (0:numel(signal)-1)./cfg.fs;
    apc = bst_apc(struct('data',signal,'time',t), struct('fA',cfg.commonFA,'epoch',[-.6 .6], ...
        'minPhaseCycles',cfg.minPhaseCycles, ...
        'decomposition','fft_peak','metric','canolty','diagm',false,'surrogates',false,'num_perm',0,'numPhaseBins',18));
    scan.methods = ["APC","MVL-scan","Ozkurt-MVL-scan","KLMI-scan","GLM-scan","Event-phase-scan"];
    scan.fp = nan(1,numel(scan.methods)); scan.fa = nan(1,numel(scan.methods)); scan.score = nan(1,numel(scan.methods));
    scan.valid = false(1,numel(scan.methods));
    scan.fp(1)=apc.phase_frequency_hz.Value(1); scan.fa(1)=apc.amplitude_frequency_hz.Value(1);
    scan.score(1)=apc.pac_strength.Value(1); scan.valid(1)=apc.status_code.Value(1)==0;
    phases = cell(1,numel(cfg.phaseGrid)); envelopes = cell(1,numel(cfg.amplitudeGrid)); events = cell(1,numel(cfg.amplitudeGrid));
    for i=1:numel(cfg.phaseGrid)
        low = local_bandpass(signal,cfg.fs,max(.5,cfg.phaseGrid(i)-cfg.phaseHalfWidth),cfg.phaseGrid(i)+cfg.phaseHalfWidth);
        phases{i}=angle(hilbert(low(:)));
    end
    for j=1:numel(cfg.amplitudeGrid)
        high = local_bandpass(signal,cfg.fs,cfg.amplitudeGrid(j)-cfg.amplitudeHalfWidth,cfg.amplitudeGrid(j)+cfg.amplitudeHalfWidth);
        envelopes{j}=abs(hilbert(high(:))); events{j}=local_events(envelopes{j},cfg.fs);
    end
    metrics = {'canolty','ozkurt','tort','glm','event'};
    for k=1:numel(metrics)
        scores = nan(numel(cfg.phaseGrid),numel(cfg.amplitudeGrid));
        for i=1:numel(cfg.phaseGrid), for j=1:numel(cfg.amplitudeGrid)
            scores(i,j)=local_metric(phases{i},envelopes{j},events{j},metrics{k});
        end,end
        [best,idx]=max(scores(:),[],'omitnan'); [i,j]=ind2sub(size(scores),idx);
        scan.fp(k+1)=cfg.phaseGrid(i); scan.fa(k+1)=cfg.amplitudeGrid(j); scan.score(k+1)=best; scan.valid(k+1)=isfinite(best);
    end
end

function indices = local_events(envelope, fs)
    threshold = median(envelope) + .75*std(envelope);
    [~,indices] = findpeaks(envelope,'MinPeakProminence',.25*std(envelope),'MinPeakDistance',max(1,round(.020*fs)));
    indices = indices(envelope(indices) >= threshold);
end

function value = local_metric(phase, envelope, eventIndices, metric)
    switch metric
        case 'glm'
            X=[ones(numel(phase),1),sin(phase),cos(phase)]; beta=X\envelope; fit=X*beta;
            value=max(0,1-sum((envelope-fit).^2)/max(sum((envelope-mean(envelope)).^2),eps));
        case 'event'
            if isempty(eventIndices), value=0; else, value=abs(mean(exp(1i*phase(eventIndices)))); end
        otherwise
            [value,~]=calc_MI_all_methods(phase,envelope,metric,false,0,1,false,18);
    end
end

function score = local_fixed_pair(signal,cfg,method)
    low=local_bandpass(signal,cfg.fs,cfg.fP-cfg.phaseHalfWidth,cfg.fP+cfg.phaseHalfWidth);
    high=local_bandpass(signal,cfg.fs,cfg.fA-cfg.amplitudeHalfWidth,cfg.fA+cfg.amplitudeHalfWidth);
    phase=angle(hilbert(low(:))); envelope=abs(hilbert(high(:))); events=local_events(envelope,cfg.fs);
    switch method
        case "MVL-scan", metric='canolty'; case "Ozkurt-MVL-scan", metric='ozkurt';
        case "KLMI-scan", metric='tort'; case "GLM-scan", metric='glm'; otherwise, metric='event';
    end
    score=local_metric(phase,envelope,events,metric);
end

function y=local_bandpass(x,fs,low,high)
    d=designfilt('bandpassiir','FilterOrder',4, ...
        'HalfPowerFrequency1',low,'HalfPowerFrequency2',high,'SampleRate',fs);
    y=filtfilt(d,double(x(:)));
end

function row=local_row(method,scale,repeat,scan,i,cfg)
    row=struct('method',method,'distractor_scale',scale,'repeat_index',repeat,'valid',scan.valid(i), ...
        'recovered_fP_hz',scan.fp(i),'recovered_fA_hz',scan.fa(i),'score',scan.score(i), ...
        'fP_abs_error_hz',abs(scan.fp(i)-cfg.fP),'fA_abs_error_hz',abs(scan.fa(i)-cfg.fA), ...
        'pair_correct',double(scan.valid(i) && abs(scan.fp(i)-cfg.fP)<=cfg.fpTolerance && abs(scan.fa(i)-cfg.fA)<=cfg.faTolerance));
end

function row=local_fixed_row(method,condition,scale,repeat,score)
    row=struct('method',method,'condition',condition,'distractor_scale',scale,'repeat_index',repeat,'score',score);
end

function summary=local_summary(T,cfg)
    methods=unique(T.method,'stable'); rows=cell(0,6);
    for i=1:numel(cfg.distractorScales), for j=1:numel(methods)
        sub=T(T.distractor_scale==cfg.distractorScales(i) & T.method==methods(j),:);
        rows(end+1,:)={cfg.distractorScales(i),methods(j),height(sub),mean(sub.pair_correct),mean(sub.fP_abs_error_hz,'omitnan'),mean(sub.fA_abs_error_hz,'omitnan')}; %#ok<AGROW>
    end,end
    summary=cell2table(rows,'VariableNames',{'distractor_scale','method','n','pair_recovery_rate','mean_fP_error_hz','mean_fA_error_hz'});
end

function summary=local_fixed_summary(T)
    methods=unique(T.method,'stable'); scales=unique(T.distractor_scale); rows=cell(0,4);
    for i=1:numel(scales), for j=1:numel(methods)
        s=T(T.distractor_scale==scales(i) & T.method==methods(j),:);
        pos=s.score(s.condition=="coupled"); neg=s.score(s.condition=="null");
        rows(end+1,:)={scales(i),methods(j),mean(pos),mean(neg)}; %#ok<AGROW>
    end,end
    summary=cell2table(rows,'VariableNames',{'distractor_scale','method','mean_coupled_score','mean_null_score'});
end

function fig=local_plot(S,F,cfg)
    methods=unique(S.method,'stable'); colors=lines(numel(methods)); fig=figure('Color','w','Position',[100 100 1250 500]);
    tiledlayout(1,2,'Padding','compact','TileSpacing','compact');
    ax=nexttile; hold(ax,'on');
    for i=1:numel(methods), x=S(S.method==methods(i),:); plot(x.distractor_scale,x.pair_recovery_rate,'-o','Color',colors(i,:),'LineWidth',1.8,'DisplayName',methods(i)); end
    ylim(ax,[0 1]); xlabel(ax,'Distractor amplitude scale'); ylabel(ax,'Joint-pair recovery'); title(ax,'A  Matched-grid recovery'); legend(ax,'Location','eastoutside','Box','off'); grid(ax,'off');
    ax=nexttile; hold(ax,'on');
    for i=1:numel(methods), x=F(F.method==methods(i),:); plot(x.distractor_scale,x.mean_coupled_score-x.mean_null_score,'-o','Color',colors(i,:),'LineWidth',1.8,'DisplayName',methods(i)); end
    xlabel(ax,'Distractor amplitude scale'); ylabel(ax,'Fixed-pair coupled minus null score'); title(ax,'B  Fixed-pair positive controls'); grid(ax,'off');
    sgtitle(sprintf('Comparator Fairness Benchmark (%s; %d repeats/level)',cfg.profileName,cfg.nRepeats),'FontWeight','bold');
end
