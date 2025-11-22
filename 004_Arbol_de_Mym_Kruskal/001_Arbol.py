import os
import math
import random
from typing import Any, List, Optional, Tuple, Dict
import networkx as nx

#!/usr/bin/env python3
"""
001_Arbol.py

Código en Python para construir un árbol de máximos y mínimos (Minimax),
mostrar paso a paso la evaluación y generar una gráfica del árbol en cada paso.

Características:
- Construye un árbol binario (o k-ario) a partir de una estructura anidada o aleatoria.
- Ejecuta Minimax (opcionalmente con alpha-beta) mostrando pasos.
- Guarda y muestra gráficas paso a paso usando networkx + matplotlib.
- Imprime en consola la traza de evaluación.

Requisitos:
- networkx
- matplotlib

Si faltan paquetes, instálelos con:
pip install networkx matplotlib
"""

import matplotlib.pyplot as plt

# -------------------------
# Estructura de datos
# -------------------------
class Node:
    def __init__(self, name: str, children: Optional[List["Node"]] = None, value: Optional[float] = None):
        self.name = name
        self.children = children or []
        self.value = value  # valor calculado por Minimax (None inicialmente para nodos internos)

    def is_leaf(self):
        return len(self.children) == 0

    def __repr__(self):
        return f"Node({self.name}, value={self.value})"

# -------------------------
# Construcción de árboles
# -------------------------
def build_tree_from_nested(structure: Any, name_prefix="N") -> Node:
    """
    Construye un árbol a partir de una estructura anidada.
    Formato aceptado:
      - Si 'structure' es un número -> hoja con ese valor.
      - Si es una lista -> nodo interno cuyas entradas son subestructuras.
    Se asignan nombres únicos basados en name_prefix y una numeración recursiva.
    """
    counter = {"i": 0}

    def _build(s) -> Node:
        counter["i"] += 1
        myname = f"{name_prefix}{counter['i']}"
        if isinstance(s, (int, float)):
            return Node(name=myname, children=[], value=float(s))
        elif isinstance(s, list):
            children = [_build(sub) for sub in s]
            return Node(name=myname, children=children, value=None)
        else:
            raise ValueError("Estructura no soportada. Use números o listas.")
    return _build(structure)

def build_random_full_tree(depth: int, branching: int = 2, leaf_range=(0, 9), name_prefix="R") -> Node:
    """
    Construye un árbol completo de profundidad 'depth' (depth=0 => solo raíz hoja).
    Cada hoja recibe un valor aleatorio en leaf_range.
    """
    counter = {"i": 0}
    def _build(d):
        counter["i"] += 1
        myname = f"{name_prefix}{counter['i']}"
        if d == 0:
            return Node(name=myname, children=[], value=float(random.randint(*leaf_range)))
        children = [_build(d-1) for _ in range(branching)]
        return Node(name=myname, children=children, value=None)
    return _build(depth)

# -------------------------
# Minimax con trazado paso a paso
# -------------------------
class StepRecorder:
    """
    Guarda "snapshots" para visualizar el árbol en distintos pasos.
    Cada snapshot contiene:
      - Qué nodo se está evaluando/actualizando (node.name)
      - Estado actual de valores en nodos (mapping name -> value or None)
      - Descripción textual del paso
    """
    def __init__(self):
        self.snapshots = []

    def record(self, root: Node, current_node: Optional[Node], description: str):
        state = {}
        def _collect(n: Node):
            state[n.name] = n.value
            for c in n.children:
                _collect(c)
        _collect(root)
        self.snapshots.append({
            "highlight": current_node.name if current_node else None,
            "state": state,
            "description": description
        })

def minimax(root: Node, maximizing_player: bool = True, recorder: Optional[StepRecorder] = None, alpha_beta: bool = False) -> float:
    """
    Ejecuta Minimax sobre 'root', actualiza node.value en cada nodo y opcionalmente
    graba pasos en recorder. Retorna el valor calculado para la raíz.

    Si alpha_beta=True, realiza poda alfa-beta y también registra los pasos importantes.
    """
    INF = float("inf")

    def _minimax(node: Node, maximizing: bool, alpha: float, beta: float) -> float:
        # Record start of evaluation
        if recorder:
            recorder.record(root, node, f"Comienza evaluación de {node.name} (maximizing={maximizing})")

        if node.is_leaf():
            # Leaf: su value ya está definido
            if recorder:
                recorder.record(root, node, f"Hoja {node.name} con valor {node.value}")
            return node.value

        if maximizing:
            value = -INF
            for child in node.children:
                v = _minimax(child, False, alpha, beta)
                if recorder:
                    recorder.record(root, child, f"{node.name}: evaluar hijo {child.name} -> {v}")
                if v > value:
                    value = v
                    if recorder:
                        recorder.record(root, node, f"{node.name}: nuevo mejor valor (max) = {value}")
                alpha = max(alpha, value)
                if alpha_beta and beta <= alpha:
                    if recorder:
                        recorder.record(root, node, f"{node.name}: poda beta (alpha={alpha} >= beta={beta})")
                    break
            node.value = value
            if recorder:
                recorder.record(root, node, f"{node.name} fijado a {node.value} (max)")
            return value
        else:
            value = INF
            for child in node.children:
                v = _minimax(child, True, alpha, beta)
                if recorder:
                    recorder.record(root, child, f"{node.name}: evaluar hijo {child.name} -> {v}")
                if v < value:
                    value = v
                    if recorder:
                        recorder.record(root, node, f"{node.name}: nuevo mejor valor (min) = {value}")
                beta = min(beta, value)
                if alpha_beta and beta <= alpha:
                    if recorder:
                        recorder.record(root, node, f"{node.name}: poda alpha (beta={beta} <= alpha={alpha})")
                    break
            node.value = value
            if recorder:
                recorder.record(root, node, f"{node.name} fijado a {node.value} (min)")
            return value

    return _minimax(root, maximizing_player, -INF, INF)

