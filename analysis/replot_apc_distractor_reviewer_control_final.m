function replot_apc_distractor_reviewer_control_final()
% REPLOT_APC_DISTRACTOR_REVIEWER_CONTROL_FINAL
% Re-render Figure 3 from completed trial-level results. Recovery panels
% show exact counts; error panels show mean errors with percentile 95%
% bootstrap intervals rather than SEM. No simulations are rerun.

    baseDir = fileparts(mfilename('fullpath'));
    data = load(fullfile(baseDir, 'apc_distractor_frequency_benchmark_reviewer_control.mat'), ...
        'cfg', 'runTable');
    cfg = data.cfg;
    runTable = data.runTable;
    methods = ["APC", "MVL-scan", "KLMI-scan", "GLM-scan"];
    rng(20261005, 'twister');

    fig = figure('Color', 'w', 'Units', 'normalized', ...
        'Position', [0.10 0.10 0.80 0.76], 'Renderer', 'painters');
    tl = tiledlayout(fig, 2, 2, 'Padding', 'compact', 'TileSpacing', 'compact');
    tl.OuterPosition = [0.06 0.07 0.88 0.78];
    annotation(fig, 'textbox', [0.10 0.91 0.80 0.04], ...
        'String', 'Dominant-Mode Recovery with a Competing High-Frequency Distractor', ...
        'EdgeColor', 'none', 'HorizontalAlignment', 'center', ...
        'VerticalAlignment', 'middle', 'FontWeight', 'bold', ...
        'FontSize', 16, 'FontName', 'Helvetica');

    local_recovery_heatmap(nexttile(tl, 1), cfg, runTable, methods, 'pair_correct', ...
        'A  Joint recovery of the true coupling pair');
    local_recovery_heatmap(nexttile(tl, 2), cfg, runTable, methods, 'fa_correct', ...
        'B  Recovery of the true burst-locked f_A band');
    local_error_lines(nexttile(tl, 3), cfg, runTable, methods, 'fa_abs_error_hz', ...
        '|f_A error| (Hz)', 'C  High-frequency carrier recovery error');
    local_error_lines(nexttile(tl, 4), cfg, runTable, methods, 'fp_abs_error_hz', ...
        '|f_P error| (Hz)', 'D  Phase-carrier recovery error');

    outputBase = fullfile(baseDir, 'apc_distractor_frequency_benchmark_reviewer_control_final');
    exportgraphics(fig, [outputBase '.png'], 'Resolution', 300);
    exportgraphics(fig, [outputBase '.pdf'], 'ContentType', 'vector');
    savefig(fig, [outputBase '.fig']);
    close(fig);
    fprintf('Saved final Figure 3 artwork with bootstrap 95%% intervals.\n');
end

function local_recovery_heatmap(ax, cfg, runTable, methods, outcome, titleText)
    scales = cfg.distractor_scale_values;
    values = nan(numel(methods), numel(scales));
    counts = nan(size(values));
    for iMethod = 1:numel(methods)
        for iScale = 1:numel(scales)
            sub = runTable(runTable.method == methods(iMethod) & ...
                abs(runTable.distractor_scale - scales(iScale)) < 1e-9, :);
            counts(iMethod, iScale) = sum(sub.(outcome));
            values(iMethod, iScale) = mean(sub.(outcome));
        end
    end
    imagesc(ax, scales, 1:numel(methods), values);
    colormap(ax, [linspace(0.94, 0.84, 128)', linspace(0.96, 0.37, 128)', linspace(0.94, 0.00, 128)']);
    clim(ax, [0 1]); cb = colorbar(ax); cb.Label.String = 'Recovery proportion'; cb.FontSize = 10;
    for iMethod = 1:numel(methods)
        for iScale = 1:numel(scales)
            color = 'k'; if values(iMethod, iScale) >= .60, color = 'w'; end
            text(ax, scales(iScale), iMethod, sprintf('%d/%d', counts(iMethod, iScale), 25), ...
                'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', ...
                'FontName', 'Helvetica', 'FontSize', 10, 'FontWeight', 'bold', 'Color', color);
        end
    end
    set(ax, 'YDir', 'reverse', 'YTick', 1:numel(methods), 'YTickLabel', methods, ...
        'XTick', scales, 'FontName', 'Helvetica', 'FontSize', 11, 'LineWidth', 1.1);
    xlabel(ax, 'Distractor amplitude scale (relative)'); title(ax, titleText, 'FontWeight', 'bold', 'FontSize', 13); box(ax, 'off');
end

function local_error_lines(ax, cfg, runTable, methods, outcome, yLabelText, titleText)
    colors = [0.84 0.37 0.00; 0.00 0.45 0.70; 0.10 0.10 0.10; 0.00 0.62 0.45];
    markers = {'o', '+', '*', '>'}; scales = cfg.distractor_scale_values;
    hold(ax, 'on');
    for iMethod = 1:numel(methods)
        means = nan(size(scales)); lower = nan(size(scales)); upper = nan(size(scales));
        for iScale = 1:numel(scales)
            sub = runTable(runTable.method == methods(iMethod) & ...
                abs(runTable.distractor_scale - scales(iScale)) < 1e-9, :);
            values = sub.(outcome);
            means(iScale) = mean(values, 'omitnan');
            bootMeans = local_bootstrap_means(values, 10000);
            limits = prctile(bootMeans, [2.5 97.5]); lower(iScale) = limits(1); upper(iScale) = limits(2);
        end
        means(means < .05) = .05; lower(lower < .05) = .05;
        errorbar(ax, scales, means, means-lower, upper-means, ...
            'Color', colors(iMethod,:), 'Marker', markers{iMethod}, 'LineWidth', 1.5, ...
            'MarkerSize', 7, 'CapSize', 3, 'DisplayName', char(methods(iMethod)));
    end
    set(ax, 'YScale', 'log', 'FontName', 'Helvetica', 'FontSize', 11, 'LineWidth', 1.1);
    xlabel(ax, 'Distractor amplitude scale (relative)'); ylabel(ax, yLabelText);
    title(ax, titleText, 'FontWeight', 'bold', 'FontSize', 13); legend(ax, 'Location', 'southwest', 'Box', 'off', 'FontSize', 9); grid(ax, 'off'); box(ax, 'off');
end

function means = local_bootstrap_means(values, nBootstrap)
    values = values(isfinite(values)); n = numel(values);
    indices = randi(n, n, nBootstrap); means = mean(values(indices), 1);
end
