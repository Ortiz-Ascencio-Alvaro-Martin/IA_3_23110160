import random

# Función para ordenar internamente cada run (simulando que está en RAM)
def internal_sort(run):
    """
    Simula el ordenamiento de un bloque de datos que cabe en la memoria principal.
    Se podría usar QuickSort, MergeSort, etc. Usaremos la función interna de Python por simplicidad.
    """
    return sorted(run)

# --- Función Principal: Distribución de Secuencias Iniciales ---
def distribution_of_initial_runs(external_data, ram_capacity):
    """
    Simula la fase de distribución y ordenamiento de las runs iniciales.
    'ram_capacity' simula el tamaño máximo de bloque que la memoria principal puede manejar.
    """
    n = len(external_data)
    runs_almacenadas = []
    
    print("INICIO: Distribución de Secuencias Iniciales")
    print(f"Capacidad de RAM simulada (Run Size): {ram_capacity}")
    print(f"Datos del Archivo (Externo): {external_data}")
    
    # Recorre el archivo externo en bloques del tamaño de la RAM
    for i in range(0, n, ram_capacity):
        # 1. LECTURA: Lee un bloque del "Archivo Externo" a la "RAM"
        current_block = external_data[i:i + ram_capacity]
        print(f"\n  > Leyendo bloque {i // ram_capacity + 1}: {current_block}")
        
        # 2. ORDENAMIENTO INTERNO: Ordena el bloque en la "RAM"
        sorted_run = internal_sort(current_block)
        
        # 3. ESCRITURA: Escribe la secuencia ordenada de vuelta al "Almacenamiento Externo"
        runs_almacenadas.append(sorted_run)
        print(f"  > Ordenamiento Interno (RAM): {sorted_run}")
        print(f"  > Escribiendo RUN {i // ram_capacity + 1} a dispositivo de mezcla.")
        
    print("\nFASE TERMINADA.")
    print("Secuencias Iniciales (Runs) Creadas:", runs_almacenadas)
    
    return runs_almacenadas

# --- Ejemplo de Uso ---
datos_externos = [50, 10, 40, 20, 60, 30, 80, 70, 90, 5]
CAPACIDAD_RAM = 3 # Simulamos que la memoria solo puede ordenar 3 elementos a la vez

runs_finales = distribution_of_initial_runs(datos_externos, CAPACIDAD_RAM)

# Estas 'runs_finales' serían las que el Straight Merging o Polyphase Sort comenzarían a mezclar.
print(f"Ready for Merging: {runs_finales}")
