function varargout = process_apc(varargin)
% PROCESS_APC: Burst-triggered amplitude-phase coupling for Brainstorm.

% @=============================================================================
% This function is part of the Brainstorm software:
% https://neuroimage.usc.edu/brainstorm
%
% Copyright (c) University of Southern California & McGill University
% This software is distributed under the terms of the GNU General Public License
% as published by the Free Software Foundation. Further details on the GPLv3
% license can be found at http://www.gnu.org/copyleft/gpl.html.
%
% FOR RESEARCH PURPOSES ONLY. THE SOFTWARE IS PROVIDED "AS IS," AND THE
% UNIVERSITY OF SOUTHERN CALIFORNIA AND ITS COLLABORATORS DO NOT MAKE ANY
% WARRANTY, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF
% MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, NOR DO THEY ASSUME ANY
% LIABILITY OR RESPONSIBILITY FOR THE USE OF THIS SOFTWARE.
%
% Authors: Niloofar Gharesi
%          Refactored for publication packaging by OpenAI Codex, 2026
% =============================================================================@

    eval(macro_method);
end


%% ===== GET DESCRIPTION =====
function sProcess = GetDescription() %#ok<DEFNU>
    % Declare the process metadata and all options shown in Brainstorm's
    % Process tab.
    sProcess.Comment     = 'Amplitude-Phase Coupling (APC)';
    sProcess.Category    = 'File';
    sProcess.SubGroup    = 'Frequency';
    sProcess.Index       = 656;
    sProcess.Description = 'https://neuroimage.usc.edu/brainstorm/Tutorials/TutPac#PAC_estimation';

    sProcess.InputTypes  = {'data', 'results', 'matrix'};
    sProcess.OutputTypes = {'data', 'results', 'matrix'};
    sProcess.nInputs     = 1;
    sProcess.nMinFiles   = 1;

    sProcess.options.label1.Comment = '<B>APC Parameters</B>';
    sProcess.options.label1.Type    = 'label';

    sProcess.options.timewindow.Comment = 'Time window:';
    sProcess.options.timewindow.Type    = 'timewindow';
    sProcess.options.timewindow.Value   = [];

    sProcess.options.fA.Comment = 'High-frequency search band:';
    sProcess.options.fA.Type    = 'range';
    sProcess.options.fA.Value   = {[16, 250], 'Hz', 16};

    sProcess.options.epoch.Comment = 'Burst-centered epoch:';
    sProcess.options.epoch.Type    = 'range';
    sProcess.options.epoch.Value   = {[-0.6, 0.6], 's', []};

    sProcess.options.decomposition.Comment = 'Phase-frequency estimator (fft_peak, trend, vmd, vmd_sym):';
    sProcess.options.decomposition.Type    = 'text';
    sProcess.options.decomposition.Value   = 'fft_peak';

    sProcess.options.metric.Comment = 'PAC metric (canolty, tort, ozkurt, plv):';
    sProcess.options.metric.Type    = 'text';
    sProcess.options.metric.Value   = 'canolty';

    sProcess.options.surrogates.Comment = 'Normalize against surrogates';
    sProcess.options.surrogates.Type    = 'checkbox';
    sProcess.options.surrogates.Value   = 0;

    sProcess.options.num_perm.Comment = 'Number of surrogate permutations:';
    sProcess.options.num_perm.Type    = 'value';
    sProcess.options.num_perm.Value   = {200, '', 0};

    sProcess.options.numPhaseBins.Comment = 'Number of phase bins:';
    sProcess.options.numPhaseBins.Type    = 'value';
    sProcess.options.numPhaseBins.Value   = {18, '', 0};

    sProcess.options.diagm.Comment = 'Show diagnostic plots';
    sProcess.options.diagm.Type    = 'checkbox';
    sProcess.options.diagm.Value   = 0;
end


%% ===== FORMAT COMMENT =====
function Comment = FormatComment(sProcess) %#ok<DEFNU>
    % Include the selected amplitude-search band in the process label.
    fA = get_option_value(sProcess.options.fA.Value);
    Comment = sprintf('%s: %.0f-%.0f Hz', sProcess.Comment, fA(1), fA(2));
end


