function results = run_apc_ec013_lfp_apc_vs_pac_analysis(baseResultsFile, comparisonMatFile)
% RUN_APC_EC013_LFP_APC_VS_PAC_ANALYSIS
% Build a reviewer-facing comparison between APC and conventional PAC
% estimators on the exact same EC013 run/rest bouts.
%
% This analysis is designed to test three questions directly:
%   1) Does APC recover a physiologically interpretable theta-high-
%      frequency mode in the rodent LFP example?
%   2) Do APC strength, surrogate-normalized strength, carrier
%      frequencies, or preferred phase differ between running and rest?
%   3) Are APC carrier estimates more stable across bouts than those
%      produced by scanned PAC estimators on the same data segments?
%
% USAGE:
%   results = run_apc_ec013_lfp_apc_vs_pac_analysis
%   results = run_apc_ec013_lfp_apc_vs_pac_analysis(baseResultsFile)
%   results = run_apc_ec013_lfp_apc_vs_pac_analysis(baseResultsFile, comparisonMatFile)
%
% INPUT:
%   baseResultsFile   : MAT file created by run_apc_ec013_run_rest
%   comparisonMatFile : MAT file created by run_apc_ec013_run_rest_method_comparison
%
% OUTPUT FILES:
%   apc_ec013_lfp_apc_vs_pac_results.mat
%   apc_ec013_lfp_apc_vs_pac_state_method_summary.csv
%   apc_ec013_lfp_apc_vs_pac_within_method_tests.csv
%   apc_ec013_lfp_apc_vs_pac_apc_vs_standard_tests.csv
%   apc_ec013_lfp_apc_vs_pac_stability_summary.csv
%   apc_ec013_lfp_apc_vs_pac_summary.txt

    if nargin < 1 || isempty(baseResultsFile)
        baseResultsFile = fullfile(fileparts(mfilename('fullpath')), 'apc_ec013_run_rest_results.mat');
    end
    if nargin < 2 || isempty(comparisonMatFile)
        comparisonMatFile = fullfile(fileparts(mfilename('fullpath')), ...
            'apc_ec013_run_rest_method_comparison_results.mat');
    end

    if ~exist(baseResultsFile, 'file')
        error('Base run/rest APC results file not found: %s', baseResultsFile);
    end

    if exist(comparisonMatFile, 'file')
        S = load(comparisonMatFile, 'results');
        if ~isfield(S, 'results')
            error('Comparison MAT file does not contain a results struct: %s', comparisonMatFile);
        end
        comparison = S.results;
    else
        comparison = run_apc_ec013_run_rest_method_comparison(baseResultsFile);
        comparisonMatFile = comparison.output_mat;
    end

    Sbase = load(baseResultsFile, 'results');
    if ~isfield(Sbase, 'results')
        error('Base results MAT file does not contain a results struct: %s', baseResultsFile);
    end
    base = Sbase.results;

    boutTable = comparison.bout_table;
    boutTable = boutTable(boutTable.valid == 1, :);
    boutTable.state = string(boutTable.state);
    boutTable.method = string(boutTable.method);

    stateMethodSummary = local_build_state_method_summary(boutTable);
    withinMethodTests = local_build_within_method_tests(boutTable);
    stabilityTable = local_build_stability_table(boutTable);
    apcVsStandardTests = local_build_apc_vs_standard_tests(boutTable);

    results = struct();
    results.base_results_file = baseResultsFile;
    results.comparison_results_file = comparisonMatFile;
    results.recording = base.recording;
    results.bout_table = boutTable;
    results.state_method_summary = stateMethodSummary;
    results.within_method_tests = withinMethodTests;
    results.stability_table = stabilityTable;
    results.apc_vs_standard_tests = apcVsStandardTests;

    outDir = fileparts(mfilename('fullpath'));
    outMat = fullfile(outDir, 'apc_ec013_lfp_apc_vs_pac_results.mat');
    outSummaryCsv = fullfile(outDir, 'apc_ec013_lfp_apc_vs_pac_state_method_summary.csv');
    outWithinCsv = fullfile(outDir, 'apc_ec013_lfp_apc_vs_pac_within_method_tests.csv');
    outApcVsCsv = fullfile(outDir, 'apc_ec013_lfp_apc_vs_pac_apc_vs_standard_tests.csv');
    outStabilityCsv = fullfile(outDir, 'apc_ec013_lfp_apc_vs_pac_stability_summary.csv');
    outTxt = fullfile(outDir, 'apc_ec013_lfp_apc_vs_pac_summary.txt');

    save(outMat, 'results', '-v7.3');
    writetable(stateMethodSummary, outSummaryCsv);
    writetable(withinMethodTests, outWithinCsv);
    writetable(apcVsStandardTests, outApcVsCsv);
    writetable(stabilityTable, outStabilityCsv);
    local_write_text_summary(outTxt, base, stateMethodSummary, withinMethodTests, apcVsStandardTests);

    results.output_mat = outMat;
    results.output_summary_csv = outSummaryCsv;
    results.output_within_method_csv = outWithinCsv;
    results.output_apc_vs_standard_csv = outApcVsCsv;
    results.output_stability_csv = outStabilityCsv;
    results.output_txt = outTxt;

    fprintf('\nSaved EC013 APC-vs-standard-PAC analysis outputs:\n');
    fprintf('  %s\n', outMat);
    fprintf('  %s\n', outSummaryCsv);
    fprintf('  %s\n', outWithinCsv);
    fprintf('  %s\n', outApcVsCsv);
    fprintf('  %s\n', outStabilityCsv);
    fprintf('  %s\n', outTxt);
