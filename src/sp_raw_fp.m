function [fp,d,status]=sp_raw_fp(signal,fs,OPTIONS)
% SP-raw baseline: the prespecified v3 peak rule on the raw Welch spectrum.
if nargin<3,OPTIONS=struct;end
fA=[80 150];minimum=1;maximum=30;
if isfield(OPTIONS,'fA'),fA=OPTIONS.fA;end
if isfield(OPTIONS,'minPhaseHz'),minimum=OPTIONS.minPhaseHz;end
if isfield(OPTIONS,'maxPhaseHz'),maximum=OPTIONS.maxPhaseHz;end
x=double(signal(:));x=fillmissing(x,'linear','EndValues','nearest');x=x-mean(x,'omitnan');T=numel(x)/fs;
flo=max(minimum,7/T);fhi=min([maximum,fs/3,fA(1)-.5]);
L=min(round(2*fs),numel(x));nfft=max([256,2^nextpow2(L),2^nextpow2(ceil(fs/.05))]);
[power,f]=pwelch(x,hann(L,'symmetric'),floor(L/2),nfft,fs);
[fp,d,status]=apc_v3_spectral_peak(power,f,flo,fhi);
d.window_samples=L;d.overlap_samples=floor(L/2);d.nfft=nfft;d.fs_hz=fs;d.duration_s=T;d.spectrum='raw signal Welch';
end
