from ezsgame.all import *

screen: Screen = get_screen()

# Clase Principal (es importada por UI.py)
class View:
    """
    Declaracion del "widget" vista izquierda
    todo en esta clase solo se dibujara en el View izquiero al ser selecionado
    """
    
    # Inicializacion de objetos -------------------------------------------------------------------------
    
    inventory_open: bool = False

    #Inventario 
    title = Text("Inventory", pos=[0,20], color="black", fontsize=30)
    center(screen, title, y_axis=False)
    
    slots = Grid(pos=[35, title.get_pos()[1] + 100], size=["90%", "60%"], grid_size=[6,3],
                 box_styles={
                        "color": "black",
                        "stroke" : 1,
                        "border_radius": [10,10,10,10]
                 })
    
    # Textos
    open_inventory_text = Text("Press \"e\" to open Inventory" , pos=["center","center"], color="black", fontsize=30)
    
    # Groupos
    inventory: Group = Group( title, slots )
    
    
    
    # Logica de dibujado
    def draw():
        # si el inventario esta abierto, se dibuja
        if View.inventory_open:
            View.inventory.draw()
            
        # si no, se dibuja el texto que indica como abrir el inventario
        else:
            View.open_inventory_text.draw()
            
             
    # Inicializacion de la clase  (si no es necesario, dejar la funcion vacia)
    def init():
        
        # Abrir y cerrar el inventario
        # Al presionar la "e" se abre el inventario y se cierra cuando se presiona otra vez
        @screen.on_key("down", ["e"])
        def open_inventory():
            if View.inventory_open:
                View.inventory_open = False
            else:
                View.inventory_open = True