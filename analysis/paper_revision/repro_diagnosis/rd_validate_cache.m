function rd_validate_cache(d)
cd(d);addpath(fullfile(d,'sources'),'-begin');maxNumCompThreads(1);
source=@rd_sparsity_source;cfg=source('profile','full');rng(cfg.random_seed,'twister');
options=struct('fA',cfg.broad_fa_band_hz,'epoch',[-.6 .6], 'decomposition','fft_peak','metric',cfg.metric,'diagm',false,'surrogates',false,'num_perm',0,'numPhaseBins',18);
rows={};
for ir=1:3
 [signal,time]=source('generate',cfg,1);input=struct('data',signal,'time',time);
 tic;[a,r1]=rd_apc_instrumented(input,options);t1=toc;
 tic;[b,r2]=rd_apc_cached(input,options);t2=toc;
 assert(isequaln(a,b)&&isequal(r1,r2),'Cache changes numerical output');
 rows{end+1}=struct('repeat_index',ir,'entire_exported_struct_exactly_equal',true,'route_exactly_equal',true,'uncached_seconds',t1,'cached_seconds',t2); %#ok<AGROW>
 fprintf('CACHE VERIFY %d: entire struct exact; uncached %.2fs cached %.2fs\n',ir,t1,t2);
end
writetable(struct2table([rows{:}]),fullfile(d,'results','cache_validation.csv'));
end
