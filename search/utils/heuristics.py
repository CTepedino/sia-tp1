import math
from typing import Callable

from fontTools.cu2qu.cli import open_ufo

from .frontierSets import Sorted
from sokoban.rules import GameState

def misplaced_boxes(state: GameState):
    return sum(1
               for box in state.boxes
               if box not in state.targets)


calculated_manhattan_distances = {}

def manhattan_distance_to_nearest_target(box, state: GameState):
    if box in calculated_manhattan_distances:
        return calculated_manhattan_distances[box]

    distance =  min(abs(box[0] - target[0]) + abs(box[1] - target[1])
        for target in state.targets)
    calculated_manhattan_distances[box] = distance
    return distance


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

            up = (box[0], box[1] - 1) in state.walls
            down = (box[0], box[1] + 1) in state.walls
            right = (box[0] + 1, box[1]) in state.walls
            left = (box[0] - 1, box[1]) in state.walls

            if (up and (left or right) or
                    (down and (left or right))):
                return float('inf')


    return 0

def no_square_blocks(state: GameState):
    box_and_walls = state.walls.union(state.boxes)
    for box in state.boxes:
        if box not in state.targets:
            up = (box[0], box[1] - 1) in box_and_walls
            down = (box[0], box[1] + 1) in box_and_walls
            right = (box[0] + 1, box[1]) in box_and_walls
            left = (box[0] - 1, box[1]) in box_and_walls

            up_right = (box[0] + 1, box[1] - 1) in box_and_walls
            up_left = (box[0] - 1 , box[1] - 1) in box_and_walls
            down_right = (box[0] + 1, box[1] + 1) in box_and_walls
            down_left = (box[0] - 1 , box[1] + 1) in box_and_walls

            if (
                    (up and up_right and right) or
                    (up and up_left and left) or
                    (down and down_right and right) or
                    (down and down_left and left)
            ):
                return float('inf')
    return 0

known_stuck_spots = []
def not_wall_stuck(state: GameState):
    for box in state.boxes:
        if box not in state.targets:

            if box in known_stuck_spots:
                return float('inf')

            up = (box[0], box[1] - 1)
            down = (box[0], box[1] + 1)
            right = (box[0] + 1, box[1])
            left = (box[0] - 1, box[1])

            for direction in [up, down]:
                if direction not in state.walls:
                    continue
                explored = []
                open_r = True
                open_l = True
                dir_r = direction
                r = box
                while open_r:
                    r = (r[0] + 1, r[1])
                    dir_r = (dir_r[0] + 1, dir_r[1])
                    explored.append(r)
                    if r in state.walls:
                        open_r = False
                    if r in state.targets:
                        break
                    if dir_r not in state.walls:
                        break
                dir_l = direction
                l = box
                if not open_r:
                    while open_l:
                        l = (l[0] - 1, l[1])
                        dir_l = (dir_l[0] - 1, dir_l[1])
                        explored.append(l)
                        if l in state.walls:
                            open_l = False
                        if l in state.targets:
                            break
                        if dir_l not in state.walls:
                            break
                if (not open_l) and (not open_r):
                    known_stuck_spots.extend(explored)
                    return float('inf')

            for direction in [left, right]:
                if direction not in state.walls:
                    continue
                explored = []
                open_u = True
                open_d = True
                dir_u = direction
                u = box
                while open_u:
                    u = (u[0], u[1] - 1)
                    dir_u = (dir_u[0], dir_u[1] - 1)
                    explored.append(u)
                    if u in state.walls:
                        open_u = False
                    if u in state.targets:
                        break
                    if dir_u not in state.walls:
                        break
                dir_d = direction
                d = box
                if not open_u:
                    while open_d:
                        d = (d[0], d[1] + 1)
                        dir_d = (dir_d[0], dir_d[1] + 1)
                        explored.append(d)
                        if d in state.walls:
                            open_d = False
                        if d in state.targets:
                            break
                        if dir_d not in state.walls:
                            break

                if (not open_u) and (not open_d):
                    known_stuck_spots.extend(explored)
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
            return result + path_len

        if current_space["space"] in state.targets:
            calculated_walled_distances[current_space["space"]] = 0
            path_len = len(current_space["path"])
            for i, space in enumerate(current_space["path"]):
                dist = path_len - i
                if space not in calculated_walled_distances or dist < calculated_walled_distances[space]:
                    calculated_walled_distances[space] = dist
            return path_len

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
def combine(heuristic_list: [Callable[[GameState], int]]):
    def combination(state: GameState):
        current_max = 0
        for heuristic in heuristic_list:
            value = heuristic(state)
            if math.isinf(value):
                return value
            if value > current_max:
                current_max = value
        return current_max

    return combination

heuristics = {
    "misplaced_boxes": misplaced_boxes,
    "manhattan_distance_sum": manhattan_distance_sum,
    "nearest_box": nearest_box,
    "walled_distance_sum": walled_distance_sum,

    "not_cornered": not_cornered,
    "no_square_blocks": no_square_blocks,
    "not_wall_stuck": not_wall_stuck,

    "avoid_deadlocks": combine([not_cornered, not_wall_stuck, no_square_blocks]),

    "manhattan_distance_sum_adl": combine([not_cornered, not_wall_stuck, no_square_blocks, manhattan_distance_sum]),
    "nearest_box_adl": combine([not_cornered, not_wall_stuck, no_square_blocks, nearest_box]),
    "walled_distance_sum_adl": combine([not_cornered, not_wall_stuck, no_square_blocks, walled_distance_sum])
}