# TP1 SIA - Métodos de Búsqueda

## Introducción

Trabajo práctico para la materia Sistemas de Inteligencia Artificial con el objetivo de implementar un motor de búsqueda de soluciones para el juego Sokoban
    
[Enunciado](docs/SIA_TP1.pdf)

### Requisitos

- Python3
- pip3
- [pipenv](https://pypi.org/project/pipenv/)

### Instalación

Parado en la carpeta del tp1 ejecutar

```sh
pipenv install
```

Para instalar las dependencias necesarias en el ambiente virtual

## Ejecución

Para jugar al juego

```
pipenv run python -m sokoban.game [configFile]
```

Para ejecutar un método de búsqueda

```
pipenv run python main.py [configFile]
```

Para correr una simulación del juego

```
pipenv run python -m sokoban.simulator [configFile]
```

## Configuración

Los archivos de configuración se leen en formato JSON

El nivel ("level") se describe como una matriz de strings, en donde cada string representa una fila del tablero.

- \# representa una pared
- P representa al jugador
- B representa una caja
- T representa un objetivo
- Un espacio representa un lugar libre

Para una búsqueda, además del nivel, se pueden especificar los siguientes parámetros en la configuración:

- method: El método de búsqueda a usar
- heuristic: La heurística a utilizar en un método informado
- depth_iteration: El aumento de profundidad máxima a utilizar en un IDDFS
- out_path:

Para una simulación, la secuencia de movimientos ("solution") se describe como un arreglo de strings que indican cada movimiento sucesivo ("Up", "Down", "Left", "Right"). 

Al ejecutar un método de búsqueda, el archivo de resultados generado puede usarse como configuración para una simulación.

## Métodos de Búsqueda disponibles

- bfs: Breadth-First Search
- dfs: Depth-First Search
- iddfs: Iterative Deepening Depth-First Search (requiere especificar la profundidad por iteración)
- greedy: Global Greedy Search (requiere especificar una heurística)
- a_star: A* Search (requiere especificar una heurística)

## Heurísticas disponibles

- misplaced_boxes: cantidad de cajas no ubicadas en objetivos
- manhattan_distance_sum: suma de las distancias manhattan de cada caja al objetivo más cercano
- nearest_box: distancia manhattan del jugador hasta la caja más cercana que no esté en un objetivo
- walled_distance_sum: suma de longitudes del camino de cada caja al objetivo más cercano, sin poder atravesar paredes
- not_cornered: detecta deadlocks causados por una caja en una esquina
- manhattan_distance_sum_and_not_cornered
- nearest_box_and_not_cornered
- walled_distance_sum_and_not_cornered