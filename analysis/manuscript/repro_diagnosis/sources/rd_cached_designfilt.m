function d=rd_cached_designfilt(fs,band)
persistent keys objects
if isempty(keys),keys={};objects={};end
key=sprintf('%.17g,%.17g,%.17g',fs,band(1),band(2));j=find(strcmp(keys,key),1);
if isempty(j)
 d=designfilt('bandpassiir','FilterOrder',4,'HalfPowerFrequency1',band(1),'HalfPowerFrequency2',band(2),'SampleRate',fs);
 keys{end+1}=key;objects{end+1}=d;
else
 d=objects{j};
end
end
