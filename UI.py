from ezsgame.all import *

class Interfaz:
    # Aqui de declaran los objetos necessarios para la interfaz
    
    test_rect:Rect = Rect(["center", "center"], [50,50], color="red")



    # dibuja los objetos
    def draw() -> None:
        # Aqui se dibujan todos los objetos de la interfaz
    
        for obj in Interfaz.__dict__.values():
            
            # si es un objecto
            if isinstance(obj, Object):
                obj.draw()
    

    