function results = run_apc_sleepedf_subject(psgFile, hypnogramFile, channelName, stageNames, faBandList)
% RUN_APC_SLEEPEDF_SUBJECT
% Starter APC pipeline for one Sleep-EDF Expanded subject.
%
% PURPOSE:
%   Load one PSG EDF and its matching hypnogram EDF, extract a scalp EEG
%   channel, isolate N2/N3 sleep, and run APC separately on those stages.
%   The script can test multiple spindle-focused amplitude bands and choose
%   the most plausible non-boundary APC solution automatically.
%
% USAGE:
%   results = run_apc_sleepedf_subject(psgFile, hypnogramFile)
%   results = run_apc_sleepedf_subject(psgFile, hypnogramFile, 'Fpz-Cz')
%   results = run_apc_sleepedf_subject(psgFile, hypnogramFile, {'Fpz-Cz','Pz-Oz'})
%   results = run_apc_sleepedf_subject(psgFile, hypnogramFile, {'Fpz-Cz','Pz-Oz'}, {'Sleep stage 2','Sleep stage 3','Sleep stage 4'}, [11 16; 12 16; 10 16])
%
% INPUTS:
%   psgFile       - Sleep-EDF PSG EDF file
%   hypnogramFile - matching hypnogram EDF file
%   channelName   - preferred EEG channel or cell array of channels.
%                   Default: {'Fpz-Cz','Pz-Oz'}
%   stageNames    - stage labels to pool. Default pools N2/N3:
%                   {'Sleep stage 2','Sleep stage 3','Sleep stage 4'}
%   faBandList    - amplitude search bands to test. Each row is [low high],
%                   or a struct with channel-specific fields.
%                   Default channel-specific candidates:
%                     Fpz-Cz: [9 12; 9 13; 10 13]
%                     Pz-Oz : [12 16; 11 16; 12 15]
%
% NOTES:
%   Sleep-EDF commonly uses EDF+ annotations such as:
%     'Sleep stage 1'
%     'Sleep stage 2'
%     'Sleep stage 3'
%     'Sleep stage 4'
%     'Sleep stage R'
%     'Sleep stage W'
%
%   This script is intentionally conservative. It tries to parse the EDF+
%   hypnogram automatically using edfread/edfinfo. If the hypnogram format
%   differs on your machine, use the inspection output to adjust the helper
%   functions rather than changing the APC logic.

    if nargin < 1 || isempty(psgFile)
        error('Please provide the Sleep-EDF PSG EDF file path.');
    end
    if nargin < 2 || isempty(hypnogramFile)
        error('Please provide the matching Sleep-EDF hypnogram EDF file path.');
    end
    if nargin < 3 || isempty(channelName)
        channelName = {'Fpz-Cz', 'Pz-Oz'};
    end
    if nargin < 4 || isempty(stageNames)
        % Pool N2 and deep NREM together in the first pass.
        stageNames = {'Sleep stage 2', 'Sleep stage 3', 'Sleep stage 4'};
    end
    if nargin < 5
        faBandList = [];
    end

    if ~exist(psgFile, 'file')
        error('PSG EDF file not found: %s', psgFile);
    end
    if ~exist(hypnogramFile, 'file')
        error('Hypnogram EDF file not found: %s', hypnogramFile);
    end

    fprintf('Loading PSG EDF:\n  %s\n', psgFile);
    psgInfo = edfinfo(psgFile);
    psgTT = edfread(psgFile);

    fprintf('Loading hypnogram EDF:\n  %s\n', hypnogramFile);
    hypInfo = edfinfo(hypnogramFile);
    hypTT = edfread(hypnogramFile);

    stageTable = local_extract_sleep_stages(hypTT, hypInfo);

    pooledStages = string(stageNames(:));
    keepRows = ismember(string(stageTable.stage_label), pooledStages);
    pooledTable = stageTable(keepRows, :);
    if isempty(pooledTable)
        error('No matching sleep stages found for requested labels.');
    end

    n2Rows = ismember(string(stageTable.stage_label), "Sleep stage 2");
    n3Rows = ismember(string(stageTable.stage_label), ["Sleep stage 3","Sleep stage 4"]);

    n2Table = stageTable(n2Rows, :);
    n3Table = stageTable(n3Rows, :);

    if ischar(channelName) || isstring(channelName)
        channelList = cellstr(string(channelName));
    else
        channelList = cellstr(string(channelName(:)));
    end

    results = struct();
    results.psg_file = psgFile;
    results.hypnogram_file = hypnogramFile;
    results.channel_requested = channelList;
    results.fa_band_list = faBandList;
    results.psg_info = psgInfo;
    results.hypnogram_info = hypInfo;
    results.stage_table = stageTable;
    results.channels = struct();
    summaryRows = table();
    fsUsed = nan(numel(channelList), 1);

    for iChan = 1:numel(channelList)
        requestedChannel = channelList{iChan};
        [signal, timeSec, fs, matchedChannel] = local_extract_eeg_channel(psgTT, psgInfo, requestedChannel);
        fsUsed(iChan) = fs;

        chanResult = struct();
        chanResult.channel_requested = requestedChannel;
        chanResult.channel_used = matchedChannel;
        chanResult.fs_hz = fs;
        bandListThisChannel = local_resolve_fa_band_list(faBandList, requestedChannel, matchedChannel);
        chanResult.fa_band_list = bandListThisChannel;
        chanResult.n2 = local_run_stage_apc_bestband(signal, timeSec, n2Table, bandListThisChannel, fs, 'N2', matchedChannel);
        chanResult.n3 = local_run_stage_apc_bestband(signal, timeSec, n3Table, bandListThisChannel, fs, 'N3', matchedChannel);
        chanResult.nrem_pooled = local_run_stage_apc_bestband(signal, timeSec, pooledTable, bandListThisChannel, fs, 'N2N3', matchedChannel);
        chanResult.summary = vertcat(chanResult.n2.summary, chanResult.n3.summary, chanResult.nrem_pooled.summary);

        safeField = matlab.lang.makeValidName(local_safe_name(matchedChannel));
        results.channels.(safeField) = chanResult;
        summaryRows = [summaryRows; chanResult.summary]; %#ok<AGROW>
    end

    results.fs_hz = fsUsed;
    results.summary = summaryRows;

    outDir = fileparts(mfilename('fullpath'));
    subjectTag = local_subject_tag(psgFile);
    outMat = fullfile(outDir, sprintf('apc_sleepedf_%s_results.mat', subjectTag));
    outCsv = fullfile(outDir, sprintf('apc_sleepedf_%s_summary.csv', subjectTag));
    figPng = fullfile(outDir, sprintf('apc_sleepedf_%s_publication_summary.png', subjectTag));
    figFig = fullfile(outDir, sprintf('apc_sleepedf_%s_publication_summary.fig', subjectTag));
    fig = local_make_sleepedf_summary_figure(results, subjectTag);
    exportgraphics(fig, figPng, 'Resolution', 300);
    savefig(fig, figFig);
    close(fig);
    save(outMat, 'results', '-v7.3');
    writetable(results.summary, outCsv);
    results.png_file = figPng;
    results.fig_file = figFig;

    fprintf('\nSleep-EDF APC summary:\n');
    disp(results.summary);
    fprintf('\nSaved outputs:\n  %s\n  %s\n  %s\n  %s\n', outMat, outCsv, figPng, figFig);
