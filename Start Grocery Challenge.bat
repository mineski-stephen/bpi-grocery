@echo off
setlocal
title BPI Grocery Challenge

REM ============================================================
REM  Double-click this file to start the BPI Grocery Challenge.
REM  It runs the local server and opens the Control panel in
REM  your browser. Close this window (or press Ctrl+C) to stop.
REM ============================================================

REM Always run from the folder this .bat lives in, so it works
REM no matter where it is launched from.
cd /d "%~dp0"

REM Find a Python command: prefer "python", fall back to the "py" launcher.
set "PY="
where python >nul 2>nul && set "PY=python"
if not defined PY (
    where py >nul 2>nul && set "PY=py"
)

if not defined PY goto :nopython

echo.
echo   Starting the BPI Grocery Challenge server...
echo   Your browser will open at http://localhost:8000/
echo   Keep this window open during the event. Press Ctrl+C to stop.
echo.

%PY% server.py

REM We only reach here after the server stops or fails to start.
echo.
echo   The server has stopped.
pause
exit /b 0

:nopython
echo.
echo   ERROR: Python was not found on this computer.
echo   Please install Python 3 from https://www.python.org and try again.
echo.
pause
exit /b 1
