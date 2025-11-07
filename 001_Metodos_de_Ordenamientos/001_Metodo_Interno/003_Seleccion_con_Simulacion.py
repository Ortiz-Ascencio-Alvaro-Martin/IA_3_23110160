def selection_sort_simulacion(arr):
    """
    Implementa el Método de Ordenamiento por Selección (Selection Sort).
    Simula visualmente cómo se selecciona y coloca cada elemento.
    """
    n = len(arr)
    print(f"Lista inicial: {arr}\n")
    
    # Recorre toda la lista
    for i in range(n - 1):
        # Asume que el elemento actual (i) es el mínimo.
        min_idx = i 
        
        print(f"--- PASADA {i + 1} ---")
        print(f"Buscando el menor a partir del índice {i} (Valor: {arr[i]})")
        
        # Busca el elemento más pequeño en la sublista no ordenada (desde i+1 hasta el final)
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j # Actualiza el índice del mínimo
                
        # Una vez que se encuentra el mínimo de la sublista no ordenada, 
        # se intercambia con el elemento en la posición actual (i).
        if min_idx != i:
            # Intercambio
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            
            # Simulación del Intercambio
            print(f"  > Seleccionado: El menor es {arr[i]} (estaba en índice {min_idx}).")
            print(f"    Intercambio realizado con el valor en índice {i}.")
            print(f"    Estado de la lista: {arr}")
        else:
            print(f"  > El valor {arr[i]} ya está en su posición correcta.")
            
    return arr

# --- Ejemplo de Uso ---
datos = [64, 25, 12, 22, 11]
print("INICIO DEL ORDENAMIENTO POR SELECCIÓN\n")
lista_ordenada = selection_sort_simulacion(datos)
print(f"\nResultado Final: {lista_ordenada}")
