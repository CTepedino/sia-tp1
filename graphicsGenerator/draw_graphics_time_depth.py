import json
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

json_path = sys.argv[1]

file_name = os.path.splitext(os.path.basename(json_path))[0]
output_file = f"grafico_tiempo_iddfs_{file_name}.png"

with open(json_path, "r") as f:
    data = json.load(f)

iddfs_executions = data["iddfs"]["executions"]


depth_times = {}
for run in iddfs_executions:
    depth = run["depth"]
    time = float(run["time"].replace("s", ""))  
    if depth in depth_times:
        depth_times[depth].append(time)
    else:
        depth_times[depth] = [time]

depths = sorted(depth_times.keys())  
times = [np.mean(depth_times[d]) for d in depths]  

plt.figure(figsize=(8, 5))
plt.bar([str(d) for d in depths], times, color="orange")

plt.ylabel("Tiempo de ejecución (s)")
plt.xlabel("Profundidad (depth)")
plt.title("Tiempo de ejecución del IDDFS en función de la profundidad")

plt.savefig(output_file)
