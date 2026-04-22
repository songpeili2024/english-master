# 📱 English Master - 英语口语练习 App

基于间隔重复（Spaced Repetition）算法的英语翻译练习应用。

## 功能特性

✅ **智能出题** - 根据设置难度等级推送句子
✅ **翻译练习** - 中文 → 英文翻译，系统自动评判
✅ **即时反馈** - 指出翻译差异，给出地道表达建议
✅ **单词库** - 一键将关键词加入单词复习库
✅ **间隔重复** - SM-2 算法决定复习时机，科学抗遗忘
✅ **动态难度** - 自动跟踪水平，升降级平滑过渡
✅ **本地存储** - 所有数据存本地 JSON，无网络依赖
✅ **学习统计** - 正确率趋势、连续天数、数据可视化

## 难度等级

| 等级 | 描述 | 例句 |
|------|------|------|
| 1 | 初中词汇，短句 | "Hello." |
| 2 | 高中词汇，简单复合句 | "I went to the supermarket yesterday." |
| 3 | 四级词汇，从句 | "The book that I bought was expensive." |
| 4 | 托福，长句习语 | "Don't put all your eggs in one basket." |
| 5 | 雅思/GRE，复杂俚语 | "Break a leg!" |

## 项目结构

```
english-master/
├── main.py              # 主程序入口 + 所有业务逻辑
├── main.kv              # KivyMD 界面布局
├── SPEC.md               # 产品规格文档
├── requirements.txt      # Python 依赖
├── buildozer.spec        # 安卓打包配置
├── data/                 # 数据文件（运行后自动生成）
│   ├── sentences.json    # 句库
│   └── user_progress.json # 用户进度
└── README.md
```

## 快速本地运行（Windows）

```bash
# 1. 安装 Python 3.10+
# 2. 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行（桌面预览）
python main.py
```

## 打包成 Android APK

### 方式一：使用 Buildozer（推荐，在 Linux / WSL）

```bash
# 安装 Buildozer
pip install buildozer

# 安装 Android SDK（首次）
buildozer android debug deploy run

# 或者完整构建
buildozer android debug
```

### 方式二：在 Windows 上用模拟器测试

```bash
# 安装 Android Studio + SDK
# 创建虚拟设备（Pixel 4 / API 30）

# 编译 APK
python -m buildozer android debug
```

### 方式三：本地导出 APK

```bash
# 确保已安装 Android NDK 和 SDK
# 编辑 buildozer.spec 设置路径
# 运行构建
buildozer android debug
```

APK 输出路径: `bin/englishmaster-1.0.0-arm64-v8a_armeabi-v7a-debug.apk`

## 句库扩展

编辑 `data/sentences.json` 添加更多句子，格式：

```json
{
  "id": "L1_001",
  "level": 1,
  "source": "老友记 S1",
  "chinese": "和你聊天很开心。",
  "english": "It's so nice talking to you.",
  "keywords": ["nice", "talking"],
  "tags": ["greeting", "social"]
}
```

字段说明：
- `level`: 难度 1-5
- `source`: 句子出处（电影/教材/通用）
- `keywords`: 可加入单词库的关键词
- `tags`: 话题标签

## 算法说明

### 间隔重复（SM-2 变体）
- 新句子：当日复习
- 正确 1 次：间隔 1 天
- 正确 2 次：间隔 3 天
- 正确 3 次：间隔 7 天
- 正确 4 次：间隔 14 天
- 正确 5 次：间隔 30 天
- 错误：重置回 1 天

### 难度自动调整
- 最近 20 题正确率 ≥ 80% → 建议升级
- 最近 5 题错误 ≥ 3 次 → 建议降级
- 当前版本：降级提示（升级自动生效）

## 截图预览

```
┌─────────────────────────┐
│ English Master          │
│ 句子 3 / 10             │
│ ████████░░░░            │
│ 来源: 老友记 S1 | 等级 2 │
├─────────────────────────┤
│                         │
│  "和你聊天很开心。"       │
│                         │
│ [___________________]   │
│ [    提交翻译 ✓    ]     │
├─────────────────────────┤
│ ✓ 正确！                  │
│ 正确翻译：               │
│ It's so nice talking    │
│ to you.                 │
│ 📝 整体正确，nice更地道  │
│ [nice] [talking]        │
│ [    下一题 →    ]       │
└─────────────────────────┘
```
