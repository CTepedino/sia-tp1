from sokobanRules import SokobanRules, Directions
from collections import deque
import heapq
import time
import json

    
def bfs(level):
    game = SokobanRules(level)
    initial_state = (game.player, frozenset(game.boxes))
    queue = deque([(initial_state, [])])  # (estado_actual, camino)
    visited = set()
    visited.add(initial_state)
    expanded = 1
    
    while queue:
        (player, boxes), path = queue.popleft()
        
        if boxes == game.targets:
            return path, expanded, len(visited)  # Devuelve la secuencia de movimientos para ganar
        
        for direction in [Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]:
            expanded += 1
            new_game = SokobanRules(level)
            new_game.player, new_game.boxes = player, set(boxes)
            new_game.move_to(direction)
            new_state = (new_game.player, frozenset(new_game.boxes))
            
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, path + [direction]))
    
    return None, expanded, len(visited)  # No se encontró solución

def dfs(level):
    game = SokobanRules(level)
    initial_state = (game.player, frozenset(game.boxes))
    stack = [(initial_state, [])]  # (estado_actual, camino)
    visited = set()
    visited.add(initial_state)
    expanded = 1
    while stack:
        (player, boxes), path = stack.pop()
        
        if boxes == game.targets:
            return path, expanded, len(visited)  # Devuelve la secuencia de movimientos para ganar
        
        #falta ver que si el proximo movimiento es un deadlock, vaya a otro estado
        for direction in [Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]:
            expanded +=1 
            new_game = SokobanRules(level)
            new_game.player, new_game.boxes = player, set(boxes)
            new_game.move_to(direction)
            new_state = (new_game.player, frozenset(new_game.boxes))
            
            if new_state not in visited:
                visited.add(new_state)
                stack.append((new_state, path + [direction]))
    
    return None, expanded, len(visited)

def heuristic_manhattan(boxes, targets):
    return sum(min(abs(bx - tx) + abs(by - ty) for tx, ty in targets) for bx, by in boxes)

def heuristic_euclidean(boxes, targets):
    return sum(min(((bx - tx) ** 2 + (by - ty) ** 2) ** 0.5 for tx, ty in targets) for bx, by in boxes)

def heuristic_misplaced_boxes(boxes, targets):
    return sum(1 for box in boxes if box not in targets)

def heuristic_player_to_nearest_box(player, boxes, targets):
    unplaced_boxes = [box for box in boxes if box not in targets]
    if not unplaced_boxes:
        return 0
    return min(abs(player[0] - bx) + abs(player[1] - by) for bx, by in unplaced_boxes)

def heuristic_box_in_corner(boxes, walls, targets):
    for box in boxes:
        if is_deadlocked(box, walls, targets):
            return float('inf')

    return 0

def is_deadlocked(box, walls, targets):
    bx, by = box

    if box in targets:
        return False

    if ((bx - 1, by) in walls and (bx, by - 1) in walls) or \
       ((bx - 1, by) in walls and (bx, by + 1) in walls) or \
       ((bx + 1, by) in walls and (bx, by - 1) in walls) or \
       ((bx + 1, by) in walls and (bx, by + 1) in walls):
        return True 

    return False

def greedy_manhattan(level):
    game = SokobanRules(level)
    initial_state = (game.player, frozenset(game.boxes))
    priority_queue = [(heuristic_manhattan(game.boxes, game.targets), initial_state, [])]  # (heurística, estado_actual, camino)
    visited = set()
    visited.add(initial_state)
    expanded = 1
    
    while priority_queue:
        _, (player, boxes), path = heapq.heappop(priority_queue)
        
        if boxes == game.targets:
            return path, expanded, len(visited)  # Devuelve la secuencia de movimientos para ganar
        
        for direction in [Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]:
            expanded += 1
            new_game = SokobanRules(level)
            new_game.player, new_game.boxes = player, set(boxes)
            new_game.move_to(direction)
            new_state = (new_game.player, frozenset(new_game.boxes))
            
            if new_state not in visited:
                visited.add(new_state)
                heapq.heappush(priority_queue, (heuristic_manhattan(new_game.boxes, game.targets), new_state, path + [direction]))
    
    return None, expanded, len(visited)  # No se encontró solución

