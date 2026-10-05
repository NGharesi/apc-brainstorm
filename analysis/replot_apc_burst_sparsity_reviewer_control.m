function replot_apc_burst_sparsity_reviewer_control()
% Replot Figure 4 from saved full benchmark trials without rerunning APC.

    baseDir = fileparts(mfilename('fullpath'));
    runs = readtable(fullfile(baseDir, 'apc_burst_sparsity_runs_full.csv'));
    methods = ["APC", "MVL-scan", "KLMI-scan", "GLM-scan"];
    keepRates = sort(unique(runs.burst_keep_rate))';
    style = local_styles();

    fig = figure('Color', 'w', 'Units', 'normalized', 'Position', [0.06 0.08 0.88 0.80], ...
        'Name', 'APC burst sparsity reviewer-control main figure', 'Renderer', 'painters');
    tl = tiledlayout(fig, 2, 2, 'Padding', 'compact', 'TileSpacing', 'compact');
    tl.OuterPosition = [0.05 0.05 0.90 0.70];
    annotation(fig, 'textbox', [0.12 0.91 0.76 0.05], ...
        'String', 'Dominant-Mode Recovery as True Coupled Bursts Become Sparse', ...
        'EdgeColor', 'none', 'HorizontalAlignment', 'center', 'FontWeight', 'bold', ...
        'FontSize', 17, 'FontName', 'Helvetica');

    local_figure_legend(fig, methods, style);

    ax1 = nexttile(tl, 1);
    local_count_heatmap(ax1, runs, methods, keepRates, 'pair_correct', ...
        'A  Joint recovery of the true coupling pair');
    ax2 = nexttile(tl, 2);
    local_count_heatmap(ax2, runs, methods, keepRates, 'fa_correct', ...
        'B  Recovery of the true burst-locked f_A band');
    ax3 = nexttile(tl, 3);
    local_error_curve(ax3, runs, methods, keepRates, 'fa_abs_error_hz', style, ...
        'C  High-frequency carrier recovery error', '|f_A error| (Hz)');
    ax4 = nexttile(tl, 4);
    local_error_curve(ax4, runs, methods, keepRates, 'fp_abs_error_hz', style, ...
        'D  Phase-carrier recovery error', '|f_P error| (Hz)');
    local_export(fig, baseDir, 'apc_burst_sparsity_benchmark_reviewer_control');
    close(fig);

    supp = figure('Color', 'w', 'Units', 'normalized', 'Position', [0.14 0.18 0.72 0.42], ...
        'Name', 'APC burst sparsity raw endpoint distributions', 'Renderer', 'painters');
    stl = tiledlayout(supp, 1, 2, 'Padding', 'compact', 'TileSpacing', 'compact');
    stl.OuterPosition = [0.05 0.08 0.92 0.80];
    annotation(supp, 'textbox', [0.10 0.89 0.80 0.07], ...
        'String', 'Supplementary per-trial endpoint distributions', 'EdgeColor', 'none', ...
        'HorizontalAlignment', 'center', 'FontWeight', 'bold', 'FontSize', 16, 'FontName', 'Helvetica');
    for i = 1:2
        ax = nexttile(stl, i);
        rate = [min(keepRates), max(keepRates)]; rate = rate(i);
        local_raw_endpoint(ax, runs(abs(runs.burst_keep_rate-rate) < 1e-9, :), methods, style);
        title(ax, sprintf('%c  |f_A error| at keep rate %.2f (n = 25/method)', 'D'+i, rate), ...
            'FontWeight', 'bold', 'FontSize', 13);
        ylabel(ax, '|f_A error| (Hz)'); xlabel(ax, 'Method'); box(ax, 'off');
    end
    local_export(supp, baseDir, 'apc_burst_sparsity_endpoint_rawpoints_reviewer_control');
    close(supp);
end

function local_figure_legend(fig, methods, style)
    y = 0.835;
    xStarts = [0.27 0.43 0.59 0.75];
    for m = 1:numel(methods)
        key = local_key(methods(m));
        annotation(fig, 'line', [xStarts(m) xStarts(m)+0.035], [y y], ...
            'Color', style.(key).color, 'LineWidth', 1.8);
        annotation(fig, 'textbox', [xStarts(m)+0.039 y-0.015 0.12 0.035], ...
            'String', char(methods(m)), 'EdgeColor', 'none', 'FontName', 'Helvetica', ...
            'FontSize', 12, 'VerticalAlignment', 'middle');
    end
end

