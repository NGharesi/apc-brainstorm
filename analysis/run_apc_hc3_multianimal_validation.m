function results = run_apc_hc3_multianimal_validation(profile)
% RUN_APC_HC3_MULTIANIMAL_VALIDATION
% Held-out, multi-animal carrier validation for APC using locally available
% CRCNS hc-3 Brainstorm exports. The raw-theta peak is a deliberately simple
% baseline: APC must add information beyond a theta-dominated LFP spectrum.
%
% Usage:
%   run_apc_hc3_multianimal_validation('screening')  % 4 windows/session
%   run_apc_hc3_multianimal_validation('reviewer')   % 12 windows/session
%
% This is a descriptive carrier-replication analysis. It does not infer
% coupling, behavior, or population effects from individual windows.

    if nargin < 1 || isempty(profile), profile = 'screening'; end
    cfg = local_config(profile);
    rng(cfg.random_seed, 'twister');
    rows = repmat(local_empty_row(), 0, 1);

    fprintf('HC-3 multi-animal APC carrier validation (%s)\n', cfg.profile);
    for iAnimal = 1:numel(cfg.animals)
        animal = cfg.animals{iAnimal};
        animalDir = fullfile(cfg.data_root, animal);
        sessions = local_sessions(animalDir);
        fprintf('  %s: %d candidate sessions\n', animal, numel(sessions));
        for iSession = 1:numel(sessions)
            dataFile = local_data_file(sessions(iSession).folder, sessions(iSession).name);
            if isempty(dataFile)
                fprintf('    %s: skipped (no supported raw export)\n', sessions(iSession).name);
                continue;
            end
            try
                [signal, time, fs] = local_load_signal(dataFile, cfg.channel_index);
                windows = local_windows(time, fs, cfg);
                fprintf('    %s: %d windows\n', sessions(iSession).name, height(windows));
                for iWindow = 1:height(windows)
                    idx = windows.start_idx(iWindow):windows.stop_idx(iWindow);
                    windowSignal = signal(idx); windowTime = time(idx);
                    apc = bst_apc(struct('data', windowSignal, 'time', windowTime), cfg.apc_options);
                    rows(end + 1, 1) = local_row(animal, sessions(iSession).name, dataFile, fs, ...
                        windows(iWindow, :), windowSignal, apc, cfg); %#ok<AGROW>
                end
            catch ME
                warning('Skipping %s: %s', sessions(iSession).name, ME.message);
            end
        end
    end

    epochTable = struct2table(rows);
    if isempty(epochTable), error('No valid session exports were found.'); end
    sessionTable = local_session_summary(epochTable);
    animalTable = local_animal_summary(sessionTable);

    outDir = fileparts(mfilename('fullpath')); tag = lower(cfg.profile);
    files.mat = fullfile(outDir, sprintf('apc_hc3_multianimal_validation_%s.mat', tag));
    files.epochs = fullfile(outDir, sprintf('apc_hc3_multianimal_validation_%s_epochs.csv', tag));
    files.sessions = fullfile(outDir, sprintf('apc_hc3_multianimal_validation_%s_sessions.csv', tag));
    files.animals = fullfile(outDir, sprintf('apc_hc3_multianimal_validation_%s_animals.csv', tag));
    files.figure = fullfile(outDir, sprintf('apc_hc3_multianimal_validation_%s.png', tag));
    files.summary = fullfile(outDir, sprintf('apc_hc3_multianimal_validation_%s_summary.txt', tag));
    writetable(epochTable, files.epochs); writetable(sessionTable, files.sessions); writetable(animalTable, files.animals);
    results = struct('config',cfg,'epoch_table',epochTable,'session_table',sessionTable, ...
        'animal_table',animalTable,'files',files);
    save(files.mat, 'results', '-v7.3');
    local_plot(animalTable, files.figure);
    local_write_summary(results, files.summary);
    fprintf('\nSaved outputs:\n  %s\n  %s\n  %s\n', files.epochs, files.sessions, files.figure);
end

function cfg = local_config(profile)
    cfg.profile = lower(char(profile));
    cfg.data_root = 'D:\APC_project\RealDatasets\LFP_data\HC3\data';
    cfg.animals = {'EC012','EC013','EC016'};
    cfg.channel_index = 1; cfg.window_s = 30; cfg.edge_trim_s = 10;
    cfg.theta_hz = [6 10]; cfg.raw_baseline_hz = [1 30]; cfg.fA_hz = [80 150]; cfg.random_seed = 20261007;
    switch cfg.profile
        case 'screening', cfg.windows_per_session = 4;
        case 'reviewer', cfg.windows_per_session = 12;
        case 'frozen_reviewer', cfg.windows_per_session = 12;   % amendment 2026-10-20: frozen v1.1.0 bst_apc
        otherwise, error('Use ''screening'', ''reviewer'' or ''frozen_reviewer''.');
    end
    cfg.apc_options = struct('fA',cfg.fA_hz,'epoch',[-.6 .6], ...
        'decomposition','fft_peak','metric','canolty','diagm',false, ...
        'surrogates',false,'num_perm',0,'numPhaseBins',18);
end

function sessions = local_sessions(animalDir)
    a = dir(fullfile(animalDir, 'ec*.eeg'));
    b = dir(fullfile(animalDir, '@rawec*.eeg'));
    % Regular Brainstorm imports and @raw folders can represent the same
    % recording. Prefer the regular import when it exists to avoid duplicates.
    if ~isempty(a), sessions = a; else, sessions = b; end
end

