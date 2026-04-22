"""
English Master - 简化版（纯 Python UI）
英语口语翻译练习应用
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')

from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import ScreenManager

# ─── 跨平台中文字体路径 ──────────────────────────────
import sys
import os

def _get_chinese_font():
    """自动检测平台并返回可用的中文字体路径"""
    # Android: 字体打包在 assets/fonts/ 或系统字体
    if 'ANDROID_ARGUMENT' in os.environ or hasattr(sys, '_MEIPASS'):
        # p4a 打包后，字体在 app 内部
        font_paths = [
            './fonts/NotoSansSC-Regular.ttf',
            '/system/fonts/NotoSansCJK-Regular.ttc',
            '/system/fonts/DroidSansFallbackFull.ttf',
            './assets/fonts/NotoSansSC-Regular.ttf',
        ]
        for fp in font_paths:
            if os.path.exists(fp):
                return fp
        return './fonts/NotoSansSC-Regular.ttf'  # fallback
    
    # Windows
    elif sys.platform == 'win32':
        win_fonts = [
            'C:/Windows/Fonts/msyh.ttc',      # 微软雅黑
        ]
        for fp in win_fonts:
            if os.path.exists(fp):
                return fp
    
    # macOS
    elif sys.platform == 'darwin':
        mac_fonts = [
            '/System/Library/Fonts/PingFang.ttc',
            '/System/Library/Fonts/STHeiti Light.ttc',
        ]
        for fp in mac_fonts:
            if os.path.exists(fp):
                return fp
    
    # Linux
    else:
        linux_fonts = [
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc',
        ]
        for fp in linux_fonts:
            if os.path.exists(fp):
                return fp
    
    # 最终 fallback - 返回空字符串，使用 Kivy 默认字体
    return ''

CHINESE_FONT = _get_chinese_font()

# 注册字体到 Kivy（如果找到了字体文件）
if CHINESE_FONT and os.path.exists(CHINESE_FONT):
    try:
        LabelBase.register(name='ChineseFont', fn_regular=CHINESE_FONT)
        CHINESE_FONT = 'ChineseFont'
    except Exception:
        CHINESE_FONT = ''

# ─── 数据目录 ───────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

PROGRESS_FILE = DATA_DIR / "user_progress.json"


# ═══════════════════════════════════════════════════════════
#  简化数据管理
# ═══════════════════════════════════════════════════════════

class DataManager:
    """用户数据和句子库"""
    
    # 内置句子库
    SENTENCES = [
        # Level 1
        {"id": "L1_01", "level": 1, "chinese": "你好。", "english": "Hello."},
        {"id": "L1_02", "level": 1, "chinese": "你好吗？", "english": "How are you?"},
        {"id": "L1_03", "level": 1, "chinese": "很高兴认识你。", "english": "Nice to meet you."},
        {"id": "L1_04", "level": 1, "chinese": "谢谢你的帮助。", "english": "Thanks for your help."},
        {"id": "L1_05", "level": 1, "chinese": "我叫李明。", "english": "My name is Li Ming."},
        {"id": "L1_06", "level": 1, "chinese": "我很好。", "english": "I'm good."},
        {"id": "L1_07", "level": 1, "chinese": "这个多少钱？", "english": "How much is this?"},
        {"id": "L1_08", "level": 1, "chinese": "我迷路了。", "english": "I'm lost."},
        {"id": "L1_09", "level": 1, "chinese": "请问，厕所在哪里？", "english": "Excuse me, where is the restroom?"},
        {"id": "L1_10", "level": 1, "chinese": "今天天气很好。", "english": "The weather is nice today."},
        # Level 2
        {"id": "L2_01", "level": 2, "chinese": "我们去看电影吧。", "english": "Let's go watch a movie."},
        {"id": "L2_02", "level": 2, "chinese": "你周末有什么计划？", "english": "What are your plans for the weekend?"},
        {"id": "L2_03", "level": 2, "chinese": "我喜欢喝咖啡。", "english": "I like drinking coffee."},
        {"id": "L2_04", "level": 2, "chinese": "这本书很有意思。", "english": "This book is very interesting."},
        {"id": "L2_05", "level": 2, "chinese": "你几点下班？", "english": "What time do you get off work?"},
        # Level 3
        {"id": "L3_01", "level": 3, "chinese": "如果你有空的话，我们一起吃饭吧。", "english": "If you're free, let's have dinner together."},
        {"id": "L3_02", "level": 3, "chinese": "我觉得这个问题很难回答。", "english": "I think this question is hard to answer."},
        {"id": "L3_03", "level": 3, "chinese": "他昨天告诉我他会来的。", "english": "He told me yesterday that he would come."},
    ]
    
    def __init__(self):
        self.progress = self._load_progress()
    
    def _load_progress(self):
        if PROGRESS_FILE.exists():
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "level": 1,
            "daily_goal": 10,
            "practiced": 0,
            "correct": 0,
            "history": []
        }
    
    def save(self):
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.progress, f, ensure_ascii=False, indent=2)
    
    def get_sentences(self, level, count):
        """获取指定等级的随机句子"""
        pool = [s for s in self.SENTENCES if s["level"] <= level]
        return random.sample(pool, min(count, len(pool)))
    
    def check_answer(self, user_input, correct_answer):
        """检查答案（简化版：忽略大小写和标点）"""
        user = user_input.lower().strip().replace(".", "").replace("?", "").replace("!", "")
        correct = correct_answer.lower().strip().replace(".", "").replace("?", "").replace("!", "")
        return user == correct


# ═══════════════════════════════════════════════════════════
#  欢迎页
# ═══════════════════════════════════════════════════════════

class WelcomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "welcome"
        
        # 主布局
        layout = BoxLayout(orientation="vertical", padding=40, spacing=20)
        
        # 背景色
        with layout.canvas.before:
            Color(0.96, 0.96, 0.98, 1)
            self.rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda obj, val: setattr(self.rect, 'pos', val))
        layout.bind(size=lambda obj, val: setattr(self.rect, 'size', val))
        
        # 弹性空间
        layout.add_widget(BoxLayout())
        
        # 标题
        title = Label(
            text="English Master",
            font_size="32sp",
            bold=True,
            halign="center",
            size_hint_y=None,
            height=80,
            color=(0.18, 0.53, 0.82, 1),
            font_name=CHINESE_FONT
        )
        layout.add_widget(title)
        
        # 副标题
        subtitle = Label(
            text="口语翻译 · 间隔重复 · 智能难度",
            font_size="16sp",
            halign="center",
            size_hint_y=None,
            height=40,
            color=(0.4, 0.4, 0.4, 1),
            font_name=CHINESE_FONT
        )
        layout.add_widget(subtitle)
        
        # 弹性空间
        layout.add_widget(BoxLayout())
        
        # 说明
        desc = Label(
            text="科学的间隔重复算法\n地道电影/教材原句\n动态难度调整",
            font_size="14sp",
            halign="center",
            size_hint_y=None,
            height=100,
            color=(0.4, 0.4, 0.4, 1),
            font_name=CHINESE_FONT
        )
        layout.add_widget(desc)
        
        # 弹性空间
        layout.add_widget(BoxLayout())
        
        # 开始按钮
        btn = Button(
            text="开始学习",
            font_size="18sp",
            size_hint=(0.8, None),
            height=56,
            background_color=(0.18, 0.53, 0.82, 1),
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5},
            font_name=CHINESE_FONT
        )
        btn.bind(on_release=self.go_practice)
        layout.add_widget(btn)
        
        # 弹性空间
        layout.add_widget(BoxLayout())
        
        self.add_widget(layout)
    
    def go_practice(self, instance):
        app = MDApp.get_running_app()
        app.start_practice()


# ═══════════════════════════════════════════════════════════
#  练习页
# ═══════════════════════════════════════════════════════════

class PracticeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "practice"
        self.sentences = []
        self.current_index = 0
        self.correct_count = 0
        
        # 主布局
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=16)
        
        # 背景色
        with self.layout.canvas.before:
            Color(0.96, 0.96, 0.98, 1)
            self.rect = Rectangle(pos=self.layout.pos, size=self.layout.size)
        self.layout.bind(pos=lambda obj, val: setattr(self.rect, 'pos', val))
        self.layout.bind(size=lambda obj, val: setattr(self.rect, 'size', val))
        
        # 进度标签
        self.progress_label = Label(
            text="句子 1 / 10",
            font_size="14sp",
            halign="center",
            size_hint_y=None,
            height=30,
            color=(0.4, 0.4, 0.4, 1),
            font_name=CHINESE_FONT
        )
        self.layout.add_widget(self.progress_label)
        
        # 进度条
        self.progress_bar = ProgressBar(value=10, max=100, size_hint_y=None, height=6)
        self.layout.add_widget(self.progress_bar)
        
        # 弹性空间
        self.layout.add_widget(BoxLayout())
        
        # 中文句子卡片
        card = FloatLayout(size_hint=(1, None), height=140)
        with card.canvas.before:
            Color(1, 1, 1, 1)
            RoundedRectangle(pos=card.pos, size=card.size, radius=[16])
        def update_card_pos(obj, val):
            card.canvas.before.children[-1].pos = val
        def update_card_size(obj, val):
            card.canvas.before.children[-1].size = val
        card.bind(pos=update_card_pos)
        card.bind(size=update_card_size)
        
        self.chinese_label = Label(
            text="",
            font_size="20sp",
            bold=True,
            halign="center",
            valign="middle",
            color=(0.1, 0.1, 0.1, 1),
            font_name=CHINESE_FONT,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        card.add_widget(self.chinese_label)
        self.layout.add_widget(card)
        
        # 输入提示
        self.layout.add_widget(Label(
            text="请将句子翻译成英文：",
            font_size="14sp",
            size_hint_y=None,
            height=30,
            color=(0.4, 0.4, 0.4, 1),
            font_name=CHINESE_FONT
        ))
        
        # 输入框
        self.input_field = TextInput(
            hint_text="输入你的翻译...",
            size_hint_y=None,
            height=52,
            font_size="16sp",
            multiline=False,
            font_name=CHINESE_FONT,
            background_color=(1, 1, 1, 1),
            foreground_color=(0.1, 0.1, 0.1, 1)
        )
        self.input_field.bind(on_text_validate=self.submit)
        self.layout.add_widget(self.input_field)
        
        # 提交按钮
        submit_btn = Button(
            text="提交翻译",
            size_hint=(1, None),
            height=50,
            background_color=(0.18, 0.53, 0.82, 1),
            color=(1, 1, 1, 1),
            font_name=CHINESE_FONT
        )
        submit_btn.bind(on_release=self.submit)
        self.layout.add_widget(submit_btn)
        
        # 反馈标签
        self.feedback_label = Label(
            text="",
            font_size="16sp",
            halign="center",
            size_hint_y=None,
            height=80,
            color=(0.4, 0.4, 0.4, 1),
            font_name=CHINESE_FONT
        )
        self.layout.add_widget(self.feedback_label)
        
        # 下一题按钮
        next_btn = Button(
            text="下一题",
            size_hint=(0.8, None),
            height=50,
            background_color=(0.18, 0.53, 0.82, 1),
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5},
            font_name=CHINESE_FONT
        )
        next_btn.bind(on_release=self.next_sentence)
        self.layout.add_widget(next_btn)
        
        # 弹性空间
        self.layout.add_widget(BoxLayout())
        
        self.add_widget(self.layout)
    
    def load_sentences(self, sentences):
        self.sentences = sentences
        self.current_index = 0
        self.correct_count = 0
        self.show_sentence()
    
    def show_sentence(self):
        if self.current_index >= len(self.sentences):
            self.show_complete()
            return
        
        s = self.sentences[self.current_index]
        self.chinese_label.text = s["chinese"]
        self.current_sentence = s
        self.input_field.text = ""
        self.feedback_label.text = ""
        
        # 更新进度
        self.progress_label.text = f"句子 {self.current_index + 1} / {len(self.sentences)}"
        self.progress_bar.value = (self.current_index + 1) / len(self.sentences) * 100
    
    def submit(self, instance):
        if not self.input_field.text.strip():
            return
        
        app = MDApp.get_running_app()
        user_input = self.input_field.text.strip()
        correct = app.data.check_answer(user_input, self.current_sentence["english"])
        
        if correct:
            self.correct_count += 1
            self.feedback_label.text = f"正确！\n{self.current_sentence['english']}"
            self.feedback_label.color = (0.2, 0.6, 0.2, 1)
        else:
            self.feedback_label.text = f"再想想\n正确答案：{self.current_sentence['english']}"
            self.feedback_label.color = (0.8, 0.2, 0.2, 1)
        
        # 记录
        app.data.progress["practiced"] += 1
        if correct:
            app.data.progress["correct"] += 1
        app.data.save()
    
    def next_sentence(self, instance):
        self.current_index += 1
        self.show_sentence()
    
    def show_complete(self):
        app = MDApp.get_running_app()
        app.show_complete(self.correct_count, len(self.sentences))


# ═══════════════════════════════════════════════════════════
#  完成页
# ═══════════════════════════════════════════════════════════

class CompleteScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "complete"
        
        layout = BoxLayout(orientation="vertical", padding=40, spacing=20)
        
        # 背景色
        with layout.canvas.before:
            Color(0.96, 0.96, 0.98, 1)
            self.rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda obj, val: setattr(self.rect, 'pos', val))
        layout.bind(size=lambda obj, val: setattr(self.rect, 'size', val))
        
        # 弹性空间
        layout.add_widget(BoxLayout())
        
        # 完成图标
        layout.add_widget(Label(
            text="Complete!",
            font_size="48sp",
            halign="center",
            size_hint_y=None,
            height=100,
            font_name=CHINESE_FONT
        ))
        
        # 统计标签
        self.stats_label = Label(
            text="今日练习完成！",
            font_size="20sp",
            halign="center",
            size_hint_y=None,
            height=60,
            color=(0.1, 0.1, 0.1, 1),
            font_name=CHINESE_FONT
        )
        layout.add_widget(self.stats_label)
        
        # 弹性空间
        layout.add_widget(BoxLayout())
        
        # 继续练习按钮
        continue_btn = Button(
            text="继续练习",
            size_hint=(0.8, None),
            height=56,
            background_color=(0.18, 0.53, 0.82, 1),
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5},
            font_name=CHINESE_FONT
        )
        continue_btn.bind(on_release=self.continue_practice)
        layout.add_widget(continue_btn)
        
        # 统计按钮
        stats_btn = Button(
            text="查看统计",
            size_hint=(0.6, None),
            height=48,
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5},
            font_name=CHINESE_FONT
        )
        stats_btn.bind(on_release=self.go_stats)
        layout.add_widget(stats_btn)
        
        # 弹性空间
        layout.add_widget(BoxLayout())
        
        self.add_widget(layout)
    
    def set_stats(self, correct, total):
        rate = int(correct / total * 100) if total > 0 else 0
        self.stats_label.text = f"完成！正确 {correct}/{total}（{rate}%）"
    
    def continue_practice(self, instance):
        app = MDApp.get_running_app()
        app.start_practice()
    
    def go_stats(self, instance):
        app = MDApp.get_running_app()
        app.switch_screen("stats")


# ═══════════════════════════════════════════════════════════
#  统计页
# ═══════════════════════════════════════════════════════════

class StatsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "stats"
        
        layout = BoxLayout(orientation="vertical", padding=20, spacing=16)
        
        # 背景色
        with layout.canvas.before:
            Color(0.96, 0.96, 0.98, 1)
            self.rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda obj, val: setattr(self.rect, 'pos', val))
        layout.bind(size=lambda obj, val: setattr(self.rect, 'size', val))
        
        # 标题
        layout.add_widget(Label(
            text="学习统计",
            font_size="22sp",
            halign="center",
            size_hint_y=None,
            height=60,
            color=(0.18, 0.53, 0.82, 1),
            font_name=CHINESE_FONT
        ))
        
        # 统计卡片
        card = FloatLayout(size_hint=(1, None), height=220)
        with card.canvas.before:
            Color(1, 1, 1, 1)
            RoundedRectangle(pos=card.pos, size=card.size, radius=[16])
        card.bind(pos=lambda obj, val: card.canvas.before.children[-1].__setattr__('pos', val))
        card.bind(size=lambda obj, val: card.canvas.before.children[-1].__setattr__('size', val))
        
        self.stats_label = Label(
            text="加载中...",
            font_size="16sp",
            halign="left",
            valign="top",
            color=(0.1, 0.1, 0.1, 1),
            font_name=CHINESE_FONT,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        card.add_widget(self.stats_label)
        layout.add_widget(card)
        
        # 弹性空间
        layout.add_widget(BoxLayout())
        
        # 返回按钮
        back_btn = Button(
            text="返回练习",
            size_hint=(0.8, None),
            height=50,
            background_color=(0.18, 0.53, 0.82, 1),
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5},
            font_name=CHINESE_FONT
        )
        back_btn.bind(on_release=lambda x: self.go_back())
        layout.add_widget(back_btn)
        
        # 弹性空间
        layout.add_widget(BoxLayout())
        
        self.add_widget(layout)
    
    def on_enter(self):
        app = MDApp.get_running_app()
        p = app.data.progress
        rate = int(p["correct"] / p["practiced"] * 100) if p["practiced"] > 0 else 0
        
        self.stats_label.text = f"""等级: {p.get('level', 1)}

