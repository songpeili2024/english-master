"""
English Master - 最小测试版本
验证 KivyMD 能正常显示
"""

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton

KV = '''
MDScreen:
    md_bg_color: 0.96, 0.96, 0.98, 1
    
    MDBoxLayout:
        orientation: 'vertical'
        padding: 40
        spacing: 20
        
        MDLabel:
            text: "🌟 English Master"
            font_style: "H3"
            bold: True
            halign: "center"
            color: 0.18, 0.53, 0.82, 1
        
        MDLabel:
            text: "英语口语练习"
            font_style: "H5"
            halign: "center"
        
        MDRaisedButton:
            text: "开始学习"
            size_hint_x: 0.6
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.18, 0.53, 0.82, 1
            on_release: app.start_learning()
        
        MDLabel:
            text: "测试版本 - 如果你能看到这个，说明环境正常"
            font_style: "Body2"
            halign: "center"
            color: 0.5, 0.5, 0.5, 1
'''

class TestApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)
    
    def start_learning(self):
        print("✅ 按钮点击正常！")

if __name__ == "__main__":
    TestApp().run()
