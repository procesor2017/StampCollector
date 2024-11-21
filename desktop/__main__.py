from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRoundFlatIconButton
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.behaviors import HoverBehavior
from kivy.properties import ListProperty

# Definování barevného schématu
class MainApp(MDApp):
    def build(self):
        Builder.load_file('views/main.kv')
        return MainLayout()

class MainLayout(MDBoxLayout):
    pass

class HomeScreen(Screen):
    pass

class EmissionScreen(Screen):
    pass

class HoverButton(MDRoundFlatIconButton, HoverBehavior):
    background = ListProperty((0/255, 0/255,0/255,1))
    color_text = 1,1,1,1
    color_icon = [1,1,1,1]
    def on_enter(self):
        self.background = (1, 222/255, 89/255, 1)
        self.color = (0, 0, 0, 1)
        self.text_color = 0.89, 0.35, 0, 1
        self.color_icon = [0.89, 0.35, 0, 1]

    def on_leave(self):
        self.background = (0, 0, 0, 1)
        self.color = (1, 1, 1, 1)
        self.text_color = 1,1,1,1
        self.color_icon = [1,1,1,1]

if __name__ == '__main__':
    app = MainApp()
    app.run()
