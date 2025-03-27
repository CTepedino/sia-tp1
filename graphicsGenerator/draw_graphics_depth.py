import json
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Obtener el path del archivo JSON desde los argumentos
json_path = sys.argv[1]

# Extraer el nombre del archivo sin la extensión .json
file_name = os.path.splitext(os.path.basename(json_path))[0]
output_file = f"grafico_costo_iddfs_{file_name}.png"

# Cargar el JSON desde el archivo especificado
with open(json_path, "r") as f:
    data = json.load(f)

# Extraer datos solo para IDDFS
iddfs_executions = data["iddfs"]["executions"]

# Obtener costos por profundidad
depth_costs = {}
for run in iddfs_executions:
    depth = run["depth"]
    cost = run["cost"]
    if depth in depth_costs:
        depth_costs[depth].append(cost)
    else:
        depth_costs[depth] = [cost]

# Calcular promedios por cada profundidad
depths = sorted(depth_costs.keys())  # Ordenar las profundidades
costs = [np.mean(depth_costs[d]) for d in depths]  # Promedio del costo por profundidad

# Crear gráfico de barras
plt.figure(figsize=(8, 5))
plt.bar([str(d) for d in depths], costs, color="purple")

# Agregar etiquetas y título
plt.ylabel("Costo")
plt.xlabel("Profundidad (depth)")
plt.title("Costo del IDDFS en función de la profundidad")

# Guardar el gráfico
plt.savefig(output_file)