@echo off
REM start_jarvis.bat - Windows startup script

cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
	echo Virtual environment not found. Create it first:
	echo python -m venv venv
	pause
	exit /b 1
)

call "venv\Scripts\activate.bat"
python main.py

echo.
echo Jarvis stopped. Press any key to close...
pause >nul
