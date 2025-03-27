import sys
import json
import time

from search.utils.heuristics import heuristics  # Asegúrate de importar las heurísticas
from search.aStarSearch import a_star
from search.globalGreedySearch import greedy

methods = {
    "greedy": lambda level, h=None: greedy(level, h),
    "a_star": lambda level, h=None: a_star(level, h)
}

heuristics_list = [
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
    "walled_distance_sum_adl"
]

def run_experiments(level, methods_to_run, heuristics_to_use, num_runs=100):
    results_map = {}

    for method_name in methods_to_run:
        results_map[method_name] = {}

        for heuristic_name in heuristics_to_use:
            executions = []
            heuristic_function = heuristics[heuristic_name]  # Convertir string en función

            for _ in range(num_runs):
                start_time = time.time()
                method = methods[method_name]

                # Ejecutar el algoritmo con la heurística seleccionada
                result = method(level, h=heuristic_function)
                dict_result = result.to_dict()

                result_data = {
                    "solved": dict_result["solved"],
                    "cost": dict_result["cost"],
                    "nodes_expanded": dict_result["nodes_expanded"],
                    "nodes_in_frontier": dict_result["nodes_in_frontier"],
                    "time": dict_result["time"]
                }

                executions.append(result_data)

            results_map[method_name][heuristic_name] = {"executions": executions}
    
    return results_map

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        config = json.load(f)

        level = config["level"]
        output = config["output"]

    # Ejecutar experimentos con greedy y A* para todas las heurísticas
    results = run_experiments(level, ["greedy", "a_star"], heuristics_list)

    # Guardar los resultados en un archivo JSON
    with open(output+"_and_heuristics.json", "w") as out_file:
        json.dump(results, out_file, ensure_ascii=False, indent=4)
