"""测试中文显示"""
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRaisedButton

KV = '''
MDFloatLayout:
    md_bg_color: 0.96, 0.96, 0.98, 1
    
    MDLabel:
        text: "测试中文显示 Test English"
        font_style: "H4"
        halign: "center"
        pos_hint: {"center_x": 0.5, "center_y": 0.7}
        color: 0.1, 0.1, 0.1, 1
    
    MDRaisedButton:
        text: "测试按钮 Test Button"
        pos_hint: {"center_x": 0.5, "center_y": 0.3}
        md_bg_color: 0.18, 0.53, 0.82, 1
'''

class TestApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

if __name__ == "__main__":
    TestApp().run()