function dataFile = local_data_file(sessionDir, sessionName)
    candidates = {fullfile(sessionDir, sessionName, 'data_block001.mat')};
    raw = dir(fullfile(sessionDir, sessionName, 'data_0raw_*.mat'));
    if ~isempty(raw), candidates{end+1} = fullfile(raw(1).folder, raw(1).name); end %#ok<AGROW>
    dataFile = '';
    for i = 1:numel(candidates)
        if exist(candidates{i}, 'file'), dataFile = candidates{i}; return; end
    end
end

function [signal,time,fs] = local_load_signal(dataFile, channelIndex)
    S = load(dataFile);
    if ~isfield(S,'F') || ~isfield(S,'Time'), error('Missing F/Time in %s.', dataFile); end
    F = double(S.F); time = double(S.Time(:).');
    if size(F,2) ~= numel(time) && size(F,1) == numel(time), F = F.'; end
    if size(F,2) ~= numel(time) || channelIndex > size(F,1), error('Invalid F/Time dimensions.'); end
    signal = F(channelIndex,:); fs = 1/median(diff(time));
    if ~isfinite(fs) || fs <= 0, error('Invalid sampling frequency.'); end
end

function windows = local_windows(time, fs, cfg)
    n = round(cfg.window_s * fs); first = round(cfg.edge_trim_s * fs) + 1;
    last = numel(time) - round(cfg.edge_trim_s * fs) - n + 1;
    if last < first, error('Recording too short.'); end
    starts = unique(round(linspace(first,last,cfg.windows_per_session))); stops = starts+n-1;
    windows = table((1:numel(starts)).', starts(:), stops(:), time(starts(:)).', time(stops(:)).', ...
        'VariableNames',{'window_index','start_idx','stop_idx','start_time_s','stop_time_s'});
end

function row = local_empty_row()
    row = struct('animal',"",'session',"",'data_file',"",'fs_hz',NaN,'window_index',NaN, ...
        'start_time_s',NaN,'stop_time_s',NaN,'apc_valid',false,'apc_fp_hz',NaN, ...
        'apc_fa_hz',NaN,'apc_strength',NaN,'raw_theta_peak_hz',NaN, ...
        'apc_theta_range',false,'raw_theta_range',false,'apc_raw_theta_abs_difference_hz',NaN);
end

function row = local_row(animal,session,dataFile,fs,window,signal,apc,cfg)
    row = local_empty_row(); row.animal=string(animal); row.session=string(session); row.data_file=string(dataFile);
    row.fs_hz=fs; row.window_index=window.window_index; row.start_time_s=window.start_time_s; row.stop_time_s=window.stop_time_s;
    row.apc_valid = apc.status_code.Value(1) == 0;
    if row.apc_valid
        row.apc_fp_hz = apc.phase_frequency_hz.Value(1); row.apc_fa_hz = apc.amplitude_frequency_hz.Value(1);
        row.apc_strength = apc.pac_strength.Value(1); row.apc_theta_range = row.apc_fp_hz >= cfg.theta_hz(1) && row.apc_fp_hz <= cfg.theta_hz(2);
    end
    [pxx,f] = pwelch(double(signal(:)), [], [], max(256,2^nextpow2(numel(signal))), fs);
    % Deliberately select the dominant low-frequency peak across 1-30 Hz,
    % rather than within theta, so theta classification is not guaranteed.
    keep = f >= cfg.raw_baseline_hz(1) & f <= cfg.raw_baseline_hz(2); [~,idx] = max(pxx(keep)); candidates=f(keep);
    row.raw_theta_peak_hz = candidates(idx);
    row.raw_theta_range = row.raw_theta_peak_hz >= cfg.theta_hz(1) && row.raw_theta_peak_hz <= cfg.theta_hz(2);
    row.apc_raw_theta_abs_difference_hz = abs(row.apc_fp_hz-row.raw_theta_peak_hz);
end

function T = local_session_summary(E)
    G = groupsummary(E, {'animal','session'}, {'mean','median'}, {'apc_valid','apc_theta_range','apc_fp_hz','apc_fa_hz','raw_theta_peak_hz','apc_raw_theta_abs_difference_hz'});
    T = G;
end

function T = local_animal_summary(S)
    G = groupsummary(S, 'animal', {'mean','median'}, S.Properties.VariableNames(contains(S.Properties.VariableNames, {'mean_','median_'})));
    T = G;
end

function local_plot(T, outFile)
    figure('Color','w','Position',[100 100 900 380]); tiledlayout(1,2,'Padding','compact','TileSpacing','compact');
    nexttile; hold on; x=categorical(T.animal); bar(x,T.median_median_apc_fp_hz); yline(6,'--'); yline(10,'--'); ylabel('Session-median APC fP (Hz)'); title('A  APC phase-carrier replication'); grid off; box off;
    nexttile; hold on; bar(x,T.median_median_apc_raw_theta_abs_difference_hz); ylabel('|APC fP - raw theta peak| (Hz)'); title('B  Raw-spectrum baseline difference'); grid off; box off;
    exportgraphics(gcf,outFile,'Resolution',300); close(gcf);
end

function local_write_summary(results, outFile)
    E=results.epoch_table; S=results.session_table; fid=fopen(outFile,'w');
    fprintf(fid,'HC-3 multi-animal APC carrier validation\n');
    fprintf(fid,'Animals: %s\nSessions: %d\nWindows: %d\n',strjoin(results.config.animals,', '),height(S),height(E));
    fprintf(fid,'Valid APC windows: %d/%d\n',sum(E.apc_valid),height(E));
    fprintf(fid,'Theta-range APC fP: %d/%d valid windows\n',sum(E.apc_theta_range),sum(E.apc_valid));
    fprintf(fid,'This is a carrier-replication and raw-spectrum-baseline analysis, not calibrated coupling detection.\n'); fclose(fid);
end
