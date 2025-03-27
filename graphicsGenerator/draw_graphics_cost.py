import json
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

json_path = sys.argv[1]

file_name = os.path.splitext(os.path.basename(json_path))[0]
output_file = f"grafico_costos_{file_name}.png"

with open(json_path, "r") as f:
    data = json.load(f)

methods = ["bfs", "dfs", "iddfs"]

costs = {method: [run["cost"] for run in data[method]["executions"]] for method in methods}

means = [np.mean(costs[method]) for method in methods]
std_devs = [np.std(costs[method]) for method in methods]

lower_errors = [min(mean, std_dev) for mean, std_dev in zip(means, std_devs)]
upper_errors = std_devs

error_bars = [lower_errors, upper_errors] 

plt.figure(figsize=(8, 5))
plt.bar(methods, means, yerr=error_bars, capsize=5, color=["blue", "green", "red"])

plt.ylabel("Costo")
plt.xlabel("Método de búsqueda")
plt.title("Comparación de costos con desviación estándar")

plt.savefig(output_file)
