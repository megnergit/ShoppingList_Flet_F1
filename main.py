import flet as ft
# from flet 
# #  Checkbox, FloatingActionButton, Page, TextField, icons
# import pdb
# WIDTH=512
PRIMARY_COLOR=ft.colors.TEAL_ACCENT_700
SECOND_COLOR=ft.colors.ORANGE
# c = ft.Container()
# dir(c)
#======================================================================
class Item(ft.Column):
#----------------------------------------------------------------------
    def __init__(self, item_name, item_delete, usual = True):
        super().__init__()
        self.item_name =  item_name
        self.item_delete = item_delete
        self.usual=usual

        if usual :  
            trash_button = ft.IconButton(ft.icons.HIGHLIGHT_REMOVE_ROUNDED,
                                         padding=0,
                                          on_click=self.delete_clicked)
        else : 
            trash_button = ft.IconButton(ft.icons.HIGHLIGHT_REMOVE_ROUNDED,
                                         icon_color = SECOND_COLOR,
                                         padding=0,
                                         on_click=self.delete_clicked)
        
        textline = ft.Text(
                       disabled=False, 
                       spans = [
                       ft.TextSpan(
                            self.item_name, 
                            ft.TextStyle(
                                   decoration=ft.TextDecoration.NONE,
                                   decoration_thickness=2,
#                                   height=0.5,
                             ), 
                            on_click = self.toggle_strike_through,
                       )
                       ]
        )

        text = ft.Container(
            content=textline,
#            width=WIDTH//4
        )

        self.item_view = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
            controls = [trash_button, text]
        )

        self.spacing=0
        self.height=24
        self.controls = [self.item_view]

#-----------------------------------

    def toggle_strike_through(self, e):
#        print(self.item_view.controls[1].content.spans[0].style.decoration)
        toggle = 4 - self.item_view.controls[1].content.spans[0].style.decoration
        self.item_view.controls[1].content.spans[0].style.decoration = toggle

#        toggle = 4 - self.item_view.controls[1].spans[0].style.decoration
#        self.item_view.controls[1].spans[0].style.decoration = toggle
        self.update()

#-----------------------------------
    def delete_clicked(self, e):
        self.item_delete(self)

#======================================================================
class ShopApp(ft.Column):
#----------------------------------------------------------------------

    def __init__(self):
        super().__init__()
        usual_item_label = "Usual stuff"
        usual_item_hint = "Tostada"
        usual_height = 32

        weeks_item_label = "This week"
        weeks_item_hint = "Toothpaste"
        weeks_height = usual_height

#-----------------
# usual stuff
        self.new_item = ft.TextField(
            label=usual_item_label,
            label_style=ft.TextStyle(color=PRIMARY_COLOR),
            focused_border_color=PRIMARY_COLOR,
            hint_text=usual_item_hint,
            height=usual_height,
            on_submit = self.add_item,
            cursor_width=0,
            content_padding=ft.Padding(left=8, top=0, right=8, bottom=0)
        )

# weekly new stuff
        self.weeks_item = ft.TextField(
            focused_border_color=SECOND_COLOR,
            autofocus=True,
            label=weeks_item_label,
            label_style=ft.TextStyle(color=SECOND_COLOR),
#            label_style=ft.TextStyle(decoration_color=SECOND_COLOR),
            hint_text=weeks_item_hint,
            hint_style=ft.TextStyle(color=ft.colors.GREY),
            height=weeks_height,
            on_submit = self.add_weeks_item,
            cursor_width=0,
            content_padding=ft.Padding(left=8, top=0, right=8, bottom=0)
        )

#-----------------
# usual list
        self.item_list = []
        self.items = ft.Column(spacing=0, 
                               wrap=True,
                               run_spacing=0,
                               height=128,
                               alignment=ft.MainAxisAlignment.START)

