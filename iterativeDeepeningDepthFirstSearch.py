from searchAlgorithm import search
from frontierSets import Sorted

import sys
import json

def iddfs(level, depth_iteration):
    return search(level, Sorted(lambda state: (((len(state.path)-1) // depth_iteration), -1 * len(state.path))))

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        config = json.load(f)

        level = config["level"]

        depth_iteration = int(config["depth_iteration"])

    if len(sys.argv) > 2:
        out_path = sys.argv[2]
    else:
        out_path = "iddfs_results.json"

    results = iddfs(level, depth_iteration)

    with open(out_path, "w") as f:
        json.dump(results.to_dict(), f, ensure_ascii=False, indent=4)