end


function T = local_build_state_method_summary(boutTable)
    methods = unique(boutTable.method, 'stable');
    states = unique(boutTable.state, 'stable');
    rows = cell(0, 21);

    for iMethod = 1:numel(methods)
        for iState = 1:numel(states)
            sub = boutTable(boutTable.method == methods(iMethod) & boutTable.state == states(iState), :);
            if isempty(sub)
                continue;
            end

            prefDeg = sub.preferred_phase_deg;
            w = double(sub.duration_s);
            w = w(:);
            [circMeanDeg, circR] = local_circular_mean_deg(prefDeg);
            rows(end + 1, :) = { ...
                string(methods(iMethod)), ...
                string(states(iState)), ...
                height(sub), ...
                mean(sub.duration_s, 'omitnan'), ...
                median(sub.duration_s, 'omitnan'), ...
                mean(sub.score_raw, 'omitnan'), ...
                median(sub.score_raw, 'omitnan'), ...
                local_weighted_mean(sub.score_raw, w), ...
                mean(sub.score_z, 'omitnan'), ...
                median(sub.score_z, 'omitnan'), ...
                local_weighted_mean(sub.score_z, w), ...
                mean(sub.phase_frequency_hz, 'omitnan'), ...
                median(sub.phase_frequency_hz, 'omitnan'), ...
                local_weighted_mean(sub.phase_frequency_hz, w), ...
                mean(sub.amplitude_frequency_hz, 'omitnan'), ...
                median(sub.amplitude_frequency_hz, 'omitnan'), ...
                local_weighted_mean(sub.amplitude_frequency_hz, w), ...
                circMeanDeg, ...
                circR, ...
                sum(sub.score_z > 1.96, 'omitnan'), ...
                mean(sub.score_z > 1.96, 'omitnan')}; %#ok<AGROW>
        end
    end

    T = cell2table(rows, 'VariableNames', { ...
        'method', 'state', 'n_bouts', ...
        'duration_mean_s', 'duration_median_s', ...
        'score_raw_mean', 'score_raw_median', 'score_raw_duration_weighted_mean', ...
        'score_z_mean', 'score_z_median', 'score_z_duration_weighted_mean', ...
        'fp_mean_hz', 'fp_median_hz', 'fp_duration_weighted_mean_hz', ...
        'fa_mean_hz', 'fa_median_hz', 'fa_duration_weighted_mean_hz', ...
        'preferred_phase_circmean_deg', 'preferred_phase_resultant_r', ...
        'n_bouts_z_gt_1p96', 'prop_bouts_z_gt_1p96'});
