import enum
import math
from typing import Callable

from sokobanRules import GameState

def misplaced_boxes(state: GameState):
    return sum(1
               for box in state.boxes
               if box not in state.targets)

def manhattan_distance_sum(state: GameState):
    return sum(
        min(abs(box[0] - target[0]) + abs(box[1] - target[1])
        for target in state.targets)
        for box in state.boxes)

def nearest_box(state: GameState):
    unplaced_boxes = [box for box in state.boxes if box not in state.targets]
    if not unplaced_boxes:
        return 0
    return min(abs(state.player[0] - box[0]) + abs(state.player[1] - box[1]) for box in unplaced_boxes)

def not_deadlocked(state: GameState):
    for box in state.boxes:
        if box not in state.targets:
            up = (box[1], box[0] - 1)
            down = (box[1], box[0] + 1)
            right = (box[1] + 1, box[0])
            left = (box[1] - 1, box[0])

            if (up in state.walls and (left in state.walls or right in state.walls) or
                    (down in state.walls and (left in state.walls or right in state.walls))):
                return float('inf')


    return 0

#IMPORTANTE: si se esta usando una heuristica que pueda devolver infinito, mandarla como primer parametro, para no perder tiempo evaluando la segunda heuristica si no hace falta
def combine(heuristic_1: Callable[[GameState], int], heuristic_2: Callable[[GameState], int]):
    def combination(state: GameState):
        value1 = heuristic_1(state)
        if math.isinf(value1):
            return value1
        return max(value1, heuristic_2(state))

    return combination

heuristics = {
    "misplaced_boxes": misplaced_boxes,
    "manhattan_distance_sum": manhattan_distance_sum,
    "nearest_box": nearest_box,
    "not_deadlocked": not_deadlocked,
    "manhattan_and_no_deadlock": combine(not_deadlocked, manhattan_distance_sum),
    "nearest_box_and_no_deadlock": combine(not_deadlocked, nearest_box)
}