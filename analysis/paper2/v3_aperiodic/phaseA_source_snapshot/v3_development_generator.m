function [signal,time,parts,cfg]=v3_development_generator(beta,duration,condition)
% Phase-A cells only; the original development-family power-law noise recipe.
cfg=struct('fs_hz',1000,'duration_s',duration,'beta',beta,'noise_sd',1, ...
 'true_fp_hz',15,'rhythm_amplitude',.6,'true_fa_hz',110,'burst_sigma_s',.01, ...
 'burst_amplitude',1.5,'cycle_keep_probability',.55,'jitter_sd_s',.005, ...
 'background_bursts',false,'condition',condition);
time=0:1/cfg.fs_hz:duration-1/cfg.fs_hz;n=numel(time);
noise=powerlaw_noise(n,beta);
if strcmp(condition,'coupled')
 centers=(.75/15):1/15:time(end);keep=rand(size(centers))<.55;
 centers=centers(keep)+.005*randn(1,sum(keep));
 rhythm=.6*sin(2*pi*15*time);
elseif strcmp(condition,'poisson_no_rhythm')
 centers=[];s=-log(max(rand,realmin))/(.55*15);
 while s<duration,centers(end+1)=s;s=s-log(max(rand,realmin))/(.55*15);end %#ok<AGROW>
 rhythm=zeros(size(time));
else,error('v3:DevelopmentCondition','Unknown Phase-A condition');end
envelope=zeros(size(time));for j=1:numel(centers),envelope=envelope+exp(-.5*((time-centers(j))/.01).^2);end
burst=1.5*envelope.*sin(2*pi*110*time);signal=noise+rhythm+burst;
parts=struct('noise',noise,'rhythm',rhythm,'true_component',burst,'event_times_s',centers);
end
function x=powerlaw_noise(n,alpha)
% Copied construction from analysis/v1_revision/v1_distractor_generator.m.
freqs=0:n-1;amp=ones(1,n);valid=freqs>0&freqs<=floor(n/2);amp(valid)=1./freqs(valid).^(alpha/2);
phaseRand=2*pi*rand(1,n);spectrum=amp.*exp(1i*phaseRand);spectrum(1)=0;
if mod(n,2)==0
 posIdx=2:n/2;negIdx=n:-1:n/2+2;spectrum(negIdx)=conj(spectrum(posIdx));spectrum(n/2+1)=real(spectrum(n/2+1));
else
 posIdx=2:(n+1)/2;negIdx=n:-1:(n+3)/2;spectrum(negIdx)=conj(spectrum(posIdx));
end
x=real(ifft(spectrum));x=x-mean(x);x=x/max(std(x),eps);
end
