import heapq
import random
import sys
import networkx as nx
from matplotlib.animation import FuncAnimation

#!/usr/bin/env python3
# GitHub Copilot
# Archivo: 001_Arbol_Parcial_Prim.py
# Genera y grafica los pasos de una ejecución parcial del algoritmo de Prim.
# Requisitos: networkx, matplotlib
# Si faltan librerías: pip install networkx matplotlib


import matplotlib.pyplot as plt

def ejemplo_grafo(n_nodes=8, seed=42, density=0.4, weight_range=(1, 20)):
    random.seed(seed)
    G = nx.Graph()
    for i in range(n_nodes):
        G.add_node(i)
    # agregar aristas aleatorias con pesos
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            if random.random() < density:
                w = random.randint(*weight_range)
                G.add_edge(i, j, weight=w)
    # asegurar conectividad mínima (añadir camino lineal)
    for i in range(n_nodes - 1):
        if not G.has_edge(i, i + 1):
            G.add_edge(i, i + 1, weight=random.randint(*weight_range))
    return G

def prim_steps(G, start=None):
    """Generador que produce los pasos de Prim.
    En cada paso yield (u, v, w, mst_edges_list, visited_set)
    """
    if start is None:
        start = list(G.nodes())[0]
    visited = set([start])
    edges_heap = []
    # añadir aristas incidentes al nodo inicial
    for v, attrs in G[start].items():
        heapq.heappush(edges_heap, (attrs['weight'], start, v))
    mst_edges = []
    while edges_heap and len(visited) < G.number_of_nodes():
        w, u, v = heapq.heappop(edges_heap)
        if v in visited and u in visited:
            continue
        # escoger la arista que conecta con nuevo nodo
        new_node = v if v not in visited else u
        if new_node in visited:
            continue
        visited.add(new_node)
        mst_edges.append((u, v, w))
        # añadir nuevas aristas que salen del nuevo nodo
        for nbr, attrs in G[new_node].items():
            if nbr not in visited:
                heapq.heappush(edges_heap, (attrs['weight'], new_node, nbr))
        yield (u, v, w, list(mst_edges), set(visited))
    # último yield para indicar final (puede repetirse con None si ya completo)
    yield (None, None, None, list(mst_edges), set(visited))

def dibujar_paso(ax, G, pos, mst_edges, highlight_edge=None, visited=None):
    ax.clear()
    ax.set_title("Árbol parcial de Prim: pasos")
    # dibujar todas las aristas en gris con pesos
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue')
    nx.draw_networkx_labels(G, pos, ax=ax)
    # dibujar aristas base
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='lightgray', width=1)
    # dibujar pesos
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    # dibujar aristas del MST en rojo
    if mst_edges:
        edges = [(u, v) for (u, v, w) in mst_edges]
        nx.draw_networkx_edges(G, pos, edgelist=edges, ax=ax, edge_color='red', width=3)
    # resaltar arista seleccionada en verde
    if highlight_edge and highlight_edge[0] is not None:
        u, v, w = highlight_edge
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], ax=ax, edge_color='green', width=4)
    # marcar nodos visitados
    if visited:
        nx.draw_networkx_nodes(G, pos, nodelist=list(visited), node_color='orange', ax=ax)

def main():
    # generar grafo de ejemplo
    G = ejemplo_grafo(n_nodes=10, seed=1, density=0.35, weight_range=(1, 15))
    pos = nx.spring_layout(G, seed=2)
    steps = list(prim_steps(G, start=0))
    fig, ax = plt.subplots(figsize=(8, 6))

    # preparar frames (todos los pasos incluidos)
    frames = steps

    def update(i):
        u, v, w, mst_edges, visited = frames[i]
        if u is None:
            titulo = f"Finalizado: MST con {len(mst_edges)} aristas, peso total = {sum(x[2] for x in mst_edges)}"
            ax.set_title(titulo)
        else:
            ax.set_title(f"Paso {i+1}: seleccionar arista ({u}, {v}) peso={w}")
        dibujar_paso(ax, G, pos, mst_edges, highlight_edge=(u, v, w) if u is not None else None, visited=visited)

    global ani
    ani = FuncAnimation(fig, update, frames=len(frames), interval=1000, repeat=False)
    plt.tight_layout()
    # Intentar guardar la animación en un archivo mp4 usando ffmpeg.
    # Si no está disponible, se intentará mostrar la figura (si hay backend).
    try:
        ani.save("prim.mp4", writer="ffmpeg", fps=1)
        print("Animación guardada en 'prim.mp4'.")
    except Exception as e:
        print("No se pudo guardar la animación con ffmpeg:", e)
        print("Intentando fallback: guardar como GIF usando 'pillow'...")
        try:
            ani.save("prim.gif", writer="pillow", fps=1)
            print("Fallback: animación guardada en 'prim.gif'.")
        except Exception as e_gif:
            print("Fallback GIF falló:", e_gif)
            print("Se intentará mostrar la animación en pantalla (si el backend lo permite)...")
            try:
                plt.show()
            except Exception as e2:
                print("Mostrar en pantalla falló:", e2)

if __name__ == "__main__":
    main()