end


function T = local_build_within_method_tests(boutTable)
    methods = unique(boutTable.method, 'stable');
    metricNames = {'score_raw', 'score_z', 'phase_frequency_hz', 'amplitude_frequency_hz'};
    prettyNames = {'PAC strength', 'PAC z-score', 'fP', 'fA'};
    rows = cell(0, 18);

    for iMethod = 1:numel(methods)
        runSub = boutTable(boutTable.method == methods(iMethod) & boutTable.state == "run", :);
        restSub = boutTable(boutTable.method == methods(iMethod) & boutTable.state == "rest", :);

        for iMetric = 1:numel(metricNames)
            x = double(runSub.(metricNames{iMetric}));
            y = double(restSub.(metricNames{iMetric}));
            S = local_mann_whitney_summary(x, y);
            rows(end + 1, :) = { ...
                string(methods(iMethod)), ...
                string(prettyNames{iMetric}), ...
                "Mann-Whitney U", ...
                numel(x), ...
                numel(y), ...
                mean(x, 'omitnan'), ...
                median(x, 'omitnan'), ...
                mean(y, 'omitnan'), ...
                median(y, 'omitnan'), ...
                S.diff_mean, ...
                S.ci_low, ...
                S.ci_high, ...
                S.U_run, ...
                S.z_approx, ...
                S.p_two_sided, ...
                S.rank_biserial, ...
                NaN, ...
                NaN}; %#ok<AGROW>
        end

        phaseRun = double(runSub.preferred_phase_deg);
        phaseRest = double(restSub.preferred_phase_deg);
        P = local_circular_group_test(phaseRun, phaseRest, 10000, 42);
        rows(end + 1, :) = { ...
            string(methods(iMethod)), ...
            "Preferred phase", ...
            "Circular permutation", ...
            numel(phaseRun), ...
            numel(phaseRest), ...
            local_circular_mean_deg(phaseRun), ...
            NaN, ...
            local_circular_mean_deg(phaseRest), ...
            NaN, ...
            P.phase_diff_deg, ...
            P.ci_low_deg, ...
            P.ci_high_deg, ...
            NaN, ...
            NaN, ...
            P.p_two_sided, ...
            P.phase_diff_deg, ...
            P.run_resultant_r, ...
            P.rest_resultant_r}; %#ok<AGROW>
    end

    T = cell2table(rows, 'VariableNames', { ...
        'method', 'metric', 'test', ...
        'n_run', 'n_rest', ...
        'run_mean_or_circmean', 'run_median', ...
        'rest_mean_or_circmean', 'rest_median', ...
        'run_minus_rest_effect', 'ci_low', 'ci_high', ...
        'test_statistic', 'z_approx', 'p_two_sided', 'effect_size', ...
        'run_resultant_r', 'rest_resultant_r'});
end


function T = local_build_stability_table(boutTable)
    methods = unique(boutTable.method, 'stable');
    states = unique(boutTable.state, 'stable');
    rows = cell(0, 10);

    for iMethod = 1:numel(methods)
        for iState = 1:numel(states)
            sub = boutTable(boutTable.method == methods(iMethod) & boutTable.state == states(iState), :);
            fpVals = double(sub.phase_frequency_hz);
            faVals = double(sub.amplitude_frequency_hz);
            fpCenter = median(fpVals, 'omitnan');
            faCenter = median(faVals, 'omitnan');
            fpAbsDev = abs(fpVals - fpCenter);
            faAbsDev = abs(faVals - faCenter);

            rows(end + 1, :) = { ...
                string(methods(iMethod)), ...
                string(states(iState)), ...
                numel(fpVals), ...
                fpCenter, ...
                faCenter, ...
                median(fpAbsDev, 'omitnan'), ...
                mean(fpAbsDev, 'omitnan'), ...
                median(faAbsDev, 'omitnan'), ...
                mean(faAbsDev, 'omitnan'), ...
                mean(double(sub.score_z > 1.96), 'omitnan')}; %#ok<AGROW>
        end
    end

    T = cell2table(rows, 'VariableNames', { ...
        'method', 'state', 'n_bouts', ...
        'fp_state_median_hz', 'fa_state_median_hz', ...
        'fp_abs_dev_median_hz', 'fp_abs_dev_mean_hz', ...
        'fa_abs_dev_median_hz', 'fa_abs_dev_mean_hz', ...
        'prop_z_gt_1p96'});
