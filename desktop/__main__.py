from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from desktop.controllers.main_screen import MainScreen  # Import pro obrazovku
from kivy.lang import Builder

class StampApp(App):
    def build(self):
        Builder.load_file('desktop/views/main_screen.kv')
        sm = ScreenManager()  # Vytvoření screen manageru pro přepínání obrazovek
        sm.add_widget(MainScreen(name="main"))  
        sm.current = "main"
        return sm

if __name__ == "__main__":
    StampApp().run()  # Spuštění aplikace