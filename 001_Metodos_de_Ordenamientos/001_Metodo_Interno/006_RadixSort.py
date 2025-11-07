def counting_sort_by_digit(arr, exp):
    """
    Función de Ordenamiento por Cuentas que ordena el arreglo 
    basándose en el dígito de la posición 'exp'.
    """
    n = len(arr)
    output = [0] * n  # El arreglo de salida ordenado
    count = [0] * 10  # 10 contenedores para dígitos del 0 al 9

    # 1. Contar: Almacenar el conteo de ocurrencias del dígito
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1

    # 2. Modificar el conteo: Cambiar count[i] para que contenga 
    # la posición real del dígito en el arreglo 'output'.
    for i in range(1, 10):
        count[i] += count[i - 1]

    # 3. Construir el arreglo de salida
    i = n - 1
    while i >= 0:
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        i -= 1

    # 4. Copiar: Copia el arreglo de salida al arreglo original
    for i in range(n):
        arr[i] = output[i]

