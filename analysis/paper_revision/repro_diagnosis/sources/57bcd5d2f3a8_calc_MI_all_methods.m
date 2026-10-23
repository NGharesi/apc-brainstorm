function [MI, PrefPhase, surrogateValues] = calc_MI_all_methods(Phase, Amp, approach, surrogates, num_perm, num_trials, diagm, varargin)
% CALC_MI_ALL_METHODS  PAC metrics with optional surrogate normalization.
%
% USAGE:
%   [MI, PrefPhase, surrogateValues] = calc_MI_all_methods( ...
%       Phase, Amp, approach, surrogates, num_perm, num_trials, diagm, nbin, surrogateMethod)
%
% INPUT:
%   Phase       : low-frequency phase in radians
%   Amp         : high-frequency amplitude envelope
%   approach    : 'tort', 'ozkurt', 'canolty', or 'plv'
%   surrogates  : 'yes' or 'no'
%   num_perm    : number of surrogate permutations
%   num_trials  : retained for backward compatibility (not used)
%   diagm       : logical or 'yes'/'no'
%   nbin        : optional number of phase bins, default = 18
%   surrogateMethod : optional 'circular_shift' (legacy default) or
%                     'phase_scramble' (rank-matched spectral null)
%
% OUTPUT:
%   MI              : raw PAC value, or z-scored PAC when surrogates='yes'
%   PrefPhase       : preferred phase in degrees
%   surrogateValues : surrogate MI distribution ([] when surrogates='no')
%
% Authors:
%   Niloofar Gharesi
%   Refactored for publication packaging by OpenAI Codex, 2026

    if nargin < 8 || isempty(varargin)
        nbin = 18;
    else
        nbin = varargin{1};
    end
    if numel(varargin) < 2 || isempty(varargin{2})
        surrogateMethod = 'circular_shift';
    else
        surrogateMethod = lower(char(string(varargin{2})));
    end

    num_trialsLocal = num_trials; %#ok<NASGU>

    [Phase, Amp] = sanitize_inputs(Phase, Amp);
    method = lower(strtrim(approach));
    showPlots = parse_flag(diagm);

    % Compute the raw PAC estimate first, then optionally normalize it
    % against a circular-shift surrogate distribution.
    [MI, PrefPhase] = compute_metric(Phase, Amp, method, nbin, showPlots);
    surrogateValues = [];

    if is_yes(surrogates)
        surrogateValues = compute_surrogates(Phase, Amp, method, nbin, max(1, round(num_perm)), surrogateMethod);
        surrogateMu = mean(surrogateValues, 'omitnan');
        surrogateSigma = std(surrogateValues, 0, 'omitnan');
        if surrogateSigma > 0
            MI = (MI - surrogateMu) ./ surrogateSigma;
        else
            MI = MI - surrogateMu;
        end
    end
end


function [Phase, Amp] = sanitize_inputs(Phase, Amp)
    % Make the metric functions robust to row/column mismatches and remove
    % invalid samples before any statistics are computed.
    Phase = double(Phase(:));
    Amp = double(Amp(:));
    n = min(numel(Phase), numel(Amp));
    Phase = Phase(1:n);
    Amp = Amp(1:n);

    valid = isfinite(Phase) & isfinite(Amp);
    Phase = Phase(valid);
    Amp = Amp(valid);

    if isempty(Phase) || isempty(Amp)
        error('calc_MI_all_methods:EmptyInput', 'Phase and amplitude must contain finite values.');
    end
end


