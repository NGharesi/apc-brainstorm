function cases=validation_ha_cases(seed)
% Same streams, draws, order, fields and generator as the frozen HA wrapper.
signalStream=new_stream(seed,1);frequencyStream=new_stream(seed,2);poissonStream=new_stream(seed,3);cases={};
for beta=[1 1.5 2],for amplitude=[.3 .5 .8],for duration=[2 6]
 for trial=1:25
  fp=6+19*rand(frequencyStream);fa=80+60*rand(frequencyStream);before=signalStream.State;
  [signal,nullSignal,time,parts,cfg]=v3_ha_generator(beta,amplitude,duration,fp,fa,signalStream,poissonStream);
  id=numel(cases)+1;c=struct('input_id',id,'paired_coupled_id',id,'scenario',"HA",'dataset',"coupled",'level',amplitude,'beta',beta,'duration_s',duration,'repeat_index',trial,'signal',signal,'time',time,'parts',parts,'cfg',cfg,'true_fd_hz',nan,'signal_rng_state_before',before,'signal_rng_state_after',signalStream.State,'pair_residual',parts.pair_residual);
  cases{end+1}=c;n=c;n.input_id=id+1;n.dataset="timing_null";n.signal=nullSignal;cases{end+1}=n; %#ok<AGROW>
 end
end;end;end
end
function stream=new_stream(seed,sub),stream=RandStream('mrg32k3a','Seed',seed);stream.Substream=sub;end
