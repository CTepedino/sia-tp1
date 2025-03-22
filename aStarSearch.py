from searchAlgorithm import search
from frontierSets import Sorted
from heuristics import heuristics
from sokobanRules import GameState

import sys
import json

def heuristic_plus_cost(heuristic):
    def f(state: GameState):
        h = heuristic(state)
        g = len(state.path)
        return g + h, h

    return f

def a_star(level, heuristic):
    return search(level, Sorted(heuristic_plus_cost(heuristic)))

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        config = json.load(f)

        level = config["level"]
        heuristic = heuristics[config["heuristic"]]

    for line in level:
        print(line)

    path = a_star(level, heuristic)
    print([direction.value for direction in path])