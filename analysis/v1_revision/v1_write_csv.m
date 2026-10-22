function v1_write_csv(T,file,append)
% 17-digit doubles and RFC-4180 quoting; provenance columns are in each row.
if nargin<3,append=false;end
newFile=~isfile(file);mode='w';if append,mode='a';end
f=fopen(file,mode);assert(f>=0,'v1:CSV','Cannot open output CSV');c=onCleanup(@() fclose(f)); %#ok<NASGU>
if ~append||newFile,fprintf(f,'%s\n',strjoin(T.Properties.VariableNames,','));end
for i=1:height(T)
 for j=1:width(T)
  if j>1,fprintf(f,',');end
  v=T{i,j};
  if isnumeric(v)||islogical(v),fprintf(f,'%.17g',double(v));
  else
   s=char(string(v));s=strrep(s,'"','""');fprintf(f,'"%s"',s);
  end
 end
 fprintf(f,'\n');
end
end
