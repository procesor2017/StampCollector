from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.behaviors import HoverBehavior
from shared.db import crud
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.image import AsyncImage
from kivymd.uix.label import MDLabel
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior

class MainApp(MDApp):
    def build(self):
        Builder.load_file('views/main.kv')
        return MainLayout()

class MainLayout(MDBoxLayout, Screen):
    def show_righ_panel(self):
        pass

class HomeScreen(Screen):
    pass

class EmissionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Načítání zemí z CRUD
        self.countries = crud.get_all_countries()
        self.menu = None
        self.emissions = []

    def show_countries_dropdown(self, dropdown_item):
        """Show the dropdown menu with countries."""
        if not self.menu:
            menu_items = [
                {
                    "text": country.name,
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=country.name: self.select_country(x, dropdown_item),
                }
                for country in self.countries
            ]
            self.menu = MDDropdownMenu(
                caller=dropdown_item,
                items=menu_items,
                width_mult=4,
            )
        self.menu.open()

    def select_country(self, country_name, dropdown_item):
        """Handle country selection."""
        dropdown_item.text = country_name
        self.menu.dismiss()
        self.filter_emissions_by_country(country_name)

    def filter_emissions_by_country(self, country_name):
        """Filter emissions based on the selected country."""
        results_box = self.ids.results_box
        results_box.clear_widgets()

        matches = crud.get_emissions_by_country(country_name)
        self.display_results(matches)

    def display_results(self, matches):
        """
        Výsledky.
        """
        results_box = self.ids.results_box
        results_box.clear_widgets()

        for match in matches:
            expansionPanel = MDExpansionPanel(
                    content=Content(match),
                    panel_cls=MDExpansionPanelOneLine(
                        text=f"{match.name}",
                        bg_color=(1,1,1,1)
                        
                        ),  # panel class
                    pos_hint= {"center_x": .5, "center_y": .5},
                )
            results_box.add_widget(expansionPanel)


class HoverButton(MDRoundFlatIconButton, HoverBehavior):
    color_text = 1,1,1,1
    def on_enter(self):
        self.text_color = 0.89, 0.35, 0, 1

    def on_leave(self):
        self.text_color = 1,1,1,1

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage

# Obsah panelu
from kivy.uix.gridlayout import GridLayout

class Content(MDBoxLayout):
    def __init__(self, emission,**kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.adaptive_height = True
        self.md_bg_color= (1,1,1,1)

        # GridLayout pro zalamování obrázků
        grid_layout = GridLayout(
            cols=3,
            row_default_height="150dp",
            row_force_default=True,
            spacing="10dp",  # Mezera mezi obrázky
            size_hint_y=None,
        )

        # Dynamická výška GridLayout podle obsahu
        grid_layout.bind(
            minimum_height=grid_layout.setter("height")
        )

        stamps_for_emission = crud.get_stamps_by_emission(emission.name)

        for match in stamps_for_emission:
            match_photo = f"./data/images/{match.photo_path_base}"
            
            # Obrázek s textem
            image_with_text = ImageWithText(
                image_source=match_photo,
                text=match.name,
            )
            grid_layout.add_widget(image_with_text)
        self.add_widget(grid_layout)


class ImageWithText(ButtonBehavior, RelativeLayout):
    def __init__(self, image_source, text, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = ("150dp", "150dp")

        # Obrázek
        self.image = AsyncImage(
            source=image_source,
            size_hint=(1, 1),
            allow_stretch=True,
        )
        self.add_widget(self.image)

        # Text
        self.label = MDLabel(
            text=text,
            halign="center",
            valign="middle",
            size_hint=(1, 1),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            bold=True,
        )

        self.add_widget(self.label)

    def on_release(self):
        app = MDApp.get_running_app()
        right_panel = app.root.ids.right_panel
        panel_label = app.root.ids.panel_label  # Label, kam se zobrazují informace

        # Získat aktuální text v panelu
        current_text = panel_label.text
        new_text = self.label.text  # Nový text na základě aktuální známky

        if right_panel:
            if right_panel.size_hint_x == 0:  # Pokud je panel skrytý, zobrazí ho
                animation = Animation(size_hint_x=0.3, duration=0.3)
                animation.start(right_panel)
                panel_label.text = new_text  # Aktualizace textu
            else:
                if current_text != new_text:  # Pokud se data změnila, aktualizujte je
                    panel_label.text = new_text
                else:  # Pokud se data nezměnila, zavřete panel
                    animation = Animation(size_hint_x=0, duration=0.3)
                    animation.start(right_panel)
        else:
            print("Right panel not found!")

        


if __name__ == '__main__':
    app = MainApp()
    app.run()
