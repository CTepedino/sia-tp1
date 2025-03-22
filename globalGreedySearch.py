from searchAlgorithm import search
from frontierSets import Sorted
from heuristics import heuristics

import sys
import json

def greedy(level, heuristic):
    return search(level, Sorted(heuristic))

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        config = json.load(f)

        level = config["level"]
        heuristic = heuristics[config["heuristic"]]

    for line in level:
        print(line)

    path = greedy(level, heuristic)
    print([direction.value for direction in path])


