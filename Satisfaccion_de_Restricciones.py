import random
from collections import Counter


class Maquina():
    def __init__(self, desocupada):
        self.desocupada = desocupada
        self.tiempo = 0


class Backtraking():  # return solution o failure
    def __init__(self, variables, dominio, restricciones_precedencia, restricciones_recursos, maquinas):
        # self.variables=variables
        # self.dominio=dominio
        # self.asignamiento=asignamiento
        self.restricciones_precedencia = restricciones_precedencia
        # self.restricciones_recursos=restricciones_recursos

        asignamiento = []
        tiempo_limite = 100
        value = self.vuelta_atras_recursiva(
            variables, dominio, asignamiento, restricciones_precedencia, restricciones_recursos, maquinas)
        print(value)

    def vuelta_atras_recursiva(self, variables, dominio, asignamiento, restricciones_precedencia, restricciones_recursos, maquinas):
        if len(asignamiento) == len(variables):
            return asignamiento
        var = self.seleccionar_variable_sin_asignar(
            variables, asignamiento, restricciones_precedencia)
        print(var)
        # asignamiento.append(var)
        for i in range(0, len(dominio)):
            if self.consistente(variables, var, i, asignamiento, restricciones_precedencia, restricciones_recursos, tiempo_limite) == True:
                asignamiento.append(var)
                resultado = self.vuelta_atras_recursiva(
                    variables, dominio, asignamiento, restricciones_precedencia, restricciones_recursos, maquinas)
                if resultado != False:
                    return resultado
                asignamiento.pop(asignamiento.index(var))
        else:
            resultado = self.vuelta_atras_recursiva(
                variables, dominio, asignamiento, restricciones_precedencia, restricciones_recursos, maquinas)
            if resultado != False:
                return resultado
        return False
    # elijo la variable mas restringida

    def seleccionar_variable_sin_asignar(self, variables, asignamiento, restricciones_precedencia):
        # aleatorio = []
        # for i in variables.keys():
        #     aleatorio.append(i)
        # for i in range(0, len(restricciones_precedencia)):
        #     aleatorio.append(restricciones_precedencia[i][0])
        # flag = False
        # while flag == False:
        #     var = random.choice(aleatorio)
        #     if var not in asignamiento:
        #         flag = True
        # return var

        r = restricciones_precedencia
        a = [i[1][0] for i in r.items()]
        count = Counter(a).items()
        count = sorted(count, key=lambda x: x[1])
        count = [i[0] for i in count if i[0] not in asignamiento]
        count = count + [i[0] for i in variables.items() if i[0]
                         not in count and i[0] not in asignamiento]
        return count[0]

    def consistente(self, variables, var, i, asignamiento, restricciones_precedencia, restricciones_recursos, tiempo_limite):
        tiempo = i
        for j in range(0, len(asignamiento)):
            tiempo = tiempo+variables[asignamiento[j]]
        tiempo = tiempo + variables[var]
        if tiempo > tiempo_limite:
            return False

        for rp in range(0, len(restricciones_precedencia)):
            if var == restricciones_precedencia[rp][1]:
                if restricciones_precedencia[rp][0] not in asignamiento:
                    return False
        return True


if __name__ == '__main__':
    variables = {"T1": 5, "T2": 15, "T3": 10, "T4": 30}
    tiempo_limite = 100

    asignamiento = []
    dominio = []

    for i in range(0, tiempo_limite):
        dominio.append(i)

    # T2 debe realizarse antes que T3
    # T4 debe realizarse antes que T1
    # T4 debe realizarse antes que T3
    restricciones_precedencia = {
        0: ("T2", "T3"), 1: ("T4", "T1"), 2: ("T4", "T3")}

    # T1 ocupa la máquina 1
    # T2 ocupa las máquinas 2 y 3
    # T3 ocupa la máquina 4
    # T4 ocupa las máquinas 1 y 3

    M1 = Maquina(True)
    M2 = Maquina(True)
    M3 = Maquina(True)
    M4 = Maquina(True)
    maquinas = [M1, M2, M3, M4]
    restricciones_recursos = {"T1": (M1), "T2": (
        M1, M2, M3), "T3": (M1, M4), "T4": (M1, M3)}

    res = Backtraking(variables, dominio, restricciones_precedencia,
                      restricciones_recursos, maquinas)
