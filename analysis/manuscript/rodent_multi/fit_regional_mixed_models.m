function fit_regional_mixed_models
out=fileparts(mfilename('fullpath'));clockStart=tic;
run=jsondecode(fileread(fullfile(out,'regional_bouts_runtime.json')));assert(strcmp(run.status,'COMPLETE'),'Rodent:BoutsIncomplete','Incomplete regional analysis');
meta=jsondecode(fileread(fullfile(out,'regional_protocol_record.json')));meta.matlab_version=version;meta.stage='region-specific REML mixed models';meta.fit_method='REML';
T=readtable(fullfile(out,'regional_bout_estimates.csv'),'TextType','string','Delimiter',',','NumHeaderLines',0,'ReadVariableNames',true,'VariableNamingRule','preserve','Encoding','UTF-8');models={};coefficientRows={};
try
 for analysis=["CA1","EC","E1_sensitivity"]
  D=T(T.analysis==analysis&T.method=="APC-v1.0",:);D.state_run=double(D.state=="run");D.animal=categorical(D.animal);D.session=categorical(D.session);
  if numel(unique(D.animal))>1,D.animal=reordercats(D.animal,{'EC012','EC013'});formula='outcome ~ state_run + animal + (1 + state_run | session)';constantAnimal=false;
  else,formula='outcome ~ state_run + (1 + state_run | session)';constantAnimal=true;end
  for name=["fP_hz","ozkurt_mvl"]
   data=D(isfinite(D.(name)),:);data.outcome=data.(name);lastwarn('');localStart=tic;
   warning('on','stats:classreg:regr:lmeutils:StandardLinearMixedModel:Message_OptimizerUnableToConverge');
   logText=evalc('model=fitlme(data,formula,''FitMethod'',''REML'');');[warnText,warnID]=lastwarn;
   C=model.Coefficients;if isa(C,'dataset'),C=dataset2table(C);end;C.analysis=repmat(analysis,height(C),1);C.outcome=repmat(name,height(C),1);C.provenance_json=repmat(string(jsonencode(meta)),height(C),1);coefficientRows{end+1}=C; %#ok<AGROW>
   [covariance,residualVariance,covarianceStatistics]=covarianceParameters(model);
   criterion=model.ModelCriterion;if isa(criterion,'dataset'),criterion=dataset2table(criterion);end
   one=struct('analysis',analysis,'outcome',name,'observations',height(data),'sessions',numel(unique(data.session)),'animals',{cellstr(unique(data.animal))},'constant_animal_term_omitted',constantAnimal,'formula',formula,'fit_method','REML', ...
    'log_likelihood',model.LogLikelihood,'model_criterion',table2struct(criterion),'random_effect_covariance',covariance{1},'random_effect_eigenvalues',eig(covariance{1}),'random_effect_numerical_rank',rank(covariance{1}),'residual_variance',residualVariance,'last_warning_identifier',warnID,'last_warning',warnText,'optimizer_nonconvergence_warning',contains(logText,'unable to converge')||contains(warnID,'Message_OptimizerUnableToConverge'),'convergence_reporting','nonconvergence warning enabled and captured; optimizer exit code is not public','elapsed_seconds',toc(localStart),'metadata',meta);
   save(fullfile(out,char("regional_mixed_"+analysis+"_"+name+".mat")),'model','one','covarianceStatistics','-v7.3');models{end+1}=one; %#ok<AGROW>
   f=fopen(fullfile(out,char("regional_mixed_"+analysis+"_"+name+"_fit.txt")),'w','n','UTF-8');fprintf(f,'Provenance: %s\n%s\n%s\n',jsonencode(meta),logText,evalc('disp(model)'));fclose(f);
   fprintf('MIXED %s %s: sessions%d n%d warning %s\n',analysis,name,one.sessions,one.observations,warnID);
  end
 end
 C=vertcat(coefficientRows{:});writetable(C,fullfile(out,'regional_mixed_model_coefficients.csv'));
 writejson(fullfile(out,'regional_mixed_models.json'),struct('status','COMPLETE','elapsed_seconds',toc(clockStart),'metadata',meta,'models',{models}));
catch err
 writejson(fullfile(out,'regional_mixed_models_failure.json'),struct('status','FAILED_STOP','identifier',err.identifier,'error',err.message,'metadata',meta));rethrow(err);
end
end
function writejson(file,s)
f=fopen(file,'w','n','UTF-8');fprintf(f,'%s\n',jsonencode(s));fclose(f);
end
