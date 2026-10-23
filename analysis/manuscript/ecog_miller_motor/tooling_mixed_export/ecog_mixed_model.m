function ecog_mixed_model
% Prespecified primary-1 mixed model, default fitlme ML, rest is baseline.
R=fileparts(mfilename('fullpath'));cd(R);assert(~isfile('STOP_METHOD'));m=jsondecode(fileread('provenance.json'));
T=readtable('mixed_model_inputs.csv','Delimiter',',','ReadVariableNames',true,'NumHeaderLines',0,'TextType','string','Encoding','UTF-8');T.patient=categorical(T.patient);T.state=categorical(T.state);T.state=reordercats(T.state,{'rest','move'});T.outcome=T.ozkurt_mvl;
lastwarn('');model=fitlme(T,'outcome ~ state + (1 + state | patient)');[warningMessage,warningID]=lastwarn;disp(model);coefficients=model.Coefficients;coefficients.git_head=repmat(string(m.git_head),height(coefficients),1);coefficients.protocol_sha256=repmat(string(m.protocol_sha256),height(coefficients),1);coefficients.seed=repmat(20261024,height(coefficients),1);writetable(coefficients,'mixed_model_coefficients.csv');save('mixed_model.mat','model','T','m','warningMessage','warningID','-v7.3');
result=struct('status','COMPLETE','formula','outcome ~ state + (1 + state | patient)','fit_method',model.FitMethod,'patients',numel(unique(T.patient)),'bouts',height(T),'warning_id',warningID,'warning_message',warningMessage,'git_head',m.git_head,'protocol_sha256',m.protocol_sha256,'seed',20261024);f=fopen('mixed_model_runtime.json','w','n','UTF-8');fprintf(f,'%s\n',jsonencode(result));fclose(f);
end
