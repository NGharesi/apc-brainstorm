function ecog_prepare
% Protocol sections 3-6: inventory, preprocessing, bouts, electrode selection.
% Writes prep\<pt>.mat (selected-channel preprocessed signals + bout tables) and summary CSVs.
R='C:\Users\nghare\.brainstorm\process\revision_checks\ecog_miller_motor';
D='D:\APC_project\RealDatasets\Miller_ECoG_library';
cd(R); if ~exist(fullfile(R,'prep'),'dir'), mkdir(fullfile(R,'prep')); end
fs=1000; scale=0.0298; % amplifier units -> microvolts (library README)
pts={'bp','ca','cc','de','fp','gc','gf','hh','hl','jc','jf','jm','jp','jt','rh','rr','ug','wc','zt'};
inv={};guards={};bouts_all={};elec={};bad={};
for k=1:numel(pts)
  pt=pts{k};
  M=load(fullfile(D,'motor_basic','data',[pt '_mot_t_h.mat']),'data','stim');
  L=load(fullfile(D,'motor_basic','locs',[pt '_electrodes.mat']),'electrodes');
  [X,badIdx,g]=preprocess(double(M.data)*scale,fs,60:60:180);
  guards=[guards;tag(g,pt,"movement")]; %#ok<AGROW>
  bad=[bad;{pt,"movement",size(M.data,2),numel(badIdx),strjoin(string(badIdx),';')}]; %#ok<AGROW>
  stim=double(M.stim(:));
  inv=[inv;inventory_row(pt,"movement",fullfile('motor_basic','data',[pt '_mot_t_h.mat']),M.data,stim,fs)]; %#ok<AGROW>
  B=make_bouts(stim,fs,[11 12]);
  good=setdiff(1:size(X,2),badIdx);
  % electrode selection data (protocol section 6)
  imgFile=fullfile(D,'imagery_basic','data',[pt '_im_t_h.mat']);
  flagged=false; selSource="imagery_rest"; mapNote="";
  if exist(imgFile,'file')
    I=load(imgFile,'data','stim'); IL=load(fullfile(D,'imagery_basic','locs',[pt '_electrodes.mat']),'electrodes');
    [XI,badI,gI]=preprocess(double(I.data)*scale,fs,60:60:180); guards=[guards;tag(gI,pt,"imagery")]; %#ok<AGROW>
    bad=[bad;{pt,"imagery",size(I.data,2),numel(badI),strjoin(string(badI),';')}]; %#ok<AGROW>
    stimI=double(I.stim(:)); inv=[inv;inventory_row(pt,"imagery",fullfile('imagery_basic','data',[pt '_im_t_h.mat']),I.data,stimI,fs)]; %#ok<AGROW>
    BI=make_bouts(stimI,fs,[11 12]);
    % map imagery channels to motor_basic channels by identical coordinates
    map=nan(size(X,2),1);
    for c=1:size(X,2)
      dd=sqrt(sum((IL.electrodes-L.electrodes(c,:)).^2,2)); [m,j]=min(dd); if m<1e-3, map(c)=j; end
    end
    goodI=setdiff(1:size(XI,2),badI);
    cand=good(~isnan(map(good)) & ismember(map(good),goodI));
    if isempty(cand)
      flagged=true; selSource="odd_rest_fallback"; mapNote="imagery montage could not be matched by coordinates";
    else
      restI=BI(BI.state=="rest",:);
      [peakH,peakF]=beta_peaks(XI(:,map(cand)),restI,fs);
      mapNote=sprintf('%d of %d good motor channels matched to imagery channels',numel(cand),numel(good));
    end
  else
    flagged=true; selSource="odd_rest_fallback"; mapNote="no imagery recording";
    XI=[];BI=table();map=[];
  end
  restB=B(B.state=="rest",:);
  if flagged
    selRest=restB(mod(restB.rest_index,2)==1,:); cand=good;
    [peakH,peakF]=beta_peaks(X(:,cand),selRest,fs);
    B.analysed=~(B.state=="rest" & mod(B.rest_index,2)==1);
  else
    B.analysed=true(height(B),1);
  end
  [~,j]=max(peakH); ch=cand(j);
  elec=[elec;{pt,ch,L.electrodes(ch,1),L.electrodes(ch,2),L.electrodes(ch,3),peakF(j),peakH(j),selSource,flagged,mapNote,numel(cand)}]; %#ok<AGROW>
  sig=X(:,ch);
  if ~isempty(XI) && ~flagged, sigI=XI(:,map(ch)); BI.analysed=true(height(BI),1); else, sigI=[]; end
  B.patient=repmat(string(pt),height(B),1); B.recording=repmat("movement",height(B),1);
  if ~isempty(BI), BI.patient=repmat(string(pt),height(BI),1); BI.recording=repmat("imagery",height(BI),1); end
  if ~isempty(sigI), bouts_all=[bouts_all;{B};{BI}]; else, bouts_all=[bouts_all;{B}]; end %#ok<AGROW>
  save(fullfile(R,'prep',[pt '.mat']),'sig','sigI','B','BI','ch','fs','flagged','-v7');
  fprintf('%s: ch %d (%s), peak %.2f Hz, %d move / %d rest bouts (analysed %d)\n',pt,ch,selSource,peakF(j),sum(B.state=="move"),sum(B.state=="rest"),sum(B.analysed));
