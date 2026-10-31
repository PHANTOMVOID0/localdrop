@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" goto run
where py >nul 2>&1
if errorlevel 1 (python setup.py) else (py -3 setup.py)
if errorlevel 1 goto fail
:run
".venv\Scripts\python.exe" server.py %*
if errorlevel 1 goto fail
exit /b 0
:fail
echo.
echo LocalDrop could not start. Read the error above and docs\TROUBLESHOOTING.md.
pause
exit /b 1
