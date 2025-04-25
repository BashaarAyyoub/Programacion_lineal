# Implementación manual del método simplex para maximizar el poder del ejército

import numpy as np

# Definimos la función objetivo y las restricciones
# Maximizar: 70*swordsmen + 95*bowmen + 230*horsemen
# Sujeto a:
# 60*swordsmen + 80*bowmen + 140*horsemen <= 1200 (Food)
# 20*swordsmen + 10*bowmen <= 800 (Wood)
# 40*bowmen + 100*horsemen <= 600 (Gold)
# swordsmen, bowmen, horsemen >= 0

# Matriz de restricciones (coeficientes)
A = np.array([
    [60, 80, 140],
    [20, 10, 0],
    [0, 40, 100]
])

# Límite de recursos
b = np.array([1200, 800, 600])

# Coeficientes de la función objetivo (negativos para maximizar)
c = np.array([-70, -95, -230])

# Agregar variables de holgura
A = np.hstack([A, np.eye(len(b))])
c = np.hstack([c, np.zeros(len(b))])

# Inicializar tabla simplex
num_vars = A.shape[1]
tableau = np.zeros((len(b) + 1, num_vars + 1))
tableau[:-1, :-1] = A
tableau[:-1, -1] = b
tableau[-1, :-1] = c

# Método simplex
while np.any(tableau[-1, :-1] < 0):  # Mientras haya coeficientes negativos en la fila objetivo
    pivot_col = np.argmin(tableau[-1, :-1])  # Columna pivote
    ratios = tableau[:-1, -1] / tableau[:-1, pivot_col]
    ratios[ratios <= 0] = np.inf  # Evitar divisiones por cero o negativas
    pivot_row = np.argmin(ratios)  # Fila pivote

    # Normalizar fila pivote
    tableau[pivot_row, :] /= tableau[pivot_row, pivot_col]

    # Eliminar el resto de la columna pivote
    for i in range(len(tableau)):
        if i != pivot_row:
            tableau[i, :] -= tableau[i, pivot_col] * tableau[pivot_row, :]

# Extraer solución
solution = tableau[:-1, -1]
optimal_value = -tableau[-1, -1]

# Imprimir resultados
print('================= Solution =================')
print(f'Optimal power = {optimal_value} 💪power')
print('Army:')
print(f' - 🗡️Swordsmen = {solution[0]}')
print(f' - 🏹Bowmen = {solution[1]}')
print(f' - 🐎Horsemen = {solution[2]}')