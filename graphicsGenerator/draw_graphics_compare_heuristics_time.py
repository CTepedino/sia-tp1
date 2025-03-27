import json
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

json_path = sys.argv[1]

file_name = os.path.splitext(os.path.basename(json_path))[0]
output_file = f"fgrafico_comparacion_heuristicas_walled_distance_sum_{file_name}.png"

with open(json_path, "r") as f:
    data = json.load(f)

# heuristics = ["manhattan_distance_sum", "manhattan_distance_sum_adl"]
# heuristics2 = ["Manhattan distance", "Manhattan distance avoid deadlocks"]
# heuristics = ["nearest_box", "nearest_box_adl"]
# heuristics2 = ["Nearest box", "Nearest box avoid deadlocks"]
heuristics = ["walled_distance_sum", "walled_distance_sum_adl"]
heuristics2 = ["Walled distance sum", "Walled distance sum avoid deadlocks"]

a_star_times = []
a_star_std_devs = []

for heuristic in heuristics:
    a_star_avg_time = data["a_star"][heuristic]["time_mean"]
    a_star_dsv = data["a_star"][heuristic]["time_std"]

    a_star_times.append(a_star_avg_time)
    a_star_std_devs.append(a_star_dsv)

bar_width = 0.35
index = np.arange(len(heuristics))

plt.figure(figsize=(8, 6))

# Agregar barras de error con el desvío estándar
plt.bar(
    index + bar_width,
    a_star_times,
    bar_width,
    color="red",
    yerr=a_star_std_devs,  # Agregar barras de error
    capsize=5,  # Tamaño de las líneas de error
    label="Tiempo promedio ± std"
)

plt.ylabel("Tiempo promedio (segundos)")
plt.title("Comparación de tiempos de A*")
plt.xticks(index + bar_width, heuristics2)
plt.legend()

plt.tight_layout()
plt.savefig(output_file)
