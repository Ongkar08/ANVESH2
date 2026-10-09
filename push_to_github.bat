@echo off
cd /d "%~dp0"
echo ===================================================
echo Pushing ANVESH Project to GitHub Repository: ANVESH2
echo Target: https://github.com/Ongkar08/ANVESH2.git
echo ===================================================
echo.
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ===================================================
    echo [SUCCESS] Successfully pushed all files to ANVESH2!
    echo URL: https://github.com/Ongkar08/ANVESH2
    echo ===================================================
) else (
    echo ===================================================
    echo [NOTE] If repository 'ANVESH2' does not exist yet on GitHub:
    echo 1. Open https://github.com/new in your browser
    echo 2. Set Repository name: ANVESH2
    echo 3. Keep it Public or Private
    echo 4. Do NOT check "Add a README file"
    echo 5. Click "Create repository"
    echo 6. Run this script again!
    echo ===================================================
)
echo.
pause
