#!/bin/bash
# English Master - WSL/Linux 运行脚本

cd "$(dirname "$0")"

echo "═══════════════════════════════════════"
echo "  English Master - Desktop Runner"
echo "═══════════════════════════════════════"

# 检查虚拟环境
if [ -d "venv" ]; then
    echo "[√] Found virtual environment"
    source venv/bin/activate
fi

# 检查依赖
python3 -c "import kivy; import kivymd" 2>/dev/null || {
    echo "[!] Installing dependencies..."
    pip3 install kivy kivymd -q
}

echo "Starting app..."
python3 main.py
