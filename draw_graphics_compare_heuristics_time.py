import json
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

json_path = sys.argv[1]

file_name = os.path.splitext(os.path.basename(json_path))[0]
output_file = f"fgrafico_comparacion_heuristicas_manhattan_distance_sum_{file_name}.png"

with open(json_path, "r") as f:
    data = json.load(f)

heuristics = ["manhattan_distance_sum", "manhattan_distance_sum_adl"]
heuristics2 = ["Manhattan distance", "Manhattan distance avoid deadlocks"]
# heuristics = ["nearest_box", "nearest_box_adl"]
# heuristics2 = ["Nearest box", "Nearest box avoid deadlocks"]
# heuristics = ["walled_distance_sum", "walled_distance_sum_adl"]
# heuristics2 = ["Walled distance sum", "Walled distance sum avoid deadlocks"]

a_star_times = []

for heuristic in heuristics:

    # a_star_data = data["a_star"][heuristic]["executions"]


    # a_star_avg_time = np.mean([float(exec_data["time"].replace("s", "")) for exec_data in a_star_data])
    a_star_avg_time = data["a_star"][heuristic]["time_mean"]


    a_star_times.append(a_star_avg_time)

bar_width = 0.35
index = np.arange(len(heuristics))

plt.figure(figsize=(8, 6))


plt.bar(index + bar_width, a_star_times, bar_width, color="red")

plt.ylabel("Tiempo promedio (segundos)")

plt.title("Comparación de tiempos de A*")
plt.xticks(index + bar_width , heuristics2)


plt.tight_layout()
plt.savefig(output_file)
