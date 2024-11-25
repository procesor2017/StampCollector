import logging
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import Screen
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
from kivymd.uix.fitimage import FitImage
from kivymd.uix.datatables.datatables import MDDataTable
from kivy.metrics import dp
from kivy.core.window import Window

class MainApp(MDApp):
    def build(self):
        Builder.load_file('views/main.kv')
        return MainLayout()
    
    def open_detail_screen(self, item_id):
        """Otevře detailní obrazovku s konkrétním stamp ID."""
        screen_manager = self.root.ids.screen_manager
        detail_screen = screen_manager.get_screen("Stamp")
        detail_screen.update_content(item_id)
        screen_manager.current = "Stamp"

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

class StampScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_content(self, item_id):
        """Aktualizuje obsah obrazovky na základě ID položky."""
        self.stamp_id_from_search = item_id

    def on_enter(self):
        # Update Top first box with image a informnation
        stamp_id = self.stamp_id_from_search
        stamp_photo_top_card = self.ids.stamp_detail_md3card_tamp_image
        stamp_detail_stamp_name = self.ids.stamp_detail_stamp_name
        stamp_detail_stamp_catalogue_number = self.ids.stamp_detail_stamp_catalogue_number
        stamp_destamp_detail_stamp_nation_and_year = self.ids.stamp_detail_stamp_nation_and_year
        stamp_detail_stamp_emision = self.ids.stamp_detail_stamp_emision
        stamp_detail_stamp_type = self.ids.stamp_detail_stamp_type

        match = crud.get_stamp_by_id(stamp_id=stamp_id)


        stamp_photo_top_card.source = f"./data/images/{match.photo_path_base}"
        stamp_detail_stamp_name.text = f"{match.name}"
        stamp_detail_stamp_catalogue_number.text = f"Cat. N.: {match.catalog_number}"
        stamp_destamp_detail_stamp_nation_and_year.text = f"{match.emission.country.name} / {match.emission.issue_year}"
        stamp_detail_stamp_emision.text = f"{match.emission.name}"
        stamp_detail_stamp_type.text = f"{crud.get_n_of_stamp_type_base(stamp_id=stamp_id)}"

        # Create article:
        # Simulovaná data z databáze
        articles = [
            {
                "title": "Článek o známce 1",
                "image": "obrazek1.jpg",
                "description": "Toto je podrobný popis k prvnímu článku."
            },
            {
                "title": "Článek o známce 2",
                "image": "obrazek2.jpg",
                "description": "Toto je podrobný popis k druhému článku."
            },
        ]

        # Vymaže aktuální widgety
        articles_container = self.ids.articles_container
        articles_container.clear_widgets()

        # Přidává články do kontejneru
        for article in articles:
            panel = MDExpansionPanel(
                icon=article["image"],
                content=ArticleContent(
                    image=article["image"],
                    description=article["description"]
                ),
                panel_cls=MDExpansionPanelOneLine(
                    text=article["title"]
                ),
                on_open=self.update_card_height,
                on_close=self.update_card_height,
            )
            articles_container.add_widget(panel)

        self.get_last_selling_for_stamp()
        self.get_subtype_stamps_to_datatable(stamp_id=stamp_id)

    def update_card_height(self, *args):
        """Aktualizuje výšku karty na základě obsahu."""
        articles_container = self.ids.articles_container
        self.ids.stamp_detail_articles_for_one_stamp.height = articles_container.height

    def get_last_selling_for_stamp(self, *args):
        """Set last selling information to card"""
        stamp_id = self.stamp_id_from_search
        selling_card = self.ids.stamp_detail_last_10_selling_information

        selling_card.clear_widgets()
        
        data_to_selling_table = crud.get_auctions_by_stamp_base(stamp_id)

        table_width = selling_card.width
        type_width = table_width * 0.08
        quality_width= table_width * 0.04
        price_width= table_width * 0.04

        column_widths = [
            ("Type", type_width),  # 30 % šířky okna
            ("Quality", quality_width),  # 20 % šířky okna
            ("Price", price_width),  # 20 % šířky okna
        ]
    
        self.selling_table = MDDataTable(
            size_hint=(1, 1),
            column_data=column_widths,
            row_data = [],
            sorted_on="Schedule",
            sorted_order="ASC",
            elevation=2,
        )

        for data in data_to_selling_table:
            row_data = (data.stamp_type_id, data.state_of_stamp, data.sale_price)
            self.selling_table.add_row(row_data)

        selling_card.add_widget(self.selling_table)

    def get_subtype_stamps_to_datatable(self, stamp_id, *args):
        stamp_subtype_table = self.ids.stamp_detail_subtype_mdcard_for_table
        # Subtype to table
        subtype_table_data = crud.get_all_stamp_type_by_id(stamp_id)

        column_widths = [
            ("Photo", dp(60)),
            ("Stamp Type Name", dp(20)),
            ("Description", dp(60)), 
            ("color", dp(35)),
            ("paper", dp(35)),
            ("perforation", dp(20)),
            ("plate_flaw", dp(60)),
            ("**", dp(10)),
            ("*", dp(10)),
            ("(*)", dp(10)),    
            ("Post cover price", dp(25)),         
        ]


        self.subtype_table = MDDataTable(
            size_hint=(1, 1),
            column_data=column_widths,
            row_data = [],
            sorted_on="Schedule",
            sorted_order="ASC",
            elevation=2,
        )

        for subtype in subtype_table_data:
            row_data = (subtype.photo_path_type,
                        subtype.type_name,
                        subtype.description,
                        subtype.color,
                        subtype.paper,
                        subtype.perforation,
                        subtype.plate_flaw,
                        subtype.catalog_price_extra_fine,
                        subtype.catalog_price_fine,
                        subtype.catalog_price_avg,
                        subtype.catalog_price_post_cover)
            self.subtype_table.add_row(row_data)
        
        stamp_subtype_table.add_widget(self.subtype_table)


