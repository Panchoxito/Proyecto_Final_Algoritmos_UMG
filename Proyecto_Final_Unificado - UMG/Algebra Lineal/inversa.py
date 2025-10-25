import copy

def matriz_inversa(A):
    """Calcula la inversa de una matriz cuadrada A usando el método de Gauss-Jordan."""
    n = len(A)
    M = copy.deepcopy(A)
    identidad = [[float(i == j) for i in range(n)] for j in range(n)]

    for i in range(n):
        # Pivote
        pivote = M[i][i]
        if pivote == 0:
            raise ValueError("La matriz no tiene inversa (det=0)")

        for j in range(n):
            M[i][j] /= pivote
            identidad[i][j] /= pivote

      
        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(n):
                    M[k][j] -= factor * M[i][j]
                    identidad[k][j] -= factor * identidad[i][j]

    return identidad
