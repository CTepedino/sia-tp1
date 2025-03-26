import json
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

json_path = sys.argv[1]

file_name = os.path.splitext(os.path.basename(json_path))[0]
output_file = f"grafico_nodos_{file_name}.png"

with open(json_path, "r") as f:
    data = json.load(f)

methods = ["bfs", "dfs", "iddfs"]

nodes_expanded = {method: [run["nodes_expanded"] for run in data[method]["executions"]] for method in methods}
nodes_in_frontier = {method: [run["nodes_in_frontier"] for run in data[method]["executions"]] for method in methods}

means_expanded = [np.mean(nodes_expanded[method]) for method in methods]
means_frontier = [np.mean(nodes_in_frontier[method]) for method in methods]

x = np.arange(len(methods))  
width = 0.35 

plt.figure(figsize=(8, 5))
plt.bar(x - width/2, means_expanded, width, label="Nodos expandidos", color="blue")
plt.bar(x + width/2, means_frontier, width, label="Nodos en frontera", color="green")

plt.ylabel("Cantidad de nodos")
plt.xlabel("Método de búsqueda")
plt.title("Comparación de nodos expandidos vs nodos en frontera")
plt.xticks(x, methods)  
plt.legend()

plt.savefig(output_file)