%% ===== RUN =====
function OutputFiles = Run(sProcess, sInput) %#ok<DEFNU>
    % Main Brainstorm entry point: read input, compute APC features, then
    % save one output file per exported feature.
    OutputFiles = {};

    OPTIONS = collect_options(sProcess);

    % Brainstorm inputs can be data, results, or matrices, but the APC
    % core only needs a time vector plus a [rows x time] matrix.
    try
        [sMatrix, sMatIn] = load_input_timeseries(sInput, OPTIONS.timewindow);
    catch ME
        bst_report('Error', sProcess, sInput, ME.message);
        return;
    end

    try
        sApc = Compute(sMatrix, OPTIONS);
    catch ME
        bst_report('Error', sProcess, sInput, ME.message);
        return;
    end

    % Export each APC feature as a separate Brainstorm file so users can
    % inspect, threshold, and combine them independently downstream.
    featureNames = fieldnames(sApc);
    for iFeature = 1:numel(featureNames)
        featureName = featureNames{iFeature};
        featureData = sApc.(featureName);
        sMatOut = create_output_matrix(sInput, sMatIn, featureName, featureData, OPTIONS);
        OutputFile = get_output_filename(sInput, featureName);
        bst_save(OutputFile, sMatOut, 'v6');
        db_add_data(sInput.iStudy, OutputFile, sMatOut);
        OutputFiles{end+1} = OutputFile; %#ok<AGROW>
    end
end


%% ===== COMPUTE =====
function sApc = Compute(sMatrix, OPTIONS) %#ok<DEFNU>
    % Thin wrapper so the core algorithm remains reusable outside the
    % Brainstorm process framework.
    sApc = bst_apc(sMatrix, OPTIONS);
end


%% ===== OPTIONS =====
function OPTIONS = collect_options(sProcess)
    % Copy GUI option values into a plain structure expected by bst_apc.
    OPTIONS = struct();
    OPTIONS.timewindow     = get_option_value(sProcess.options.timewindow.Value);
    OPTIONS.fA             = get_option_value(sProcess.options.fA.Value);
    OPTIONS.epoch          = get_option_value(sProcess.options.epoch.Value);
    OPTIONS.decomposition  = get_option_value(sProcess.options.decomposition.Value);
    OPTIONS.metric         = get_option_value(sProcess.options.metric.Value);
    OPTIONS.diagm          = get_option_value(sProcess.options.diagm.Value);
    OPTIONS.surrogates     = get_option_value(sProcess.options.surrogates.Value);
    OPTIONS.num_perm       = get_option_value(sProcess.options.num_perm.Value);
    OPTIONS.numPhaseBins   = get_option_value(sProcess.options.numPhaseBins.Value);
end


function value = get_option_value(rawValue)
    % Brainstorm option values are sometimes stored directly and sometimes
    % wrapped in a cell array.
    if iscell(rawValue)
        value = rawValue{1};
    else
        value = rawValue;
    end
end


%% ===== LOAD INPUT =====
function [sMatrix, sMatIn] = load_input_timeseries(sInput, timeWindow)
    % Load any supported Brainstorm input type and normalize it to the
    % simple [rows x time] representation used by the APC core.
    % Normalize the supported Brainstorm file types into the same in-memory
    % representation before passing them to bst_apc.
    switch lower(sInput.FileType)
        case 'data'
            if exist('in_bst_data', 'file') == 2
                sMatIn = in_bst_data(sInput.FileName);
            else
                sMatIn = load(file_fullpath(sInput.FileName));
            end
            data = infer_matrix_field(sMatIn, {'F'});
            time = infer_time_field(sMatIn);

        case 'results'
            if exist('in_bst_results', 'file') == 2
                sMatIn = in_bst_results(sInput.FileName, 1);
            else
                sMatIn = load(file_fullpath(sInput.FileName));
            end
            data = infer_matrix_field(sMatIn, {'ImageGridAmp'});
            time = infer_time_field(sMatIn);

        case 'matrix'
            if exist('in_bst_matrix', 'file') == 2
                sMatIn = in_bst_matrix(sInput.FileName);
            else
                sMatIn = load(file_fullpath(sInput.FileName));
            end
            data = infer_matrix_field(sMatIn, {'Value', 'F', 'ImageGridAmp'});
            time = infer_time_field(sMatIn);

        otherwise
            error('Unsupported input type: %s', sInput.FileType);
    end

    if isempty(time)
        error('Input file does not contain a valid time vector.');
    end

    if ~isempty(timeWindow)
        timeMask = (time >= timeWindow(1)) & (time <= timeWindow(2));
        if ~any(timeMask)
            error('The selected time window does not overlap with the input file.');
        end
        data = data(:, timeMask);
        time = time(timeMask);
    end

    sMatrix = struct('data', data, 'time', time);
