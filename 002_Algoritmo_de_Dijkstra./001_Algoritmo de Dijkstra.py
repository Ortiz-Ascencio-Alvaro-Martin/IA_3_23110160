#!/usr/bin/env python3
"""
Algoritmo de Dijkstra - implementación simple y con salida paso a paso.

Este script muestra cómo progresa el algoritmo: selección del vértice
con distancia mínima, relajación de aristas y actualización de distancias
y predecesores. Está escrito en español para fines didácticos.
"""
import heapq
import math
from typing import Dict, List, Tuple, Any


def imprimir_estado(dist: Dict[Any, float], prev: Dict[Any, Any], visitados: set, paso: int):
	print(f"\n--- Paso {paso} ---")
	print("Nodos visitados:", sorted(visitados))
	print("Distancias actuales:")
	for nodo in sorted(dist.keys()):
		d = dist[nodo]
		d_str = "∞" if d == math.inf else str(d)
		print(f"  {nodo}: {d_str}")
	print("Predecesores:")
	for nodo in sorted(prev.keys()):
		print(f"  {nodo}: {prev[nodo]}")


def reconstruir_camino(prev: Dict[Any, Any], destino: Any) -> List[Any]:
	camino = []
	u = destino
	while u is not None:
		camino.append(u)
		u = prev[u]
	camino.reverse()
	return camino


def dijkstra(grafo: Dict[Any, List[Tuple[Any, float]]], origen: Any, verbose: bool = True):
	"""
	grafo: dict donde cada clave es un nodo y su valor es una lista de tuplas (vecino, peso)
	origen: nodo inicial
	verbose: si True imprime paso a paso

	Devuelve: (distancias, predecesores)
	"""
	# Inicialización
	dist: Dict[Any, float] = {n: math.inf for n in grafo}
	prev: Dict[Any, Any] = {n: None for n in grafo}
	dist[origen] = 0

	# Heap de prioridad: (distancia, nodo)
	heap: List[Tuple[float, Any]] = [(0, origen)]
	visitados = set()
	paso = 0

	if verbose:
		print("Estado inicial:")
		imprimir_estado(dist, prev, visitados, paso)

	while heap:
		d_u, u = heapq.heappop(heap)

		# Si ya visitamos este nodo con una mejor distancia, lo ignoramos
		if u in visitados:
			continue

		# Marcar como visitado
		visitados.add(u)
		paso += 1
		if verbose:
			print(f"\nSeleccionado nodo con mínima distancia: {u} (dist = {d_u})")

		# Relajación de aristas (u, v)
		for v, peso in grafo.get(u, []):
			if v in visitados:
				# No relajamos aristas hacia nodos ya fijados
				continue
			alt = dist[u] + peso
			if verbose:
				print(f"  Considerando arista {u} -> {v} (peso {peso}), alt = {alt}")
			if alt < dist[v]:
				if verbose:
					anterior = "∞" if dist[v] == math.inf else dist[v]
					print(f"    Mejora: {v} distancia {anterior} -> {alt} (predecesor {u})")
				dist[v] = alt
				prev[v] = u
				heapq.heappush(heap, (alt, v))
			else:
				if verbose:
					print(f"    No mejora para {v} (actual {dist[v]})")

		if verbose:
			imprimir_estado(dist, prev, visitados, paso)

	if verbose:
		print("\nAlgoritmo completado. Distancias finales:")
		for nodo in sorted(dist.keys()):
			d = dist[nodo]
			d_str = "∞" if d == math.inf else str(d)
			print(f"  {nodo}: {d_str}")

	return dist, prev


def ejemplo():
	# Grafo de ejemplo (dirigido o no dirigido según cómo se defina):
	grafo = {
		'A': [('B', 4), ('C', 2)],
		'B': [('A', 4), ('C', 1), ('D', 5)],
		'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
		'D': [('B', 5), ('C', 8), ('E', 2), ('F', 6)],
		'E': [('C', 10), ('D', 2), ('F', 3)],
		'F': [('D', 6), ('E', 3)],
	}

	origen = 'A'
	print(f"\nEjecutando Dijkstra desde el origen: {origen}")
	dist, prev = dijkstra(grafo, origen, verbose=True)

	print("\nCaminos más cortos desde origen:")
	for destino in sorted(grafo.keys()):
		if dist[destino] == math.inf:
			print(f"  {origen} -> {destino}: no existe camino")
		else:
			camino = reconstruir_camino(prev, destino)
			print(f"  {origen} -> {destino}: distancia {dist[destino]}, camino: {' -> '.join(camino)}")


if __name__ == '__main__':
	ejemplo()

