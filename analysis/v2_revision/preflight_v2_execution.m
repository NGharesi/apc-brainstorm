function preflight_v2_execution()
% Validate held-out comparator implementation on an existing saved input.
A=strrep(fileparts(mfilename('fullpath')),'/','\');repo=fileparts(fileparts(A));root=fileparts(repo);out=fullfile(root,'revision_checks','v2','candidate_03');
old=pwd;cleanup=onCleanup(@() cd(old)); %#ok<NASGU>
cd(out);addpath(A,'-begin');addpath(fullfile(repo,'src'),'-begin');addpath(fullfile(repo,'analysis','v1_revision'),'-begin');
b=load(fullfile(root,'revision_checks','v1_rerun','main_distractor_level_0.mat'),'cases');c=b.cases{1};
start=tic;actual=v2_heldout_comparators(c.signal,c.cfg.fs_hz);assert(numel(actual)==8);
x=double(c.signal(:));fs=c.cfg.fs_hz;fpGrid=3:.5:14;faGrid=80:4:160;reference=actual;
k=0;
for mode=["A2_prime","A1_prime"]
 scores=nan(numel(fpGrid),numel(faGrid),4);
 for ip=1:numel(fpGrid)
  fp=fpGrid(ip);[b,a]=butter(4,[fp-1.5,fp+1.5]/(fs/2),'bandpass');phase=angle(hilbert(filtfilt(b,a,x)));
  for ia=1:numel(faGrid)
   half=14;if mode=="A1_prime",half=fp;end
   band=[max(1,faGrid(ia)-half),min(fs/2-1,faGrid(ia)+half)];[b,a]=butter(4,band/(fs/2),'bandpass');amp=abs(hilbert(filtfilt(b,a,x)));
   raw=abs(mean(amp.*exp(1i*phase)));scores(ip,ia,1)=raw;scores(ip,ia,2)=raw/sqrt(mean(amp.^2));
   scores(ip,ia,3)=calc_MI_all_methods(phase,amp,'tort',false,0,1,false,18);
   X=[ones(size(phase)),sin(phase),cos(phase)];beta=X\amp;scores(ip,ia,4)=max(0,1-sum((amp-X*beta).^2)/sum((amp-mean(amp)).^2));
  end
 end
 for m=1:4
  k=k+1;map=scores(:,:,m);[score,idx]=max(map(:),[],'omitnan');[ip,ia]=ind2sub(size(map),idx);
  reference(k).fp=fpGrid(ip);reference(k).fa=faGrid(ia);reference(k).score=score;
  assert(actual(k).fp==reference(k).fp && actual(k).fa==reference(k).fa && abs(actual(k).score-score)<1e-12,'v2:ComparatorPreflight','Comparator differs from literal reference');
 end
end
u=jsondecode(fileread(fullfile(out,'unit_attempt_01','unit_results.json')));metadata=u.metadata;
result=struct('passed',true,'n_metric_configurations',8,'existing_input','main_distractor_level_0.mat repeat 1','elapsed_seconds',toc(start),'metadata',metadata);
f=fopen(fullfile(out,'comparator_preflight.json'),'w','n','UTF-8');assert(f>=0);closing=onCleanup(@() fclose(f)); %#ok<NASGU>
fprintf(f,'%s',jsonencode(result,'PrettyPrint',true));fprintf('COMPARATOR PREFLIGHT PASSED 8/8; %.3f seconds\n',toc(start));
end
