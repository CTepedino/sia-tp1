from searchAlgorithm import search
from frontierSets import Queue

import sys
import json

def bfs(level):
    return search(level, Queue())

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        config = json.load(f)

        level = config["level"]

    for line in level:
        print(line)

    path = bfs(level)
    print([direction.value for direction in path])


