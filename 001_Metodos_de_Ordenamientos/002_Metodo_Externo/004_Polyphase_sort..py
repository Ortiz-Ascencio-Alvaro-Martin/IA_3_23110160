import random

# --- Función Auxiliar: Mezcla (Merge) ---
def merge(run1, run2):
    """Combina dos secuencias ordenadas."""
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

# --- Función Auxiliar: Distribución Inicial (Simulación con 3 dispositivos, K=3) ---
# En un Polyphase real, esta distribución inicial sería desigual y precisa.
def distribute_runs_initial(data, run_size, k_devices=3):
    """
    Simula la distribución inicial de runs ordenadas en K-1 dispositivos.
    """
    initial_runs = []
    # Crea las runs iniciales ordenadas internamente
    for i in range(0, len(data), run_size):
        run = data[i:i + run_size]
        initial_runs.append(sorted(run))

    # Distribuye las runs a K-1 dispositivos (Dispositivo 0 y 1 en este caso)
    devices = [[] for _ in range(k_devices)]
    k_minus_1 = k_devices - 1 
    
    # Distribución simple: Alterna las runs entre K-1 dispositivos
    for i, run in enumerate(initial_runs):
        devices[i % k_minus_1].append(run)
        
    return devices

# --- Función Principal: Polyphase Sort (Simulación) ---
def polyphase_sort(external_data, run_size, k_devices=3):
    """
    Simula el proceso iterativo de Polyphase Sort con K dispositivos.
    """
    if k_devices < 2:
        raise ValueError("Polyphase Sort requiere al menos 2 dispositivos (cintas).")
    
    print("INICIO DEL ORDENAMIENTO EXTERNO: Polyphase Sort")
    print(f"Dispositivos (K): {k_devices}")
    
    # Inicializa K dispositivos. Los K-1 primeros tendrán datos. El último (K-1) estará vacío.
    devices = distribute_runs_initial(external_data, run_size, k_devices)
    
    print("\nFASE 1: Distribución Inicial")
    for i, dev in enumerate(devices):
        print(f"  Dispositivo D{i} (Runs: {len(dev)}): {dev}")
        
    pasada = 1
    # Bucle principal: Continúa hasta que todas las runs estén en un solo dispositivo.
    while sum(len(dev) for dev in devices) > 1:
        
        # Identifica el dispositivo VACÍO (el que actuará como SALIDA)
        output_device_index = next(i for i, dev in enumerate(devices) if not dev)
        
        # Los otros K-1 dispositivos actúan como ENTRADA
        input_device_indices = [i for i in range(k_devices) if i != output_device_index]
        
        print(f"\n--- PASADA {pasada} ---")
        print(f"  Dispositivo de SALIDA: D{output_device_index}")
        print(f"  Dispositivos de ENTRADA: {[f'D{i}' for i in input_device_indices]}")
        
        # Determina cuántas runs se pueden mezclar: el mínimo número de runs presentes en CADA dispositivo de ENTRADA.
        num_merges = min(len(devices[i]) for i in input_device_indices)
        
        merged_runs = 0
        
        # Realiza las mezclas
        for _ in range(num_merges):
            
            # Toma la primera run de cada dispositivo de entrada
            run_to_merge = [devices[i].pop(0) for i in input_device_indices]
            
            # Mezcla las runs (aquí se simplifica a una mezcla binaria)
            # En la realidad, se haría una K-way merge de las runs.
            merged_run = run_to_merge[0]
            for run in run_to_merge[1:]:
                merged_run = merge(merged_run, run)

            # Escribe la run mezclada al dispositivo de SALIDA
            devices[output_device_index].append(merged_run)
            merged_runs += 1
            
        print(f"  Mezclas realizadas: {merged_runs}. Runs restantes en entrada: {len(devices[input_device_indices[0]])}")
        
        # Al finalizar la pasada, el dispositivo de SALIDA se vacía (se convierte en ENTRADA)
        # y uno de los dispositivos de ENTRADA se vacía (se convierte en SALIDA).
        # En esta simulación, la lógica es implícita: el dispositivo de SALIDA ahora tiene runs.
        
        pasada += 1
        
    return devices[output_device_index][0] if devices[output_device_index] else devices[input_device_indices[0]][0]


# --- Ejemplo de Uso (Simulación) ---
datos_externos = [10, 80, 30, 90, 40, 50, 70, 20, 100, 5, 25, 45]
TAMAÑO_RAM = 2  # Tamaño del bloque para el ordenamiento interno inicial
K_DISPOSITIVOS = 3 # Usaremos 3 "cintas" o dispositivos

lista_ordenada = polyphase_sort(datos_externos, TAMAÑO_RAM, K_DISPOSITIVOS)

print(f"\nResultado Final (Archivo Ordenado): {lista_ordenada}")
