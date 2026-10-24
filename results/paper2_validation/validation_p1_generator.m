function varargout=validation_p1_generator(action,varargin)
% Adapter only; copied generator functions below are unchanged.
switch action
 case 'profile',varargout{1}=local_get_profile('holdout');
 case 'cells',varargout{1}=local_cells();
 case 'trial'
  cfg=varargin{1};c=varargin{2};t=0:1/cfg.fs_hz:cfg.duration_s-1/cfg.fs_hz;
  x=local_simulate_two_rhythm(t,cfg,c);x=local_add_mixed_noise(x,cfg.snr_db);
  varargout={x,t};
 otherwise,error('Validation:P1Action','Unknown generator action');
end
end

function cfg = local_get_profile(profileName)
    cfg = struct();
    cfg.profile_name = char(lower(string(profileName)));
    cfg.fs_hz = 500; cfg.duration_s = 8.0; cfg.true_fa_hz = 120.0;
    cfg.phase_offset_deg = -90; cfg.true_high_amp = 1.30; cfg.base_hf_amp = 0.08;
    cfg.burst_sigma_s = 0.028; cfg.burst_phase_jitter_s = 0.010; cfg.snr_db = -3.0;
    cfg.coupling_level = 0.60; cfg.background_burst_scale = 0.18;
    cfg.broad_fa_band_hz = [80 152]; cfg.phase_scan_hz = 1:1:30;
    cfg.amplitude_scan_hz = 88:4:148; cfg.metric = 'canolty';
    cfg.fa_tolerance_hz = 8.0; cfg.fp_tolerance_hz = 1.0; cfg.min_phase_cycles = 3;
    cfg.welch_window_s = 2; cfg.welch_nfft = 4096; cfg.spectral_range_hz = [1 30];
    cfg.n_boot = 10000;
    switch lower(string(profileName))
        case "smoke",   cfg.n_repeats = 1;   cfg.random_seed = 20261019;
        case "holdout", cfg.n_repeats = 100; cfg.random_seed = 20261021;
        otherwise, error('Use profile ''smoke'' or ''holdout''.');
    end
end


function cells = local_cells()
    mk = @(name, fr, ar, fd, ad, keep, coupled) struct('name', string(name), ...
        'rhythm_hz', fr, 'rhythm_amp', ar, 'distractor_hz', fd, 'distractor_amp', ad, ...
        'keep_rate', keep, 'is_coupled', coupled);
    cells = [ ...
        mk("A_keep100", 5, 0.5, 11, 1.0, 1.00, true), ...
        mk("A_keep040", 5, 0.5, 11, 1.0, 0.40, true), ...
        mk("B_keep100", 11, 0.5, 5, 1.0, 1.00, true), ...
        mk("B_keep040", 11, 0.5, 5, 1.0, 0.40, true), ...
        mk("R_single_keep100", 8, 1.0, NaN, 0.0, 1.00, true), ...
        mk("N_uncoupled", 8, 1.0, NaN, 0.0, 1.00, false)];
end


function signal = local_simulate_two_rhythm(t, cfg, c)
    fp = c.rhythm_hz;
    low = c.rhythm_amp * sin(2 * pi * fp * t);
    if c.distractor_amp > 0
        low = low + c.distractor_amp * sin(2 * pi * c.distractor_hz * t + 2 * pi * rand);
    end
    phi0 = deg2rad(cfg.phase_offset_deg);
    cycleTimes = ((phi0 + pi / 2) / (2 * pi * fp)) + (0:ceil(t(end) * fp) + 2) / fp;
    cycleTimes = cycleTimes(cycleTimes >= t(1) - 1 / fp & cycleTimes <= t(end) + 1 / fp);
    if c.is_coupled
        keepMask = rand(size(cycleTimes)) <= c.keep_rate;
        eventTimes = cycleTimes(keepMask) + cfg.burst_phase_jitter_s * randn(1, sum(keepMask));
    else
        nEvents = round(c.keep_rate * numel(cycleTimes));
        eventTimes = t(1) + (t(end) - t(1)) * rand(1, nEvents);
    end
    trueEnv = local_gaussian_burst_envelope(t, eventTimes, cfg.burst_sigma_s);
    if max(trueEnv) > 0, trueEnv = trueEnv ./ max(trueEnv); end
    randTimes = linspace(t(1), t(end), numel(cycleTimes) + 2);
    randTimes = randTimes(2:end-1);
    randTimes = randTimes + (0.45 / fp) * (2 * rand(size(randTimes)) - 1);
    randTimes = min(max(randTimes, t(1)), t(end));
    bgEnv = local_gaussian_burst_envelope(t, randTimes, cfg.burst_sigma_s);
    if max(bgEnv) > 0, bgEnv = bgEnv ./ max(bgEnv); end
    hfEnvelope = cfg.base_hf_amp + cfg.true_high_amp * ...
        (cfg.coupling_level * trueEnv + cfg.background_burst_scale * bgEnv);
    signal = low + hfEnvelope .* sin(2 * pi * cfg.true_fa_hz * t);
end


function env = local_gaussian_burst_envelope(t, eventTimes, sigmaS)
    env = zeros(size(t));
    for iEvent = 1:numel(eventTimes)
        env = env + exp(-0.5 * ((t - eventTimes(iEvent)) / sigmaS) .^ 2);
    end
end


function signalOut = local_add_mixed_noise(signalIn, snrDb)
    n = numel(signalIn);
    signalPower = mean(signalIn .^ 2);
    pink = local_powerlaw_noise(n, 1.0);
    white = randn(1, n);
    noiseMix = pink + 0.5 * white;
    noiseMix = noiseMix - mean(noiseMix);
    noiseMix = noiseMix ./ max(sqrt(mean(noiseMix .^ 2)), eps);
    noisePowerTarget = signalPower / (10 ^ (snrDb / 10));
    signalOut = signalIn + sqrt(noisePowerTarget) * noiseMix;
end


function x = local_powerlaw_noise(n, alpha)
    freqs = (0:(n - 1));
    amp = ones(1, n);
    valid = freqs > 0 & freqs <= floor(n / 2);
    amp(valid) = 1 ./ (freqs(valid) .^ (alpha / 2));
    phaseRand = 2 * pi * rand(1, n);
    spectrum = amp .* exp(1i * phaseRand);
    spectrum(1) = 0;

    if mod(n, 2) == 0
        posIdx = 2:(n / 2);
        negIdx = n:-1:(n / 2 + 2);
        spectrum(negIdx) = conj(spectrum(posIdx));
        spectrum(n / 2 + 1) = real(spectrum(n / 2 + 1));
    else
        posIdx = 2:((n + 1) / 2);
        negIdx = n:-1:((n + 3) / 2);
        spectrum(negIdx) = conj(spectrum(posIdx));
    end

    x = real(ifft(spectrum));
    x = x - mean(x);
    x = x ./ max(std(x), eps);
end