每日目标: {p.get('daily_goal', 10)} 句

已练习: {p['practiced']} 句

正确: {p['correct']} 句

正确率: {rate}%"""
    
    def go_back(self):
        app = MDApp.get_running_app()
        app.switch_screen("practice")


# ═══════════════════════════════════════════════════════════
#  主应用
# ═══════════════════════════════════════════════════════════

class EnglishMasterApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        # 初始化数据
        self.data = DataManager()
        
        # 屏幕管理器
        self.sm = ScreenManager()
        self.sm.add_widget(WelcomeScreen())
        self.sm.add_widget(PracticeScreen())
        self.sm.add_widget(CompleteScreen())
        self.sm.add_widget(StatsScreen())
        
        return self.sm
    
    def switch_screen(self, name):
        self.sm.current = name
    
    def start_practice(self):
        level = self.data.progress.get("level", 1)
        goal = self.data.progress.get("daily_goal", 10)
        sentences = self.data.get_sentences(level, goal)
        
        practice_screen = self.sm.get_screen("practice")
        practice_screen.load_sentences(sentences)
        
        self.sm.current = "practice"
    
    def show_complete(self, correct, total):
        complete_screen = self.sm.get_screen("complete")
        complete_screen.set_stats(correct, total)
        self.sm.current = "complete"


if __name__ == "__main__":
    EnglishMasterApp().run()
