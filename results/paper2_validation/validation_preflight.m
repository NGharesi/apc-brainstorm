function validation_preflight
O=fileparts(mfilename('fullpath'));root=fileparts(fileparts(O));repo=fullfile(root,'apc-brainstorm-publish');cd(O);
addpath(fullfile(repo,'results','paper2_ablation'),'-begin');addpath(fullfile(root,'revision_checks','final'),'-begin');addpath(O,'-begin');addpath(fullfile(repo,'src'),'-begin');
G=jsondecode(fileread(fullfile(O,'all_gate_results.json')));assert(strcmp(G.status,'PASS'));m=jsondecode(fileread(fullfile(O,'provenance.json')));
Q=readtable(fullfile(root,'revision_checks','final','burst_coupled_input.csv'),'Delimiter',',','NumHeaderLines',0,'ReadVariableNames',true,'Encoding','UTF-8');x=Q.signal;rows={};
for pair={{'V1','heldout'},{'V2','HA'},{'ecog','ecog'}}
 p=pair{1};[a,s]=scan_fa_given_fp(x,500,8,string(p{2}));[b,u]=validation_scan_fa(x,500,8,string(p{1}));assert(isequaln(a,b)&&isequaln(s,u),'Validation:ScanAdapter','Profile adapter changed original scan');
 cfg=validation_settings(p{1});mode="A2_prime";if cfg.amplitude_half_width_hz==30,mode="HA_A2_prime";end
 [a,amap]=a2_reference_map(x,500,string(p{2}),mode,.5);[b,bmap]=validation_a2_map(x,500,string(p{1}),mode,.5);
 assert(isequaln(a,b)&&isequaln(amap{1}.scores,bmap{1}.scores),'Validation:MapAdapter','Profile adapter changed original score computation');
 rows{end+1}=struct('profile',string(p{1}),'scan_identical',true,'a2_map_identical',true); %#ok<AGROW>
end
% Verify new V3/rodent profile rows against their own exact A2' map row.
for profile=["V3","rodent"]
 cfg=validation_settings(profile);mode="A2_prime";if profile=="rodent",mode="rodent_A2_prime";end
 [~,map]=validation_a2_map(x,500,profile,mode,.5);[~,s]=validation_scan_fa(x,500,8,profile);ip=find(map{1}.fp_grid_hz==8);
 assert(max(abs(s-map{1}.scores(ip,:,2)))<=1e-10,'Validation:NewProfile','New profile row differs');
 rows{end+1}=struct('profile',profile,'scan_identical',true,'a2_map_identical',true); %#ok<AGROW>
end
writejson(fullfile(O,'adapter_verification.json'),struct('status','PASS','rows',{rows},'provenance',m));fprintf('All profile adapters preserve exact computations\n');
end
function writejson(file,v),f=fopen(file,'w','n','UTF-8');assert(f>=0);c=onCleanup(@()fclose(f));fprintf(f,'%s\n',jsonencode(v));end
