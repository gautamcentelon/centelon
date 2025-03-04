import flet as ft
import csv

def main(page: ft.Page):
    page.fonts = {
        "Galada": "https://github.com/google/fonts/raw/refs/heads/main/ofl/galada/Galada-Regular.ttf",
        "Open Sans": "/fonts/OpenSans-Regular.ttf",
        "Changa": "https://github.com/google/fonts/raw/refs/heads/main/ofl/changaone/ChangaOne-Regular.ttf"
    }

    page.window_height = 1920
    page.window_width = 1080
    page.window_maximized = True

    page.theme = ft.Theme(font_family="Open Sans")
    

    categories = []
    products = []

    categories_row= ft.Row(spacing=10, wrap=False, scroll=ft.ScrollMode.HIDDEN)
    #products_column = ft.Column([products_grid],spacing=10, wrap=True, scroll=ft.ScrollMode.HIDDEN)
    #products_grid= ft.GridView(expand=True, runs_count=2,spacing=20,run_spacing=20)
    cart_items = ft.GridView(expand=True, runs_count=1, spacing=10, run_spacing=10)
    bg_img = ft.Image(src="img.png",expand=True,fit=ft.ImageFit.FILL)

    contentl = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text("Print your favourite posters", weight="Regular", size=40, font_family="Changa"),
                    padding=ft.padding.only(top=50,bottom=5),
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    content=ft.SearchBar(view_elevation=4, divider_color="#750000", bar_hint_text="Search Your Favourite Posters"),
                    padding=ft.padding.only(top=10, bottom=40),
                    alignment=ft.alignment.center
                ),
                ft.Text("Categories", size=20, weight="Regular", color="#750000"),
                ft.Container(content=categories_row, padding=ft.padding.only(bottom=20)),
                ft.Row(
                    [
                        ft.Text("Products", size=20, weight="Regular", color="#750000"),
                        ft.ElevatedButton("View All", bgcolor="#eb9025", icon=ft.Icons.KEYBOARD_DOUBLE_ARROW_DOWN_SHARP)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=10
        ),
        width=1080*0.6,
        height=1920*0.95,
        image=ft.DecorationImage(src="img.jpg", fit=ft.ImageFit.FILL, opacity=0.3),
        padding=ft.padding.all(20),
        border=ft.border.all(1, "#c78933"),
    )

    contentr = ft.Container(
        content=ft.Column(
            [
            ft.Text("Cart Items", size=20, weight="bold", color="#750000"),
            ft.Container(content=cart_items, padding=ft.padding.only(top=20))
            ],
            spacing=10
        ),
        width=1080*0.375,
        height=1920*0.95,
        padding=ft.padding.all(20),
        border=ft.border.all(1, "#c78933"),
        image=ft.DecorationImage(src="img.jpg", fit=ft.ImageFit.FILL, opacity=0.2),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLUE_GREY_300,
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER,
        ),

    )
    
    

    

    


    with open('categories.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            categories.append(row)

    with open('products.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append(row)

    cart=[]

    displayed_products = products[:]

    def update_products_grid():
        pass        
    def view_all():
        pass
    def search_products():
        pass    

    page.add(ft.Row([contentl,contentr],spacing=5))
ft.app(target=main, assets_dir="assets")