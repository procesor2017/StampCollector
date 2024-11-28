import os
import matplotlib.pyplot as plt
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRoundFlatIconButton, MDRaisedButton, MDFlatButton
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
from kivy.uix.image import Image
from datetime import datetime
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from collections import defaultdict

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
        stamp_detail_stamp_avg_auction_price = self.ids.stamp_detail_avg_auction_price_number
        stamp_detail_stamp_catalogue_price = self.ids.stamp_detail_catalogue_price_number

        match = crud.get_stamp_by_id(stamp_id=stamp_id)
        price = crud.get_total_avg_price_by_stamp_id(stamp_id=stamp_id)
        avg_auction = crud.get_average_auction_price_by_stamp_id(stamp_id=stamp_id)

        stamp_photo_top_card.source = f"./data/images/{match.photo_path_base}"
        stamp_detail_stamp_name.text = f"{match.name}"
        stamp_detail_stamp_catalogue_number.text = f"Cat. N.: {match.catalog_number}"
        stamp_destamp_detail_stamp_nation_and_year.text = f"{match.emission.country.name} / {match.emission.issue_year}"
        stamp_detail_stamp_emision.text = f"{match.emission.name}"
        stamp_detail_stamp_type.text = f"{crud.get_n_of_stamp_type_base(stamp_id=stamp_id)}"
        stamp_detail_stamp_avg_auction_price.text = f"{avg_auction}"
        stamp_detail_stamp_catalogue_price.text = f"{int(price)}"


        # Create article/ details:
        details = crud.get_stamp_detail_by_stamp_id(stamp_id=stamp_id)

        # Vymaže aktuální widgety
        articles_container = self.ids.articles_container
        articles_container.clear_widgets()

        # Přidává detaily do kontejneru
        for detail in details:
            # Určí, co se zobrazí v těle panelu (podle dostupnosti dat)
            content_text = (
                detail.production_notes
                or detail.history
                or detail.origin
                or "Žádné další informace nejsou k dispozici."
            )

            panel = MDExpansionPanel(
                icon="file-document-outline",  # Ikona panelu (můžete nahradit vlastním obrázkem)
                content=ArticleContent(
                    image=detail.photo_paths.split(',')[0] if detail.photo_paths else "",
                    description=content_text
                ),
                panel_cls=MDExpansionPanelOneLine(
                    text=detail.description or "Bez popisu"
                ),
                on_open=self.update_card_height,
                on_close=self.update_card_height,
            )
            articles_container.add_widget(panel)

        self.get_last_selling_for_stamp()
        self.get_subtype_stamps_to_datatable(stamp_id=stamp_id)
        self.get_plot_auction_sales(stamp_id=stamp_id)


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

    def get_subtype_stamps_to_datatable(self, stamp_id):
        """
        Zobrazí detailní tabulku podtypů známek s podporou stránkování.
        """
        # Načtení rodičovského widgetu, kde bude tabulka zobrazena
        stamp_subtype_table = self.ids.stamp_detail_subtype_mdcard_for_table

        # Načtení dat z databáze
        subtype_table_data = crud.get_all_stamp_type_by_id(stamp_id)

        # Transformace dat pro použití v tabulce
        stamp_data = [
            {
                "photo_path_type": subtype.photo_path_type,
                "type_name": subtype.type_name,
                "description": subtype.description,
                "color": subtype.color,
                "paper": subtype.paper,
                "perforation": subtype.perforation,
                "plate_flaw": subtype.plate_flaw,
                "catalog_price_extra_fine": subtype.catalog_price_extra_fine,
                "catalog_price_fine": subtype.catalog_price_fine,
                "catalog_price_avg": subtype.catalog_price_avg,
                "catalog_price_post_cover": subtype.catalog_price_post_cover,
            }
            for subtype in subtype_table_data
        ]

        # Vyčištění starého obsahu
        stamp_subtype_table.clear_widgets()

        # Vytvoření paginatoru a jeho připojení do rozhraní
        StampTablePaginator(
            parent_widget=stamp_subtype_table,
            data=stamp_data,
            rows_per_page=10  # Počet řádků na stránku
        )

    def get_image_widget(self, image_path):
        """
        Vrací widget obrázku nebo textovou náhradu, pokud obrázek neexistuje.
        """
        if os.path.exists(image_path):
            return Image(source=image_path, size_hint=(None, None), size=(dp(100), dp(100)))
        else:
            return MDLabel(text="No Image", size_hint_y=None, height=dp(40))
        
    def get_plot_auction_sales(self, stamp_id):
        # Získání prodeje aukcí z databáze
        auction_sales = crud.get_all_auction_by_stamp_type(stamp_id)

        if not auction_sales:
            print("No auction sales found for the given stamp_id.")
        else:
            print(f"Found {len(auction_sales)} auction sales.")

        # Příprava dat pro graf
        sales_by_stamp_type = defaultdict(list)  # Použijeme defaultdict pro seskupení prodejů podle typu známky

        for sale in auction_sales:
            sales_by_stamp_type[sale[3]].append((sale[0], sale[1]))  # sale[3] je type_name (název typu známky), sale[0] je sale_date, sale[1] je sale_price

        # Vytvoření grafu
        plt.figure(figsize=(10, 6))

        # Pro každý název typu známky vykreslíme samostatnou čáru
        for stamp_type_name, sales in sales_by_stamp_type.items():
            dates = [sale[0] for sale in sales]
            prices = [sale[1] for sale in sales]
            plt.plot(dates, prices, label=stamp_type_name)  # Použijeme název typu známky místo stamp_type_id

        plt.title(f"Prodeje aukcí pro známku {stamp_id}")
        plt.xlabel("Datum")
        plt.ylabel("Cena")
        plt.grid(True)
        plt.legend()  # Přidáme legendu pro různé typy známek (nyní podle názvů)

        # Přidání grafu do Kivy aplikace
        canvas = self.ids.stamp_detail_selling_graph
        canvas.clear_widgets()  # Vyčistit předchozí graf
        canvas.add_widget(FigureCanvasKivyAgg(plt.gcf()))



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
                data=match
            )
            grid_layout.add_widget(image_with_text)
        self.add_widget(grid_layout)