def greedy_euclidean(level):
    game = SokobanRules(level)
    initial_state = (game.player, frozenset(game.boxes))
    priority_queue = [(heuristic_manhattan(game.boxes, game.targets), initial_state, [])]  # (heurística, estado_actual, camino)
    visited = set()
    visited.add(initial_state)
    expanded = 1
    
    while priority_queue:
        _, (player, boxes), path = heapq.heappop(priority_queue)
        
        if boxes == game.targets:
            return path, expanded, len(visited)  # Devuelve la secuencia de movimientos para ganar
        
        for direction in [Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]:
            expanded += 1
            new_game = SokobanRules(level)
            new_game.player, new_game.boxes = player, set(boxes)
            new_game.move_to(direction)
            new_state = (new_game.player, frozenset(new_game.boxes))
            
            if new_state not in visited:
                visited.add(new_state)
                heapq.heappush(priority_queue, (heuristic_manhattan(new_game.boxes, game.targets), new_state, path + [direction]))
    
    return None, expanded, len(visited) # No se encontró solución

def greedy_misplaced_boxes(level):
    game = SokobanRules(level)
    initial_state = (game.player, frozenset(game.boxes))
    priority_queue = [(heuristic_manhattan(game.boxes, game.targets), initial_state, [])]  # (heurística, estado_actual, camino)
    visited = set()
    visited.add(initial_state)
    expanded = 1
    
    while priority_queue:
        _, (player, boxes), path = heapq.heappop(priority_queue)
        
        if boxes == game.targets:
            return path, expanded, len(visited)  # Devuelve la secuencia de movimientos para ganar
        
        for direction in [Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]:
            expanded += 1
            new_game = SokobanRules(level)
            new_game.player, new_game.boxes = player, set(boxes)
            new_game.move_to(direction)
            new_state = (new_game.player, frozenset(new_game.boxes))
            
            if new_state not in visited:
                visited.add(new_state)
                heapq.heappush(priority_queue, (heuristic_manhattan(new_game.boxes, game.targets), new_state, path + [direction]))
    
    return None, expanded, len(visited) # No se encontró solución


def a_star_manhattan(level):
    game = SokobanRules(level)
    initial_state = (game.player, frozenset(game.boxes))
    priority_queue = [(heuristic_manhattan(game.boxes, game.targets), 0, initial_state, [])]  # (f_score, g_score, estado_actual, camino)
    visited = {}
    visited[initial_state] = 0
    expanded = 1
    
    while priority_queue:
        _, g, (player, boxes), path = heapq.heappop(priority_queue)
        
        if boxes == game.targets:
            return path, expanded, len(visited)  # Devuelve la secuencia de movimientos para ganar
        
        for direction in [Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]:
            expanded += 1
            new_game = SokobanRules(level)
            new_game.player, new_game.boxes = player, set(boxes)
            new_game.move_to(direction)
            new_state = (new_game.player, frozenset(new_game.boxes))
            
            new_g = g + 1  # Costo real del camino
            new_f = new_g + heuristic_manhattan(new_game.boxes, game.targets)  # f = g + h
            
            if new_state not in visited or new_g < visited[new_state]:
                visited[new_state] = new_g
                heapq.heappush(priority_queue, (new_f, new_g, new_state, path + [direction]))
    
    return None, expanded, len(visited)

