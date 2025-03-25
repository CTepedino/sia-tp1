import sys
import json
import time

from search.utils.heuristics import heuristics
from search.aStarSearch import a_star
from search.breadthFirstSearch import bfs
from search.depthFirstSearch import dfs
from search.globalGreedySearch import greedy
from search.iterativeDeepeningDepthFirstSearch import iddfs

methods = {
    "bfs": lambda level, h=None, d_i=None: bfs(level),
    "dfs": lambda level, h=None, d_i=None: dfs(level),
    "iddfs": lambda level, h=None, d_i=None: iddfs(level, d_i),
    "greedy": lambda level, h=None, d_i=None: greedy(level, h),
    "a_star": lambda level, h=None, d_i=None: a_star(level, h)
}

heuristics = {
    "misplaced_boxes",
    "manhattan_distance_sum",
    "nearest_box",
    "walled_distance_sum",
    "not_cornered",
    "no_square_blocks", 
    "not_wall_stuck",
    "avoid_deadlocks", 
    "nearest_box_adl", 
    "manhattan_distance_sum_adl", 
    "walled_distance_sum_adl",
    "manhattan_distance_sum_times_5"
}

def run_experiments(level, methods_to_run, num_runs=50):
    results_map = {}

    for method_name in methods_to_run:
        executions = []
        for i in range(num_runs):
            start_time = time.time()
            method = methods[method_name]

            heuristic = "manhattan_distance_sum" if method_name in ["greedy", "a_star"] else None
            depth_iteration = (i // 5) + 1 if method_name == "iddfs" else None

            # Run the method
            result = method(level, h=heuristic, d_i=depth_iteration)
            dict_result = result.to_dict()
            result_data = {
                "solved": dict_result["solved"],
                "cost": dict_result["cost"],
                "nodes_expanded": dict_result["nodes_expanded"],
                "nodes_in_frontier": dict_result["nodes_in_frontier"],
                "time": dict_result["time"],
                "depth":depth_iteration
            }
            
            executions.append(result_data)

        results_map[method_name] = {"executions": executions}
    
    return results_map

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        config = json.load(f)

        level = config["level"]
        output = config["output"]
    
    # Run the experiment for BFS, DFS, and IDDFS
    results = run_experiments(level, ["bfs", "dfs", "iddfs"])
    
    # Print or save the results
    with open(output, "w") as out_file:
        json.dump(results, out_file, ensure_ascii=False, indent=4)