class ImageWithText(ButtonBehavior, RelativeLayout):
    def __init__(self, image_source, data, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = ("150dp", "150dp")
        self.stamp_id = data.stamp_id
        self.data = data
        # Obrázek
        self.image = AsyncImage(
            source=image_source,
            size_hint=(1, 1),
            allow_stretch=True,
        )
        self.add_widget(self.image)

        # Text
        self.label = MDLabel(
            text=data.name,
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
        detail_about_stamp = app.root.ids.right_panel_detail_about_stamps
        number_of_stamp_type = app.root.ids.right_panel_number_of_stamp_type_inf
        saved_number_of_sale = app.root.ids.right_panel_saved_number_of_sale_inf

        # Získat aktuální text v panelu
        current_text = stamp_name.text
        new_text = self.label.text

        # Defination ID for *.kv file
        right_panel.stamp_id = self.stamp_id
        photo = f"./data/images/{self.data.photo_path_base}"
        detail = f"{self.data.emission.name}"
        n_stamp_type = f"{crud.get_n_of_stamp_type_base(self.stamp_id)}"
        n_of_sale =crud.get_count_of_auction_by_stamp_base(stamp_id=self.stamp_id)


        if right_panel:
            if right_panel.size_hint_x == 0:  # Pokud je panel skrytý, zobrazí ho
                animation = Animation(size_hint_x=0.45, duration=0.3)
                animation.start(right_panel)
                stamp_name.text = new_text
                stamp_photo.source = photo
                detail_about_stamp.text = detail
                number_of_stamp_type.text = n_stamp_type
                saved_number_of_sale.text = f"{n_of_sale}"
            else:
                # Refresh data
                if current_text != new_text:
                    stamp_name.text = new_text
                    stamp_photo.source = photo
                    detail_about_stamp.text = detail
                    number_of_stamp_type.text = n_stamp_type
                    saved_number_of_sale.text = f"{n_of_sale}"
                else:  # Pokud se data nezměnila, zavřete panel
                    animation = Animation(size_hint_x=0, duration=0.3)
                    animation.start(right_panel)
        else:
            print("Right panel not found!")

class StampTablePaginator:
    def __init__(self, parent_widget, data, rows_per_page=10):
        self.parent_widget = parent_widget
        self.data = data
        self.rows_per_page = rows_per_page
        self.current_page = 0

        self.table_layout = GridLayout(
            cols=11,
            size_hint=(1, None),
            spacing=dp(10),
        )

        self.table_layout.bind(minimum_height=self.table_layout.setter("height"))

        # Vytvoření navigačních tlačítek
        self.navigation_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(50),
            spacing=dp(10)
        )

        self.parent_widget.height = self.table_layout.height + self.navigation_layout.height

        self.prev_button = MDRaisedButton(
            text="Předchozí",
            on_release=lambda x: self.prev_page(x),
            disabled=True
        )
        self.next_button = MDRaisedButton(
            text="Další",
            on_release=lambda x: self.next_page(x)
        )

        self.next_button.bind(on_press=self.next_page)

        self.navigation_layout.add_widget(self.prev_button)
        self.navigation_layout.add_widget(self.next_button)

        # Přidání tabulky a navigace do rodičovského widgetu
        self.parent_widget.clear_widgets()
        self.parent_widget.add_widget(self.table_layout)
        self.parent_widget.add_widget(self.navigation_layout)

        # Vykreslení první stránky
        self.show_page(0)

    def show_page(self, page_number):
        """
        Zobrazí data pro zadanou stránku.
        """
        self.current_page = page_number
        self.table_layout.clear_widgets()

        # Záhlaví tabulky
        headers = [
            "Photo", "Type Sign", "Description", "Color", "Paper",
            "Perforation", "Plate Flaw", "**", "*", "(*)", "Post Cover Price"
        ]
        for header in headers:
            self.table_layout.add_widget(MDLabel(text=header, size_hint_y=None, height=dp(40), bold=True))

        # Výpočet dat pro stránku
        start_index = page_number * self.rows_per_page
        end_index = start_index + self.rows_per_page
        page_data = self.data[start_index:end_index]

        # Přidání datových řádků
        for subtype in page_data:
            # Přidání obrázku
            self.table_layout.add_widget(self.get_image_widget(subtype['photo_path_type']))

            # Vytvoření a přizpůsobení MDLabel widgetů
            type_label = MDLabel(
                text=subtype['type_name'],
                size_hint_y=None,
                height=dp(150)
            )
            type_label.halign = "center"
            type_label.valign = "center"
            type_label.text_size = (None, None)  # Ujisti se, že textové zarovnání funguje
            self.table_layout.add_widget(type_label)

            
            for key in ['description', 'color', 'paper', 'perforation', 'plate_flaw',
                        'catalog_price_extra_fine', 'catalog_price_fine', 
                        'catalog_price_avg', 'catalog_price_post_cover']:
                label = MDLabel(
                    text=str(subtype[key]),  # Konverze na text
                    size_hint_y=None,
                    height=dp(150)
                )
                label.halign = "center"
                label.valign = "center"
                label.text_size = (None, None)
                self.table_layout.add_widget(label)

        # Dynamická výška rodiče
        self.parent_widget.height = (
            self.table_layout.height + self.navigation_layout.height
        )

        # Aktualizace stavu tlačítek
        self.prev_button.disabled = (page_number == 0)
        self.next_button.disabled = (end_index >= len(self.data))

    def prev_page(self, instance):
            if self.current_page > 0:
                self.show_page(self.current_page - 1)

    def next_page(self, instance):
        print("mačkám tlačítko")
        if (self.current_page + 1) * self.rows_per_page < len(self.data):
            self.show_page(self.current_page + 1)

    def get_image_widget(self, image_path):
        """
        Vrací widget obrázku nebo textovou náhradu, pokud obrázek neexistuje.
        """
        
        real_photo_path = f"data/images/{image_path}"
        if os.path.exists(real_photo_path):
            return Image(source=real_photo_path, size_hint=(None, None), size=(dp(150), dp(150)))
        else:
            return MDLabel(text="No need for a picture", size_hint_y=None, height=dp(40))

            

if __name__ == '__main__':
    app = MainApp()
    app.run()