end


function [signal, timeSec, fs, matchedChannel] = local_extract_eeg_channel(psgTT, psgInfo, channelName)
    vars = string(psgTT.Properties.VariableNames);
    target = string(channelName);
    varsNorm = strings(size(vars));
    for iVar = 1:numel(vars)
        varsNorm(iVar) = string(local_normalize_name(vars(iVar)));
    end
    targetNorm = local_normalize_name(target);

    idx = find(strcmpi(vars, target), 1);
    if isempty(idx)
        idx = find(contains(lower(vars), lower(target)), 1);
    end
    if isempty(idx)
        idx = find(strcmp(varsNorm, targetNorm), 1);
    end
    if isempty(idx)
        idx = find(contains(varsNorm, targetNorm) | contains(targetNorm, varsNorm), 1);
    end
    if isempty(idx)
        error('Could not find requested EEG channel "%s". Available channels:\n%s', ...
            channelName, strjoin(cellstr(vars), ', '));
    end

    matchedChannel = char(vars(idx));
    signal = local_table_var_to_vector(psgTT.(matchedChannel));

    if isprop(psgTT, 'Properties') && ~isempty(psgTT.Properties.RowTimes)
        rowTimes = seconds(psgTT.Properties.RowTimes - psgTT.Properties.RowTimes(1));
        timeSec = double(rowTimes(:));
        if numel(timeSec) == numel(signal)
            timeSec = timeSec(:);
            fs = 1 / median(diff(timeSec));
            return;
        end
    end

    fs = local_find_channel_fs(psgInfo, matchedChannel, numel(signal));
    timeSec = ((0:(numel(signal) - 1)) ./ fs).';
