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
        #print(f"\t{(g+h, h)} - {state}")
        return g + h, h

    return f

def a_star(level, heuristic):
    return search(level, Sorted(heuristic_plus_cost(heuristic)))

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        config = json.load(f)

        level = config["level"]
        heuristic = heuristics[config["heuristic"]]

    if len(sys.argv) > 2:
        out_path = sys.argv[2]
    else:
        out_path = f"a_star_{config['heuristic']}_results.json"

    results = a_star(level, heuristic)


    with open(out_path, "w") as f:
        json.dump(results.to_dict(), f, ensure_ascii=False, indent=4)