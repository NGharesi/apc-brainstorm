function results = run_apc_ec013_session_replication(profile)
% RUN_APC_EC013_SESSION_REPLICATION
% Replicate APC carrier estimates across all locally available EC013 LFP
% sessions.  This is a within-rat session-replication analysis, not a
% multi-animal or run/rest analysis.
%
% Run from MATLAB with bst_apc.m on the path:
%   results = run_apc_ec013_session_replication;
%   results = run_apc_ec013_session_replication('reviewer');
%
% The script uses independent contiguous windows and summarizes first
% within session, preventing long recordings from acting as extra animals.

    if nargin < 1 || isempty(profile)
        profile = 'screening';
    end

    cfg = local_config(profile);
    sessionDirs = dir(fullfile(cfg.data_root, 'ec013.*.eeg'));
    rows = repmat(local_empty_row(), 0, 1);

    fprintf('EC013 session-replication analysis (%s profile)\n', cfg.profile);
    fprintf('Data root: %s\n', cfg.data_root);

    for iSession = 1:numel(sessionDirs)
        sessionName = sessionDirs(iSession).name;
        dataFile = fullfile(sessionDirs(iSession).folder, sessionName, 'data_block001.mat');
        if ~exist(dataFile, 'file')
            fprintf('  [%d/%d] %s: skipped (no data_block001.mat)\n', ...
                iSession, numel(sessionDirs), sessionName);
            continue;
        end

        fprintf('  [%d/%d] %s\n', iSession, numel(sessionDirs), sessionName);
        [signal, time, fs] = local_load_signal(dataFile, cfg.channel_index);
        windows = local_make_windows(time, cfg);

        for iWindow = 1:height(windows)
            idx = windows.start_idx(iWindow):windows.stop_idx(iWindow);
            out = bst_apc(struct('data', signal(idx), 'time', time(idx)), cfg.apc_options);
            rows(end + 1, 1) = local_pack_row(sessionName, dataFile, fs, windows(iWindow, :), out); %#ok<AGROW>
        end
    end

    epochTable = struct2table(rows);
    if isempty(epochTable)
        error('No EC013 session windows were analyzed. Check cfg.data_root and raw data files.');
    end
    sessionTable = local_session_summary(epochTable);

    outDir = fileparts(mfilename('fullpath'));
    suffix = lower(cfg.profile);
    outMat = fullfile(outDir, sprintf('apc_ec013_session_replication_%s.mat', suffix));
    outEpochCsv = fullfile(outDir, sprintf('apc_ec013_session_replication_%s_epochs.csv', suffix));
    outSessionCsv = fullfile(outDir, sprintf('apc_ec013_session_replication_%s_sessions.csv', suffix));
    outFigure = fullfile(outDir, sprintf('apc_ec013_session_replication_%s.png', suffix));
    outText = fullfile(outDir, sprintf('apc_ec013_session_replication_%s_summary.txt', suffix));

    results = struct();
    results.config = cfg;
    results.epoch_table = epochTable;
    results.session_table = sessionTable;
    results.output_mat = outMat;
    results.output_epoch_csv = outEpochCsv;
    results.output_session_csv = outSessionCsv;
    results.output_figure = outFigure;
    results.output_summary = outText;

    save(outMat, 'results', '-v7.3');
    writetable(epochTable, outEpochCsv);
    writetable(sessionTable, outSessionCsv);
    local_plot_session_summary(sessionTable, outFigure);
    local_write_summary(sessionTable, cfg, outText);

    fprintf('\nSaved session-replication outputs:\n  %s\n  %s\n  %s\n  %s\n', ...
        outMat, outEpochCsv, outSessionCsv, outFigure);
end


