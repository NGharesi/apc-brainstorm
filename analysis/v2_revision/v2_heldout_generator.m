function varargout=v2_heldout_generator(action,varargin)
% Signal formulas are inherited; frequency draws and streams are external.
switch action
 case 'sparsity_profile'
  varargout{1}=v1_sparsity_generator('profile');
 case 'distractor_profile'
  varargout{1}=v1_distractor_generator('profile');
 case 'slow_profile'
  cfg=v2_unit_generator('profile');cfg.snr_db=-3;varargout{1}=cfg;
 case 'sparsity'
  [varargout{1:nargout}]=v1_sparsity_generator('generate',varargin{:});
 case 'distractor'
  [varargout{1:nargout}]=v1_distractor_generator('generate',varargin{:});
 case 'slow'
  [varargout{1:nargout}]=v2_unit_generator('generate',varargin{:});
 case 'continuous'
  cfg=varargin{1};t=0:1/cfg.fs_hz:cfg.duration_s-1/cfg.fs_hz;phase=2*pi*cfg.true_fp_hz*t;
  low=sin(phase);low=low/std(low);carrier=sin(2*pi*cfg.true_fa_hz*t+.2);
  env=1+.70*cos(phase-pi/2);clean=low+1.25*env.*carrier;
  pink=powerlaw_noise(numel(t));white=randn(size(t));noise=pink+.5*white;noise=noise-mean(noise);noise=noise/max(sqrt(mean(noise.^2)),eps);
  signal=clean+sqrt(mean(clean.^2)/(10^(cfg.snr_db/10)))*noise;
  parts=struct('true_envelope',env,'carrier',carrier,'true_component',1.25*.70*cos(phase-pi/2).*carrier, ...
   'low_component',low,'background_component',zeros(size(t)),'distractor_component',zeros(size(t)),'noise',signal-clean);
  varargout={signal,t,parts};
 otherwise,error('v2:GeneratorAction','Unknown held-out generator action');
end
end
function x=powerlaw_noise(n)
freqs=0:n-1;amp=ones(1,n);valid=freqs>0 & freqs<=floor(n/2);amp(valid)=1./sqrt(freqs(valid));
spectrum=amp.*exp(1i*2*pi*rand(1,n));spectrum(1)=0;
if mod(n,2)==0,pos=2:n/2;neg=n:-1:n/2+2;spectrum(neg)=conj(spectrum(pos));spectrum(n/2+1)=real(spectrum(n/2+1));
else,pos=2:(n+1)/2;neg=n:-1:(n+3)/2;spectrum(neg)=conj(spectrum(pos));end
x=real(ifft(spectrum));x=x-mean(x);x=x/max(std(x),eps);
end
