# English Master Android 打包指南

## 方法一：GitHub Actions 自动构建（推荐 ⭐）

最简单的方式，无需本地配置。

### 步骤

1. **将代码推送到 GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/english-master.git
   git push -u origin main
   ```

2. **触发构建**
   - 访问 GitHub 仓库 → Actions 标签
   - 点击 "Build Android APK" workflow
   - 点击 "Run workflow"

3. **下载 APK**
   - 构建完成后，在 Actions 页面下载 `english-master-apk` artifact
   - 解压得到 `englishmaster-1.0.0-arm64-v8a_armeabi-v7a-debug.apk`

### 构建时间
- 首次构建：15-30 分钟（下载 Android SDK/NDK）
- 后续构建：5-10 分钟

---

## 方法二：本地 WSL2 + buildozer

### 前置条件
- Windows 10/11 64位
- 管理员权限

### 步骤

1. **运行安装脚本**（管理员 PowerShell）
   ```powershell
   # 以管理员身份运行 PowerShell
   cd C:\Users\songpeili\.qclaw\workspace-agent-pc\english-master
   .\setup_wsl_buildozer.ps1
   ```

2. **重启电脑**

3. **进入 WSL 并构建**
   ```bash
   wsl -d Ubuntu
   cd ~/english-master
   ~/.local/bin/buildozer android debug
   ```

4. **获取 APK**
   - 构建完成后，APK 在 `bin/` 目录
   - Windows 路径：`\\wsl$\Ubuntu\home\<username>\english-master\bin\`

---

## 方法三：Docker（高级用户）

```bash
# 使用 kivy/buildozer 镜像
docker run -it --rm \
  -v $(pwd):/home/user/app \
  -v ~/.buildozer:/home/user/.buildozer \
  kivy/buildozer android debug
```

---

## APK 安装

### 安装到 Android 设备

1. **开启开发者选项**
   - 设置 → 关于手机 → 连续点击"版本号"7次
   - 返回 → 系统 → 开发者选项 → 开启"USB调试"

2. **连接电脑**
   ```bash
   adb devices  # 确认设备已连接
   adb install englishmaster-1.0.0-arm64-v8a-debug.apk
   ```

3. **或直接在手机上安装**
   - 将 APK 复制到手机
   - 文件管理器点击安装（需允许"未知来源"）

---

## 常见问题

### Q: 中文显示为方块？
**A**: 字体已打包在 `fonts/NotoSansSC-Regular.ttf`，代码会自动检测 Android 环境并加载。

### Q: 构建失败 "No module named 'android'"？
**A**: 这是正常的，buildozer 会自动处理 Android 依赖。

### Q: APK 文件太大？
**A**: 首次构建包含完整 Python 环境（约 50MB），这是正常的。

### Q: 如何发布到 Google Play？
**A**: 
1. 生成签名密钥：`keytool -genkey -v ...`
2. 修改 buildozer.spec：`android.release_artifact = apk`
3. 构建 release 版本：`buildozer android release`
4. 使用 jarsigner 签名
5. 上传到 Google Play Console

---

## 文件结构

```
english-master/
├── main.py              # 主入口（Android 兼容版）
├── main_v2.py           # 原版（Windows 专用）
├── buildozer.spec       # buildozer 配置
├── icon.png             # 应用图标
├── fonts/
│   └── NotoSansSC-Regular.ttf  # 中文字体
├── .github/workflows/
│   └── build-android.yml       # GitHub Actions
├── setup_wsl_buildozer.ps1     # WSL 安装脚本
└── ANDROID_BUILD.md            # 本文件
```
