def quicksort(arr):
    """
    Función principal que inicia el QuickSort.
    """
    if len(arr) <= 1:
        return arr
    
    # Llama a la función recursiva que ordena in-place
    _quicksort_recursivo(arr, 0, len(arr) - 1)
    return arr

def _quicksort_recursivo(arr, low, high):
    """
    Función recursiva de QuickSort.
    Ordena la sublista entre los índices 'low' y 'high'.
    """
    if low < high:
        # Pasa 1: Partición
        # 'pi' es el índice del pivote, ahora en su posición final ordenada.
        pi = _partition(arr, low, high)
        
        # Pasa 2: Recursión (Divide y Vencerás)
        
        # Ordena la sublista de elementos a la izquierda del pivote
        _quicksort_recursivo(arr, low, pi - 1)
        
        # Ordena la sublista de elementos a la derecha del pivote
        _quicksort_recursivo(arr, pi + 1, high)

def _partition(arr, low, high):
    """
    Función que realiza la partición:
    Coloca el pivote (último elemento) en su posición correcta
    y todos los elementos menores a la izquierda y mayores a la derecha.
    Devuelve el índice del pivote.
    """
    # Selecciona el pivote (aquí elegimos el último elemento)
    pivot = arr[high]
    
    # 'i' es el índice del elemento más pequeño encontrado hasta ahora
    i = low - 1  
    
    # Recorre todos los elementos desde 'low' hasta el pivote (high - 1)
    for j in range(low, high):
        
        # Si el elemento actual es menor o igual al pivote
        if arr[j] <= pivot:
            # Incrementa el índice del elemento más pequeño
            i = i + 1
            
            # Intercambia arr[i] y arr[j]
            arr[i], arr[j] = arr[j], arr[i]
    
    # Coloca el pivote en su posición correcta, intercambiando arr[i+1] y arr[high]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    
    return i + 1

# --- Ejemplo de Uso ---
datos = [10, 80, 30, 90, 40, 50, 70]
print("INICIO DEL ORDENAMIENTO QUICK SORT")
print(f"Lista inicial: {datos}")

lista_ordenada = quicksort(datos)

print(f"Resultado Final: {lista_ordenada}")