end


function x = local_table_var_to_vector(v)
    if isnumeric(v)
        x = double(v(:));
        return;
    end
    if iscell(v)
        try
            x = double(cell2mat(v(:)));
            x = x(:);
            return;
        catch
        end
    end
    error('Unsupported EDF channel storage format for EEG signal.');
end


function faBands = local_resolve_fa_band_list(faBandList, requestedChannel, matchedChannel)
    if ~isempty(faBandList)
        if isnumeric(faBandList)
            faBands = faBandList;
            return;
        end

        if isstruct(faBandList)
            keysToTry = { ...
                matlab.lang.makeValidName(char(string(matchedChannel))), ...
                matlab.lang.makeValidName(char(string(requestedChannel))), ...
                local_channel_family_key(matchedChannel), ...
                local_channel_family_key(requestedChannel)};
            for iKey = 1:numel(keysToTry)
                key = keysToTry{iKey};
                if isfield(faBandList, key)
                    faBands = faBandList.(key);
                    return;
                end
            end
        end

        error(['faBandList must be empty, a numeric [nBands x 2] matrix, ' ...
               'or a struct with channel-specific fields.']);
    end

    chanKey = local_channel_family_key(matchedChannel);
    switch chanKey
        case 'fpz_cz'
            faBands = [9 12; 9 13; 10 13];
        case 'pz_oz'
            faBands = [12 16; 11 16; 12 15];
        otherwise
            faBands = [10 16; 11 16; 12 16];
    end
end


function key = local_channel_family_key(channelName)
    s = lower(char(string(channelName)));
    s = regexprep(s, '[^a-z0-9]+', '_');

    if contains(s, 'fpz') && contains(s, 'cz')
        key = 'fpz_cz';
    elseif contains(s, 'pz') && contains(s, 'oz')
        key = 'pz_oz';
    else
        key = matlab.lang.makeValidName(s);
    end
end


function fs = local_find_channel_fs(psgInfo, matchedChannel, nSamples)
    fs = [];

    infoText = evalc('disp(psgInfo)');
    tok = regexp(infoText, 'NumDataRecords\s*:\s*(\d+)', 'tokens', 'once');
    durTok = regexp(infoText, 'DataRecordDuration\s*:\s*([0-9.]+)', 'tokens', 'once');
    if ~isempty(tok) && ~isempty(durTok)
        nRec = str2double(tok{1});
        recDur = str2double(durTok{1});
        if isfinite(nRec) && isfinite(recDur) && nRec > 0 && recDur > 0
            fs = nSamples / (nRec * recDur);
        end
    end

    if isempty(fs) || ~isfinite(fs) || fs <= 0
        error('Could not infer sampling rate for channel %s from EDF info.', matchedChannel);
    end
end


