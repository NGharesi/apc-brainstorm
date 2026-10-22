function v1_make_figures(outDir,metadata)
T=readtable(fullfile(outDir,'main_trials.csv'),'TextType','string');
for bench=["sparsity","distractor"]
 S=T(T.benchmark==bench,:);levels=unique(S.level);fig=figure('Visible','off','Color','w','Position',[50 50 1450 570]);
 fig.UserData=metadata;layout=tiledlayout(fig,1,2,'Padding','compact');colors=lines(4);
 nexttile;hold on;presets=v1_options();
 for k=1:4
  x=S(S.method=="APC" & S.configuration==string(presets(k).name),:);counts=zeros(size(levels));
  for il=1:numel(levels),q=x(x.level==levels(il),:);counts(il)=sum(abs(q.recovered_fp_hz-q.true_fp_hz)<=1 & abs(q.recovered_fa_hz-q.true_fa_hz)<=8 & q.valid);end
  plot(levels,counts,'-o','Color',colors(k,:),'LineWidth',1.5,'DisplayName',presets(k).name);
 end
 ylabel('Joint recovery /25');xlabel(char(bench+' level'));title('APC configurations');ylim([0 25]);grid on;
 legend('Location','southoutside','Interpreter','none');
 nexttile;hold on;names=["MVL-raw","MVL-Ozkurt","KLMI-scan","GLM-scan"];
 for im=1:2
  mode="A0";style='-o';if im==2,mode="A1";style='--s';end
  for k=1:4
   x=S(S.method==names(k)&S.configuration==mode,:);counts=zeros(size(levels));
   for il=1:numel(levels),q=x(x.level==levels(il),:);counts(il)=sum(abs(q.recovered_fp_hz-q.true_fp_hz)<=1 & abs(q.recovered_fa_hz-q.true_fa_hz)<=8 & q.valid);end
   plot(levels,counts,style,'Color',colors(k,:),'LineWidth',1.3,'DisplayName',mode+" "+names(k));
  end
 end
 ylabel('Joint recovery /25');xlabel(char(bench+' level'));title('Comparator settings');ylim([0 25]);grid on;
 legend('Location','southoutside','NumColumns',2,'Interpreter','none');
 title(layout,sprintf('%s: 25 paired repeats; fP tolerance 1 Hz, fA tolerance 8 Hz',bench),'Interpreter','none');
 stem=fullfile(outDir,char('joint_recovery_'+bench));
 print(fig,[stem '.png'],'-dpng','-r150');print(fig,[stem '.svg'],'-dsvg');savefig(fig,[stem '.fig']);close(fig);
 % Embed full provenance in the SVG (the Python report writer embeds PNG text).
 text=fileread([stem '.svg']);encoded=jsonencode(metadata);
 encoded=strrep(encoded,'&','&amp;');encoded=strrep(encoded,'<','&lt;');encoded=strrep(encoded,'>','&gt;');
 text=strrep(text,'</svg>',['<metadata id="APC-v1-provenance">' encoded '</metadata></svg>']);
 f=fopen([stem '.svg'],'w');c=onCleanup(@() fclose(f));fprintf(f,'%s',text);clear c;
end
end
