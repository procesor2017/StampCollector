from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRoundFlatIconButton
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

class HoverItem(MDRoundFlatIconButton):
    '''Custom item implementing hover behavior.'''

    def on_enter(self, *args):
        '''The method will be called when the mouse cursor
        is within the borders of the current widget.'''

        self.md_bg_color = (1, 1, 1, 1)

    def on_leave(self, *args):
        '''The method will be called when the mouse cursor goes beyond
        the borders of the current widget.'''

        self.md_bg_color = self.theme_cls.bg_darkest



if __name__ == '__main__':
    app = MainApp()
    app.run()
