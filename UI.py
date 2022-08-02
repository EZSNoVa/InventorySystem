from ezsgame.all import *

screen: Screen = get_screen()


class Interfaz:
    # Aqui de declaran los objetos necessarios para la interfaz
    
    # variables ---------------------------------------------------------------------------------------
    inventory_open: bool = False
    
    # objectos ---------------------------------------------------------------------------------------
    
    #Inventario 
    title = Text("Inventory", pos=[0,20], color="black", fontsize=30)
    center(screen, title, y_axis=False)
    
    slots = Grid(pos=[35, title.get_pos()[1] + 100], size=["90%", "60%"], grid_size=[6,3],
                 box_styles={
                        "color": "black",
                        "stroke" : 1,
                        "border_radius": [10,10,10,10]
                 })
    
    
    inventory: Group = Group(
        title, slots
    )
    
    # Textos
    open_inventory_text = Text("Press \"e\" to open Inventory" , pos=["center","center"], color="black", fontsize=30)
    

    # dibuja los objetos
    def draw() -> None:    
        
        # dibuja el inventario si esta abierto
        if Interfaz.inventory_open:
            Interfaz.inventory.draw()
            
        #  dibuja el texto que te indica como abrir el inventario si esta cerrado
        else:
            Interfaz.open_inventory_text.draw()
            
    
    # inicializa la interfaz
    def init() -> None:
        
        # Abrir y cerrar el inventario
        # Al presionar la "e" se abre el inventario y se cierra cuando se presiona otra vez
        @screen.on_key("down", ["e"])
        def open_inventory():
            Interfaz.inventory_open = not Interfaz.inventory_open
