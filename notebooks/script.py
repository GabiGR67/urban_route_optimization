import osmnx as ox
import matplotlib.pyplot as plt
from shapely.geometry import Point
from geopy.distance import geodesic

# Define la zona
place = "Salamanca, Madrid, Spain"

# Descarga la red vial para coches
G = ox.graph_from_place(place, network_type="drive")

# Detectar semáforos reales desde OSM
semaforo_nodes = [
    n for n, d in G.nodes(data=True)
    if d.get('highway') == 'traffic_signals'
]

# Detectar señales simuladas (añade tus nodos reales aquí)
signal_nodes = [list(G.nodes)[0], list(G.nodes)[10], list(G.nodes)[20]]

# Crear listas por tipo
lista_semaforos = []
lista_senales = []
lista_interseccion_2 = []
lista_interseccion_3 = []
lista_interseccion_4plus = []
lista_irrelevantes = []

for node, data in G.nodes(data=True):
    tipo = data["type"]
    if tipo == "semaforo":
        lista_semaforos.append(node)
    elif tipo == "senal":
        lista_senales.append(node)
    elif tipo == "interseccion_2":
        lista_interseccion_2.append(node)
    elif tipo == "interseccion_3":
        lista_interseccion_3.append(node)
    elif tipo == "interseccion_4+":
        lista_interseccion_4plus.append(node)
    elif tipo == "irrelevante":
        lista_irrelevantes.append(node)

for node, data in G.nodes(data=True):
    if node in semaforo_nodes:
        data["type"] = str("semaforo")
    elif node in signal_nodes:
        data["type"] = str("senal")
    else:
        sc = data.get("street_count", 0)
        if sc == 2:
            data["type"] = str("interseccion_2")
        elif sc == 3:
            data["type"] = str("interseccion_3")
        elif sc >= 4:
            data["type"] = str("interseccion_4+")
        else:
            data["type"] = str("irrelevante")


from geopy.distance import geodesic
import pandas as pd

CSV_PATH = "../data/graph_data/TL_coords.csv"
THRESHOLD_METERS = 5

# --- Leer coordenadas de semáforos desde CSV
df_semaforos = pd.read_csv(CSV_PATH)
semaforo_coords = list(zip(df_semaforos["GPSLatitude"], df_semaforos["GPSLongitude"]))

# --- Asignar tipo de nodo "semaforo" si está cerca de una coordenada conocida
for node, data in G.nodes(data=True):
    coord_node = (data["y"], data["x"])
    for coord_semaforo in semaforo_coords:
        if geodesic(coord_node, coord_semaforo).meters < THRESHOLD_METERS:
            data["type"] = "semaforo"
            break  # evitar marcar múltiples veces

# --- Guardar el grafo con los nuevos atributos
ox.save_graphml(G, filepath="../data/graph_data/graph_tl.graphml")


# ------------------------------------------------


import osmnx as ox
import matplotlib.pyplot as plt

# Cargar el grafo con los tipos ya asignados y guardados
graph_path = "../data/graph_data/graph_tl.graphml"
G = ox.load_graphml(graph_path)

# Parámetros
SIZE = 10

# Diccionario de colores por tipo
color_map = {
    "semaforo": "blue",
    "senal": "purple",
    "interseccion_2": "green",
    "interseccion_3": "orange",
    "interseccion_4+": "red",
    "irrelevante": "yellow"
}

# Listas para visualización
node_xs, node_ys, node_colors, node_sizes = [], [], [], []

# Construir listas con prioridad visual: semáforo > señal > intersecciones > irrelevante
for node, data in G.nodes(data=True):
    x, y = data["x"], data["y"]
    tipo = data.get("type", "irrelevante")
    color = color_map.get(tipo, "yellow")

    node_xs.append(x)
    node_ys.append(y)
    node_colors.append(color)
    node_sizes.append(SIZE)

# Dibujar grafo sin nodos por defecto
fig, ax = ox.plot_graph(
    G,
    node_size=0,
    edge_color='gray',
    show=False,
    close=False
)

# Pintar nodos personalizados por tipo
ax.scatter(
    node_xs,
    node_ys,
    c=node_colors,
    s=node_sizes,
    edgecolors='black',
    zorder=3
)

plt.show()


# ------------------------------------------------

import networkx as nx
import math

# Cargar el grafo directamente desde GraphML con networkx
graph_path = "../data/graph_data/graph_tl.graphml"
G = nx.read_graphml(graph_path)

# Convertir nodos a float para asegurar precisión
for node, data in G.nodes(data=True):
    data["x"] = float(data["x"])
    data["y"] = float(data["y"])

# Penalizaciones
SEMAFORO_PENALTY = 15
SENAL_PENALTY = 5
INTERSECTION_3_PENALTY = 2
INTERSECTION_4_PENALTY = 4
LEFT_TURN_PENALTY = 8
RIGHT_TURN_PENALTY = 4

