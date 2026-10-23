function rd_run_cached_all(diagnosisDir)
% Reproduce every original APC trial, recording the actual Step 4 branch.
    diagnosisDir=strrep(diagnosisDir,'/',filesep);
    rootDir=fileparts(fileparts(diagnosisDir));
    out=fullfile(diagnosisDir,'results');
    oldPath=path;oldDirectory=pwd;oldRng=rng;
    oldThreads=maxNumCompThreads(1);
    cleanup=onCleanup(@() local_restore(oldPath,oldDirectory,oldRng,oldThreads)); %#ok<NASGU>
    cd(diagnosisDir);addpath(fullfile(diagnosisDir,'sources'),'-begin');
    assert(strcmp(which('bst_apc'),fullfile(diagnosisDir,'sources','bst_apc.m')));
    assert(strcmp(which('calc_MI_all_methods'),fullfile(diagnosisDir,'sources','calc_MI_all_methods.m')));
    diary(fullfile(out,'progress_cached.log'));logCleanup=onCleanup(@() diary('off')); %#ok<NASGU>
    started=tic;
    meta=struct('status','RUNNING','started_local',char(datetime('now','Format','yyyy-MM-dd HH:mm:ss')), ...
        'matlab_version',version,'release',version('-release'),'computation_threads',1, ...
        'previous_thread_setting',oldThreads,'baseline_commit','82f7559fd570133bd05ec0a583299a50613ffc2a', ...
        'baseline_source',which('bst_apc'),'instrumented_source',which('rd_apc_cached'));
    local_json(fullfile(out,'runtime_cached.json'),meta);
    fprintf('Diagnosis start: %s; MATLAB %s; computation threads 1\n',meta.started_local,version);
    local_result_metadata(rootDir,out);
    prior=readtable(fullfile(rootDir,'revision_checks','results','reproduction_completed_trials.csv'),'TextType','string');
    prior=prior(prior.method=="APC",:);
    for benchmark=["sparsity","distractor"]
        if benchmark=="sparsity"
            source=@rd_sparsity_source;cfg=source('profile','full');levels=cfg.burst_keep_rates;
        else
            source=@rd_distractor_source;cfg=source('profile','reviewer_control');levels=cfg.distractor_scale_values;
        end
        assert(cfg.n_repeats==25 && cfg.random_seed==20260618);
        rng(cfg.random_seed,'twister');rows={};signalBank={};
        previousRows={};
        checkpointFile=fullfile(out,char('checkpoint_'+benchmark+'.mat'));
        if isfile(checkpointFile)
            checkpoint=load(checkpointFile,'rows');previousRows=checkpoint.rows;
            fprintf('RESUME %s with %d completed uncached trials; regenerate all inputs in original order.\n',benchmark,numel(previousRows));
        end
        fprintf('BEGIN %s: %d conditions, 25 repeats each\n',benchmark,numel(levels));
        for il=1:numel(levels)
            level=levels(il);
            for ir=1:cfg.n_repeats
                [signal,time]=source('generate',cfg,level);
                signalBank{end+1}=signal; %#ok<AGROW>
                trialOrdinal=(il-1)*cfg.n_repeats+ir;
                if trialOrdinal<=numel(previousRows)
                    rows{end+1}=previousRows{trialOrdinal};
                    continue;
                end
                options=struct('fA',cfg.broad_fa_band_hz,'epoch',[-.6 .6], ...
                    'decomposition','fft_peak','metric',cfg.metric,'diagm',false, ...
                    'surrogates',false,'num_perm',0,'numPhaseBins',18);
                input=struct('data',signal,'time',time);
                beforeAnalysis=rng;trialStart=tic;
                [result,route]=rd_apc_cached(input,options);
                trialSeconds=toc(trialStart);
                assert(isequal(beforeAnalysis,rng),'repro_diagnosis:RNG','APC unexpectedly consumed random numbers.');
                neutralTest=false;
                if trialOrdinal==numel(previousRows)+1 || (il==numel(levels) && ir==cfg.n_repeats)
                    original=bst_apc(input,options);
                    assert(isequaln(original,result),'repro_diagnosis:Instrumentation','Instrumentation changed exported output.');
                    neutralTest=true;
                    fprintf('Instrumentation matches unmodified exported struct exactly (%s first trial).\n',benchmark);
                end
                fp=double(result.phase_frequency_hz.Value(1));fa=double(result.amplitude_frequency_hz.Value(1));
                coupling=double(result.pac_strength.Value(1));status=double(result.status_code.Value(1));
                q=prior(prior.benchmark==benchmark & abs(prior.level-level)<1e-10 & prior.repeat_index==ir,:);
                priorVerified=false;
                if height(q)==1
                    assert(abs(q.recovered_fp_hz-fp)<1e-7 && abs(q.recovered_fa_hz-fa)<1e-7 && abs(q.score-coupling)<1e-12, ...
                        'repro_diagnosis:PriorMismatch','Instrumented output differs from prior preserved-code reproduction.');
                    priorVerified=true;
                end
                rows{end+1}=struct('benchmark',benchmark,'level',level,'repeat_index',ir, ...
                    'reproduced_fp_hz',fp,'reproduced_fa_hz',fa,'reproduced_C_APC',coupling, ...
                    'status_code',status,'selection_route',route(1),'trial_seconds',trialSeconds, ...
                    'rng_unchanged_during_analysis',true,'instrumentation_neutrality_test',neutralTest, ...
                    'prior_reproduction_verified',priorVerified, ...
                    'baseline_commit',"82f7559fd570133bd05ec0a583299a50613ffc2a"); %#ok<AGROW>
                if mod(ir,5)==0 || ir==1
                    fprintf('%s level %.2f repeat %d/25: fP %.8f fA %.2f; %s; %.2fs trial; %.1fs total\n', ...
                        benchmark,level,ir,fp,fa,route(1),trialSeconds,toc(started));
                end
                if mod(ir,5)==0 || ir==25
                    T=struct2table([rows{:}]);
                    writetable(T,fullfile(out,char('observed_apc_'+benchmark+'.csv')));
                    checkpointRng=rng; %#ok<NASGU>
                    save(fullfile(out,char('checkpoint_'+benchmark+'.mat')),'cfg','rows','il','ir','checkpointRng','-v7');
                end
            end
            fprintf('COMPLETE %s level %.2f (%d total trials)\n',benchmark,level,numel(rows));
        end
        save(fullfile(out,char('generated_inputs_'+benchmark+'.mat')),'signalBank','cfg','levels','-v7');
    end
    meta.status='COMPLETE';meta.elapsed_seconds=toc(started);
    meta.completed_local=char(datetime('now','Format','yyyy-MM-dd HH:mm:ss'));
    local_json(fullfile(out,'runtime_cached.json'),meta);
    fprintf('DIAGNOSIS REPRODUCTION COMPLETE: 350 trials in %.1fs\n',meta.elapsed_seconds);
