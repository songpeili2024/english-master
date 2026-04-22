# GitHub 仓库设置步骤

## 1. 创建 GitHub 仓库

访问 https://github.com/new

填写信息：
- **Repository name**: `english-master`
- **Description**: 英语口语翻译练习应用 - Android
- **Public** 或 **Private** 都可以
- ✅ Initialize with a README (可选)
- ✅ Add .gitignore: Python (可选)

点击 **Create repository**

## 2. 获取仓库地址

创建后，复制仓库地址，格式为：
```
https://github.com/YOUR_USERNAME/english-master.git
```

## 3. 推送代码

将地址告诉我，我会执行：
```bash
git remote add origin https://github.com/YOUR_USERNAME/english-master.git
git branch -M main
git push -u origin main
```

## 4. 触发构建

推送后：
1. 访问 GitHub 仓库页面
2. 点击 **Actions** 标签
3. 点击 **Build Android APK**
4. 点击 **Run workflow** → **Run workflow**

## 5. 下载 APK

等待 15-30 分钟后：
1. 进入完成的 workflow
2. 底部 **Artifacts** 区域
3. 下载 `english-master-apk`
4. 解压得到 APK 文件

---

## 替代方案：如果你不想用 GitHub

### 方案 A：Docker 本地构建
```bash
# 安装 Docker 后运行
docker run -it --rm -v "${PWD}:/home/user/app" kivy/buildozer android debug
```

### 方案 B：GitLab CI
创建 `.gitlab-ci.yml` 文件，类似 GitHub Actions 的配置。

### 方案 C：手动 WSL2
按照 `ANDROID_BUILD.md` 中的 WSL2 方案操作。
