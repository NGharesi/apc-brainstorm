function fit_rodent_mixed_models
out=fileparts(mfilename('fullpath'));gate=jsondecode(fileread(fullfile(out,'chunked_behavior_validation.json')));assert(gate.passed,'Rodent:Gate','Reference validation failed');
run=jsondecode(fileread(fullfile(out,'multi_bouts_runtime.json')));assert(strcmp(run.status,'COMPLETE'),'Rodent:BoutsIncomplete','Incomplete bout analysis');
meta=jsondecode(fileread(fullfile(out,'protocol_amendments_record.json')));meta.matlab_version=version;meta.stage='specified REML random-intercept/random-slope mixed model';
meta.formula='outcome ~ state_run + animal + (1 + state_run | session)';meta.fit_method='REML';meta.animal_reference='EC012';
T=readtable(fullfile(out,'bout_estimates.csv'),'TextType','string');D=T(T.analysis=="theta_delta_primary"&T.method=="APC-v1.0",:);D.state_run=double(D.state=="run");D.animal=categorical(D.animal);D.animal=reordercats(D.animal,{'EC012','EC013'});D.session=categorical(D.session);
models={};coefficientRows={};
for name=["fP_hz","ozkurt_mvl"]
 data=D(isfinite(D.(name)),:);data.outcome=data.(name);lastwarn('');clockStart=tic;
 try
  logText=evalc('model=fitlme(data,''outcome ~ state_run + animal + (1 + state_run | session)'',''FitMethod'',''REML'');');
  [warnText,warnID]=lastwarn;C=model.Coefficients;C.outcome=repmat(name,height(C),1);C.provenance_json=repmat(string(jsonencode(meta)),height(C),1);coefficientRows{end+1}=C; %#ok<AGROW>
  [covariance,residualVariance,covarianceStatistics]=covarianceParameters(model);
  one=struct('outcome',name,'observations',height(data),'sessions',numel(unique(data.session)),'formula',meta.formula,'fit_method','REML','log_likelihood',model.LogLikelihood,'model_criterion',table2struct(model.ModelCriterion),'random_effect_covariance',covariance{1},'residual_variance',residualVariance,'last_warning_identifier',warnID,'last_warning',warnText,'elapsed_seconds',toc(clockStart),'metadata',meta);
  save(fullfile(out,char("mixed_model_"+name+".mat")),'model','one','covarianceStatistics','-v7.3');models{end+1}=one; %#ok<AGROW>
  f=fopen(fullfile(out,char("mixed_model_"+name+"_fit.txt")),'w','n','UTF-8');fprintf(f,'Provenance: %s\n%s\n%s\n',jsonencode(meta),logText,evalc('disp(model)'));fclose(f);
 catch err
  one=struct('status','FAILED_STOP','outcome',name,'identifier',err.identifier,'error',err.message,'metadata',meta);writejson(fullfile(out,'mixed_models_failure.json'),one);rethrow(err);
 end
end
C=vertcat(coefficientRows{:});writetable(C,fullfile(out,'mixed_model_coefficients.csv'));writejson(fullfile(out,'mixed_models.json'),struct('metadata',meta,'models',{models}));
end
function writejson(file,s)
f=fopen(file,'w','n','UTF-8');fprintf(f,'%s\n',jsonencode(s));fclose(f);
end