class ArticleContent(MDBoxLayout):
    def __init__(self, image, description, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.spacing = "8dp"
        self.padding = "8dp"

        # Obrázek vlevo
        self.add_widget(FitImage(source=image, size_hint=(0.5, 1)))

        # Popis vpravo
        text_box = MDBoxLayout(orientation="vertical", spacing="4dp")
        text_box.add_widget(MDLabel(text=description, theme_text_color="Secondary", halign="left"))
        self.add_widget(text_box)

class HoverButton(MDRoundFlatIconButton, HoverBehavior):
    color_text = 1,1,1,1
    def on_enter(self):
        self.text_color = 0.89, 0.35, 0, 1

    def on_leave(self):
        self.text_color = 1,1,1,1

class ClickableBox(ButtonBehavior, MDBoxLayout):
    pass

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
            spacing="10dp",
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
                stamp_id=match.stamp_id
            )
            grid_layout.add_widget(image_with_text)
        self.add_widget(grid_layout)

class ImageWithText(ButtonBehavior, RelativeLayout):
    def __init__(self, image_source, text, stamp_id, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = ("150dp", "150dp")
        self.stamp_id = stamp_id
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
        stamp_name = app.root.ids.stamp_name
        stamp_photo = app.root.ids.right_panel_md3card_tamp_image

        # Získat aktuální text v panelu
        current_text = stamp_name.text
        new_text = self.label.text

        # Defination ID for *.kv file
        right_panel.stamp_id = self.stamp_id

        if right_panel:
            if right_panel.size_hint_x == 0:  # Pokud je panel skrytý, zobrazí ho
                animation = Animation(size_hint_x=0.45, duration=0.3)
                animation.start(right_panel)
                stamp_name.text = new_text  # Aktualizace textu
                stamp_photo.source = self.image.source
            else:
                if current_text != new_text:  # Pokud se data změnila, aktualizujte je
                    stamp_name.text = new_text
                else:  # Pokud se data nezměnila, zavřete panel
                    animation = Animation(size_hint_x=0, duration=0.3)
                    animation.start(right_panel)
        else:
            print("Right panel not found!")


            

if __name__ == '__main__':
    app = MainApp()
    app.run()
