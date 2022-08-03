from turtle import back
from typing import Dict
from ezsgame.all import *
from vistas import right, left

screen: Screen = get_screen()
    
def get_arrow(direction:str, view_direction:str) -> Image:
    """
    #### Retornate el objeto de la flecha apuntado hacia x direction para moverte entre vistas
    
    #### Params
    - direction : left, right, up or down
    - to_return : invierte la flecha si es True
    """
    
    # calculate pos
    arrow: Image = Image(pos=[0,0], size=[35,35], image="assets/img/arrow.png")
    
    if direction == "left":
        arrow.pos[0] = 20
        center(screen, arrow, x_axis=False)
        arrow.rotate(90)
    
    elif direction == "right":
        arrow.pos[0] = screen.size[0] - arrow.get_size()[0] - 20
        center(screen, arrow, x_axis=False)
        arrow.rotate(-90)
        
    arrow.extends(IObject)
        
    arrow.__setattr__("direction", view_direction)
    
    return arrow 
      
class Interfaz:
    """
    Clase que maneja la inferfaz
    En esta clase solo deben hacer cosas que sean necesarias para la interfaz principal
    """
    
    # Inicializacion de objetos -------------------------------------------------------------------------
    current_view: str = "main"    
    
    to_left_arrow, to_right_arrow = get_arrow("left", "left"), get_arrow("right", "right")
    back_right_arrow, back_left_arrow = get_arrow("right", "main"), get_arrow("left", "mian")
    
        
    arrows: Dict[str, Group] = {
            "main" : Group(to_left_arrow, to_right_arrow),
            "left" : Group(back_right_arrow),
            "right" : Group(back_left_arrow)
        }

    main_text = Text("Click arrows to change view", pos=["center","center"], fontsize=40, color="black")
    
    # DRAWING GROUPS -----------------------------------------------------------------------------------
    views = {
        "left" : left.View,
        "right" : right.View
    }
    
    
    # dibuja los objetos
    def draw() -> None:    
        
        # dibuja la vista principal
        if Interfaz.current_view == "main":
            Interfaz.main_text.draw()
            
        else:
            # dibuja la vista actual
            Interfaz.views[Interfaz.current_view].draw()        

        # dibuja las flechas
        Interfaz.arrows[Interfaz.current_view].draw()
    
    # inicializa la interfaz y las vistas
    def init() -> None:
        Interfaz.change_view(Interfaz.current_view)
        
        for view_obj in Interfaz.views.values():
            view_obj.init()
    

    def change_view(new_view:str):
        # remove events from arrows
        if new_view in ("left", "right"):
            screen.remove_event("to_left_arrow_event")
            screen.remove_event("to_right_arrow_event")
            
        else:
            screen.remove_event("back_right_arrow_event")
            screen.remove_event("back_left_arrow_event")

        # add events to arrows
        if new_view == "left":
            Interfaz.back_right_arrow.click(lambda: Interfaz.change_view("main"), "back_right_arrow_event")

        elif new_view == "right":
            Interfaz.back_left_arrow.click(lambda: Interfaz.change_view("main"), "back_left_arrow_event")
        
        else:
            Interfaz.to_left_arrow.click(lambda: Interfaz.change_view("left"), "to_left_arrow_event")
            Interfaz.to_right_arrow.click(lambda: Interfaz.change_view("right"), "to_right_arrow_event")
            
        Interfaz.current_view = new_view
        Interfaz.draw()