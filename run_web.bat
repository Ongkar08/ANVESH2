@echo off
setlocal
set "PATH=C:\Program Files\nodejs\;%PATH%"
cd /d "%~dp0web"
echo ===================================================
echo Starting ANVESH Web Workstation (Port 5173)...
echo ===================================================
if exist "C:\Program Files\nodejs\npm.cmd" (
    call "C:\Program Files\nodejs\npm.cmd" run dev
) else (
    call npm run dev
)
pause
