def get_natural_runs(data):
    """
    Identifica y devuelve una lista de secuencias naturales (sublistas ordenadas)
    de tamaño variable de los datos.
    """
    runs = []
    n = len(data)
    if n == 0:
        return runs
    
    start = 0
    while start < n:
        end = start + 1
        # Encuentra el final de la secuencia natural (mientras el elemento actual sea menor que el siguiente)
        while end < n and data[end - 1] <= data[end]:
            end += 1
        
        # Agrega la secuencia natural encontrada a la lista de runs
        runs.append(data[start:end])
        start = end
        
    return runs

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
            
    merged.extend(run1[i:])
    merged.extend(run2[j:])
    return merged

# --- Función Principal: Natural Merging Sort ---
def natural_merging_sort(external_data):
    """
    Implementa el Natural Merging (Mezcla Natural).
    """
    
    print("FASE 1: Identificación de Secuencias Naturales (Runs de tamaño variable)")
    runs = get_natural_runs(external_data)
    print(f"Secuencias Iniciales (Runs Naturales): {runs}")

    if not runs:
        return []
    
    # 2. Fase de Mezcla Repetitiva
    pasada = 1
    while len(runs) > 1:
        new_runs = []
        print(f"\n--- PASADA DE MEZCLA {pasada} ---")
        
        # Recorre las secuencias en pares
        for i in range(0, len(runs), 2):
            run1 = runs[i]
            run2 = runs[i + 1] if i + 1 < len(runs) else []
            
            # Mezcla las dos secuencias ordenadas
            if run2:
                merged_run = merge(run1, run2)
                print(f"  Mezclando: {run1} y {run2} -> {merged_run}")
            else:
                merged_run = run1 # Transfiere la última run impar
                print(f"  Transferido (Run impar): {run1}")

            new_runs.append(merged_run)
            
        runs = new_runs
        pasada += 1

    return runs[0] if runs else []

# --- Ejemplo de Uso (Simulación con secuencias pre-ordenadas) ---
# Simular un archivo donde ya existen segmentos ordenados
datos_externos = [10, 20, 30, 5, 15, 25, 40, 50, 2] 
# Las secuencias naturales son: [10, 20, 30], [5, 15, 25, 40, 50], [2]

print("INICIO DEL ORDENAMIENTO EXTERNO: Natural Merging")
print(f"Datos originales (Simulación de Archivo): {datos_externos}")

lista_ordenada = natural_merging_sort(datos_externos)

print(f"\nResultado Final (Archivo Ordenado): {lista_ordenada}")
