function cfg=validation_settings(profile)
persistent settings
if isempty(settings),settings=jsondecode(fileread(fullfile(fileparts(mfilename('fullpath')),'configuration.json')));end
cfg=settings.(char(profile));cfg.amplitude_grid_hz=cfg.amplitude_grid_hz(:).';cfg.phase_grid_hz=cfg.phase_grid_hz(:).';
end