end


function data = infer_matrix_field(sMatIn, candidateFields)
    % The main numeric field differs by file type, so probe a short list of
    % expected field names.
    data = [];
    for iField = 1:numel(candidateFields)
        fieldName = candidateFields{iField};
        if isfield(sMatIn, fieldName) && ~isempty(sMatIn.(fieldName))
            data = sMatIn.(fieldName);
            return;
        end
    end
    error('Could not infer the data matrix from the input file.');
end


function time = infer_time_field(sMatIn)
    % Brainstorm time-resolved files typically expose their sample times in
    % the Time field.
    if isfield(sMatIn, 'Time') && ~isempty(sMatIn.Time)
        time = sMatIn.Time(:).';
    else
        time = [];
    end
end


%% ===== OUTPUT =====
function sMatOut = create_output_matrix(sInput, sMatIn, featureName, featureData, OPTIONS)
    % Package one scalar APC feature back into a Brainstorm-compatible file
    % of the same general type as the original input.
    values = featureData.Value(:);
    fileComment = sprintf('%s | APC: %s', sInput.Comment, strrep(featureName, '_', ' '));

    % Mirror the input type on output so the feature maps stay convenient
    % to manipulate within standard Brainstorm workflows.
    switch lower(sInput.FileType)
        case 'results'
            sMatOut = db_template('resultsmat');
            sMatOut.ImageGridAmp = values;
            sMatOut = copy_if_present(sMatIn, sMatOut, {'SurfaceFile', 'HeadModelFile', 'GridLoc', 'GridOrient', 'GridAtlas', 'Atlas', 'nComponents'});

        case 'data'
            sMatOut = db_template('datamat');
            sMatOut.F = values;
            if isfield(sMatIn, 'ChannelFlag')
                sMatOut.ChannelFlag = sMatIn.ChannelFlag;
            end
            sMatOut.DataType = '';

        case 'matrix'
            sMatOut = db_template('matrixmat');
            sMatOut.Value = values;

        otherwise
            error('Unsupported output type: %s', sInput.FileType);
    end

    sMatOut.Time = 0;
    sMatOut.Comment = fileComment;
    sMatOut.DisplayUnits = featureData.Units;
    if isfield(sMatOut, 'Description')
        sMatOut.Description = {featureData.Description};
    end

    historyLine = sprintf([ ...
        'process_apc: %s | fA=[%g %g] Hz | epoch=[%g %g] s | ' ...
        'decomp=%s | metric=%s | phaseBins=%d | surrogates=%d | nPerm=%d'], ...
        featureName, ...
        OPTIONS.fA(1), OPTIONS.fA(2), ...
        OPTIONS.epoch(1), OPTIONS.epoch(2), ...
        OPTIONS.decomposition, ...
        OPTIONS.metric, ...
        OPTIONS.numPhaseBins, ...
        OPTIONS.surrogates, ...
        OPTIONS.num_perm);
    sMatOut = bst_history('add', sMatOut, 'process', historyLine);
end


function sMatOut = copy_if_present(sMatIn, sMatOut, fieldNames)
    % Preserve optional geometry and source metadata when exporting result
    % maps.
    for iField = 1:numel(fieldNames)
        fieldName = fieldNames{iField};
        if isfield(sMatIn, fieldName)
            sMatOut.(fieldName) = sMatIn.(fieldName);
        end
    end
end


function OutputFile = get_output_filename(sInput, featureName)
    % Save outputs next to the original file using a feature-specific
    % suffix and Brainstorm's uniqueness helper.
    [originalPath, originalBase, originalExt] = bst_fileparts(file_fullpath(sInput.FileName));
    OutputFile = bst_fullfile(originalPath, [originalBase, '_apc_', featureName, originalExt]);
    OutputFile = file_unique(OutputFile);
end
