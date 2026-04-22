@echo off
chcp 65001 >nul
echo.
echo ═══════════════════════════════════════
echo   English Master - 桌面运行脚本
echo ═══════════════════════════════════════
echo.

cd /d "%~dp0"

:: 检查虚拟环境
if exist "venv\Scripts\python.exe" (
    echo [√] 发现虚拟环境
    call venv\Scripts\activate.bat
) else (
    echo [!] 使用系统 Python
)

:: 检查依赖
python -c "import kivy; import kivymd" 2>nul
if errorlevel 1 (
    echo [!] 首次运行，正在安装依赖...
    pip install kivy kivymd -q
    echo [√] 依赖安装完成
)

echo.
echo 启动应用...
echo ───────────────────────────────────────
python main.py
pause