end


function T = local_build_apc_vs_standard_tests(boutTable)
    states = unique(boutTable.state, 'stable');
    comparators = setdiff(unique(boutTable.method, 'stable'), "APC", 'stable');
    metricDefs = { ...
        'score_raw', 'PAC strength', false; ...
        'score_z', 'PAC z-score', false; ...
        'phase_frequency_hz', 'fP absolute deviation', true; ...
        'amplitude_frequency_hz', 'fA absolute deviation', true};

    rows = cell(0, 14);
    for iState = 1:numel(states)
        apcSub = local_sort_bouts(boutTable(boutTable.method == "APC" & boutTable.state == states(iState), :));
        for iComp = 1:numel(comparators)
            cmpSub = local_sort_bouts(boutTable(boutTable.method == comparators(iComp) & boutTable.state == states(iState), :));
            nPairs = min(height(apcSub), height(cmpSub));
            if nPairs == 0
                continue;
            end
            apcSub = apcSub(1:nPairs, :);
            cmpSub = cmpSub(1:nPairs, :);

            for iMetric = 1:size(metricDefs, 1)
                fieldName = metricDefs{iMetric, 1};
                metricLabel = metricDefs{iMetric, 2};
                useAbsDev = metricDefs{iMetric, 3};

                x = double(apcSub.(fieldName));
                y = double(cmpSub.(fieldName));
                if useAbsDev
                    x = abs(x - median(x, 'omitnan'));
                    y = abs(y - median(y, 'omitnan'));
                end

                P = local_paired_permutation_summary(x, y, 10000, 99);
                rows(end + 1, :) = { ...
                    string(states(iState)), ...
                    "APC", ...
                    string(comparators(iComp)), ...
                    string(metricLabel), ...
                    nPairs, ...
                    mean(x, 'omitnan'), ...
                    median(x, 'omitnan'), ...
                    mean(y, 'omitnan'), ...
                    median(y, 'omitnan'), ...
                    P.diff_mean, ...
                    P.ci_low, ...
                    P.ci_high, ...
                    P.p_two_sided, ...
                    P.zero_or_better_prop}; %#ok<AGROW>
            end
        end
    end

    T = cell2table(rows, 'VariableNames', { ...
        'state', 'reference_method', 'comparison_method', 'metric', ...
        'n_pairs', ...
        'ref_mean', 'ref_median', ...
        'cmp_mean', 'cmp_median', ...
        'ref_minus_cmp_mean', 'ci_low', 'ci_high', ...
        'p_two_sided', 'prop_pairs_ref_lte_cmp'});
end


function T = local_sort_bouts(T)
    [~, idx] = sort(T.bout_index);
    T = T(idx, :);
end


