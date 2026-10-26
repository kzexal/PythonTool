
@echo off
setlocal

cd /d "%~dp0"

if not exist "output" mkdir "output"

".venv\Scripts\python.exe" "main.py" >> "output\scheduled_run.log" 2>&1

exit /b %errorlevel%
