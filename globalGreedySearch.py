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

    if len(sys.argv) > 2:
        out_path = sys.argv[2]
    else:
        out_path = f"greedy_{config['heuristic']}_results.json"

    results = greedy(level, heuristic)

    with open(out_path, "w") as f:
        json.dump(results.to_dict(), f, ensure_ascii=False, indent=4)