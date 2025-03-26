import json
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

json_path = sys.argv[1]

file_name = os.path.splitext(os.path.basename(json_path))[0]
output_file = f"grafico_tiempos_{file_name}.png"

with open(json_path, "r") as f:
    data = json.load(f)

heuristics = list(data["greedy"].keys())  
greedy_times = []
a_star_times = []

for heuristic in heuristics:
    greedy_data = data["greedy"][heuristic]["executions"]
    a_star_data = data["a_star"][heuristic]["executions"]

    greedy_avg_time = np.mean([float(exec_data["time"].replace("s", "")) for exec_data in greedy_data])
    a_star_avg_time = np.mean([float(exec_data["time"].replace("s", "")) for exec_data in a_star_data])

    greedy_times.append(greedy_avg_time)
    a_star_times.append(a_star_avg_time)

bar_width = 0.35
index = np.arange(len(heuristics))

plt.figure(figsize=(10, 6))

plt.bar(index, greedy_times, bar_width, label="Greedy", color="blue")
plt.bar(index + bar_width, a_star_times, bar_width, label="A*", color="red")

plt.ylabel("Tiempo promedio (segundos)")
plt.xlabel("Heurísticas")
plt.title("Comparación de tiempos entre Greedy y A*")
plt.xticks(index + bar_width / 2, heuristics, rotation=75)
plt.legend()

plt.tight_layout()
plt.savefig(output_file)
