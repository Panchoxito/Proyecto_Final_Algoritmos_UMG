def multiplicar_matrices(A, B):
    """Multiplica dos matrices A y B si las dimensiones son compatibles."""
    if len(A[0]) != len(B):
        raise ValueError("No se pueden multiplicar las matrices: dimensiones incompatibles")

    filas, columnas = len(A), len(B[0])
    resultado = [[0 for _ in range(columnas)] for _ in range(filas)]

    for i in range(filas):
        for j in range(columnas):
            for k in range(len(B)):
                resultado[i][j] += A[i][k] * B[k][j]

    return resultado