function [MI, PrefPhase] = compute_metric(Phase, Amp, method, nbin, showPlots)
    % Keep the API flexible while routing everything through a small set
    % of well-defined PAC estimators.
    switch method
        case 'tort'
            [MI, PrefPhase, binCenters, meanAmp] = compute_tort(Phase, Amp, nbin);
            if showPlots
                plot_binned_phase_amplitude(binCenters, meanAmp, MI, PrefPhase, 'Tort KL-MI');
            end

        case 'ozkurt'
            [MI, PrefPhase, binCenters, meanAmp] = compute_ozkurt(Phase, Amp, nbin);
            if showPlots
                plot_binned_phase_amplitude(binCenters, meanAmp, MI, PrefPhase, 'Ozkurt MVL');
            end

        case {'plv', 'phase_locking_value'}
            [MI, PrefPhase] = compute_plv(Phase, Amp);
            if showPlots
                plot_complex_summary(Amp .* exp(1i * Phase), MI, PrefPhase, 'PLV');
            end

        otherwise
            [MI, PrefPhase] = compute_canolty(Phase, Amp);
            if showPlots
                plot_complex_summary(Amp .* exp(1i * Phase), MI, PrefPhase, 'Canolty MVL');
            end
    end
end


function [MI, PrefPhase, binCenters, meanAmp] = compute_tort(Phase, Amp, nbin)
    % Tort MI measures how strongly the amplitude distribution across phase
    % bins deviates from uniform.
    [binCenters, meanAmp] = phase_binned_amplitude(Phase, Amp, nbin);
    totalAmp = sum(meanAmp);
    if totalAmp <= 0 || ~isfinite(totalAmp)
        MI = 0;
        PrefPhase = nan;
        return;
    end
    prob = meanAmp ./ totalAmp;
    prob(prob <= 0) = eps;
    MI = (log(nbin) - (-sum(prob .* log(prob)))) ./ log(nbin);
    [~, iMax] = max(meanAmp);
    PrefPhase = rad2deg(binCenters(iMax));
end


function [MI, PrefPhase, binCenters, meanAmp] = compute_ozkurt(Phase, Amp, nbin)
    % Ozkurt's normalization scales the mean vector length by total
    % amplitude power, reducing sensitivity to raw envelope magnitude.
    N = numel(Amp);
    z = Amp .* exp(1i * Phase);
    ampNorm = sqrt(mean(Amp .* Amp));
    if ampNorm <= 0 || ~isfinite(ampNorm)
        MI = 0;
    else
        MI = (1 / sqrt(N)) * abs(mean(z)) / ampNorm;
    end
    PrefPhase = rad2deg(angle(mean(z)));
    [binCenters, meanAmp] = phase_binned_amplitude(Phase, Amp, nbin);
end


function [MI, PrefPhase] = compute_canolty(Phase, Amp)
    % Canolty PAC is the magnitude of the complex average of
    % amplitude-weighted phase vectors.
    z = Amp .* exp(1i * Phase);
    meanVec = mean(z, 'omitnan');
    MI = abs(meanVec);
    PrefPhase = rad2deg(angle(meanVec));
end


function [MI, PrefPhase] = compute_plv(Phase, Amp)
    % PLV compares the slow phase to the instantaneous phase of the
    % amplitude envelope itself.
    ampPhase = angle(hilbert(detrend(Amp)));
    meanVec = mean(exp(1i * (Phase - ampPhase)), 'omitnan');
    MI = abs(meanVec);
    PrefPhase = rad2deg(angle(meanVec));
end


function [binCenters, meanAmp] = phase_binned_amplitude(Phase, Amp, nbin)
    % Bin amplitude by phase so bin-based metrics and QC plots share the
    % same internal representation.
    edges = linspace(-pi, pi, nbin + 1);
    binCenters = edges(1:end-1) + diff(edges) / 2;
    meanAmp = zeros(1, nbin);

    for iBin = 1:nbin
        idx = (Phase >= edges(iBin)) & (Phase < edges(iBin + 1));
        if iBin == nbin
            idx = idx | (Phase == edges(end));
        end
        if any(idx)
            meanAmp(iBin) = mean(Amp(idx), 'omitnan');
        else
            meanAmp(iBin) = 0;
        end
    end
end


