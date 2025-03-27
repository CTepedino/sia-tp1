import json
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

json_path = sys.argv[1]

file_name = os.path.splitext(os.path.basename(json_path))[0]
output_file = f"fgrafico_nodos_exp_dfs_greedy_{file_name}.png"

with open(json_path, "r") as f:
    data = json.load(f)

methods = [ "misplaced_boxes", "manhattan_distance_sum", "walled_distance_sum", "nearest_box"]
methods2 = [ "Dfs", "Greedy \nMisplaced Boxes", "Greedy \nManhattan distance", "Greedy \nWalled distance", "Greedy \nNearest box"]


means_expanded = [data["dfs"]["nodes_expanded_mean"]] + [data["greedy"][method]["nodes_expanded_mean"] for method in methods]

x = np.arange(len(methods2))
width = 0.35

plt.figure(figsize=(10, 5))
plt.bar(x , means_expanded, width, label="Nodos expandidos", color="blue")


plt.ylabel("Cantidad de nodos")
plt.xlabel("Método de búsqueda")
plt.title("Comparación de nodos expandidos ")
plt.xticks(x, methods2)
plt.legend()

plt.savefig(output_file)
