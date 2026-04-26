@echo off
echo Creating virtual environment...
python -m venv venv
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to create virtual environment! Is Python installed and in your PATH?
    pause
    exit /b %ERRORLEVEL%
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Pip install failed! Please check the red text above.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Setup complete! You can now double-click start_automation.bat to run the script.
pause
