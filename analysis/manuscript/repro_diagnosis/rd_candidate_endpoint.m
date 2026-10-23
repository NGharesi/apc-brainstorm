function rd_candidate_endpoint(d)
cd(d);addpath(fullfile(d,'sources'),'-begin');maxNumCompThreads(1);
source=@rd_sparsity_source;cfg=source('profile','full');rng(cfg.random_seed,'twister');rows={};
options=struct('fA',cfg.broad_fa_band_hz,'epoch',[-.6 .6], 'decomposition','fft_peak','metric',cfg.metric,'diagm',false,'surrogates',false,'num_perm',0,'numPhaseBins',18);
for il=1:numel(cfg.burst_keep_rates)
 for ir=1:cfg.n_repeats
  [signal,time]=source('generate',cfg,cfg.burst_keep_rates(il));
  if cfg.burst_keep_rates(il)~=.15,continue;end
  input=struct('data',signal,'time',time);before=rng;tic;
  [r,route]=rd_apc_historical_candidate(input,options);
  assert(isequal(before,rng));
  rows{end+1}=struct('repeat_index',ir,'candidate_fp_hz',double(r.phase_frequency_hz.Value(1)), ...
   'candidate_fa_hz',double(r.amplitude_frequency_hz.Value(1)),'candidate_C_APC',double(r.pac_strength.Value(1)), ...
   'selection_route',route(1),'trial_seconds',toc); %#ok<AGROW>
  fprintf('JUNE STEP4 CANDIDATE %d/25: fp %.8f fa %.2f C %.17g; %.2fs\n',ir,rows{end}.candidate_fp_hz,rows{end}.candidate_fa_hz,rows{end}.candidate_C_APC,rows{end}.trial_seconds);
  save(fullfile(d,'results','historical_candidate_endpoint.mat'),'rows','cfg','-v7');
  writetable(struct2table([rows{:}]),fullfile(d,'results','historical_candidate_endpoint.csv'));
 end
end
fprintf('JUNE STEP4 CANDIDATE COMPLETE\n');
end
