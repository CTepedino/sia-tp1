import enum
import math
from typing import Callable

from frontierSets import Sorted
from sokobanRules import GameState

def misplaced_boxes(state: GameState):
    return sum(1
               for box in state.boxes
               if box not in state.targets)

def manhattan_distance_to_nearest_target(box, state: GameState):

    return min(abs(box[0] - target[0]) + abs(box[1] - target[1])
        for target in state.targets)

def manhattan_distance_sum(state: GameState):
    return sum(manhattan_distance_to_nearest_target(box, state)
        for box in state.boxes)

def nearest_box(state: GameState):
    unplaced_boxes = [box for box in state.boxes if box not in state.targets]
    if not unplaced_boxes:
        return 0
    return min(abs(state.player[0] - box[0]) + abs(state.player[1] - box[1]) for box in unplaced_boxes) if unplaced_boxes else 0


def not_cornered(state: GameState):
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


calculated_walled_distances = {}

def walled_distance(box, state: GameState):
    if box in calculated_walled_distances:
        return calculated_walled_distances[box]

    frontier = Sorted(lambda space_info: manhattan_distance_to_nearest_target(space_info["space"], state) + len(space_info["path"]))

    current_space = {"space": box, "path": []}

    while current_space is not None:
        if current_space["space"] in calculated_walled_distances:
            result = calculated_walled_distances[current_space["space"]]
            path_len = len(current_space["path"])
            for i, space in enumerate(current_space["path"]):
                dist = result + (path_len - i)
                if space not in calculated_walled_distances or dist < calculated_walled_distances[space]:
                    calculated_walled_distances[space] = dist
            return result

        if current_space["space"] in state.targets:
            calculated_walled_distances[current_space["space"]] = 0
            path_len = len(current_space["path"])
            for i, space in enumerate(current_space["path"]):
                dist = path_len - i
                if space not in calculated_walled_distances or dist < calculated_walled_distances[space]:
                    calculated_walled_distances[space] = dist
            return len(current_space["path"])

        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_space = {
                "space":(direction[0] + current_space["space"][0], direction[1] + current_space["space"][1])
            }

            if new_space["space"] not in state.walls and new_space["space"] not in current_space["path"]:
                new_space["path"] = current_space["path"] + [current_space["space"]]
                frontier.add(new_space)
        current_space = frontier.next()

    return float('inf')


def walled_distance_sum(state: GameState):
    return sum(walled_distance(box, state) for box in state.boxes)


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
    "walled_distance_sum": walled_distance_sum,

    "not_cornered": not_cornered,
    "manhattan_and_not_cornered": combine(not_cornered, manhattan_distance_sum),
    "nearest_box_and_not_cornered": combine(not_cornered, nearest_box),
    "walled_distance_sum_and_not_cornered": combine(not_cornered, walled_distance_sum)
}