function stageTable = local_extract_sleep_stages(hypTT, hypInfo)
    startSec = [];
    durationSec = [];
    stageLabel = strings(0, 1);
    parsedOk = false;

    if isprop(hypInfo, 'Annotations') && ~isempty(hypInfo.Annotations)
        [stageLabel, startSec, durationSec, parsedOk] = local_parse_annotation_timetable(hypInfo.Annotations);
    end

    if ~parsedOk && ~isempty(hypTT)
        vars = string(hypTT.Properties.VariableNames);
        for iVar = 1:numel(vars)
            raw = hypTT.(vars(iVar));
            if iscell(raw)
                texts = strings(size(raw));
                for i = 1:numel(raw)
                    texts(i) = local_cell_to_string(raw{i});
                end
            elseif isstring(raw)
                texts = raw;
            elseif ischar(raw)
                texts = string(cellstr(raw));
            else
                continue;
            end

            for i = 1:numel(texts)
                txt = strtrim(texts(i));
                if startsWith(txt, "Sleep stage", 'IgnoreCase', true)
                    stageLabel(end+1, 1) = txt; %#ok<AGROW>
                end
            end

            if ~isempty(stageLabel)
                parsedOk = true;
                break;
            end
        end
    end

    if ~parsedOk
        [stageLabel, startSec, durationSec, parsedOk] = local_parse_edfplus_annotations(hypTT, hypInfo);
    end

    if ~parsedOk || isempty(stageLabel)
        error(['Could not parse sleep-stage labels automatically from the hypnogram EDF. ' ...
               'Please run: hypInfo = edfinfo(hypFile); hypTT = edfread(hypFile); ' ...
               'hypTT.Properties.VariableNames; hypTT(1:10,:) and send the output.']);
    end

    if isempty(startSec) && isprop(hypTT, 'Properties') && ~isempty(hypTT.Properties.RowTimes)
        rowSec = seconds(hypTT.Properties.RowTimes - hypTT.Properties.RowTimes(1));
        rowSec = double(rowSec(:));
        nAvail = min(numel(rowSec), numel(stageLabel));
        startSec = rowSec(1:nAvail);
        stageLabel = stageLabel(1:nAvail);
    elseif isempty(startSec)
        startSec = (0:(numel(stageLabel) - 1))' * 30;
    end

    if isempty(durationSec)
        durationSec = 30 * ones(numel(stageLabel), 1);
    end

    if numel(durationSec) ~= numel(stageLabel)
        durationSec = repmat(durationSec(1), numel(stageLabel), 1);
    end

    stopSec = startSec + durationSec;

    stageTable = table(startSec, stopSec, durationSec, stageLabel, ...
        'VariableNames', {'start_s', 'stop_s', 'duration_s', 'stage_label'});
end


function out = local_cell_to_string(v)
    if isstring(v)
        out = v;
    elseif ischar(v)
        out = string(v);
    elseif isnumeric(v)
        out = string(v);
    else
        out = "";
    end
end