end

function local_result_metadata(rootDir,out)
    metadata=struct();
    files={'apc_burst_sparsity_benchmark_full.mat','apc_distractor_frequency_benchmark_reviewer_control.mat'};
    for i=1:numel(files)
        file=fullfile(rootDir,files{i});v=whos('-file',file);S=load(file);
        record=struct('file',file,'top_level_names',{fieldnames(S)},'cfg',S.cfg);
        inventory=struct('name',{},'class',{},'size',{},'bytes',{});
        for k=1:numel(v)
            inventory(k)=struct('name',v(k).name,'class',v(k).class,'size',v(k).size,'bytes',v(k).bytes); %#ok<AGROW>
        end
        record.inventory=inventory;
        record.runTable_variable_names=S.runTable.Properties.VariableNames;
        record.runTable_user_data=S.runTable.Properties.UserData;
        record.runTable_description=S.runTable.Properties.Description;
        record.runTable_variable_descriptions=S.runTable.Properties.VariableDescriptions;
        if i==1,metadata.sparsity=record;else,metadata.distractor=record;end
    end
    local_json(fullfile(out,'saved_mat_metadata.json'),metadata);
end

function local_json(file,value)
    f=fopen(file,'w');c=onCleanup(@() fclose(f)); %#ok<NASGU>
    fprintf(f,'%s',jsonencode(value,'PrettyPrint',true));
end
function local_restore(p,d,r,t)
    path(p);cd(d);rng(r);maxNumCompThreads(t);
end
