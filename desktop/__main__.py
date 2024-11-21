from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

class MainApp(MDApp):
    def build(self):
        Builder.load_file('views/main.kv')
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"  # Dark nebo Light
        return MainLayout()

class MainLayout(GridLayout):
    pass

class HomeScreen(Screen):
    pass

class EmissionScreen(Screen):
    pass

if __name__ == '__main__':
    app = MainApp()
    app.run()