# weeks list
        self.weeks_item_list = []
        self.weeks_items = ft.Column(spacing=0, 
                               wrap=True,
                               run_spacing=0,
#                              height=180,
                               alignment=ft.MainAxisAlignment.START)

#-----------------
# usual clear button
        self.clear_button = ft.ElevatedButton("Clear", 
                                              adaptive=True,
                                              icon="directions_transit_filled_outlined", 
                                              style=ft.ButtonStyle(padding=0,
                                                                   elevation=4,

                                              ), 
                                              on_click=self.clear_items
        )

# weeks delete button
        self.delete_button = ft.ElevatedButton("Delete", 
                                              color=SECOND_COLOR,
                                              adaptive=True,
                                              icon="forklift",
                                              icon_color=SECOND_COLOR,
                                              style=ft.ButtonStyle(padding=0,
                                                                   elevation=16,
                                              ), 
                                              on_click=self.delete_weeks_items
        )

#-----------------
# put them all in one widget 

        divider = ft.Divider(height=16)
#        print(f"spacing {self.spacing}")
        self.spacing = 0
#        self.tight = True

        self.controls = [
            ft.Row([
                ft.Container(self.new_item, 
                             expand = 3,
                             padding=0, margin=0),
                ft.Container(self.clear_button, 
                             expand=1, 
                             padding = ft.padding.only(right=16), 
                             margin=0),
            ]),
            self.items,
            divider,
            ft.Row([
                ft.Container(self.weeks_item, 
                             expand = 3,
                             padding=0, margin=0),
                ft.Container(self.delete_button, 
                             expand=1, 
                             padding=ft.padding.only(right=16),
                             margin=0),
            ]),
            self.weeks_items,
#             ft.Container(content=self.items)
#                          bgcolor=ft.colors.AMBER_100),
        ]
#----------------------------------------------------------------------
#----------------------------------------------------------------------
    def add_item(self, e):

        item_list = self.item_list + (self.new_item.value).split(",")
        item_list = [x.replace(" ", "") for x in item_list]
        self.item_list = list(set(item_list))
        self.items.controls = [Item(i, self.item_delete) for i in self.item_list]

        self.new_item.value = ""
        self.update()
#-----------------------------------
    def add_weeks_item(self, e):

        item_list = self.weeks_item_list + (self.weeks_item.value).split(",")
        item_list = [x.replace(" ", "") for x in item_list]
        self.weeks_item_list = list(set(item_list))
        self.weeks_items.controls = [Item(i, self.weeks_item_delete, False) for i in self.weeks_item_list]

        self.weeks_item.value = ""
        self.update()

#-----------------------------------
    def delete_weeks_items(self, e):

        self.weeks_items.controls = []
        self.update()

#-----------------------------------
    def clear_items(self, e):
        x = self.items.controls

        for i in x: 
             i.item_view.controls[1].content.spans[0].style.decoration = 0

        self.update()
#-----------------------------------
    def item_delete(self, item):
        self.items.controls.remove(item)
        self.update()

#-----------------------------------
    def weeks_item_delete(self, item):
        self.weeks_items.controls.remove(item)
        self.update()

#======================================================================
def main(page: ft.Page):

#    page.adaptive=True
#    page.window_width = WIDTH
#    page.bgcolor=ft.colors.ORANGE_100
    page.theme_mode = "light"    
#    page.theme_mode = "dark"
    page.theme = ft.Theme(
#         color_scheme_seed=ft.colors.TEAL_ACCENT_700,
#        color_scheme_seed=ft.colors.ORANGE,
         color_scheme=ft.ColorScheme(primary=PRIMARY_COLOR,
                                     secondary=SECOND_COLOR),
#         color_scheme_seed=ft.colors.TEAL_900,
#        color_scheme_seed=ft.cupertino_colors.SYSTEM_TEAL,
    )
    page.update()
    app = ShopApp()
    page.add(app)
#    WIDTH = page.window_width
#    print(f"WIDTH {WIDTH}")

ft.app(target=main)

#======================================================================
