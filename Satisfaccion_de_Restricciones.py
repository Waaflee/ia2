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
        aleatorio = []
        for i in variables.keys():
            aleatorio.append(i)
        for i in range(0, len(restricciones_precedencia)):
            aleatorio.append(restricciones_precedencia[i][0])
        flag = False
        while flag == False:
            var = random.choice(aleatorio)
            if var not in asignamiento:
                flag = True
        return var

        # repetitions = []
        # restrictions = restricciones_precedencia.items()
        # restrictions = [i for i in restrictions if i[0] not in asignamiento]
        # for i in restrictions:
        #     repetitions.append(restrictions[i[0]][0])
        # count = Counter(repetitions).items()
        # count = sorted(count, key=lambda x: x[1])
        # return count[1][0]

        # Esto era para elegir el más restringido pero se me fue de las manos así que me quedé que elija el más probable
        """t1=0
        t2=0
        t3=0
        t4=0
        t=[]
        #asignamiento.append("T4")
        for i in range (0,len(restricciones_precedencia)):
            for j in variables.keys():
                if restricciones_precedencia[i][0] not in asignamiento:
                    if restricciones_precedencia[i][0] == j:
                        if j=="T1":
                            t1=t1+1
                        if j=="T2":
                            t2=t2+1
                        if j=="T3":
                            t3=t3+1
                        if j=="T4":
                            t4=t4+1
        t.insert(0,t1)
        t.insert(1,t2)
        t.insert(2,t3)
        t.insert(3,t4)
        for i in range(0, len(t)-1):
            if t[i+1] < t[i]:
                numero_clave = i
        print(t.index(numero_clave))
        #for i in range(1, len(t)):
        #    if
        #asignamiento.append()
        for i in variables.keys():
            if i == restricciones_precedencia[t.index(numero_clave)][0]:
                var=i
        print(var)
        """

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

        # for r in variables.keys():
        #    if var == restricciones_recursos[r]:
        # for m in range(0, len(restricciones_recursos)):
        #    if restricciones_recursos[var][m].desocupada==False:
        #        return False

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
