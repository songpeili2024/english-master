# APK 构建方案

## 方案 1: GitHub Actions（推荐）

**优点**：免费、云端构建、无需本地配置  
**缺点**：首次推送需要手动创建 GitHub 仓库

### 步骤：
1. 访问 https://github.com/new
2. Repository name: `english-master`
3. 点击 Create repository（不要勾选任何初始化选项）
4. 复制仓库地址给我

我帮你推送代码并触发构建。

---

## 方案 2: 本地 Docker（需要手动安装）

需要先安装：
1. WSL2：`wsl --install`（需要管理员权限，重启电脑）
2. Docker Desktop：https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe

安装后运行：
```bash
docker run -it --rm -v "C:\Users\songpeili\.qclaw\workspace-agent-pc\english-master:/home/user/app" kivy/buildozer android debug
```

---

## 当前状态

- ✅ Git 本地仓库已初始化
- ✅ 代码已提交（55 个文件）
- ⏳ 等待选择构建方案
