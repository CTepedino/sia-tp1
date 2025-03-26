import json
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

json_path = sys.argv[1]

file_name = os.path.splitext(os.path.basename(json_path))[0]
output_file = f"grafico_nodosexp_{file_name}.png"

with open(json_path, "r") as f:
    data = json.load(f)

methods = [ "dfs", "greedy mispl", "greedy manh", "greedy wall", "greedy nearest"]
methods2 = [ "Dfs", "Greedy \nMisplaced Boxes", "Greedy \nManhattan distance", "Greedy \nWalled distance", "Greedy \nNearest box"]


nodes_expanded = {method: [run["nodes_expanded"] for run in data[method]["executions"]] for method in methods}


means_expanded = [np.mean(nodes_expanded[method]) for method in methods]


x = np.arange(len(methods))
width = 0.35

plt.figure(figsize=(10, 5))
plt.bar(x , means_expanded, width, label="Nodos expandidos", color="blue")


plt.ylabel("Cantidad de nodos")
plt.xlabel("Método de búsqueda")
plt.title("Comparación de nodos expandidos ")
plt.xticks(x, methods2)
plt.legend()

plt.savefig(output_file)
