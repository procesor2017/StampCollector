from kivy.uix.boxlayout import BoxLayout
from shared.db import crud
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box_layout = BoxLayout()
        self.add_widget(box_layout)

    def on_enter(self):
        """Načte data při vstupu na obrazovku."""
        self.load_stamps()

    def load_stamps(self):
        stamps = crud.get_all_stamps()  # Získání známek
        stamp_list = self.ids.stamp_list
        stamp_list.clear_widgets()  # Smaže všechny existující widgety

        for stamp in stamps:
            stamp_label = Label(
                text=f"{stamp.name} ({stamp.catalog_number})",
                size_hint_y=None,  # Nutné pro správnou výšku widgetu
                height=40  # Nastavení pevné výšky pro každý řádek
            )
            stamp_list.add_widget(stamp_label)