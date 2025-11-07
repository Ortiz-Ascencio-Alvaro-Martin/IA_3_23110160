def shell_sort_simulacion(arr):
    """
    Implementa el Método ShellSort.
    Simula visualmente el proceso mostrando el 'salto' (gap) actual.
    """
    n = len(arr)
    
    # Define la secuencia inicial de saltos (gap), típicamente n/2
    gap = n // 2 
    
    print(f"Lista inicial: {arr}\n")
    
    # Bucle principal: Continúa mientras el salto sea mayor que 0
    while gap > 0:
        print(f"--- PASADA con SALTO (gap) = {gap} ---")
        
        # Realiza un Insertion Sort en sublistas separadas por el 'gap'.
        # El bucle comienza en 'gap' porque el primer subarreglo ya está implícitamente ordenado.
        for i in range(gap, n):
            
            # Almacena el elemento a ser insertado
            temp = arr[i]
            
            # Mueve los elementos anteriores 'gap' posiciones a la derecha hasta encontrar el lugar de inserción
            j = i
            while j >= gap and arr[j - gap] > temp:
                # Corrimiento: mueve el elemento
                arr[j] = arr[j - gap]
                j -= gap
                
                # Simulación del Corrimiento
                print(f"  > Corrimiento: El elemento en índice {j+gap} se mueve debido al gap {gap}.")
                print(f"    Estado temporal: {arr}")
                
            # Inserta el elemento 'temp' en su posición correcta
            arr[j] = temp
            
        print(f"  Lista después del Insertion Sort con gap {gap}: {arr}")
        
        # Reduce el valor del salto para la siguiente pasada
        gap //= 2
        
    return arr

# --- Ejemplo de Uso ---
datos = [12, 34, 54, 2, 3]
print("INICIO DEL ORDENAMIENTO SHELLSORT\n")

lista_ordenada = shell_sort_simulacion(datos)

print(f"\nResultado Final: {lista_ordenada}")
