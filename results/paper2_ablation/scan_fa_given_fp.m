function [result,scores,settings]=scan_fa_given_fp(signal,fs,fp,profile)
% A2-prime MVL-Ozkurt selection restricted to one supplied phase band.
signal=double(signal(:));settings=struct('phase_fp_hz',fp,'phase_half_width_hz',1.5,'amplitude_grid_hz',80:4:160,'amplitude_half_width_hz',14,'filter','original SOS-guarded butter(4), filtfilt','tie_rule','first grid maximum','metric','raw Canolty MVL / sqrt(mean(A.^2))');
if profile=="HA",settings.amplitude_half_width_hz=30;
elseif profile=="ecog",settings.amplitude_grid_hz=80:4:148;settings.amplitude_half_width_hz=30;
else,assert(profile=="heldout",'Paper2:Profile','Unknown scan profile');end
result=struct('fp',fp,'fa',nan,'selection_score',nan,'status',3,'amplitude_band_hz',[nan nan]);scores=nan(size(settings.amplitude_grid_hz));
if ~isscalar(fp)||~isfinite(fp)||fp<=0,return;end
phase=angle(hilbert(final_sos_filter(signal,fs,[max(.5,fp-1.5),fp+1.5])));
for ia=1:numel(settings.amplitude_grid_hz)
 fa=settings.amplitude_grid_hz(ia);half=settings.amplitude_half_width_hz;band=[max(1,fa-half),min(fs/2-1,fa+half)];A=abs(hilbert(final_sos_filter(signal,fs,band)));
 raw=calc_MI_all_methods(phase,A,'canolty',false,0,1,false,18);ampRms=sqrt(mean(A.^2));if ampRms>0,scores(ia)=raw/ampRms;else,scores(ia)=0;end
end
[score,j]=max(scores(:),[],'omitnan');result.fa=settings.amplitude_grid_hz(j);result.selection_score=score;result.status=double(~isfinite(score));result.amplitude_band_hz=[max(1,result.fa-settings.amplitude_half_width_hz),min(fs/2-1,result.fa+settings.amplitude_half_width_hz)];
end
