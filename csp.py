
dead_line = 100


if __name__ == "__main__":
    # Variables X: Tareas
    # Tarea 1: T1
    # Duración d1 = 5
    # Tarea 2: T2
    # Duración d1 = 15
    # Tarea 3: T3
    # Duración d1 = 10
    # Tarea 4: T4
    # Duración d1 = 30
    T = {
        "d1": 5,
        "d2": 15,
        "d3": 10,
        "d4": 30,
    }
    # Dominio:
    D = []
    # Periodo de inicio de c/tarea
    # Di = {1, 2, 3, ...} ɛ IN i > 1 && i < Dead Line - T["di"]
    # Must start with enough margin to complete the task.
    for key, value in T.items():
        D.append(list(range(0, dead_line - value)))

    # Restricciones:
    # T2 debe realizarse antes que T3 ⇒  C1: T2 + d2 <= T3
    # T4 debe realizarse antes que T1 ⇒  C2: T4 + d4 <= T1
    # T4 debe realizarse antes que T3 ⇒  C3: T4 + d4 <= T3
    R = {
        "T4": []
    }