function local_count_heatmap(ax, runs, methods, rates, field, titleText)
    counts = zeros(numel(methods), numel(rates)); n = zeros(size(counts));
    for m = 1:numel(methods)
        for r = 1:numel(rates)
            sub = runs(runs.method == methods(m) & abs(runs.burst_keep_rate-rates(r)) < 1e-9, :);
            counts(m,r) = sum(sub.(field) ~= 0); n(m,r) = height(sub);
        end
    end
    imagesc(ax, counts ./ n, [0 1]);
    colormap(ax, [linspace(0.94,0.84,128)', linspace(0.96,0.37,128)', linspace(0.94,0.00,128)']);
    cb = colorbar(ax, 'Ticks', 0:0.2:1); ylabel(cb, 'Recovery proportion');
    xticks(ax, 1:numel(rates)); xticklabels(ax, compose('%.2f', rates));
    yticks(ax, 1:numel(methods)); yticklabels(ax, methods);
    xlabel(ax, 'True burst keep rate'); title(ax, titleText, 'FontWeight', 'bold', 'FontSize', 13);
    for m = 1:numel(methods), for r = 1:numel(rates)
        labelColor = [0 0 0];
        if counts(m,r)/n(m,r) > 0.62, labelColor = [1 1 1]; end
        text(ax, r, m, sprintf('%d/%d', counts(m,r), n(m,r)), 'HorizontalAlignment', 'center', ...
            'FontWeight', 'bold', 'Color', labelColor, 'FontSize', 11);
    end, end
    set(ax, 'FontName', 'Helvetica', 'FontSize', 11, 'LineWidth', 1.0); box(ax, 'off');
end

function local_error_curve(ax, runs, methods, rates, field, style, titleText, yLabel)
    hold(ax, 'on'); rng(20261004, 'twister'); floorVal = 0.05;
    for m = 1:numel(methods)
        y = nan(size(rates)); lo = y; hi = y;
        for r = 1:numel(rates)
            v = runs.(field)(runs.method == methods(m) & abs(runs.burst_keep_rate-rates(r)) < 1e-9);
            y(r) = mean(v); boot = mean(v(randi(numel(v), 10000, numel(v))), 2);
            ci = prctile(boot, [2.5 97.5]); lo(r) = ci(1); hi(r) = ci(2);
        end
        key = local_key(methods(m)); yp = max(y, floorVal);
        errorbar(ax, rates, yp, max(yp-lo,0), max(hi-yp,0), 'Color', style.(key).color, ...
            'LineStyle', '-', 'Marker', style.(key).marker, 'LineWidth', 1.6, 'MarkerSize', 7, ...
            'CapSize', 4, 'DisplayName', char(methods(m)));
    end
    set(ax, 'YScale', 'log', 'FontName', 'Helvetica', 'FontSize', 12, 'LineWidth', 1.1);
    xlim(ax, [min(rates) max(rates)]); xlabel(ax, 'True burst keep rate'); ylabel(ax, yLabel);
    title(ax, titleText, 'FontWeight', 'bold', 'FontSize', 13); box(ax, 'off');
end

function local_raw_endpoint(ax, sub, methods, style)
    hold(ax, 'on'); rng(20261004, 'twister');
    for m = 1:numel(methods)
        vals = sub.fa_abs_error_hz(sub.method == methods(m)); key = local_key(methods(m));
        x = m + 0.18*(rand(size(vals))-0.5);
        scatter(ax, x, vals, 28, style.(key).color, 'filled', 'MarkerFaceAlpha', 0.65, 'MarkerEdgeColor', 'none');
        q = prctile(vals, [25 50 75]); plot(ax, [m m], q([1 3]), 'Color', style.(key).color, 'LineWidth', 2);
        plot(ax, [m-.14 m+.14], [q(2) q(2)], 'Color', style.(key).color, 'LineWidth', 2.5);
    end
    xlim(ax, [.5 numel(methods)+.5]); xticks(ax, 1:numel(methods)); xticklabels(ax, methods);
    set(ax, 'FontName', 'Helvetica', 'FontSize', 11, 'LineWidth', 1.1); grid(ax, 'off');
end

function local_export(fig, baseDir, stem)
    exportgraphics(fig, fullfile(baseDir, [stem '.png']), 'Resolution', 300);
    exportgraphics(fig, fullfile(baseDir, [stem '.pdf']), 'ContentType', 'vector');
    savefig(fig, fullfile(baseDir, [stem '.fig']));
end

function style = local_styles()
    style.APC = struct('color',[.84 .37 0], 'marker','o');
    style.MVLscan = struct('color',[0 .45 .70], 'marker','+');
    style.KLMIscan = struct('color',[.10 .10 .10], 'marker','*');
    style.GLMscan = struct('color',[0 .62 .45], 'marker','>');
end

function key = local_key(method)
    key = char(erase(string(method), '-'));
end
