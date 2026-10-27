function confirm_generate
O=fileparts(mfilename('fullpath'));R=fileparts(fileparts(O));repo=fullfile(R,'apc-brainstorm-publish');V=fullfile(R,'revision_checks','paper2_validation');cd(O);
addpath(fullfile(repo,'analysis','v1_revision'),'-begin');addpath(fullfile(repo,'analysis','v2_revision'),'-begin');addpath(fullfile(repo,'results','paper2_validation'),'-begin');addpath(O,'-begin');
m=jsondecode(fileread(fullfile(O,'provenance.json')));assert(m.push_succeeded_before_signal_generation);assert(~isfile(fullfile(O,'generator_check.json'))&&~isfile(fullfile(O,'generation_complete.json')));start=tic;
try
 checks={};cfg=validation_p1_generator('profile');cfg.random_seed=20261112;cells=validation_p1_generator('cells');saved=load(fullfile(V,'V3_inputs.mat'),'cases');rng(20261112,'twister');
 for j=1:numel(cells)
  for ir=1:100
   [x,t]=validation_p1_generator('trial',cfg,cells(j));
   if ir==1,c=saved.cases{(j-1)*100+1};ok=isequal(x,c.signal)&&isequal(t,c.time);checks{end+1}=struct('suite',"V3",'cell',cells(j).name,'seed',20261112,'repeat_index',ir,'signal_equal',isequal(x,c.signal),'time_equal',isequal(t,c.time),'sha256',string(signalsha(x)),'saved_sha256',string(c.signal_sha256));assert(ok,'Confirm:GeneratorCheck','V3 %s first repeat mismatch',cells(j).name);end %#ok<AGROW>
  end
 end
 clear saved;
 old=load(fullfile(R,'revision_checks','v3_aperiodic','HB_inputs.mat'),'meta');meta=old.meta;meta.git_commit=m.git_head;checkdir=fullfile(O,'generator_check_source');mkdir(checkdir);validation_hb_cases(checkdir,meta,20261110);q=load(fullfile(checkdir,'HB_inputs.mat'),'cases');saved=load(fullfile(V,'V1_inputs.mat'),'cases');c=q.cases{1};s=saved.cases{1};checks{end+1}=struct('suite',"V1",'cell',"first_trial",'seed',20261110,'repeat_index',1,'signal_equal',isequal(c.signal,s.signal),'time_equal',isequal(c.time,s.time),'sha256',string(signalsha(c.signal)),'saved_sha256',string(s.signal_sha256));assert(isequal(c.signal,s.signal)&&isequal(c.time,s.time),'Confirm:GeneratorCheck','V1 first trial mismatch');clear q saved;
 writejson(fullfile(O,'generator_check.json'),struct('status','PASS','classification','confirmatory','checks',{checks},'git_commit',m.git_head,'protocol_sha256',m.protocol_sha256,'note','P1 advances the unchanged full stream to reach first repeat of each cell. Full legacy HB wrapper is generated for checking, with only first V1 trial compared; no methods run on check inputs.'));
 truths={};
 for suite=["W3","W1"]
  seed=20261120;if suite=="W1",seed=20261121;end
  assert(~isfile(fullfile(O,char(suite+"_inputs.mat"))));
  if suite=="W3"
   cfg=validation_p1_generator('profile');cfg.random_seed=seed;rng(seed,'twister');cases={};
   for j=1:numel(cells),for ir=1:100
    [x,t]=validation_p1_generator('trial',cfg,cells(j));cc=cfg;cc.true_fp_hz=cells(j).rhythm_hz;dataset="coupled";if ~cells(j).is_coupled,dataset="uncoupled";end
    id=numel(cases)+1;cases{end+1}=struct('input_id',id,'paired_coupled_id',nan,'scenario',cells(j).name,'dataset',dataset,'level',cells(j).keep_rate,'repeat_index',ir,'signal',x,'time',t,'cfg',cc,'true_fd_hz',cells(j).distractor_hz); %#ok<AGROW>
   end;end
  else
   d=fullfile(O,'W1_source');mkdir(d);validation_hb_cases(d,meta,seed);q=load(fullfile(d,'HB_inputs.mat'),'cases');keep=false(size(q.cases));
   for j=1:numel(keep),c=q.cases{j};keep(j)=startsWith(string(c.scenario),"H1")&&ismember(string(c.dataset),["coupled","timing_null"]);end
   cases=q.cases(keep);clear q;
  end
  expected=600;if suite=="W1",expected=350;end;assert(numel(cases)==expected);
  for j=1:numel(cases)
   c=cases{j};c.signal_sha256=signalsha(c.signal);cases{j}=c;truths{end+1}=struct('suite',suite,'case_index',j,'input_id',c.input_id,'paired_coupled_id',c.paired_coupled_id,'key',suite+"_"+c.input_id,'scenario',string(c.scenario),'dataset',string(c.dataset),'level',c.level,'repeat_index',c.repeat_index,'true_fp_hz',c.cfg.true_fp_hz,'true_fa_hz',c.cfg.true_fa_hz,'true_fd_hz',c.true_fd_hz,'seed',seed,'signal_sha256',string(c.signal_sha256),'classification',"confirmatory",'git_commit',string(m.git_head),'protocol_sha256',string(m.protocol_sha256),'generator_settings_json',string(jsonencode(c.cfg))); %#ok<AGROW>
  end
  bankmeta=m;bankmeta.seed=seed;save(fullfile(O,char(suite+"_inputs.mat")),'cases','bankmeta','-v7.3');fprintf('%s generated %d inputs\n',suite,numel(cases));clear cases;
 end
 v1_write_csv(struct2table(vertcat(truths{:})),fullfile(O,'truths.csv'));writejson(fullfile(O,'generation_complete.json'),struct('status','COMPLETE','classification','confirmatory','inputs',950,'elapsed_seconds',toc(start),'git_commit',m.git_head,'protocol_sha256',m.protocol_sha256));
catch err
 writejson(fullfile(O,'generation_error.json'),struct('identifier',err.identifier,'message',err.message,'stack',err.stack));f=fopen(fullfile(O,'STOPPED.md'),'w','n','UTF-8');fprintf(f,'# Confirmation stopped\n\n%s: %s\n',err.identifier,err.message);fclose(f);rethrow(err);
end
end
function s=signalsha(x),h=java.security.MessageDigest.getInstance('SHA-256');h.update(typecast(double(x(:)),'uint8'));b=typecast(h.digest(),'uint8');s=lower(reshape(dec2hex(b,2).',1,[]));end
function writejson(p,x),f=fopen(p,'w','n','UTF-8');assert(f>=0);c=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(x));end
