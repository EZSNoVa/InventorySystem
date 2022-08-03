from ezsgame.all import *

screen: Screen = get_screen()

# Clase Principal (es importada por UI.py)
class View:
    """
    Declaracion del "widget" vista izquierda
    todo en esta clase solo se dibujara en el View izquiero al ser selecionado
    """
    
    # Inicializacion de objetos -------------------------------------------------------------------------
    
    test_text = Text("Test", pos=["center", 0], color="black", fontsize=30)
    

    # Logica de dibujado
    def draw():
        View.test_text.draw()
        
    # Inicializacion de la clase  (si no es necesario, dejar la funcion vacia)
    def init():
        pass