import sys
import json

from search.utils.heuristics import heuristics
from search.aStarSearch import a_star
from search.breadthFirstSearch import bfs
from search.depthFirstSearch import dfs
from search.globalGreedySearch import greedy
from search.iterativeDeepeningDepthFirstSearch import iddfs

def method_wrapper(method, level, heuristic=None, depth_iteration=None):
    if heuristic is not None:
        return method(level, heuristic)
    if depth_iteration is not None:
        return method(level, depth_iteration)
    return method(level)

methods = {
    "bfs": lambda level, h = None, d_i = None:  bfs(level),
    "dfs": lambda level, h = None, d_i = None:  dfs(level),
    "iddfs": lambda level, h = None, d_i = None:  iddfs(level, d_i),
    "greedy": lambda level, h = None, d_i = None:  greedy(level, h),
    "a_star": lambda level, h = None, d_i = None:  a_star(level, h)
}

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        config = json.load(f)

        level = config["level"]

        if "heuristic" in config:
            heuristic = heuristics[config["heuristic"]]
        else:
            heuristic = None

        if "depth_iteration" in config:
            depth_iteration = int(config["depth_iteration"])
        else:
            depth_iteration = None

        method = methods[config["method"]]

        if "out_path" in config:
            out_path = config["out_path"]
        else:
            out_path = f"{config['method']}_result.json"

    results = method(level, h=heuristic, d_i=depth_iteration)

    with open(out_path, "w") as f:
        json.dump(results.to_dict(), f, ensure_ascii=False, indent=4)