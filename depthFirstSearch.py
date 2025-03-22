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

    for line in level:
        print(line)

    path = dfs(level)
    print([direction.value for direction in path])


