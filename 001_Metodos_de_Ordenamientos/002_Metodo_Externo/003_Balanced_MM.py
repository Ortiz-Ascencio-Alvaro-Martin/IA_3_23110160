def distribute_runs(data, k_devices, run_size):
    """
    Simula la Fase Inicial: Distribuye los runs ordenados
    equilibradamente entre los dispositivos de salida (simulados).
    """
    n = len(data)
    
    # Crea las runs iniciales ordenadas internamente
    initial_runs = []
    for i in range(0, n, run_size):
        run = data[i:i + run_size]
        run_ordenada = sorted(run)  # Usamos 'sorted' para simplificar el ordenamiento interno
        initial_runs.append(run_ordenada)

    # Distribuye las runs a los K dispositivos de salida (Simulación)
    devices = [[] for _ in range(k_devices)]
    for i, run in enumerate(initial_runs):
        # Distribución equilibrada (ronda-robin)
        devices[i % k_devices].append(run)
        
    return devices

def multiway_merge(input_devices):
    """
    Realiza la mezcla de múltiples secuencias (K-way merge).
    input_devices es una lista de listas de runs (los dispositivos de lectura).
    """
    import heapq
    
    # Inicializa el heap de prioridad (min-heap)
    # Almacenará tuplas: (valor, índice_run, índice_dispositivo)
    heap = []
    
    # Simplificación: Combina todas las runs de todos los dispositivos de entrada en un solo pool para la mezcla
    all_runs = []
    for device_runs in input_devices:
        all_runs.extend(device_runs)
    
    # Inicializa índices para cada run
    run_indices = [0] * len(all_runs)
    
    # Introduce el primer elemento de cada run al heap
    for i, run in enumerate(all_runs):
        if run:
            heapq.heappush(heap, (run[0], i)) # (valor, índice_run)

    final_merged_run = []
    
    while heap:
        # Extrae el elemento más pequeño del heap
        value, run_index = heapq.heappop(heap)
        final_merged_run.append(value)
        
        # Mueve el puntero de esa run al siguiente elemento
        run_indices[run_index] += 1
        
        # Si la run aún tiene elementos, agrega el siguiente al heap
        next_index = run_indices[run_index]
        if next_index < len(all_runs[run_index]):
            next_value = all_runs[run_index][next_index]
            heapq.heappush(heap, (next_value, run_index))
            
    return [final_merged_run] # Devuelve una única run grande (el resultado de la pasada)


# --- Función Principal: Balanced Multiway Merging ---
def balanced_multiway_sort(external_data, run_size, k_devices=3):
    """
    Simula el Balanced Multiway Merging.
    """
    print("INICIO DEL ORDENAMIENTO EXTERNO: Balanced Multiway Merging")
    print(f"Número de dispositivos de mezcla (K): {k_devices}")
    
    # FASE 1: Distribución Inicial de Runs Ordenadas
    # devices_in_use[0] a [k-1] simulan los dispositivos.
    devices = distribute_runs(external_data, k_devices, run_size)
    print("\nFASE 1: Runs Iniciales Ordenadas y Distribuidas (Tamaño de Run = %d)" % run_size)
    for i, dev in enumerate(devices):
        print(f"  Dispositivo {i+1} (Salida): {dev}")
    
    # FASE 2: Mezcla Iterativa (K-way Merges)
    pasada = 1
    # Bucle principal: Simula la alternancia entre dispositivos de entrada/salida
    while sum(len(dev) for dev in devices) > 1 or (len(devices) == 1 and len(devices[0][0]) < len(external_data)):
        
        # Simulación de alternancia: Los dispositivos que eran de Salida ahora son de Entrada, y viceversa.
        # En la práctica, se usarían K/2 para entrada y K/2 para salida.
        
        # Aquí, por simplicidad, los mezclamos todos en una única pasada y redistribuimos.
        
        all_runs_to_merge = [run for dev in devices for run in dev]
        
        if len(all_runs_to_merge) <= 1:
             break # Finaliza si solo queda una única run

        # Realiza la mezcla K-way
        print(f"\n--- PASADA DE MEZCLA {pasada} (Mezclando {len(all_runs_to_merge)} runs) ---")
        
        # Mezcla todas las runs para formar una única gran run
        merged_result = multiway_merge([all_runs_to_merge])
        
        # Redistribución del resultado (para simular la preparación de la siguiente pasada)
        devices = distribute_runs(merged_result[0], k_devices, len(merged_data))
        print("  Resultado de la Mezcla Total (Redistribución):", merged_result[0])
        
        pasada += 1
        # Detiene la simulación si el resultado ya es un único arreglo ordenado
        if len(merged_result[0]) == len(external_data):
             return merged_result[0] 

    return devices[0][0] if devices[0] else []


# --- Ejemplo de Uso ---
datos_externos = [3, 15, 8, 20, 1, 12, 18, 5, 14, 2, 7, 10]
TAMAÑO_RAM = 4  # Capacidad de la memoria para ordenar inicialmente
K_DISPOSITIVOS = 3 # Número de cintas/discos usados para la mezcla

lista_ordenada = balanced_multiway_sort(datos_externos, TAMAÑO_RAM, K_DISPOSITIVOS)

print(f"\nResultado Final (Archivo Ordenado): {lista_ordenada}")