# -------------------------
# Visualización con networkx + matplotlib
# -------------------------
def tree_to_networkx(root: Node) -> nx.DiGraph:
    G = nx.DiGraph()
    def _add(n: Node):
        label = f"{n.name}\n{'' if n.value is None else n.value}"
        G.add_node(n.name, label=label, node_obj=n)
        for c in n.children:
            G.add_edge(n.name, c.name)
            _add(c)
    _add(root)
    return G

def hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
    """
    Positioning for a tree — returns dict {node: (x,y)}.
    """
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    children = list(G.successors(root))
    if len(children) != 0:
        dx = width / len(children)
        nextx = xcenter - width/2 - dx/2
        for child in children:
            nextx += dx
            pos = hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root)
    return pos

def plot_snapshot(root: Node, snapshot: Dict, step_index: int, out_dir: str):
    G = tree_to_networkx(root)
    pos = hierarchy_pos(G, root.name, width=1.0, vert_gap=0.15, vert_loc=0.9, xcenter=0.5)

    labels = {}
    node_colors = []
    node_sizes = []
    highlight = snapshot.get("highlight")

    # Map node values from snapshot
    state = snapshot["state"]

    for n in G.nodes:
        val = state.get(n, None)
        label = f"{n}\n{'' if val is None else val}"
        labels[n] = label
        node_obj = G.nodes[n].get("node_obj")
        # color logic: highlight node in red, leaves grey, internal blue
        if n == highlight:
            node_colors.append("#ff6666")
            node_sizes.append(900)
        elif (node_obj and node_obj.is_leaf()):
            node_colors.append("#cccccc")
            node_sizes.append(700)
        else:
            node_colors.append("#88c0ff")
            node_sizes.append(900)

    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, labels=labels, with_labels=True,
            node_color=node_colors, node_size=node_sizes,
            font_size=10, font_weight='bold', arrows=False)
    # add step description
    desc = snapshot.get("description", "")
    plt.title(f"Paso {step_index}: {desc}", fontsize=10)
    plt.axis('off')
    os.makedirs(out_dir, exist_ok=True)
    filename = os.path.join(out_dir, f"step_{step_index:03d}.png")
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    return filename

def play_snapshots(root: Node, recorder: StepRecorder, delay: float = 1.0, out_dir="minimax_steps"):
    """
    Dibuja/guarda cada snapshot y muestra en ventana secuencialmente.
    """
    files = []
    for i, snap in enumerate(recorder.snapshots, start=1):
        fname = plot_snapshot(root, snap, i, out_dir)
        files.append(fname)
        # Mostrar en pantalla si hay display disponible
        try:
            img = plt.imread(fname)
            plt.figure(figsize=(10, 6))
            plt.imshow(img)
            plt.axis('off')
            plt.pause(delay)
            plt.close()
        except Exception:
            # si no es posible mostrar (p. ej. headless), solo seguimos
            pass
    print(f"Se guardaron {len(files)} imágenes en '{out_dir}/' (una por paso).")

# -------------------------
# Ejemplo de uso
# -------------------------
if __name__ == "__main__":
    # Ejemplo: podemos definir un árbol manualmente o generar uno aleatorio.

    # 1) Árbol definido manualmente (listas anidadas):
    #    [ [3, 5], [6, [9, 1]], [2, 7] ]
    manual_structure = [
        [3, 5],
        [6, [9, 1]],
        [2, 7]
    ]
    root = build_tree_from_nested(manual_structure, name_prefix="M")

    # 2) O crear uno aleatorio:
    # root = build_random_full_tree(depth=3, branching=2, leaf_range=(0, 9), name_prefix="R")

    print("Árbol inicial (valores en hojas):")
    def print_tree(n, indent=0):
        print("  " * indent + f"- {n.name}: value={n.value}")
        for c in n.children:
            print_tree(c, indent+1)
    print_tree(root)

    # Ejecutar Minimax mostrando pasos
    recorder = StepRecorder()
    print("\nEjecutando Minimax (sin poda alfa-beta), registro de pasos...")
    root_value = minimax(root, maximizing_player=True, recorder=recorder, alpha_beta=False)
    print(f"\nValor de la raíz (Minimax) = {root_value}")

    # Guardar y mostrar gráficos paso a paso
    print("\nGenerando imágenes por paso y mostrando...")
    play_snapshots(root, recorder, delay=0.8, out_dir="minimax_steps_manual")

    # También puede probar con poda alfa-beta:
    # recorder2 = StepRecorder()
    # minimax(root, maximizing_player=True, recorder=recorder2, alpha_beta=True)
    # play_snapshots(root, recorder2, delay=0.8, out_dir="minimax_steps_ab")

    print("\nProceso terminado. Revise la carpeta 'minimax_steps_manual/' para ver las capturas.")