function surrogateValues = compute_surrogates(Phase, Amp, method, nbin, numPerm, surrogateMethod)
    n = numel(Amp);
    surrogateValues = nan(1, numPerm);

    minShift = max(1, floor(0.10 * n));
    maxShift = max(minShift, floor(0.90 * n));

    % Circular shifts are retained as a legacy option. For stationary
    % periodic signals, however, a shift can preserve MVL magnitude. The
    % phase-scramble option preserves the amplitude spectrum while
    % destroying its temporal alignment with low-frequency phase.
    for iPerm = 1:numPerm
        switch surrogateMethod
            case 'circular_shift'
                if maxShift > minShift
                    shift = randi([minShift, maxShift], 1, 1);
                else
                    shift = minShift;
                end
                ampSurr = circshift(Amp, shift);
            case 'phase_scramble'
                ampSurr = phase_scramble(Amp);
            otherwise
                error('calc_MI_all_methods:InvalidSurrogateMethod', ...
                    'Unknown surrogate method: %s', surrogateMethod);
        end
        surrogateValues(iPerm) = compute_metric(Phase, ampSurr, method, nbin, false);
    end
end


function xSurr = phase_scramble(x)
    % Randomize Fourier phases with Hermitian symmetry, then rank-match the
    % result to the original envelope. Rank matching retains the observed
    % nonnegative amplitude distribution while the scrambled ordering
    % removes its temporal alignment with slow phase.
    x = double(x(:));
    n = numel(x);
    xMean = mean(x, 'omitnan');
    spectrum = fft(x - xMean);
    if mod(n, 2) == 0
        positive = 2:(n / 2);
        negative = n:-1:(n / 2 + 2);
    else
        positive = 2:((n + 1) / 2);
        negative = n:-1:((n + 3) / 2);
    end
    % spectrum is a column vector after input sanitization, so retain a
    % column orientation to avoid implicit expansion during assignment.
    randomPhase = 2 * pi * rand(numel(positive), 1);
    spectrum(positive) = abs(spectrum(positive)) .* exp(1i * randomPhase);
    spectrum(negative) = conj(spectrum(positive));
    xSurr = real(ifft(spectrum)) + xMean;
    [~, order] = sort(xSurr, 'ascend');
    sortedEnvelope = sort(x, 'ascend');
    xSurr(order) = sortedEnvelope;
end


function tf = is_yes(value)
    % Accept both text and non-text flag styles.
    if ischar(value)
        tf = any(strcmpi(value, {'yes','true','on'}));
    else
        tf = parse_flag(value);
    end
end


function tf = parse_flag(value)
    % Normalize permissive user input to a plain logical value.
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


function plot_binned_phase_amplitude(binCenters, meanAmp, MI, prefPhase, methodLabel)
    % Shared QC figure for estimators that reduce the signal to
    % phase-binned amplitudes.
    figure('Color', 'w');
    tiledlayout(1, 2, 'Padding', 'compact', 'TileSpacing', 'compact');

    nexttile;
    plot(binCenters, meanAmp, 'k', 'LineWidth', 1.5);
    xlabel('Phase (rad)');
    ylabel('Mean amplitude');
    title(sprintf('%s | MI = %.4f', methodLabel, MI));
    grid on;

    nexttile;
    bar(rad2deg(binCenters), meanAmp, 'FaceColor', [0.1 0.1 0.1]);
    xlabel('Phase (deg)');
    ylabel('Mean amplitude');
    title(sprintf('Preferred phase = %.2f deg', prefPhase));
end


function plot_complex_summary(signalPac, MI, prefPhase, methodLabel)
    % Shared QC figure for estimators based on a complex mean vector.
    meanVec = mean(signalPac, 'omitnan');
    figure('Color', 'w');
    polarplot(signalPac, '.k');
    hold on;
    polarplot(meanVec, 'or', 'MarkerFaceColor', 'r', 'MarkerSize', 8);
    title(sprintf('%s | MI = %.4f | Preferred phase = %.2f deg', methodLabel, MI, prefPhase));
end
