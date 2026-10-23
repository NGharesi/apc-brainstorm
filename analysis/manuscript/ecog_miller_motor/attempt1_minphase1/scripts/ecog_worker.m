function ecog_worker(w,nw)
% Protocol section 7: APC (repo src, default v1) and four ecog scans on every analysed bout.
% Worker w of nw takes every nw-th patient. Rows are appended to estimates_w<w>.csv (resume-safe).
R='C:\Users\nghare\.brainstorm\process\revision_checks\ecog_miller_motor';
repo='C:\Users\nghare\.brainstorm\process\apc-brainstorm-publish';
RC='C:\Users\nghare\.brainstorm\process\revision_checks';
cd(R);
addpath(fullfile(RC,'final'));addpath(fullfile(RC,'rodent_multi'));addpath(R);addpath(fullfile(repo,'src'),'-begin');
clear bst_apc calc_MI_all_methods
assert(strcmpi(which('bst_apc'),fullfile(repo,'src','bst_apc.m')),'ECOG:WrongAPCPath','Wrong APC path');
pts={'bp','ca','cc','de','fp','gc','gf','hh','hl','jc','jf','jm','jp','jt','rh','rr','ug','wc','zt'};
mine=pts(w:nw:end);
outF=fullfile(R,sprintf('estimates_w%d.csv',w));
done=strings(0);
if exist(outF,'file'), T0=readtable(outF,'TextType','string'); done=unique(T0.key); end
fid=fopen(outF,'a');
if ftell(fid)==0
  fprintf(fid,'key,patient,recording,bout,state,movement_type,code,rest_index,duration_s,method,fP_hz,fA_hz,score,raw_mvl,ozkurt_mvl,preferred_phase_deg,status,route,n_bursts,boundary_fp_low,boundary_fp_high,boundary_fa_low,boundary_fa_high\n');
end
nDone=0;nFail=0;
for k=1:numel(mine)
  pt=mine{k}; S=load(fullfile(R,'prep',[pt '.mat']));
  recs={'movement'}; if ~isempty(S.sigI), recs{end+1}='imagery'; end
  for r=1:numel(recs)
    if strcmp(recs{r},'movement'), B=S.B; x=S.sig; else, B=S.BI; x=S.sigI; end
    B=B(B.analysed,:);
    for b=1:height(B)
      key=sprintf('%s_%s_%03d',pt,recs{r},B.bout(b));
      if any(done==key), continue; end
      if exist(fullfile(R,'STOP_METHOD'),'file'), fclose(fid); error('ECOG:Stopped','STOP_METHOD flag present'); end
      seg=x(B.start_sample(b):B.end_sample(b)); t=(0:numel(seg)-1)/S.fs;
      [row,~]=v1_bout_features(seg,t);
      bf=[abs(row.fP_hz-1)<=.05, abs(row.fP_hz-30)<=.05, row.fA_hz==80, row.fA_hz==150];
      writeRow(fid,key,pt,recs{r},B(b,:),'APC-v1.0',row.fP_hz,row.fA_hz,row.score,row.raw_mvl,row.ozkurt_mvl,row.preferred_phase_deg,row.status,row.route,NaN,bf);
      c=ecog_comparators(seg,S.fs,"ecog","ecog_A2_prime",.5);
      for m=1:numel(c)
        bf=[c(m).fp==6, c(m).fp==30, c(m).fa==80, c(m).fa==148];
        writeRow(fid,key,pt,recs{r},B(b,:),char(c(m).method),c(m).fp,c(m).fa,c(m).score,c(m).raw_mvl,c(m).ozkurt_mvl,c(m).preferred_phase_deg,c(m).status,"not_applicable",NaN,bf);
      end
      nDone=nDone+1; nFail=nFail+(row.status~=0);
      if mod(nDone,25)==0
        writejson(fullfile(R,sprintf('status_w%d.json',w)),struct('bouts',nDone,'apc_invalid',nFail));
        fprintf('worker %d: %d bouts, %d APC invalid\n',w,nDone,nFail);
        tot=0;bad=0;fl=dir(fullfile(R,'status_w*.json'));
        for q=1:numel(fl), J=jsondecode(fileread(fullfile(R,fl(q).name))); tot=tot+J.bouts; bad=bad+J.apc_invalid; end
        if tot>=200 && bad/tot>0.5
          writejson(fullfile(R,'STOP_METHOD'),struct('reason','more than half of completed bouts invalid for APC (protocol 9.4)','bouts',tot,'apc_invalid',bad));
        end
      end
    end
  end
end
fclose(fid);
writejson(fullfile(R,sprintf('status_w%d.json',w)),struct('bouts',nDone,'apc_invalid',nFail,'finished',true));
G=final_sos_filter('registry'); if ~isempty(G), writetable(struct2table(G),fullfile(R,sprintf('filter_guards_w%d.csv',w))); end
fprintf('WORKER %d DONE\n',w);
end

function writeRow(fid,key,pt,rec,Bb,method,fp,fa,score,raw,oz,pref,status,route,nb,bf)
fprintf(fid,'%s,%s,%s,%d,%s,%s,%d,%d,%.6f,%s,%.15g,%.15g,%.15g,%.15g,%.15g,%.15g,%d,%s,%g,%d,%d,%d,%d\n', ...
  key,pt,rec,Bb.bout,Bb.state,Bb.movement_type,Bb.code,Bb.rest_index,Bb.duration_s,method,fp,fa,score,raw,oz,pref,status,string(route),nb,bf);
end

function writejson(path,value)
f=fopen(path,'w');fprintf(f,'%s\n',jsonencode(value));fclose(f);
end