end
writetable(cell2table(inv,'VariableNames',{'patient','recording','file','n_samples','n_channels','duration_s','fs_hz','codes_and_counts'}),fullfile(R,'inventory.csv'));
writetable(cell2table(bad,'VariableNames',{'patient','recording','n_channels','n_bad','bad_channels'}),fullfile(R,'bad_channels.csv'));
writetable(cell2table(elec,'VariableNames',{'patient','channel','x_tal','y_tal','z_tal','beta_peak_hz','beta_peak_height','selection_source','flagged','mapping_note','n_candidates'}),fullfile(R,'electrodes.csv'));
G=vertcat(guards{:}); writetable(G,fullfile(R,'notch_filter_guards.csv'));
allB=vertcat(bouts_all{:}); writetable(allB,fullfile(R,'bouts.csv'));
fprintf('PREPARE DONE\n');
end

function [X,badIdx,G]=preprocess(X,fs,notchF)
v=var(X,0,1); mv=median(v); badIdx=find(v>5*mv | v<0.2*mv);
good=setdiff(1:size(X,2),badIdx);
X(:,good)=X(:,good)-mean(X(:,good),2);
G=table();
for f=notchF
  [z,p,k]=butter(4,[f-1 f+1]/(fs/2),'stop'); [sos,g]=zp2sos(z,p,k);
  r=max(abs(p)); assert(r<1,'ECOG:NotchUnstable','Notch %g Hz unstable',f);
  X=filtfilt(sos,g,X);
  G=[G;table(f,r,'VariableNames',{'notch_hz','max_pole_radius'})]; %#ok<AGROW>
end
assert(all(isfinite(X(:))),'ECOG:Nonfinite','Nonfinite after preprocessing');
end

function T=tag(G,pt,rec)
T={[G table(repmat(string(pt),height(G),1),repmat(rec,height(G),1),'VariableNames',{'patient','recording'})]};
end

function row=inventory_row(pt,rec,file,data,stim,fs)
u=unique(stim); s=strings(numel(u),1);
for i=1:numel(u), s(i)=sprintf('%g:%d',u(i),sum(stim==u(i))); end
row={pt,rec,file,size(data,1),size(data,2),size(data,1)/fs,fs,strjoin(s,';')};
end

function B=make_bouts(stim,fs,moveCodes)
% Runs of identical stim; movement = codes 11/12 (pooled), rest = 0. Other codes are not analysed.
n=numel(stim); edges=[1;find(diff(stim)~=0)+1;n+1];
st=[];en=[];code=[];
for i=1:numel(edges)-1, st(end+1,1)=edges(i); en(end+1,1)=edges(i+1)-1; code(end+1,1)=stim(edges(i)); end %#ok<AGROW>
keep=ismember(code,[0 moveCodes]); st=st(keep);en=en(keep);code=code(keep);
trim=round(0.5*fs); s2=st+trim; e2=en-trim; len=e2-s2+1;
ok=len>=round(2.0*fs) & s2>round(2*fs) & e2<=n-round(2*fs);
s2=s2(ok);e2=e2(ok);code=code(ok);len=len(ok);
state=repmat("rest",numel(code),1); state(code~=0)="move";
mtype=repmat("rest",numel(code),1); mtype(code==11)="tongue"; mtype(code==12)="hand";
restIdx=zeros(numel(code),1); r=0; for i=1:numel(code), if code(i)==0, r=r+1; restIdx(i)=r; end, end
B=table((1:numel(code))',s2,e2,len/fs,code,state,mtype,restIdx,'VariableNames',{'bout','start_sample','end_sample','duration_s','code','state','movement_type','rest_index'});
end

function [H,F]=beta_peaks(X,restB,fs)
P=0;
for b=1:height(restB)
  seg=X(restB.start_sample(b):restB.end_sample(b),:);
  [pxx,f]=pwelch(seg,hann(1000),500,1000,fs); P=P+pxx;
end
P=P/height(restB); idx=f>=8 & f<=30; lf=log10(f(idx));
H=nan(1,size(X,2));F=H;
for c=1:size(X,2)
  lp=log10(P(idx,c)); q=polyfit(lf,lp,1); res=lp-polyval(q,lf); [H(c),j]=max(res); F(c)=f(find(idx,1)+j-1);
end
end