function cfg = local_config(profile)
    cfg = struct();
    cfg.profile = lower(char(profile));
    cfg.data_root = 'D:\APC_project\RealDatasets\LFP_data\HC3\data\EC013';
    cfg.channel_index = 1;
    cfg.window_s = 30;
    cfg.edge_trim_s = 10;
    cfg.fA_hz = [80 150];
    cfg.theta_hz = [6 10];

    switch cfg.profile
        case 'screening'
            cfg.windows_per_session = 6;
        case 'reviewer'
            cfg.windows_per_session = 12;
        otherwise
            error('Unknown profile ''%s''. Use ''screening'' or ''reviewer''.', cfg.profile);
    end

    cfg.apc_options = struct( ...
        'fA', cfg.fA_hz, ...
        'epoch', [-0.6 0.6], ...
        'decomposition', 'fft_peak', ...
        'metric', 'canolty', ...
        'diagm', false, ...
        'surrogates', false, ...
        'num_perm', 0, ...
        'numPhaseBins', 18);
end


function [signal, time, fs] = local_load_signal(dataFile, channelIndex)
    S = load(dataFile);
    if ~isfield(S, 'F') || ~isfield(S, 'Time')
        error('%s must contain Brainstorm F and Time variables.', dataFile);
    end
    F = double(S.F);
    time = double(S.Time(:).');
    if size(F, 2) ~= numel(time) && size(F, 1) == numel(time)
        F = F.';
    end
    if size(F, 2) ~= numel(time)
        error('F/Time dimensions do not match in %s.', dataFile);
    end
    if channelIndex > size(F, 1)
        error('Requested channel %d, but %s has only %d channel(s).', ...
            channelIndex, dataFile, size(F, 1));
    end
    signal = F(channelIndex, :);
    fs = 1 / median(diff(time));
    if ~isfinite(fs) || fs <= 0
        error('Could not determine sampling rate from %s.', dataFile);
    end
end


function windows = local_make_windows(time, cfg)
    fs = 1 / median(diff(time));
    nWindow = round(cfg.window_s * fs);
    firstStart = round(cfg.edge_trim_s * fs) + 1;
    lastStart = numel(time) - round(cfg.edge_trim_s * fs) - nWindow + 1;
    if lastStart < firstStart
        error('Recording is too short for %g-s windows after edge trimming.', cfg.window_s);
    end
    starts = unique(round(linspace(firstStart, lastStart, cfg.windows_per_session)));
    stops = starts + nWindow - 1;
    windows = table((1:numel(starts)).', starts(:), stops(:), time(starts(:)).', time(stops(:)).', ...
        'VariableNames', {'window_index', 'start_idx', 'stop_idx', 'start_time_s', 'stop_time_s'});
end


function row = local_empty_row()
    row = struct( ...
        'session', "", 'data_file', "", 'fs_hz', NaN, 'window_index', NaN, ...
        'start_time_s', NaN, 'stop_time_s', NaN, 'duration_s', NaN, ...
        'status_code', NaN, 'is_valid', false, 'phase_frequency_hz', NaN, ...
        'amplitude_frequency_hz', NaN, 'pac_strength', NaN, ...
        'preferred_phase_deg', NaN, 'n_bursts', NaN, 'n_troughs', NaN);
end


function row = local_pack_row(sessionName, dataFile, fs, window, out)
    row = local_empty_row();
    row.session = string(sessionName);
    row.data_file = string(dataFile);
    row.fs_hz = fs;
    row.window_index = window.window_index;
    row.start_time_s = window.start_time_s;
    row.stop_time_s = window.stop_time_s;
    row.duration_s = window.stop_time_s - window.start_time_s;

    row.status_code = local_feature(out, 'status_code');
    row.is_valid = row.status_code == 0;
    row.phase_frequency_hz = local_feature(out, 'phase_frequency_hz');
    row.amplitude_frequency_hz = local_feature(out, 'amplitude_frequency_hz');
    row.pac_strength = local_feature(out, 'pac_strength');
    row.preferred_phase_deg = local_feature(out, 'preferred_phase_deg');
    row.n_bursts = local_feature(out, 'n_bursts');
    row.n_troughs = local_feature(out, 'n_phase_events');
end


function value = local_feature(S, name)
    if isfield(S, name) && isfield(S.(name), 'Value')
        value = double(S.(name).Value(1));
    else
        value = NaN;
    end
end


function T = local_session_summary(epochTable)
    sessions = unique(epochTable.session, 'stable');
    rows = cell(numel(sessions), 10);
    for i = 1:numel(sessions)
        sub = epochTable(epochTable.session == sessions(i), :);
        valid = sub(sub.is_valid, :);
        nValid = height(valid);
        if nValid > 0
            thetaProp = mean(valid.phase_frequency_hz >= 6 & valid.phase_frequency_hz <= 10);
            fpMedian = median(valid.phase_frequency_hz, 'omitnan');
            faMedian = median(valid.amplitude_frequency_hz, 'omitnan');
            strengthMedian = median(valid.pac_strength, 'omitnan');
        else
            thetaProp = NaN; fpMedian = NaN; faMedian = NaN; strengthMedian = NaN;
        end
        rows(i, :) = {sessions(i), height(sub), nValid, nValid / height(sub), thetaProp, ...
            fpMedian, faMedian, strengthMedian, min(sub.fs_hz), string(sub.data_file(1))};
    end
    T = cell2table(rows, 'VariableNames', {'session', 'n_windows', 'n_valid', ...
        'valid_proportion', 'theta_proportion_valid', 'fp_median_hz', 'fa_median_hz', ...
        'pac_strength_median', 'fs_hz', 'data_file'});
end


function local_plot_session_summary(T, outFigure)
    figure('Color', 'w', 'Position', [100 100 1200 430]);
    tiledlayout(1, 3, 'TileSpacing', 'compact', 'Padding', 'compact');
    x = 1:height(T);

    nexttile;
    plot(x, T.fp_median_hz, 'o-', 'LineWidth', 1.5, 'MarkerFaceColor', [0.85 0.33 0.10]);
    yline(6, '--', 'Color', [0.25 0.25 0.25]); yline(10, '--', 'Color', [0.25 0.25 0.25]);
    xlim([0.5 height(T) + 0.5]); ylabel('Session median f_P (Hz)'); xlabel('EC013 session');
    title('A  Phase-carrier replication'); grid off;

    nexttile;
    plot(x, T.fa_median_hz, 'o-', 'LineWidth', 1.5, 'MarkerFaceColor', [0.20 0.47 0.72]);
    xlim([0.5 height(T) + 0.5]); ylabel('Session median f_A (Hz)'); xlabel('EC013 session');
    title('B  Amplitude-carrier replication'); grid off;

    nexttile;
    bar(x, T.theta_proportion_valid, 'FaceColor', [0.18 0.60 0.40]);
    ylim([0 1]); xlim([0.5 height(T) + 0.5]); ylabel('Valid windows with 6-10 Hz f_P');
    xlabel('EC013 session'); title('C  Prespecified theta criterion'); grid off;
    exportgraphics(gcf, outFigure, 'Resolution', 250);
    close(gcf);
end


function local_write_summary(T, cfg, outFile)
    fid = fopen(outFile, 'w');
    if fid < 0, error('Could not write %s.', outFile); end
    cleaner = onCleanup(@() fclose(fid)); %#ok<NASGU>
    fprintf(fid, 'EC013 within-rat session-replication analysis\n');
    fprintf(fid, 'Profile: %s | windows/session: %d | window duration: %.1f s\n', ...
        cfg.profile, cfg.windows_per_session, cfg.window_s);
    fprintf(fid, 'This is a descriptive same-rat, multi-session analysis; sessions are not independent animals.\n\n');
    fprintf(fid, 'session,n_windows,n_valid,valid_proportion,theta_proportion,fp_median_hz,fa_median_hz,pac_strength_median\n');
    for i = 1:height(T)
        fprintf(fid, '%s,%d,%d,%.4f,%.4f,%.6f,%.6f,%.8g\n', T.session(i), ...
            T.n_windows(i), T.n_valid(i), T.valid_proportion(i), T.theta_proportion_valid(i), ...
            T.fp_median_hz(i), T.fa_median_hz(i), T.pac_strength_median(i));
    end
end
