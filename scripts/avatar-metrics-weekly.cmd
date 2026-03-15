@echo off
REM Weekly avatar metrics check + auto-regeneration
REM Runs via Windows Task Scheduler every Sunday at 3 AM
REM Logs output to portfolio/logs/

setlocal
set LOGDIR=C:\Users\dbhav\Projects\portfolio\logs
if not exist "%LOGDIR%" mkdir "%LOGDIR%"

set LOGFILE=%LOGDIR%\avatar-metrics-%date:~-4,4%%date:~-7,2%%date:~-10,2%.log

echo [%date% %time%] Starting avatar metrics update >> "%LOGFILE%" 2>&1

cd /d C:\Users\dbhav\Projects\isabelle
.venv\Scripts\python.exe ..\portfolio\scripts\update-avatar-metrics.py --apply >> "%LOGFILE%" 2>&1

echo [%date% %time%] Done >> "%LOGFILE%" 2>&1
