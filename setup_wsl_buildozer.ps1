# WSL2 + buildozer 安装脚本
# 以管理员身份运行

Write-Host "=== English Master Android 打包环境设置 ===" -ForegroundColor Green

# 1. 启用 WSL2
Write-Host "[1/5] 启用 WSL2..." -ForegroundColor Cyan
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 2. 设置 WSL 默认版本为 2
wsl --set-default-version 2

# 3. 安装 Ubuntu
Write-Host "[2/5] 安装 Ubuntu..." -ForegroundColor Cyan
wsl --install -d Ubuntu

Write-Host "[3/5] 等待 Ubuntu 初始化..." -ForegroundColor Cyan
Write-Host "请按提示设置 Ubuntu 用户名和密码" -ForegroundColor Yellow
wsl -d Ubuntu -e echo "Ubuntu ready"

# 4. 在 Ubuntu 中安装 buildozer 和依赖
Write-Host "[4/5] 在 Ubuntu 中安装 buildozer..." -ForegroundColor Cyan
wsl -d Ubuntu -e bash -c "
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev automake
pip3 install --user buildozer cython
"

# 5. 复制项目到 WSL
Write-Host "[5/5] 复制项目到 WSL..." -ForegroundColor Cyan
$ProjectPath = "C:\Users\songpeili\.qclaw\workspace-agent-pc\english-master"
$WslPath = "/home/`$(whoami)/english-master"
wsl -d Ubuntu -e bash -c "mkdir -p $WslPath"
Get-ChildItem -Path $ProjectPath -Recurse | ForEach-Object {
    $relativePath = $_.FullName.Substring($ProjectPath.Length + 1)
    if ($_.PSIsContainer) {
        wsl -d Ubuntu -e mkdir -p "$WslPath/$relativePath"
    } else {
        $content = [System.IO.File]::ReadAllBytes($_.FullName)
        $base64 = [Convert]::ToBase64String($content)
        wsl -d Ubuntu -e bash -c "echo '$base64' | base64 -d > '$WslPath/$relativePath'"
    }
}

Write-Host "=== 安装完成 ===" -ForegroundColor Green
Write-Host "请重启电脑后运行: wsl -d Ubuntu" -ForegroundColor Yellow
Write-Host "然后在 Ubuntu 中运行: cd ~/english-master && ~/.local/bin/buildozer android debug" -ForegroundColor Yellow
