function select_channels
root='C:\Users\nghare\.brainstorm\process';out=fullfile(root,'revision_checks','rodent_multi');cd(out);maxNumCompThreads(1);
gate=jsondecode(fileread(fullfile(out,'behavior_reproduction.json')));assert(gate.passed,'Rodent:BehaviorGate','Reproduction gate failed');
T=readtable(fullfile(out,'mapping_checks.csv'),'TextType','string','Delimiter',',');assert(all(abs(T.tracking_to_lfp_duration_ratio-1)<=.05),'Rodent:MappingGate','Duration mismatch');
meta=jsondecode(fileread(fullfile(out,'inventory.json')));meta=meta.metadata;meta.matlab_version=version;meta.stage='whole-recording Welch channel selection';meta.welch=struct('window','symmetric Hann round(4*fs)','overlap_fraction',.5,'nfft','2^nextpow2(window samples)','detrend','per-channel mean removal','integration','linear endpoint interpolation; trapezoid','theta_hz',[6 10],'delta_hz',[1 4]);
rows={};selected={};start=tic;
for j=1:height(T)
 file=fullfile(out,T.session(j)+"_channel_selection.mat");
 if isfile(file),b=load(file,'channelTable','choice');rows{end+1}=b.channelTable;selected{end+1}=b.choice;continue;end %#ok<AGROW>
 if T.session(j)=="ec013.157",s=load(T.lfp_file(j),'test');F=s.test.F;time=s.test.Time;flags=s.test.ChannelFlag;
 else,s=load(T.lfp_file(j),'F','Time','ChannelFlag');F=s.F;time=s.Time;flags=s.ChannelFlag;end
 fs=1/median(diff(time));nwin=round(4*fs);window=hann(nwin);nover=floor(nwin/2);nfft=2^nextpow2(nwin);rr={};
 for ch=1:size(F,1)
  x=double(F(ch,:));theta=nan;delta=nan;ratio=nan;reason="";
  if all(isfinite(x)),x=x-mean(x);[p,f]=pwelch(x,window,nover,nfft,fs);theta=integral(p,f,[6 10]);delta=integral(p,f,[1 4]);if delta>0,ratio=theta/delta;else,reason="nonpositive delta power";end
  else,reason="nonfinite input samples";end
  flag=nan;if numel(flags)>=ch,flag=flags(ch);end
  rr{end+1}=struct('animal',T.animal(j),'session',T.session(j),'channel_index',ch,'channel_name',"E"+ch,'theta_power',theta,'delta_power',delta,'theta_delta_ratio',ratio,'source_channel_flag',flag,'undefined_reason',reason,'n_samples',numel(time),'fs_hz',fs,'source_file',T.lfp_file(j),'git_commit',string(meta.git_commit),'provenance_json',string(jsonencode(meta))); %#ok<AGROW>
 end
 channelTable=struct2table([rr{:}]);[best,index]=max(channelTable.theta_delta_ratio,[],'omitnan');assert(isfinite(best),'Rodent:Channel','No defined channel ratio');
 choice=struct('animal',T.animal(j),'session',T.session(j),'channel_index',index,'channel_name',"E"+index,'theta_delta_ratio',best,'source_file',T.lfp_file(j),'region',"unverified",'shank',"unverified",'git_commit',string(meta.git_commit),'provenance_json',string(jsonencode(meta)));
 rows{end+1}=channelTable;selected{end+1}=choice;save(file,'channelTable','choice','meta','-v7');clear F s
 fprintf('CHANNEL %d/%d %s E%d ratio %.8g\n',j,height(T),T.session(j),index,best);
end
R=vertcat(rows{:});C=struct2table([selected{:}]);writetable(R,fullfile(out,'channel_ratios.csv'));writetable(C,fullfile(out,'selected_channels.csv'));
r=struct('status','COMPLETE','elapsed_seconds',toc(start),'metadata',meta);f=fopen(fullfile(out,'channel_selection_runtime.json'),'w','n','UTF-8');fprintf(f,'%s\n',jsonencode(r));fclose(f);
end
function power=integral(p,f,b)
ix=f>b(1)&f<b(2);ff=[b(1);f(ix);b(2)];pp=[interp1(f,p,b(1));p(ix);interp1(f,p,b(2))];power=trapz(ff,pp);
end
