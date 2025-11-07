def insertion_sort_simulacion_corregida(arr):
    """
    Implementa el Método de Ordenamiento por Inserción (Insertion Sort).
    Simula visualmente los corrimientos y la inserción de cada elemento.
    """
    n = len(arr)
    
    print(f"Lista inicial: {arr}\n")
    
    # Comienza en el índice 1, asumiendo que el elemento en el índice 0 ya está ordenado.
    for i in range(1, n):
        # El elemento que se va a insertar en la sublista ordenada.
        valor_actual = arr[i]
        j = i - 1 # Índice del último elemento de la sublista ya ordenada.
        
        print(f"--- Paso {i}: Preparando la inserción del valor {valor_actual} ---")
        
        # Bucle para realizar el corrimiento de elementos a la derecha.
        while j >= 0 and arr[j] > valor_actual:
            
            # Corrimiento: Mueve el elemento de la izquierda (arr[j]) una posición a la derecha (arr[j+1]).
            arr[j + 1] = arr[j]
            
            # Simulación del Corrimiento
            print(f"  > Corrimiento: El {arr[j+1]} en índice {j} se mueve a {j+1}.")
            print(f"    Estado temporal: {arr}")
            
            j -= 1
            
        # Inserción: Coloca el 'valor_actual' en la posición vacía que queda (j + 1).
        arr[j + 1] = valor_actual
        
        print(f"  > Inserción finalizada: {valor_actual} colocado en la posición {j + 1}")
        print(f"    Lista después de la inserción: {arr}")
        
    return arr

# --- Ejemplo de Uso ---
datos = [5, 1, 4, 2, 8]
print("INICIO DEL ORDENAMIENTO POR INSERCIÓN (Corregido)\n")
lista_ordenada = insertion_sort_simulacion_corregida(datos)
print(f"\nResultado Final: {lista_ordenada}")
