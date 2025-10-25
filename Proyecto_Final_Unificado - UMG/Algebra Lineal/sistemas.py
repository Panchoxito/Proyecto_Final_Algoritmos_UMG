import numpy as np
from fractions import Fraction


def formato_fraccion(valor):
    try:
        if float(valor).is_integer():
            return str(int(valor))
        return str(Fraction(valor).limit_denominator())
    except Exception:
        return str(valor)

def gauss_jordan(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)

  
    M = np.hstack([A, b.reshape(-1, 1)])


    for i in range(n):
        if M[i, i] == 0:
            for k in range(i + 1, n):
                if M[k, i] != 0:
                    M[[i, k]] = M[[k, i]]
                    break

        pivote = M[i, i]
        if pivote != 0:
            M[i] = M[i] / pivote

        for j in range(n):
            if j != i:
                M[j] = M[j] - M[j, i] * M[i]

  
    x = M[:, -1]
    x_formateado = [formato_fraccion(v) for v in x]

   
    resultado = "\nMatriz reducida (Gauss-Jordan):\n"
    for fila in M:
        resultado += "| " + "   ".join(formato_fraccion(v) for v in fila) + " |\n"

    resultado += "\nSolución:\n"
    for i, val in enumerate(x_formateado, start=1):
        resultado += f"x{i} = {val}\n"

    return resultado

def regla_de_cramer(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    det_A = np.linalg.det(A)

    if abs(det_A) < 1e-10:
        return "El sistema no tiene solución: determinante = 0."

    n = len(b)
    resultado = f"Determinante de A = {formato_fraccion(det_A)}\n\n"
    soluciones = []

    for i in range(n):
        Ai = np.copy(A)
        Ai[:, i] = b
        det_Ai = np.linalg.det(Ai)
        xi = det_Ai / det_A
        soluciones.append(formato_fraccion(xi))
        resultado += f"Determinante A{i+1} = {formato_fraccion(det_Ai)}  →  x{i+1} = {formato_fraccion(xi)}\n"

    resultado += "\nSolución final:\n"
    for i, val in enumerate(soluciones, start=1):
        resultado += f"x{i} = {val}\n"

    return resultado

if __name__ == "__main__":
    print("=== Ejemplo Gauss-Jordan ===")
    A = [[3, 4],
         [7, -4]]
    b = [-4, 5]
    print(gauss_jordan(A, b))

    print("\n=== Ejemplo Regla de Cramer ===")
    A = [[3, 4],
         [7, -4]]
    b = [-4, 5]
    print(regla_de_cramer(A, b))