function [stageLabel, startSec, durationSec, parsedOk] = local_parse_edfplus_annotations(hypTT, hypInfo)
    stageLabel = strings(0, 1);
    startSec = [];
    durationSec = [];
    parsedOk = false;

    try
        vars = string(hypTT.Properties.VariableNames);
    catch
        vars = strings(0, 1);
    end

    allStrings = strings(0, 1);
    for iVar = 1:numel(vars)
        raw = hypTT.(vars(iVar));
        if iscell(raw)
            for i = 1:numel(raw)
                txt = local_cell_to_string(raw{i});
                if strlength(txt) > 0
                    allStrings(end+1, 1) = txt; %#ok<AGROW>
                end
            end
        elseif isstring(raw)
            nonEmpty = raw(strlength(raw) > 0);
            allStrings = [allStrings; nonEmpty(:)]; %#ok<AGROW>
        elseif ischar(raw)
            cellTxt = string(cellstr(raw));
            nonEmpty = cellTxt(strlength(cellTxt) > 0);
            allStrings = [allStrings; nonEmpty(:)]; %#ok<AGROW>
        end
    end

    if isempty(allStrings)
        infoText = evalc('disp(hypInfo)');
        allStrings = string(regexp(infoText, 'Sleep stage\s+[0-9WR?]', 'match')).';
    end

    if isempty(allStrings)
        return;
    end

    joined = strjoin(allStrings, " ");
    joined = replace(joined, string(char(0)), " ");
    joined = regexprep(joined, '\s+', ' ');

    tokenPattern = '([+\-]?\d+(?:\.\d+)?)\x15(\d+(?:\.\d+)?)\x14(Sleep stage [0-9WR?])';
    tokenCells = regexp(joined, tokenPattern, 'tokens');

    if isempty(tokenCells)
        % Fallback: try label-only extraction and assume 30 s epochs.
        labelMatches = regexp(joined, 'Sleep stage [0-9WR?]', 'match');
        if isempty(labelMatches)
            return;
        end
        stageLabel = string(labelMatches(:));
        parsedOk = true;
        return;
    end

    nTok = numel(tokenCells);
    stageLabel = strings(nTok, 1);
    startSec = zeros(nTok, 1);
    durationSec = zeros(nTok, 1);
    for iTok = 1:nTok
        tok = tokenCells{iTok};
        startSec(iTok) = str2double(tok{1});
        durationSec(iTok) = str2double(tok{2});
        stageLabel(iTok) = string(tok{3});
    end
    parsedOk = true;
end


function [stageLabel, startSec, durationSec, parsedOk] = local_parse_annotation_timetable(TT)
    stageLabel = strings(0, 1);
    startSec = [];
    durationSec = [];
    parsedOk = false;

    if isempty(TT)
        return;
    end

    rowTimes = [];
    if isprop(TT, 'Properties') && ~isempty(TT.Properties.RowTimes)
        rowTimes = seconds(TT.Properties.RowTimes - TT.Properties.RowTimes(1));
        rowTimes = double(rowTimes(:));
    end

    vars = string(TT.Properties.VariableNames);
    nRows = height(TT);
    labels = strings(0, 1);
    starts = [];
    durs = [];

    for iRow = 1:nRows
        rowStrings = strings(0, 1);
        rowDuration = NaN;

        for iVar = 1:numel(vars)
            value = TT.(vars(iVar))(iRow);
            txt = local_cell_to_string(value);
            if strlength(txt) > 0
                rowStrings(end+1, 1) = txt; %#ok<AGROW>
            end

            if isnumeric(value) && isscalar(value) && isfinite(value)
                rowDuration = double(value);
            else
                numVal = str2double(txt);
                if isfinite(numVal)
                    rowDuration = numVal;
                end
            end
        end

        hit = "";
        for iTxt = 1:numel(rowStrings)
            txt = strtrim(rowStrings(iTxt));
            if startsWith(txt, "Sleep stage", 'IgnoreCase', true)
                hit = txt;
                break;
            end
        end

        if strlength(hit) > 0
            labels(end+1, 1) = hit; %#ok<AGROW>
            if ~isempty(rowTimes) && iRow <= numel(rowTimes)
                starts(end+1, 1) = rowTimes(iRow); %#ok<AGROW>
            else
                starts(end+1, 1) = 30 * (numel(labels) - 1); %#ok<AGROW>
            end

            if isfinite(rowDuration) && rowDuration > 0
                durs(end+1, 1) = rowDuration; %#ok<AGROW>
            else
                durs(end+1, 1) = 30; %#ok<AGROW>
            end
        end
    end

    if isempty(labels)
        return;
    end

    stageLabel = labels;
    startSec = starts;
    durationSec = durs;
    parsedOk = true;
end


