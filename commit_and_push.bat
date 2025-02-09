@echo off
cd /d "E:\--CODE--\25Q1_Fab_InkShow"
:: Ensure Git remote is set
git remote -v >nul 2>&1
if %errorlevel% neq 0 (
    git remote add origin https://github.com/fabertel/Fab_InkShow.git
)
:: Check if there are changes
git status | findstr /C:"nothing to commit" >nul
if %errorlevel% equ 0 (
    echo No changes to commit.
) else (
    git add -A
    git commit -m "Auto-commit"
    git push origin main
)
echo Done. Press any key to exit...
pause