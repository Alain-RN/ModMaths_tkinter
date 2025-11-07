import numpy as np

def resoudre_systeme(A, b):
    try:
        return np.linalg.solve(A, b)
    except ValueError:
        print("Pas de solution")
        return []