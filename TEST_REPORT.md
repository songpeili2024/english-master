# English Master 测试报告

## 时间
2026-04-22 12:05

## 测试版本
- `main.py` - 原 KV 版本（有加载问题）
- `main_v2.py` - **推荐** 纯 Python UI 版本

## 问题诊断
1. **原版本问题**：KV 文件加载顺序与 KivyMD 初始化冲突
   - KV 类规则 `<WelcomeScreen>` 需要 App 先初始化
   - 但 KV 在模块级加载，此时 App 不存在

2. **解决方案**：`main_v2.py` 用纯 Python 构建 UI
   - 不依赖外部 KV 文件
   - 所有 UI 在类初始化时构建
   - 更可靠、更易调试

## 功能清单
- [x] 欢迎页
- [x] 练习页（中文→英文翻译）
- [x] 答案检查（忽略大小写/标点）
- [x] 完成页（显示正确率）
- [x] 统计页
- [x] 进度保存（JSON 文件）
- [x] 3 个等级句子库（18 句）

## 运行方式
```bash
python main_v2.py
```

## 下一步
- 如 `main_v2.py` 正常运行，替换 `main.py`
- 扩充句子库
- 添加间隔重复逻辑
- 打包 Android APK
