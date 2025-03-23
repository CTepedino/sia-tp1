from searchAlgorithm import search
from frontierSets import Stack

import sys
import json

def dfs(level):
    return search(level, Stack())

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        config = json.load(f)

        level = config["level"]

    if len(sys.argv) > 2:
        out_path = sys.argv[2]
    else:
        out_path = "dfs_results.json"

    results = dfs(level)

    with open(out_path, "w") as f:
        json.dump(results.to_dict(), f, ensure_ascii=False, indent=4)


