import flet as ft
import csv
import os
from printpy import print_photo, download_image
def main(page: ft.Page):
    page.fonts = {
        "Galada": "https://github.com/google/fonts/raw/refs/heads/main/ofl/galada/Galada-Regular.ttf",
        "Open Sans": "/fonts/OpenSans-Regular.ttf",
        "Changa": "https://github.com/google/fonts/raw/refs/heads/main/ofl/changaone/ChangaOne-Regular.ttf"
    }
    page.title="Poster Print"
    page.window_height = 1920
    page.window_width = 1080
    page.window_maximized = True

    page.theme = ft.Theme(font_family="Open Sans")

    categories = []

    with open('categories.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            categories.append({
                "name": row["name"],
                "highlighted": False,
                "image_url": row["image_url"]
            })

    products = []

    with open('products.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            products.append({
                "name": row["name"],
                "price": float(row["price"]),
                "image_url": row["image_url"],
                "category": row["category"]
            })


    cart = []

    # Filtered products based on selected category
    displayed_products = products[:]

    # Update the products grid
    def update_products_grid():
        products_grid.controls.clear()
        for product in displayed_products:
            products_grid.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Image(product["image_url"], width=500, height=300,fit="fill",border_radius=8),
                                padding=ft.padding.only(top=10),
                            ),

                            ft.Container(
                                content=ft.Text(product["name"], size=30, weight="bold", text_align=ft.TextAlign.CENTER),
                                padding=ft.padding.only(left=5,right=5,bottom=-5),
                                alignment=ft.alignment.top_center,
                                
                                                               
                            ),
                            ft.Container(
                                content = ft.Row(
                                    [
                                        ft.Text(f"${product['price']:.2f}", size=20, weight="bold", color="green"),
                                        ft.IconButton(ft.Icons.ADD_SHOPPING_CART, data=product, on_click=add_to_cart),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                    spacing=5,
                                ),
                                padding=ft.padding.only(bottom=20,left=50,right=50)
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    padding=ft.padding.only(top=0,left=5,right=5,bottom=5),
                    bgcolor="white",
                    border=ft.border.all(color="#f8f8f8", width=0.5),
                    border_radius=8,
                    alignment=ft.alignment.center,
                )
            )
        products_grid.update()

    def add_to_cart(e):
        product = e.control.data
        existing_item = next((item for item in cart if item["name"] == product["name"]), None)
        if existing_item:
            existing_item["quantity"] += 1
        else:
            cart.append({"name": product["name"], "price": product["price"], "quantity": 1, "image_url": product["image_url"]})
        update_cart()

    def update_cart():
        cart_items.controls.clear()  # Clear the cart items list
        total = 0
        for item in cart:
            total += item["price"] * item["quantity"]
            cart_items.controls.append(
                ft.Row(
                    [
                        # Enlarged Image
                        ft.Container(
                            content=ft.Image(item["image_url"], width=95, height=110, fit=ft.ImageFit.FILL,border_radius=10),
                            alignment=ft.alignment.center,
                            margin=ft.margin.only(right=10),
                        ),
                        # Item Name and Price
                        ft.Column(
                            [
                                ft.Text(item["name"], weight="bold", size=14, no_wrap=False),
                                ft.Text(f"${item['price']:.2f}", color="red", size=12),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            expand=True,
                        ),
                        # Quantity Selector
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Text("-", size=16, weight="bold", color="white"),
                                    bgcolor="red",
                                    width=30,
                                    height=30,
                                    alignment=ft.alignment.center,
                                    border_radius=5,
                                    on_click=lambda _, i=item: change_quantity(i, -1),
                                ),
                                ft.Text(f"{item['quantity']}", size=14, weight="bold", text_align="center"),
                                ft.Container(
                                    content=ft.Text("+", size=16, weight="bold", color="white"),
                                    bgcolor="green",
                                    width=30,
                                    height=30,
                                    alignment=ft.alignment.center,
                                    border_radius=5,
                                    on_click=lambda _, i=item: change_quantity(i, 1),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                            spacing=8,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                )
            )
        total_text.value = f"Total: ${total:.2f}"
        cart_column.update()


    def change_quantity(item, change):
        item["quantity"] += change
        if item["quantity"] <= 0:
            cart.remove(item)
        update_cart()

    def show_all_products(e):
        nonlocal displayed_products
        displayed_products = products[:]
        for category in categories:
            category["highlighted"] = False
        update_categories()
        update_products_grid()

    def filter_products_by_category(category_name):
        nonlocal displayed_products
        displayed_products = [p for p in products if p["category"] == category_name]
        update_products_grid()

    def toggle_category(e):
        selected_category = e.control.data
        for category in categories:
            category["highlighted"] = category["name"] == selected_category
        update_categories()
        filter_products_by_category(selected_category)

    def update_categories():
        categories_row.controls.clear()
        for category in categories:
            categories_row.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(content=ft.Image(category["image_url"], width=100, height=110, fit="cover", border_radius=10),alignment=ft.alignment.center),
                            ft.Container(content=ft.Text(category["name"], text_align=ft.TextAlign.CENTER, weight="bold", size=14, no_wrap=False),alignment=ft.alignment.center),
                        ],
                        spacing=2,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    bgcolor="red" if category["highlighted"] else "#f5f5f5",
                    width=125,
                    height=145,
                    alignment=ft.alignment.center,
                    border_radius=14,
                    padding=ft.padding.only(bottom=10,top=8,left=5,right=5),
                    on_click=lambda e, c=category: toggle_category(e),
                    data=category["name"],
                )
            )
        categories_row.update()
    def filter_products(search_query=""):
        nonlocal displayed_products
        displayed_products = [p for p in products if search_query.lower() in p["name"].lower()]
        update_products_grid()

    def hello():
        confirm_checkout
        close_dialog()    

    def show_checkout_dialog():
        """Show a confirmation dialog before printing posters."""
        if not cart:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Cart is Empty!"),
                content=ft.Text("Please add items to the cart before checking out."),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: close_dialog()),
                ],
            )

            

        else:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Confirm Checkout"),
                content=ft.Text(f"Are you sure you want to print {sum(item['quantity'] for item in cart)} posters?"),
                actions=[
                    ft.TextButton("Yes", on_click=lambda e: [confirm_checkout(e), close_dialog()]),
                    ft.TextButton("Cancel", on_click=lambda e: close_dialog()),
                ],
            )
        page.dialog.open = True
        page.update()

    def close_dialog():
        """Close the dialog box."""
        page.dialog.open = False
        page.update()

    def confirm_checkout(e):
        """Triggered only when user confirms the checkout."""
        if not cart:
            print("Cart is empty, nothing to print.")
            return

        # Proceed with printing only after confirmation
        try:
            for item in cart:
                # Download and print the image
                downloaded_image_path = download_image(item["image_url"])
                if downloaded_image_path:
                    print_photo(downloaded_image_path)  # Print the image
                    os.remove(downloaded_image_path)  # Delete temp file
        except Exception as ex:
            print(f"Error during printing: {ex}")
        finally:
            # Clear cart after printing
            cart.clear()
            update_cart()
            page.snack_bar = ft.SnackBar(ft.Text("Order placed successfully!"),bgcolor="green")
            page.snack_bar.open = True
            page.update()

        

    # Categories Row
    categories_row = ft.Row(spacing=10, wrap=False, scroll=ft.ScrollMode.HIDDEN)

    # Products Grid
    products_grid = ft.GridView(
        expand=True,
        runs_count=2,
        spacing=40,
        run_spacing=20,
        child_aspect_ratio=0.7,        
    )

    # Cart Section
    cart_items = ft.Column(spacing=50, scroll=ft.ScrollMode.HIDDEN)

    total_text = ft.Text("Total: $0.00", size=16, weight="bold", color="black", text_align="center")

    cart_column = ft.Container(
        content=ft.Column(
            [
                # "My Orders" Heading
                ft.Container(
                    content=ft.Row([
                        ft.Text(
                        "My Orders",
                        size=20,
                        weight="bold",
                        text_align="center",
                        ),
                        ft.TextButton("Clear Cart",on_click=lambda e: clr_cart())
                    ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    
                    
                    padding=ft.padding.only(top=100, bottom=10),
                ),
                # Scrollable Items Container
                ft.Container(
                    content=cart_items,
                    padding=ft.padding.only(top=20, bottom=5, left=5, right=5),
                    height=1400,
                ),
                # Total Price
                ft.Container(
                    content=total_text,
                    padding=ft.padding.only(top=100, bottom=0),
                    alignment=ft.alignment.center,
                ),
                # Checkout Button
                ft.Container(
                    content=ft.ElevatedButton(
                        "Checkout",
                        bgcolor="#FFD700",
                        color="black",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.symmetric(vertical=20, horizontal=40),
                        ),
                        on_click=lambda _: show_checkout_dialog(),
                    ),
                    alignment=ft.alignment.center,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        width=1080 * 0.325,
        height=1920 * 0.95,
        padding=ft.padding.all(20),
        border=ft.border.all(ft.border.BorderSide(1, "#c78933")),
        image=ft.DecorationImage(src="img.jpg", fit=ft.ImageFit.FILL, opacity=0.2),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLUE_GREY_300,
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER,
        ),
    )

    def clr_cart():
        cart.clear()
        update_cart()
        

    cart_colu = ft.Stack(
        [  
            ft.Image(
                src="1234.jpg",  # Background image URL
                width=(0.322*1080),
                height=(95*1920),
                fit=ft.ImageFit.FILL,
            ), 
            ft.Container(
                content=ft.Column(
                    [
                        # "My Orders" Heading
                        ft.Container(
                            content=ft.Text(
                                "My Orders",
                                size=20,
                                weight="bold",
                                text_align="center",
                            ),
                            padding=ft.padding.only(top=100, bottom=10),
                        ),
                        # Scrollable Items Container
                        ft.Container(
                            content=cart_items,
                            padding=ft.padding.only(top=20, bottom=5, left=5, right=5),
                            height=1400,
                        ),
                        # Total Price
                        ft.Container(
                            content=total_text,
                            padding=ft.padding.only(top=100, bottom=0),
                            alignment=ft.alignment.center,
                        ),
                        # Checkout Button
                        ft.Container(
                            content=ft.ElevatedButton(
                                "Checkout",
                                bgcolor="#FFD700",
                                color="black",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    padding=ft.padding.symmetric(vertical=20, horizontal=40),
                                ),
                                on_click=lambda _: page.snack_bar(ft.SnackBar("Order placed!")),
                            ),
                            alignment=ft.alignment.center,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                width=348,
                padding=ft.padding.all(16),
                bgcolor=ft.Colors.with_opacity(0.70, "#f8f8f8"),
                border=ft.border.all(color="#dcdcdc", width=1),
            )
        ] 
    )    
    
    # Left Column - Main Content
    left_column = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text("Print your favourite posters", weight="Regular", size=40, font_family="Changa"),
                        padding=ft.padding.only(top=50,bottom=5),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.SearchBar(view_elevation=4, divider_color="#750000", bar_hint_text="Search Your Favourite Posters",on_change=lambda e: filter_products(e.control.value)),
                        padding=ft.padding.only(top=10, bottom=40),
                        alignment=ft.alignment.center
                    ),
                    ft.Text("Categories", size=20, weight="Regular", color="#750000"),
                    ft.Container(content=categories_row, padding=ft.padding.only(bottom=20)),
                    ft.Row(
                        [
                            ft.Text("Posters", size=20, weight="Regular", color="#750000"),
                            ft.ElevatedButton("View All", bgcolor="#eb9025", icon=ft.Icons.KEYBOARD_DOUBLE_ARROW_DOWN_SHARP,on_click=show_all_products)
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    products_grid     
                    
                ],
                spacing=10
            ),
            width=1080*0.65,
            height=1920*0.95,
            image=ft.DecorationImage(src="img.jpg", fit=ft.ImageFit.FILL, opacity=0.3),
            padding=ft.padding.all(20),
            border=ft.border.all(1, "#c78933"),
        )


    # Add layout and initialize
    page.add(ft.Row([left_column, cart_column],spacing=5, expand=True))
    update_categories()
    update_products_grid()

ft.app(target=main)