function S = local_mann_whitney_summary(x, y)
    x = x(isfinite(x));
    y = y(isfinite(y));
    if isempty(x) || isempty(y)
        S = local_empty_test_summary();
        return;
    end

    allVals = [x(:); y(:)];
    ranks = local_tiedrank(allVals);
    n1 = numel(x);
    n2 = numel(y);
    r1 = sum(ranks(1:n1));
    u1 = r1 - n1 * (n1 + 1) / 2;
    uSmall = min(u1, n1 * n2 - u1);

    tieCounts = local_tie_counts(allVals);
    n = n1 + n2;
    tieTerm = sum(tieCounts .^ 3 - tieCounts);
    varU = (n1 * n2 / 12) * ((n + 1) - tieTerm / max(n * (n - 1), 1));
    muU = n1 * n2 / 2;
    if varU > 0
        cc = 0.5 * sign(uSmall - muU);
        z = (uSmall - muU - cc) / sqrt(varU);
        p = 2 * (1 - local_normcdf(abs(z)));
    else
        z = NaN;
        p = NaN;
    end

    ci = local_bootstrap_diff_ci(x, y, false, 10000, 11);
    S = struct();
    S.U_run = u1;
    S.z_approx = z;
    S.p_two_sided = p;
    S.rank_biserial = (2 * u1) / max(n1 * n2, 1) - 1;
    S.diff_mean = mean(x, 'omitnan') - mean(y, 'omitnan');
    S.ci_low = ci(1);
    S.ci_high = ci(2);
end


function S = local_paired_permutation_summary(x, y, nPerm, seed)
    keep = isfinite(x) & isfinite(y);
    x = x(keep);
    y = y(keep);
    if isempty(x)
        S = struct('diff_mean', NaN, 'ci_low', NaN, 'ci_high', NaN, ...
            'p_two_sided', NaN, 'zero_or_better_prop', NaN);
        return;
    end

    d = x(:) - y(:);
    obs = mean(d, 'omitnan');
    rng(seed, 'twister');
    permStat = nan(nPerm, 1);
    for iPerm = 1:nPerm
        signFlip = (randi([0 1], size(d)) * 2) - 1;
        permStat(iPerm) = mean(d .* signFlip, 'omitnan');
    end

    S = struct();
    S.diff_mean = obs;
    S.p_two_sided = mean(abs(permStat) >= abs(obs));
    ci = local_bootstrap_diff_ci(x, y, true, 10000, seed + 1);
    S.ci_low = ci(1);
    S.ci_high = ci(2);
    S.zero_or_better_prop = mean(d <= 0, 'omitnan');
end


function ci = local_bootstrap_diff_ci(x, y, pairedFlag, nBoot, seed)
    rng(seed, 'twister');
    if pairedFlag
        n = numel(x);
        bootStat = nan(nBoot, 1);
        for iBoot = 1:nBoot
            idx = randi(n, [n, 1]);
            bootStat(iBoot) = mean(x(idx) - y(idx), 'omitnan');
        end
    else
        nX = numel(x);
        nY = numel(y);
        bootStat = nan(nBoot, 1);
        for iBoot = 1:nBoot
            idxX = randi(nX, [nX, 1]);
            idxY = randi(nY, [nY, 1]);
            bootStat(iBoot) = mean(x(idxX), 'omitnan') - mean(y(idxY), 'omitnan');
        end
    end
    ci = local_percentile(bootStat, [2.5 97.5]);
end


function out = local_empty_test_summary()
    out = struct('U_run', NaN, 'z_approx', NaN, 'p_two_sided', NaN, ...
        'rank_biserial', NaN, 'diff_mean', NaN, 'ci_low', NaN, 'ci_high', NaN);
end


function [muDeg, r] = local_circular_mean_deg(thetaDeg)
    thetaDeg = thetaDeg(isfinite(thetaDeg));
    if isempty(thetaDeg)
        muDeg = NaN;
        r = NaN;
        return;
    end
    z = mean(exp(1i * deg2rad(thetaDeg)));
    muDeg = local_wrap_to_180(rad2deg(angle(z)));
    r = abs(z);
end


