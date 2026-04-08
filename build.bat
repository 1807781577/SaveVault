@echo off
chcp 65001 >nul
echo ====================================
echo   游戏存档备份工具 - 打包脚本
echo ====================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)

REM 安装 PyInstaller
echo [1/3] 正在安装 PyInstaller...
pip install pyinstaller -q

REM 打包
echo [2/3] 正在打包程序...
pyinstaller --onefile --windowed --name "游戏存档备份工具" --icon=NONE game_save_manager.py

if errorlevel 1 (
    echo [错误] 打包失败
    pause
    exit /b 1
)

echo [3/3] 打包完成！
echo.
echo 输出文件: dist\游戏存档备份工具.exe
echo.
pause
