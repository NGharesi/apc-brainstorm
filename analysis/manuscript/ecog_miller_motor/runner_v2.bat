@echo off
title APC job runner v2 (ecog_miller_motor) - close this window to stop
set R=C:\Users\nghare\.brainstorm\process\revision_checks\ecog_miller_motor
set IDLE=0
:loop
cd /d "%R%"
set RAN=0
for %%f in ("%R%\queue\*.bat") do (
  set RAN=1
  move "%%f" "%R%\running\%%~nxf" >nul
  echo START %%~nxf %time% >> "%R%\logs\runner.log"
  cmd /c ""%R%\running\%%~nxf"" > "%R%\logs\%%~nf.out" 2>&1
  echo END %%~nxf >> "%R%\logs\runner.log"
  move "%R%\running\%%~nxf" "%R%\done\%%~nxf" >nul
)
if exist "%R%\STOP_RUNNER" goto end
if "%RAN%"=="1" (set IDLE=0) else (set /a IDLE+=1)
if %IDLE% GEQ 2160 goto end
timeout /t 10 /nobreak >nul
goto loop
:end
echo runner v2 stopped >> "%R%\logs\runner.log"