def a_star_euclidean(level):
    game = SokobanRules(level)
    initial_state = (game.player, frozenset(game.boxes))
    priority_queue = [(heuristic_manhattan(game.boxes, game.targets), 0, initial_state, [])]  # (f_score, g_score, estado_actual, camino)
    visited = {}
    visited[initial_state] = 0
    expanded = 1
    
    while priority_queue:
        _, g, (player, boxes), path = heapq.heappop(priority_queue)
        
        if boxes == game.targets:
            return path, expanded, len(visited)  # Devuelve la secuencia de movimientos para ganar
        
        for direction in [Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]:
            expanded += 1
            new_game = SokobanRules(level)
            new_game.player, new_game.boxes = player, set(boxes)
            new_game.move_to(direction)
            new_state = (new_game.player, frozenset(new_game.boxes))
            
            new_g = g + 1  # Costo real del camino
            new_f = new_g + heuristic_manhattan(new_game.boxes, game.targets)  # f = g + h
            
            if new_state not in visited or new_g < visited[new_state]:
                visited[new_state] = new_g
                heapq.heappush(priority_queue, (new_f, new_g, new_state, path + [direction]))
    
    return None, expanded, len(visited)

def a_star_misplaced_boxes(level):
    game = SokobanRules(level)
    initial_state = (game.player, frozenset(game.boxes))
    priority_queue = [(heuristic_manhattan(game.boxes, game.targets), 0, initial_state, [])]  # (f_score, g_score, estado_actual, camino)
    visited = {}
    visited[initial_state] = 0
    expanded = 1
    
    while priority_queue:
        _, g, (player, boxes), path = heapq.heappop(priority_queue)
        
        if boxes == game.targets:
            return path, expanded, len(visited)  # Devuelve la secuencia de movimientos para ganar
        
        for direction in [Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]:
            expanded += 1
            new_game = SokobanRules(level)
            new_game.player, new_game.boxes = player, set(boxes)
            new_game.move_to(direction)
            new_state = (new_game.player, frozenset(new_game.boxes))
            
            new_g = g + 1  # Costo real del camino
            new_f = new_g + heuristic_manhattan(new_game.boxes, game.targets)  # f = g + h
            
            if new_state not in visited or new_g < visited[new_state]:
                visited[new_state] = new_g
                heapq.heappush(priority_queue, (new_f, new_g, new_state, path + [direction]))
    
    return None, expanded, len(visited)

def a_star_box_in_corner(level):
    game = SokobanRules(level)
    initial_state = (game.player, frozenset(game.boxes))
    priority_queue = [(heuristic_box_in_corner(game.boxes, game.walls, game.targets), 0, initial_state, [])]  # (f_score, g_score, estado_actual, camino)
    visited = {}
    visited[initial_state] = 0
    expanded = 1
    
    while priority_queue:
        _, g, (player, boxes), path = heapq.heappop(priority_queue)
        
        if boxes == game.targets:
            return path, expanded, len(visited)  # Devuelve la secuencia de movimientos para ganar
        
        for direction in [Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]:
            expanded += 1
            new_game = SokobanRules(level)
            new_game.player, new_game.boxes = player, set(boxes)
            new_game.move_to(direction)
            new_state = (new_game.player, frozenset(new_game.boxes))
            
            new_g = g + 1  # Costo real del camino
            new_f = new_g + heuristic_box_in_corner(new_game.boxes, game.walls, game.targets)  # f = g + h
            
            if new_state not in visited or new_g < visited[new_state]:
                visited[new_state] = new_g
                heapq.heappush(priority_queue, (new_f, new_g, new_state, path + [direction]))
    
    return None, expanded, len(visited)

if __name__ == "__main__":
    level= [
    "########",
    "#  T   #",
    "#  B   #",
    "# ###  #",
    "#   #P #",
    "#  B T #",
    "########"
    ]


    start = time.time()
    solution, expanded, frontier = a_star_box_in_corner(level)
    end = time.time()
    
    print("Éxito" if solution is not None else "Fracaso")
    print(f"Solución: {solution}")
    print(f"Costo: {len(solution)}")
    print(f"Cantidad de nodos expandidos: {expanded}")
    print(f"Cantidad de nodos frontera: {frontier}")
    print(f"Tiempo de procesamiento: {(end - start):.2f} segundos")

    result = {
        "solution": [direction.value for direction in solution], 
        "cost": len(solution),  
        "expanded_nodes": expanded,  
        "frontier_nodes": frontier,
        "level": level,
        "current_level":1
    }


    with open("result.json", "w") as file:
        json.dump(result, file, indent=4)

    print("Resultados guardados en 'result.json'")


