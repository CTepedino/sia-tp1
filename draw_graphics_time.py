import json
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

json_path = sys.argv[1]

file_name = os.path.splitext(os.path.basename(json_path))[0]
output_file = f"grafico_resultados_{file_name}.png"

with open(json_path, "r") as f:
    data = json.load(f)

methods = ["bfs", "dfs", "iddfs"]

times = {method: [float(run["time"].replace("s", "")) for run in data[method]["executions"]] for method in methods}

means = [np.mean(times[method]) for method in methods]
std_devs = [np.std(times[method]) for method in methods]

lower_errors = [min(mean, std_dev) for mean, std_dev in zip(means, std_devs)]
upper_errors = std_devs

error_bars = [lower_errors, upper_errors]  

plt.figure(figsize=(8, 5))
plt.bar(methods, means, yerr=error_bars, capsize=5, color=["blue", "green", "red"])

plt.ylabel("Tiempo de ejecución (s)")
plt.xlabel("Método de búsqueda")
plt.title("Comparación de tiempos de búsqueda con desviación estándar")

plt.savefig(output_file)
