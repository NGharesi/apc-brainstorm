function options = paper2_options(optionsIn)
    % Fill in missing options so direct script calls and Brainstorm GUI
    % calls both reach the computational code in a uniform format.
    options = struct();
    options.fA = get_option(optionsIn, 'fA', [80 150]);
    options.epoch = get_option(optionsIn, 'epoch', [-0.6 0.6]);
    options.decomposition = get_option(optionsIn, 'decomposition', 'fft_peak');
    options.metric = lower(get_option(optionsIn, 'metric', 'canolty'));
    options.showPlots = parse_flag(get_option(optionsIn, 'diagm', false));
    options.useSurrogates = parse_flag(get_option(optionsIn, 'surrogates', false));
    options.numPerm = get_option(optionsIn, 'num_perm', 200);
    options.numPhaseBins = get_option(optionsIn, 'numPhaseBins', 18);
    options.burstTimeBandwidth = get_option(optionsIn, 'burstTimeBandwidth', 5);
    options.phaseTimeBandwidth = get_option(optionsIn, 'phaseTimeBandwidth', 20);
    options.phaseEpochCycles = get_option(optionsIn, 'phaseEpochCycles', 3);
    options.minPhaseHz = get_option(optionsIn, 'minPhaseHz', 1);
    options.maxPhaseHz = get_option(optionsIn, 'maxPhaseHz', 30);
    options.flipTroughs = parse_flag(get_option(optionsIn, 'flipTroughs', true));
    options.burstProminenceScale = get_option(optionsIn, 'burstProminenceScale', 0.75);
    options.surrogateMethod = lower(string(get_option(optionsIn, 'surrogateMethod', 'circular_shift')));
    options.amplitudeBandWidthHz = get_option(optionsIn, 'amplitudeBandWidthHz', 4);
    options.stepFourMode=lower(char(string(get_option(optionsIn,'stepFourMode','v1'))));
    options.fPRefine=parse_flag(get_option(optionsIn,'fPRefine',true));
    options.fPMaxBinSpacingHz=get_option(optionsIn,'fPMaxBinSpacingHz',0.05);
    if ~ismember(options.stepFourMode,{'v1','oct2026','june2026_clipped'})
        error('bst_apc:StepFourMode','Unknown Step 4 mode.');
    end
    if ~isscalar(options.fPMaxBinSpacingHz)||~isfinite(options.fPMaxBinSpacingHz)||options.fPMaxBinSpacingHz<=0||options.fPMaxBinSpacingHz>0.05
        error('bst_apc:SpectralSpacing','fPMaxBinSpacingHz must be positive and <=0.05 Hz.');
    end

    options.fA = double(options.fA(:).');
    options.epoch = double(options.epoch(:).');

    if numel(options.fA) ~= 2 || options.fA(1) <= 0 || options.fA(2) <= options.fA(1)
        error('bst_apc:InvalidFrequencyBand', 'OPTIONS.fA must be [fLow fHigh] in Hz.');
    end
    if numel(options.epoch) ~= 2 || options.epoch(1) >= options.epoch(2)
        error('bst_apc:InvalidEpoch', 'OPTIONS.epoch must be [tStart tStop] in seconds.');
    end
    if ~isscalar(options.burstProminenceScale) || ~isfinite(options.burstProminenceScale) || options.burstProminenceScale <= 0
        error('bst_apc:InvalidBurstProminenceScale', ...
            'OPTIONS.burstProminenceScale must be a positive finite scalar.');
    end
    if ~ismember(options.surrogateMethod, ["circular_shift", "phase_scramble"])
        error('bst_apc:InvalidSurrogateMethod', ...
            'OPTIONS.surrogateMethod must be circular_shift or phase_scramble.');
    end
    options.surrogateMethod = char(options.surrogateMethod);
    if ~isscalar(options.amplitudeBandWidthHz) || ~isfinite(options.amplitudeBandWidthHz) || options.amplitudeBandWidthHz <= 0
        error('bst_apc:InvalidAmplitudeBandWidth', ...
            'OPTIONS.amplitudeBandWidthHz must be a positive finite scalar.');
    end
end


function value = get_option(optionsIn, fieldName, defaultValue)
    % Return a default when optional fields were not supplied by the
    % caller.
    if isstruct(optionsIn) && isfield(optionsIn, fieldName) && ~isempty(optionsIn.(fieldName))
        value = optionsIn.(fieldName);
    else
        value = defaultValue;
    end
end


function tf = parse_flag(value)
    % Accept logicals, numerics, and common yes/no strings for convenience.
    if islogical(value)
        tf = value;
    elseif isnumeric(value)
        tf = (value ~= 0);
    elseif ischar(value)
        tf = any(strcmpi(value, {'yes','true','on'}));
    else
        tf = false;
    end
end


