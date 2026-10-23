@echo off
title APC job runner (ecog_miller_motor) - close this window to stop
cd /d C:\Users\nghare\.brainstorm\process\revision_checks\ecog_miller_motor
set IDLE=0
:loop
set RAN=0
for %%f in (queue\*.bat) do (
  set RAN=1
  move "%%f" "running\%%~nxf" >nul
  echo %date% %time% START %%~nxf >> logs\runner.log
  call "running\%%~nxf" > "logs\%%~nf.out" 2>&1
  echo %date% %time% END %%~nxf done >> logs\runner.log
  move "running\%%~nxf" "done\%%~nxf" >nul
)
if exist STOP_RUNNER goto end
if "%RAN%"=="1" (set IDLE=0) else (set /a IDLE+=1)
if %IDLE% GEQ 2160 goto end
timeout /t 10 /nobreak >nul
goto loop
:end
echo %date% %time% runner stopped >> logs\runner.log