# Calcular ángulo entre aristas
def calculate_turn_angle(u, v, w):
    try:
        x1, y1 = G.nodes[u]['x'], G.nodes[u]['y']
        x2, y2 = G.nodes[v]['x'], G.nodes[v]['y']
        x3, y3 = G.nodes[w]['x'], G.nodes[w]['y']

        vec1 = (x2 - x1, y2 - y1)
        vec2 = (x3 - x2, y3 - y2)

        dot = vec1[0]*vec2[0] + vec1[1]*vec2[1]
        mag1 = math.hypot(*vec1)
        mag2 = math.hypot(*vec2)
        if mag1 * mag2 == 0:
            return 0
        cos_angle = dot / (mag1 * mag2)
        angle_rad = math.acos(min(1, max(-1, cos_angle)))
        return math.degrees(angle_rad)
    except:
        return 0

# Asignar pesos
for u, v, data in G.edges(data=True):
    length = float(data.get('length', 1))
    weight = length / 5

    for node in [u, v]:
        tipo = G.nodes[node].get('type', '')
        if tipo == 'semaforo':
            weight += SEMAFORO_PENALTY
        elif tipo == 'senal':
            weight += SENAL_PENALTY
        elif tipo == 'interseccion_3':
            weight += INTERSECTION_3_PENALTY
        elif tipo == 'interseccion_4+':
            weight += INTERSECTION_4_PENALTY

    # Simular giro (simplemente tomando un sucesor si existe)
    successors = list(G.successors(v)) if hasattr(G, 'successors') else []
    if successors:
        next_node = successors[0]
        angle = calculate_turn_angle(u, v, next_node)
        if angle > 180:
            angle = 360 - angle
        if angle > 100:
            weight += LEFT_TURN_PENALTY
        elif angle < 80:
            weight += RIGHT_TURN_PENALTY

    data['weight'] = weight

# Guardar grafo con pesos
output_path = "../data/graph_data/graph_weighted_full.graphml"
nx.write_graphml(G, output_path)


# ------------------------------------------------

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from geopy.distance import geodesic
import pandas as pd
from networkx.algorithms.simple_paths import shortest_simple_paths


# Definir coordenadas de origen y destino
lat_origen, lon_origen = 40.442163, -3.663568
lat_destino, lon_destino = 40.424965, -3.678606

# Función para encontrar el nodo más cercano
def closest_node(lat, lon, G):
    min_dist = float('inf')
    closest = None
    for node, data in G.nodes(data=True):
        node_lat = float(data['y'])
        node_lon = float(data['x'])
        dist = geodesic((lat, lon), (node_lat, node_lon)).meters
        if dist < min_dist:
            min_dist = dist
            closest = node
    return closest

# Encontrar nodos más cercanos
start_node = closest_node(lat_origen, lon_origen, G)
end_node = closest_node(lat_destino, lon_destino, G)

# Ejecutar algoritmos y registrar resultados
results = {}

# Obtener las 2 rutas más cortas (en cuanto a 'weight')
k_paths = list(shortest_simple_paths(G, start_node, end_node, weight='weight'))

# Primera es la de Dijkstra/A*, segunda es una alternativa
ruta_alternativa = k_paths[1]  # Segunda mejor ruta
costo_alternativa = sum(G[u][v][0]['weight'] for u, v in zip(ruta_alternativa[:-1], ruta_alternativa[1:]))

# Dijkstra
path_dijkstra = nx.shortest_path(G, start_node, end_node, weight='weight')
cost_dijkstra = nx.shortest_path_length(G, start_node, end_node, weight='weight')
results['Dijkstra'] = {'path': path_dijkstra, 'cost': cost_dijkstra}

# A*
path_astar = nx.astar_path(G, start_node, end_node, weight='weight')
cost_astar = nx.astar_path_length(G, start_node, end_node, weight='weight')
results['A*'] = {'path': path_astar, 'cost': cost_astar}

# Dibujar grafo con caminos
pos = {node: (float(G.nodes[node]['x']), float(G.nodes[node]['y'])) for node in G.nodes}

plt.figure(figsize=(12, 10))
nx.draw(G, pos, node_size=5, edge_color='lightgray', with_labels=False)

# Dijkstra (verde línea continua)
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=list(zip(path_dijkstra[:-1], path_dijkstra[1:])),
    edge_color='green',
    width=2,
    label='Dijkstra'
)

# A* (azul línea discontinua)
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=list(zip(path_astar[:-1], path_astar[1:])),
    edge_color='blue',
    width=2,
    style='dashed',
    label='A*'
)

# Ruta alternativa (roja punteada)
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=list(zip(ruta_alternativa[:-1], ruta_alternativa[1:])),
    edge_color='red',
    width=2,
    style='dotted',
    label='Ruta alternativa'
)

# Leyenda
dijkstra_line = mlines.Line2D([], [], color='green', label='Dijkstra')
astar_line = mlines.Line2D([], [], color='blue', linestyle='--', label='A*')
alt_line = mlines.Line2D([], [], color='red', linestyle=':', label='Ruta alternativa')
plt.legend(handles=[dijkstra_line, astar_line, alt_line])

plt.title("Comparación de rutas: Dijkstra (verde) vs A* (azul)")
plt.axis('off')
plt.show()

# Mostrar tabla comparativa
pd.DataFrame({
    "Algoritmo": ["Dijkstra", "A*", "Ruta Alternativa"],
    "Coste Total": [cost_dijkstra, cost_astar, costo_alternativa],
    "Nodos en Ruta": [len(path_dijkstra), len(path_astar), len(ruta_alternativa)]
})