function stageResult = local_run_stage_apc_bestband(signal, timeSec, stageTable, faBandList, fs, stageTag, channelName)
    if isempty(stageTable)
        stageResult = struct();
        stageResult.summary = local_empty_stage_summary(stageTag, channelName);
        stageResult.signal = [];
        stageResult.time = [];
        return;
    end

    keepMask = false(size(signal));
    for iRow = 1:height(stageTable)
        keepMask = keepMask | (timeSec >= stageTable.start_s(iRow) & timeSec < stageTable.stop_s(iRow));
    end

    sigKeep = signal(keepMask);
    timeKeep = timeSec(keepMask);

    if isempty(sigKeep)
        stageResult = struct();
        stageResult.summary = local_empty_stage_summary(stageTag, channelName);
        stageResult.signal = [];
        stageResult.time = [];
        return;
    end

    % Concatenate kept samples onto a contiguous stage-specific timeline.
    timeContig = (0:(numel(sigKeep) - 1)) ./ fs;
    sMatrix = struct('data', sigKeep(:).', 'time', timeContig(:).');

    candidateRows = table();
    apcCandidates = cell(size(faBandList, 1), 1);
    scores = -inf(size(faBandList, 1), 1);

    for iBand = 1:size(faBandList, 1)
        options = struct( ...
            'fA', faBandList(iBand, :), ...
            'epoch', [-1.5 1.5], ...
            'decomposition', 'fft_peak', ...
            'metric', 'canolty', ...
            'diagm', false, ...
            'surrogates', false, ...
            'num_perm', 0, ...
            'numPhaseBins', 18, ...
            'minPhaseHz', 0.5, ...
            'maxPhaseHz', 4.0);

        apc = bst_apc(sMatrix, options);
        apcCandidates{iBand} = apc;
        oneRow = local_pack_apc_summary(apc, stageTag, channelName, numel(sigKeep) / fs, height(stageTable), faBandList(iBand, :));
        oneRow.selection_score = local_candidate_score(oneRow);
        candidateRows = [candidateRows; oneRow]; %#ok<AGROW>
        scores(iBand) = oneRow.selection_score;
    end

    [~, bestIdx] = max(scores);
    bestApc = apcCandidates{bestIdx};
    bestBand = faBandList(bestIdx, :);
    bestRow = candidateRows(bestIdx, :);
    bestRow.selected_solution = true;
    candidateRows.selected_solution = false(height(candidateRows), 1);
    candidateRows.selected_solution(bestIdx) = true;

    stageResult = struct();
    stageResult.stage_table = stageTable;
    stageResult.signal = sigKeep;
    stageResult.time = timeContig;
    stageResult.apc = bestApc;
    stageResult.summary = bestRow;
    stageResult.candidate_summary = candidateRows;
    stageResult.selected_fa_band = bestBand;
end


function T = local_pack_apc_summary(apc, stageTag, channelName, durationSec, nEpochs, faBand)
    T = table( ...
        string(stageTag), ...
        string(channelName), ...
        durationSec, ...
        nEpochs, ...
        faBand(1), ...
        faBand(2), ...
        double(apc.status_code.Value(1)), ...
        double(apc.phase_frequency_hz.Value(1)), ...
        double(apc.amplitude_frequency_hz.Value(1)), ...
        double(apc.preferred_phase_deg.Value(1)), ...
        double(apc.pac_strength.Value(1)), ...
        double(apc.n_bursts.Value(1)), ...
        double(apc.n_phase_events.Value(1)), ...
        false, ...
        'VariableNames', {'stage','channel','duration_s','n_stage_epochs','fa_search_low_hz','fa_search_high_hz','status_code', ...
        'phase_frequency_hz','amplitude_frequency_hz','preferred_phase_deg', ...
        'pac_strength','n_bursts','n_phase_events','selected_solution'});
end


function T = local_empty_stage_summary(stageTag, channelName)
    T = table( ...
        string(stageTag), string(channelName), 0, 0, NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, false, -1e9, ...
        'VariableNames', {'stage','channel','duration_s','n_stage_epochs','fa_search_low_hz','fa_search_high_hz','status_code', ...
        'phase_frequency_hz','amplitude_frequency_hz','preferred_phase_deg', ...
        'pac_strength','n_bursts','n_phase_events','selected_solution','selection_score'});
end


function tag = local_subject_tag(psgFile)
    [~, name] = fileparts(psgFile);
    tag = local_safe_name(name);
end


function s = local_safe_name(x)
    s = regexprep(char(string(x)), '[^A-Za-z0-9]+', '_');
    s = regexprep(s, '^_+|_+$', '');
