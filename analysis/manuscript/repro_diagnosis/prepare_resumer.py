from pathlib import Path
D=Path(__file__).resolve().parent
s=(D/'rd_run_all.m').read_text().replace('function rd_run_all(', 'function rd_run_cached_all(',1)
s=s.replace("'progress.log'","'progress_cached.log'").replace("'runtime.json'","'runtime_cached.json'")
s=s.replace('which(\'rd_apc_instrumented\')',"which('rd_apc_cached')")
s=s.replace('        rng(cfg.random_seed,\'twister\');rows={};signalBank={};', '''        rng(cfg.random_seed,'twister');rows={};signalBank={};
        previousRows={};
        checkpointFile=fullfile(out,char('checkpoint_'+benchmark+'.mat'));
        if isfile(checkpointFile)
            checkpoint=load(checkpointFile,'rows');previousRows=checkpoint.rows;
            fprintf('RESUME %s with %d completed uncached trials; regenerate all inputs in original order.\\n',benchmark,numel(previousRows));
        end''')
s=s.replace("                options=struct('fA'", """                trialOrdinal=(il-1)*cfg.n_repeats+ir;
                if trialOrdinal<=numel(previousRows)
                    rows{end+1}=previousRows{trialOrdinal};
                    continue;
                end
                options=struct('fA'""")
s=s.replace('[result,route]=rd_apc_instrumented(input,options);','[result,route]=rd_apc_cached(input,options);')
s=s.replace('if il==1 && ir==1','if trialOrdinal==numel(previousRows)+1 || (il==numel(levels) && ir==cfg.n_repeats)')
s=s.replace("'baseline_commit',\"82f7559fd570133bd05ec0a583299a50613ffc2a\");", "'baseline_commit',\"82f7559fd570133bd05ec0a583299a50613ffc2a\");")
(D/'rd_run_cached_all.m').write_text(s)
(D/'run_cached_diagnosis.m').write_text("d=fileparts(mfilename('fullpath'));addpath(d,'-begin');rd_run_cached_all(d);\n")
print('Prepared checkpoint resumer using numerically verified filter caching.')
