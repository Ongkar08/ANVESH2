@echo off
cd /d "%~dp0"
echo ===================================================
echo Pushing ANVESH Project to GitHub...
echo Target: https://github.com/Ongkar08/ANVESH.git
echo ===================================================
echo.
git push -u origin main
echo.
echo ===================================================
pause
