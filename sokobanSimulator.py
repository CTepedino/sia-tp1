import json
import time
from sokobanGame import Sokoban  # Aquí importa las clases o funciones necesarias de tu juego

# Función que lee el archivo JSON
def cargar_resultados_json(ruta_json):
    with open(ruta_json, 'r') as f:
        data = json.load(f)
    return data['solution']

# Función que simula el juego
def simular_juego(ruta_json):
    with open(ruta_json, 'r') as f:
        data = json.load(f)
    movimientos = data['solution']
    level = data['level']
    juego = Sokoban(level)  # Suponiendo que tienes una clase `Sokoban`
    juego.automatic_start(movimientos)  # Si tu juego tiene un método de inicio
    # print("partido empezado")
    # for movimiento in movimientos:
    #     print("el mov es: "+movimiento)
    #     if movimiento == "up":
    #         print("Moviendo hacia arriba")
    #         juego.move_up()
    #     elif movimiento == "down":
    #         print("Moviendo hacia abajo")
    #         juego.move_down()
    #     elif movimiento == "left":
    #         print("Moviendo hacia la izquierda")
    #         juego.move_left()
    #     elif movimiento == "right":
    #         print("Moviendo hacia la derecha")
    #         juego.move_right()
        
    #     # Esperar medio segundo antes de hacer el siguiente movimiento
    #     time.sleep(0.5)

# Ruta al archivo JSON con los movimientos
ruta_json = 'result.json'

# Ejecutar simulador
simular_juego(ruta_json)