end


function s = local_normalize_name(x)
    s = lower(char(string(x)));
    s = regexprep(s, '[^a-z0-9]+', '');
end


function score = local_candidate_score(oneRow)
    if ~isfinite(oneRow.status_code) || oneRow.status_code ~= 0 || ~isfinite(oneRow.pac_strength)
        score = -1e9;
        return;
    end

    fa = oneRow.amplitude_frequency_hz;
    low = oneRow.fa_search_low_hz;
    high = oneRow.fa_search_high_hz;

    % Prefer solutions that do not sit on the search-band boundary.
    boundaryTol = 0.25;
    isBoundary = abs(fa - low) <= boundaryTol || abs(fa - high) <= boundaryTol;

    score = 1000 * double(~isBoundary) + 100 * oneRow.pac_strength;

    % Slight preference for a spindle-like center near the middle of the band.
    bandMid = mean([low high]);
    if isfinite(fa)
        score = score - 0.5 * abs(fa - bandMid);
    end
end


function fig = local_make_sleepedf_summary_figure(results, subjectTag)
    fig = figure('Color', 'w', 'Units', 'normalized', ...
        'Position', [0.08 0.12 0.84 0.72], ...
        'Name', 'Sleep-EDF APC summary', ...
        'Renderer', 'painters');

    T = results.summary;
    stages = ["N2","N3","N2N3"];
    channels = unique(string(T.channel), 'stable');
    colors = lines(max(numel(channels), 2));

    tl = tiledlayout(fig, 2, 2, 'Padding', 'compact', 'TileSpacing', 'compact');
    title(tl, sprintf('Sleep-EDF APC Summary | %s', strrep(subjectTag, '_', '\_')), ...
        'FontName', 'Helvetica', 'FontSize', 17, 'FontWeight', 'bold');

    ax1 = nexttile(tl, 1);
    local_plot_stage_metric(ax1, T, stages, channels, colors, 'pac_strength', 'PAC strength', 'A  APC strength by stage');

    ax2 = nexttile(tl, 2);
    local_plot_stage_metric(ax2, T, stages, channels, colors, 'phase_frequency_hz', 'Recovered f_P (Hz)', 'B  Recovered slow phase carrier');

    ax3 = nexttile(tl, 3);
    local_plot_stage_metric(ax3, T, stages, channels, colors, 'amplitude_frequency_hz', 'Recovered f_A (Hz)', 'C  Recovered spindle carrier');

    ax4 = nexttile(tl, 4);
    local_plot_stage_metric(ax4, T, stages, channels, colors, 'n_bursts', 'Detected bursts', 'D  Burst counts');
end


function local_plot_stage_metric(ax, T, stages, channels, colors, fieldName, yLabelText, titleText)
    hold(ax, 'on');
    x = 1:numel(stages);
    offsets = linspace(-0.14, 0.14, max(numel(channels), 1));

    for iChan = 1:numel(channels)
        y = nan(size(stages));
        for iStage = 1:numel(stages)
            idx = find(string(T.channel) == channels(iChan) & string(T.stage) == stages(iStage), 1);
            if ~isempty(idx)
                y(iStage) = T.(fieldName)(idx);
            end
        end
        plot(ax, x + offsets(iChan), y, '-o', ...
            'Color', colors(iChan, :), ...
            'LineWidth', 1.6, ...
            'MarkerSize', 7, ...
            'DisplayName', char(channels(iChan)));
    end

    set(ax, 'XTick', x, 'XTickLabel', cellstr(stages));
    xlabel(ax, 'Sleep stage');
    ylabel(ax, yLabelText);
    title(ax, titleText, 'FontWeight', 'bold', 'FontSize', 13);
    set(ax, 'FontName', 'Helvetica', 'FontSize', 12, 'LineWidth', 1.1);
    grid(ax, 'on');
    box(ax, 'off');
    legend(ax, 'Location', 'best', 'Box', 'off', 'FontSize', 11);
end