function S = local_circular_group_test(thetaRunDeg, thetaRestDeg, nPerm, seed)
    thetaRunDeg = thetaRunDeg(isfinite(thetaRunDeg));
    thetaRestDeg = thetaRestDeg(isfinite(thetaRestDeg));
    [muRun, rRun] = local_circular_mean_deg(thetaRunDeg);
    [muRest, rRest] = local_circular_mean_deg(thetaRestDeg);
    obsDiff = local_circular_distance_deg(muRun, muRest);

    allTheta = [thetaRunDeg(:); thetaRestDeg(:)];
    nRun = numel(thetaRunDeg);
    rng(seed, 'twister');
    permDiff = nan(nPerm, 1);
    for iPerm = 1:nPerm
        idx = randperm(numel(allTheta));
        permRun = allTheta(idx(1:nRun));
        permRest = allTheta(idx(nRun + 1:end));
        mu1 = local_circular_mean_deg(permRun);
        mu2 = local_circular_mean_deg(permRest);
        permDiff(iPerm) = local_circular_distance_deg(mu1, mu2);
    end

    bootDiff = nan(nPerm, 1);
    for iBoot = 1:nPerm
        idxRun = randi(nRun, [nRun, 1]);
        idxRest = randi(numel(thetaRestDeg), [numel(thetaRestDeg), 1]);
        mu1 = local_circular_mean_deg(thetaRunDeg(idxRun));
        mu2 = local_circular_mean_deg(thetaRestDeg(idxRest));
        bootDiff(iBoot) = local_circular_distance_deg(mu1, mu2);
    end

    S = struct();
    S.phase_diff_deg = obsDiff;
    S.p_two_sided = mean(permDiff >= obsDiff);
    S.ci_low_deg = local_percentile(bootDiff, 2.5);
    S.ci_high_deg = local_percentile(bootDiff, 97.5);
    S.run_resultant_r = rRun;
    S.rest_resultant_r = rRest;
end


function d = local_circular_distance_deg(aDeg, bDeg)
    d = abs(local_wrap_to_180(aDeg - bDeg));
end


function local_write_text_summary(outTxt, base, summaryTbl, withinTbl, apcVsTbl)
    lines = {};
    lines{end + 1} = sprintf('EC013 rodent LFP APC-versus-standard-PAC analysis | recording %s', base.recording);
    lines{end + 1} = sprintf('Analysis window: %.3f to %.3f s', base.analysis_window_s(1), base.analysis_window_s(2));
    lines{end + 1} = sprintf('Run bouts: %d | Rest bouts: %d', height(base.run.bouts), height(base.rest.bouts));
    lines{end + 1} = 'Primary inferential unit: bout (one observation per bout).';
    lines{end + 1} = 'Unequal bout durations are retained in the dataset; duration-weighted state means are also reported for sensitivity.';
    lines{end + 1} = '';

    lines{end + 1} = 'State/method summary:';
    for iRow = 1:height(summaryTbl)
        lines{end + 1} = sprintf(['  %s | %s | n=%d | raw PAC median=%.6f | zPAC median=%.3f | ' ...
            'fP median=%.3f Hz | fA median=%.1f Hz | pref=%.1f deg | R=%.3f | weighted zPAC=%.3f'], ...
            summaryTbl.method(iRow), summaryTbl.state(iRow), summaryTbl.n_bouts(iRow), ...
            summaryTbl.score_raw_median(iRow), summaryTbl.score_z_median(iRow), ...
            summaryTbl.fp_median_hz(iRow), summaryTbl.fa_median_hz(iRow), ...
            summaryTbl.preferred_phase_circmean_deg(iRow), summaryTbl.preferred_phase_resultant_r(iRow), ...
            summaryTbl.score_z_duration_weighted_mean(iRow));
    end
    lines{end + 1} = '';

    lines{end + 1} = 'Within-method run-vs-rest tests:';
    for iRow = 1:height(withinTbl)
        if withinTbl.metric(iRow) == "Preferred phase"
            lines{end + 1} = sprintf('  %s | %s | diff=%.1f deg | p=%.4g | Rrun=%.3f | Rrest=%.3f', ...
                withinTbl.method(iRow), withinTbl.metric(iRow), withinTbl.run_minus_rest_effect(iRow), ...
                withinTbl.p_two_sided(iRow), withinTbl.run_resultant_r(iRow), withinTbl.rest_resultant_r(iRow));
        else
            lines{end + 1} = sprintf('  %s | %s | run median=%.6g | rest median=%.6g | p=%.4g | effect=%.4f | 95%% CI=[%.6g, %.6g]', ...
                withinTbl.method(iRow), withinTbl.metric(iRow), withinTbl.run_median(iRow), ...
                withinTbl.rest_median(iRow), withinTbl.p_two_sided(iRow), ...
                withinTbl.effect_size(iRow), withinTbl.ci_low(iRow), withinTbl.ci_high(iRow));
        end
    end
    lines{end + 1} = '';

    lines{end + 1} = 'APC versus scanned PAC on matched bouts:';
    for iRow = 1:height(apcVsTbl)
        lines{end + 1} = sprintf('  %s | %s vs %s | %s | delta=%.6g | p=%.4g | 95%% CI=[%.6g, %.6g]', ...
            apcVsTbl.state(iRow), apcVsTbl.reference_method(iRow), apcVsTbl.comparison_method(iRow), ...
            apcVsTbl.metric(iRow), apcVsTbl.ref_minus_cmp_mean(iRow), ...
            apcVsTbl.p_two_sided(iRow), apcVsTbl.ci_low(iRow), apcVsTbl.ci_high(iRow));
    end

    fid = fopen(outTxt, 'w');
    cleanupObj = onCleanup(@() fclose(fid));
    for iLine = 1:numel(lines)
        fprintf(fid, '%s\n', lines{iLine});
    end
