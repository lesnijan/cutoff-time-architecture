@echo off
REM Cutoff Time API - Demo Launcher for Windows
REM

echo.
echo ====================================
echo   Cutoff Time API - Demo Launcher
echo ====================================
echo.

REM Check if Poetry is installed
where poetry >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Poetry is not installed!
    echo Please install Poetry first: https://python-poetry.org/docs/#installation
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
poetry install

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo [2/3] Starting Cutoff Time API...
echo.
echo ====================================
echo   Demo Dashboard:
echo   http://localhost:8080/static/demo.html
echo.
echo   API Documentation:
echo   http://localhost:8080/api/v1/docs
echo ====================================
echo.
echo [3/3] Server starting (press Ctrl+C to stop)...
echo.

poetry run uvicorn app.main:app --reload --port 8080

pause
