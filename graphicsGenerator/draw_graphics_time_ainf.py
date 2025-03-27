import json
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

json_path = sys.argv[1]

file_name = os.path.splitext(os.path.basename(json_path))[0]
output_file = f"fgrafico_tiempo_bfs_a_star_{file_name}.png"

with open(json_path, "r") as f:
    data = json.load(f)

methods = ["not_cornered", "not_wall_stuck", "avoid_deadlocks"]
methods2 = [ "Bfs", "A* Not cornered", "A* Not wall stuck", "A* Avoid deadlocks"]


means = [data["bfs"]["time_mean"]] + [data["a_star"][method]["time_mean"] for method in methods]
std_devs = [data["bfs"]["time_std"]] + [data["a_star"][method]["time_std"] for method in methods]

lower_errors = [min(mean, std_dev) for mean, std_dev in zip(means, std_devs)]
upper_errors = std_devs

error_bars = [lower_errors, upper_errors]

plt.figure(figsize=(10, 5))
plt.bar(methods2, means, yerr=error_bars, capsize=5, color=["blue", "green", "red","yellow","purple"])

plt.ylabel("Tiempo de ejecución (s)")
plt.xlabel("Método de búsqueda")
plt.title("Comparación de tiempos de búsqueda con desviación estándar")

plt.savefig(output_file)
