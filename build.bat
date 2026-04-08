@echo off
chcp 65001 >nul
echo ====================================
echo   SaveVault - Build Script
echo ====================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [Error] Python not found, please install Python 3.7+
    pause
    exit /b 1
)

REM Install PyInstaller
echo [1/3] Installing PyInstaller...
pip install pyinstaller -q

REM Build
echo [2/3] Building...
pyinstaller --onefile --windowed --name "SaveVault" savevault.py

if errorlevel 1 (
    echo [Error] Build failed
    pause
    exit /b 1
)

echo [3/3] Build complete!
echo.
echo Output: dist\SaveVault.exe
echo.
pause
