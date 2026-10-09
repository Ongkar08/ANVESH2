@echo off
setlocal
title Launching ANVESH Platform

echo =====================================================================
echo Launching ANVESH Full Cyber Forensic Web Platform...
echo =====================================================================
echo.

REM 1. Start Backend Server in a dedicated window
echo [1/2] Starting FastAPI Core Backend (Port 8000)...
start "ANVESH Backend Core" cmd /c "%~dp0run_backend.bat"

REM 2. Wait 3 seconds for backend to initialize
timeout /t 3 /nobreak >nul

REM 3. Start Web Workstation in a dedicated window
echo [2/2] Starting React Web Workstation (Port 5173)...
start "ANVESH Web Workstation" cmd /c "%~dp0run_web.bat"

REM 4. Wait 3 seconds and open browser
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo.
echo =====================================================================
echo ANVESH Platform is online!
echo  * Web Workstation: http://localhost:5173
echo  * Backend API:     http://localhost:8000/docs
echo =====================================================================
timeout /t 5 /nobreak >nul
