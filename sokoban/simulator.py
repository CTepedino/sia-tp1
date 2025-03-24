import json
import sys
from game import Sokoban

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        config = json.load(f)

        level = config["level"]
        solution = config["solution"]

    Sokoban(level).automatic_game(solution)
