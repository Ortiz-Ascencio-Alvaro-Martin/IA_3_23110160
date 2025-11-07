def bubble_sort_simulacion(arr):
    """
    Implementa el Ordenamiento Burbuja y simula visualmente
    los intercambios que ocurren en la lista.
    """
    n = len(arr)
    # Variable de control para saber si se hizo algún intercambio en una pasada.
    hubo_intercambio = False 
    
    print(f"Lista inicial: {arr}\n")
    
    # El ciclo exterior itera sobre el número de pasadas necesarias.
    for i in range(n - 1): 
        # Restablece la bandera al comienzo de cada nueva pasada.
        hubo_intercambio = False 
        print(f"--- PASADA {i + 1} ---")

        # El ciclo interior realiza las comparaciones e intercambios, 
        # sin revisar los últimos 'i' elementos ya ordenados.
        for j in range(n - 1 - i):
            
            # Compara el elemento actual (arr[j]) con el siguiente (arr[j+1])
            if arr[j] > arr[j + 1]:
                
                # Intercambio (Swap) si el orden es incorrecto
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                hubo_intercambio = True
                
                # Representación Visual del Intercambio (Simulación)
                # Muestra el estado actual de la lista después del intercambio
                print(f"  - Intercambio realizado. Comparando índice {j} y {j+1}")
                print(f"    Estado actual: {arr}")
                
        # Optimización: Si no hubo intercambios en una pasada completa, 
        # la lista ya está ordenada.
        if not hubo_intercambio:
            print(f"\nLista ordenada en Pasada {i + 1}. Proceso terminado.")
            break
            
    return arr

# --- Ejemplo de Uso ---
datos = [5, 1, 4, 2, 8]
print("INICIO DEL ORDENAMIENTO BURBUJA\n")
lista_ordenada = bubble_sort_simulacion(datos)
print(f"\nResultado Final: {lista_ordenada}")
