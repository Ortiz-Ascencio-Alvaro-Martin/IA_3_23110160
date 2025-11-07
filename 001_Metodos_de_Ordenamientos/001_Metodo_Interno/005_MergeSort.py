def merge_sort(arr):
    """
    Función principal de MergeSort. Divide el arreglo recursivamente.
    """
    if len(arr) > 1:
        # 1. DIVIDIR: Encuentra el punto medio del arreglo
        mid = len(arr) // 2 
        
        # Crea las dos mitades: izquierda y derecha
        left_half = arr[:mid]
        right_half = arr[mid:]
        
        # 2. RECURSIÓN: Ordena recursivamente las dos mitades
        merge_sort(left_half)
        merge_sort(right_half)
        
        # 3. COMBINAR (MERGE): Llama a la función de combinación
        # Inicializa índices para la lista izquierda (i), derecha (j) y el arreglo original (k)
        i = j = k = 0
        
        # Copia los datos temporalmente a 'i', 'j', y 'k' mientras compara
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
            
        # Agrega los elementos restantes de la mitad izquierda, si los hay
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
            
        # Agrega los elementos restantes de la mitad derecha, si los hay
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

# --- Ejemplo de Uso ---
datos = [38, 27, 43, 3, 9, 82, 10]
print("INICIO DEL ORDENAMIENTO MERGESORT")
print(f"Lista inicial: {datos}")

merge_sort(datos)

print(f"Resultado Final: {datos}")
