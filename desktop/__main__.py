from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import ScreenManager

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

if __name__ == '__main__':
    app = MainApp()
    app.run()
