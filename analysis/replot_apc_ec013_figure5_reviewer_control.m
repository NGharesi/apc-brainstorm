function replot_apc_ec013_figure5_reviewer_control()
% Replot compact Figure 5 from saved matched-bout results; no LFP reanalysis.

    baseDir = fileparts(mfilename('fullpath'));
    S = load(fullfile(baseDir, 'apc_ec013_lfp_apc_vs_pac_results.mat'), 'results');
    T = S.results.bout_table; T.method = string(T.method); T.state = string(T.state);
    summary = S.results.state_method_summary;
    methods = ["APC", "MVL-scan", "KLMI-scan", "GLM-scan"];
    states = ["run", "rest"]; colors = [0.10 0.45 0.80; 0.90 0.45 0.15];

    fig = figure('Color','w','Units','normalized','Position',[.05 .08 .88 .80], ...
        'Name','EC013 Figure 5 reviewer-control main panels','Renderer','painters');
    tl = tiledlayout(fig, 2, 3, 'Padding','compact','TileSpacing','compact');
    tl.OuterPosition = [.05 .06 .90 .80];
    annotation(fig,'textbox',[.12 .92 .76 .045], 'String', ...
        'EC013 Hippocampal LFP: APC and Standard PAC on Matched Run/Rest Bouts', ...
        'EdgeColor','none','HorizontalAlignment','center','FontWeight','bold','FontSize',16,'FontName','Helvetica');
    local_legend(fig, colors);

    ax = nexttile(tl,1); local_scatter(ax,T,methods,states,colors,'score_z','raw', ...
        'A  Coupling above within-bout surrogate null','PAC z-score');
    yline(ax,1.96,'--','Color',[.5 .5 .5],'LineWidth',1); ylim(ax,[-3 14]);
    ax = nexttile(tl,2); local_fraction(ax,summary,methods,states,colors);
    ax = nexttile(tl,3); local_scatter(ax,T,methods,states,colors,'phase_frequency_hz','raw', ...
        'C  Recovered phase carrier','f_P (Hz)'); ylim(ax,[3.5 10.5]);
    patch(ax,[.5 4.5 4.5 .5],[6 6 10 10],[.92 .97 1],'EdgeColor','none','FaceAlpha',.35); uistack(findobj(ax,'Type','patch'),'bottom');
    text(ax,.55,10.25,'theta range','FontSize',9,'Color',[.25 .35 .55]);
    ax = nexttile(tl,4); local_scatter(ax,T,methods,states,colors,'amplitude_frequency_hz','raw', ...
        'D  Recovered high-frequency carrier','f_A (Hz)'); ylim(ax,[75 150]);
    ax = nexttile(tl,5,[1 2]); local_scatter(ax,T,methods,states,colors,'phase_frequency_hz','absdev', ...
        'E  Phase-carrier stability','|f_P - state median| (Hz)'); ylim(ax,[-.05 3.6]);
    annotation(fig,'textbox',[.12 .015 .76 .028], 'String', ...
        'Points are individual bouts; horizontal bars are medians; whiskers are interquartile ranges. n = 12 run and 12 rest bouts/method.', ...
        'EdgeColor','none','HorizontalAlignment','center','FontSize',9,'Color',[.35 .35 .35]);
    local_export(fig,baseDir,'apc_ec013_figure5_reviewer_control_main'); close(fig);

    supp = figure('Color','w','Units','normalized','Position',[.18 .20 .64 .48], ...
        'Name','EC013 Figure 5 supplementary carrier stability','Renderer','painters');
    ax = axes(supp,'Position',[.11 .28 .84 .54]);
    local_scatter(ax,T,methods,states,colors,'amplitude_frequency_hz','absdev', ...
        'Supplementary Figure S5  High-frequency-carrier stability','|f_A - state median| (Hz)');
    hRun = scatter(ax,nan,nan,36,colors(1,:),'filled','DisplayName','Run');
    hRest = scatter(ax,nan,nan,36,colors(2,:),'filled','DisplayName','Rest');
    lgd = legend(ax,[hRun hRest],{'Run','Rest'},'Location','southoutside','Orientation','horizontal','Box','off');
    lgd.FontName = 'Helvetica'; lgd.FontSize = 11;
    local_export(supp,baseDir,'apc_ec013_figure5_reviewer_control_supplement'); close(supp);
end

function local_scatter(ax,T,methods,states,colors,field,mode,titleText,yText)
    hold(ax,'on'); offset=.16;
    for m=1:numel(methods), for s=1:numel(states)
        v = double(T.(field)(T.method==methods(m) & T.state==states(s)));
        if strcmp(mode,'absdev'), v=abs(v-median(v,'omitnan')); end
        x=m+(-offset+(s-1)*2*offset)+.055*linspace(-1,1,numel(v));
        scatter(ax,x,v,30,colors(s,:),'filled','MarkerFaceAlpha',.76,'MarkerEdgeColor','none');
        q=prctile(v,[25 50 75]); plot(ax,[m+(-offset+(s-1)*2*offset)-.10 m+(-offset+(s-1)*2*offset)+.10],[q(2) q(2)],'Color',colors(s,:),'LineWidth',2.2);
        plot(ax,[m+(-offset+(s-1)*2*offset) m+(-offset+(s-1)*2*offset)],q([1 3]),'Color',colors(s,:),'LineWidth',1.3);
    end,end
    set(ax,'XTick',1:numel(methods),'XTickLabel',cellstr(methods),'FontName','Helvetica','FontSize',10,'LineWidth',1.1);
    xlim(ax,[.5 4.5]); xlabel(ax,'Method'); ylabel(ax,yText); title(ax,titleText,'FontWeight','bold','FontSize',12); box(ax,'off'); grid(ax,'off');
end

function local_fraction(ax,S,methods,states,colors)
    vals=nan(2,numel(methods));
    for m=1:numel(methods), for s=1:2
        r=S(S.method==methods(m) & S.state==states(s),:); vals(s,m)=r.prop_bouts_z_gt_1p96(1);
    end,end
    bar(ax,(1:4)-.17,vals(1,:),.34,'FaceColor',colors(1,:),'EdgeColor','none'); hold(ax,'on');
    bar(ax,(1:4)+.17,vals(2,:),.34,'FaceColor',colors(2,:),'EdgeColor','none');
    set(ax,'XTick',1:4,'XTickLabel',cellstr(methods),'FontName','Helvetica','FontSize',10,'LineWidth',1.1); ylim(ax,[0 1.08]); xlim(ax,[.5 4.5]);
    xlabel(ax,'Method'); ylabel(ax,'Proportion bouts with z > 1.96'); title(ax,'B  Significant-bout fraction','FontWeight','bold','FontSize',12); box(ax,'off'); grid(ax,'off');
end

function local_legend(fig,colors)
    annotation(fig,'line',[.42 .46],[.875 .875],'Color',colors(1,:),'LineWidth',2);
    annotation(fig,'textbox',[.465 .86 .06 .03],'String','Run','EdgeColor','none','FontSize',11);
    annotation(fig,'line',[.54 .58],[.875 .875],'Color',colors(2,:),'LineWidth',2);
    annotation(fig,'textbox',[.585 .86 .06 .03],'String','Rest','EdgeColor','none','FontSize',11);
end

function local_export(fig,baseDir,stem)
    exportgraphics(fig,fullfile(baseDir,[stem '.png']),'Resolution',300);
    exportgraphics(fig,fullfile(baseDir,[stem '.pdf']),'ContentType','vector'); savefig(fig,fullfile(baseDir,[stem '.fig']));
end
