function varargout=v2_unit_generator(action,varargin)
% Analysis-only scenario derivative of frozen distractor generator.
switch action
 case 'profile'
  cfg=local_get_profile('reviewer_control');cfg.true_fp_hz=8;cfg.snr_db=20;cfg.broad_fa_band_hz=[80 160];
  cfg.phase_offset_deg=180;cfg.distractor_base_amp=0;
  cfg.slow_distractor_hz=11;cfg.slow_amplitude_ratios=[0 3];
  cfg.slow_distractor_phase_rad=0;cfg.slow_amplitude_ratio=0;
  cfg.high_frequency_distractor_present=false;
  varargout{1}=cfg;
 case 'generate'
  cfg=varargin{1};ratio=varargin{2};t=0:1/cfg.fs_hz:cfg.duration_s-1/cfg.fs_hz;
  [~,parts]=local_simulate_distractor_signal(t,cfg,0,'coupled');
  unusedNull=local_simulate_distractor_signal(t,cfg,0,'null');
  slow10=ratio*cfg.low_amp*sin(2*pi*cfg.slow_distractor_hz*t+cfg.slow_distractor_phase_rad);
  parts.distractor_component=slow10;
  parts.base_carrier_component=cfg.base_hf_amp*parts.carrier;
  clean=parts.low_component+parts.base_carrier_component+parts.true_component+slow10;
  signal=local_add_mixed_noise(clean,cfg.snr_db);
  unusedNull=local_add_mixed_noise(unusedNull,cfg.snr_db); %#ok<NASGU>
  parts.noise=signal-clean;
  varargout={signal,t,parts};
 otherwise
  error('followup:GeneratorAction','Unknown generator action');
end
end
function cfg = local_get_profile(profileName)
    profileName = lower(string(profileName));

    cfg = struct();
    cfg.profile_name = char(profileName);
    cfg.random_seed = 20260618;
    cfg.fs_hz = 500;
    cfg.duration_s = 6.0;
    cfg.true_fp_hz = 8.0;
    cfg.true_fa_hz = 120.0;
    cfg.distractor_fa_hz = 96.0;
    cfg.phase_offset_deg = -90;
    cfg.low_amp = 1.0;
    cfg.true_high_amp = 1.3;
    cfg.distractor_base_amp = 0.6;
    cfg.base_hf_amp = 0.08;
    cfg.burst_sigma_s = 0.028;
    cfg.coupling_level = 0.60;
    cfg.burst_phase_jitter_s = 0.010;
    cfg.snr_db = -3.0;
    cfg.broad_fa_band_hz = [80 150];
    cfg.phase_scan_hz = 4:1:12;
    cfg.amplitude_scan_hz = 80:8:152;
    cfg.phase_band_half_width_hz = 1.5;
    cfg.amplitude_band_half_width_hz = 6.0;
    cfg.metric = 'canolty';
    cfg.fa_tolerance_hz = 8.0;
    cfg.fp_tolerance_hz = 1.0;
    cfg.oracle_control_distractor_scale = 0.0;

    switch profileName
        case "fast"
            cfg.n_repeats = 10;
            cfg.distractor_scale_values = [0.0 0.5 1.0 1.5 2.0 2.5];
        case "full"
            cfg.n_repeats = 25;
            cfg.distractor_scale_values = [0.0 0.5 1.0 1.5 2.0 2.5 3.0];
        case "reviewer_control"
            % Full replication of the reviewer-requested fixed-pair control.
            cfg.n_repeats = 25;
            cfg.distractor_scale_values = [0.0 0.5 1.0 1.5 2.0 2.5 3.0];
        otherwise
            error('Unknown profileName: %s', profileName);
    end
end


function [signal,parts] = local_simulate_distractor_signal(t, cfg, distractorScale, couplingMode)
    if nargin < 4 || isempty(couplingMode)
        couplingMode = 'coupled';
    end

    fp = cfg.true_fp_hz;
    phi0 = deg2rad(cfg.phase_offset_deg);

    low = cfg.low_amp * sin(2 * pi * fp * t);

    cycleTimes = ((phi0 + pi / 2) / (2 * pi * fp)) + (0:ceil(t(end) * fp) + 2) / fp;
    cycleTimes = cycleTimes(cycleTimes >= t(1) - 1 / fp & cycleTimes <= t(end) + 1 / fp);

    if strcmpi(couplingMode, 'coupled')
        coupledTimes = cycleTimes + cfg.burst_phase_jitter_s * randn(size(cycleTimes));
    else
        coupledTimes = linspace(t(1), t(end), numel(cycleTimes) + 2);
        coupledTimes = coupledTimes(2:end-1);
        coupledTimes = coupledTimes + 0.45 / fp * (2 * rand(size(coupledTimes)) - 1);
        coupledTimes = min(max(coupledTimes, t(1)), t(end));
    end
    trueEnv = zeros(size(t));
    for iCycle = 1:numel(coupledTimes)
        trueEnv = trueEnv + exp(-0.5 * ((t - coupledTimes(iCycle)) / cfg.burst_sigma_s) .^ 2);
    end
    if max(trueEnv) > 0
        trueEnv = trueEnv ./ max(trueEnv);
    end

    randTimes = linspace(t(1), t(end), numel(cycleTimes) + 2);
    randTimes = randTimes(2:end-1);
    randTimes = randTimes + 0.45 / fp * (2 * rand(size(randTimes)) - 1);
    randTimes = min(max(randTimes, t(1)), t(end));
    distractorEnv = zeros(size(t));
    for iRand = 1:numel(randTimes)
        distractorEnv = distractorEnv + exp(-0.5 * ((t - randTimes(iRand)) / cfg.burst_sigma_s) .^ 2);
    end
    if max(distractorEnv) > 0
        distractorEnv = distractorEnv ./ max(distractorEnv);
    end

    trueHfEnvelope = cfg.base_hf_amp + cfg.true_high_amp * cfg.coupling_level * trueEnv;
    distractorEnvelope = cfg.base_hf_amp + cfg.distractor_base_amp * distractorScale * distractorEnv;

    trueHf = trueHfEnvelope .* sin(2 * pi * cfg.true_fa_hz * t);
    distractorHf = distractorEnvelope .* sin(2 * pi * cfg.distractor_fa_hz * t + 2 * pi * rand());
    signal = low + trueHf + distractorHf;
    parts=struct('true_event_times',coupledTimes,'true_envelope',trueEnv,'carrier',sin(2*pi*cfg.true_fa_hz*t), ...
       'true_component',cfg.true_high_amp*cfg.coupling_level*trueEnv.*sin(2*pi*cfg.true_fa_hz*t), ...
       'low_component',low,'background_component',zeros(size(t)),'distractor_component',distractorHf);
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
    noiseScaled = sqrt(noisePowerTarget) * noiseMix;
    signalOut = signalIn + noiseScaled;
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