end


function mu = local_weighted_mean(x, w)
    x = double(x(:));
    w = double(w(:));
    keep = isfinite(x) & isfinite(w) & (w > 0);
    if ~any(keep)
        mu = NaN;
        return;
    end
    x = x(keep);
    w = w(keep);
    mu = sum(w .* x) / sum(w);
end


function ranks = local_tiedrank(x)
    x = double(x(:));
    [sortedX, order] = sort(x);
    ranksSorted = zeros(size(sortedX));
    iStart = 1;
    while iStart <= numel(sortedX)
        iStop = iStart;
        while iStop < numel(sortedX) && sortedX(iStop + 1) == sortedX(iStart)
            iStop = iStop + 1;
        end
        ranksSorted(iStart:iStop) = mean(iStart:iStop);
        iStart = iStop + 1;
    end
    ranks = zeros(size(sortedX));
    ranks(order) = ranksSorted;
end


function counts = local_tie_counts(x)
    x = double(x(:));
    if isempty(x)
        counts = [];
        return;
    end
    sortedX = sort(x);
    counts = [];
    iStart = 1;
    while iStart <= numel(sortedX)
        iStop = iStart;
        while iStop < numel(sortedX) && sortedX(iStop + 1) == sortedX(iStart)
            iStop = iStop + 1;
        end
        counts(end + 1, 1) = iStop - iStart + 1; %#ok<AGROW>
        iStart = iStop + 1;
    end
end


function p = local_normcdf(x)
    p = 0.5 * (1 + erf(double(x) ./ sqrt(2)));
end


function q = local_percentile(x, pct)
    x = double(x(:));
    x = x(isfinite(x));
    if isempty(x)
        q = nan(size(pct));
        return;
    end
    x = sort(x);
    pct = double(pct);
    q = nan(size(pct));
    for iPct = 1:numel(pct)
        p = min(max(pct(iPct), 0), 100) / 100;
        if numel(x) == 1
            q(iPct) = x;
            continue;
        end
        pos = 1 + (numel(x) - 1) * p;
        lo = floor(pos);
        hi = ceil(pos);
        if lo == hi
            q(iPct) = x(lo);
        else
            alpha = pos - lo;
            q(iPct) = (1 - alpha) * x(lo) + alpha * x(hi);
        end
    end
end


function y = local_wrap_to_180(x)
    y = mod(double(x) + 180, 360) - 180;
end
