import random

# --- Función Auxiliar 1: Ordenamiento Interno (Para ordenar los 'runs' iniciales) ---
def merge_sort_interno(arr):
    """
    Función interna (MergeSort) utilizada para ordenar bloques que caben en memoria.
    """
    if len(arr) > 1:
        mid = len(arr) // 2 
        left_half = arr[:mid]
        right_half = arr[mid:]
        
        merge_sort_interno(left_half)
        merge_sort_interno(right_half)
        
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]; i += 1
            else:
                arr[k] = right_half[j]; j += 1
            k += 1
            
        while i < len(left_half): arr[k] = left_half[i]; i += 1; k += 1
        while j < len(right_half): arr[k] = right_half[j]; j += 1; k += 1
    return arr

# --- Función Auxiliar 2: Función de Mezcla (Merge) ---
def merge(run1, run2):
    """
    Combina (intercala) dos secuencias ordenadas en una sola secuencia ordenada.
    """
    merged = []
    i = j = 0
    while i < len(run1) and j < len(run2):
        if run1[i] < run2[j]:
            merged.append(run1[i])
            i += 1
        else:
            merged.append(run2[j])
            j += 1
            
    # Agrega los elementos restantes (solo uno de los dos bloques tendrá sobrantes)
    merged.extend(run1[i:])
    merged.extend(run2[j:])
    return merged

# --- Función Principal: Straight Merging Sort ---
def straight_merging_sort(external_data, run_size):
    """
    Implementa el Straight Merging (Mezcla Directa).
    'run_size' simula el tamaño de bloque que cabe en memoria.
    """
    n = len(external_data)
    
    # 1. Fase Inicial: Distribución y Ordenamiento de Runs (Bloques internos)
    runs = []
    print("FASE 1: Ordenamiento Interno de Runs Iniciales")
    for i in range(0, n, run_size):
        # Lee un bloque (run) del "disco"
        run = external_data[i:i + run_size]
        # Ordena el bloque en "RAM"
        run_ordenada = merge_sort_interno(run)
        # Escribe el bloque ordenado de vuelta al "disco"
        runs.append(run_ordenada)
        print(f"  Run ordenada: {run_ordenada}")
    
    # 2. Fase de Mezcla Repetitiva (Merges Sucesivos)
    longitud_secuencia = run_size # La longitud de las secuencias a mezclar
    
    # Bucle que se ejecuta mientras no todas las runs estén en una sola secuencia
    while len(runs) > 1 or (len(runs) == 1 and len(runs[0]) < n):
        new_runs = []
        print(f"\nFASE 2: Mezcla (Merge) - Mezclando secuencias de tamaño {longitud_secuencia}")
        
        # Recorre las secuencias en pares
        for i in range(0, len(runs), 2):
            run1 = runs[i]
            
            # Intenta tomar la run2; si no existe, run2 es una lista vacía
            run2 = runs[i + 1] if i + 1 < len(runs) else []
            
            merged_run = merge(run1, run2)
            new_runs.append(merged_run)
            
            print(f"  Mezclando: {run1} y {run2} -> {merged_run}")
            
        runs = new_runs
        
        # La longitud de las secuencias ordenadas se duplica en cada pasada
        longitud_secuencia *= 2 

    return runs[0] if runs else []

# --- Ejemplo de Uso (Simulación de datos en un "Archivo Externo") ---
# Simular un archivo de 20 elementos
datos_externos = random.sample(range(1, 100), 20)
# Simular que solo caben 4 elementos en la memoria principal (run_size)
TAMAÑO_RAM = 4

print("INICIO DEL ORDENAMIENTO EXTERNO: Straight Merging")
print(f"Datos originales (Simulación de Archivo): {datos_externos}")

lista_ordenada = straight_merging_sort(datos_externos, TAMAÑO_RAM)

print(f"\nResultado Final (Archivo Ordenado): {lista_ordenada}")
