import random
from ia_atacante import IAAttacker
class IADefensoraEvolutiva:
    # Inicializador con referencia a la red
    def __init__(self, red):
        self.red = red
        self.estrategias = [self.abrir_puertos_al_inicio, self.abrir_puertos_al_final, self.abrir_puertos_aleatorios]
        self.poblacion = self.generar_poblacion(10)  # Generamos una población inicial de 10 individuos
        self.mejor_estrategia = None  # Inicializamos mejor_estrategia como None
        self.mejor_fitness = -float('inf')  # Inicializamos mejor_fitness como muy bajo
        self.turno_actual = 0  # Contador de turnos
        self.resumen = []  # Para almacenar los resultados al final de cada ciclo de 15 turnos

    # Método para generar una población de individuos con combinaciones aleatorias de estrategias
    def generar_poblacion(self, tamaño_poblacion=10):
        poblacion = []
        for _ in range(tamaño_poblacion):
            # Cada individuo tiene una lista de 0s y 1s donde cada índice corresponde a una estrategia
            # 1 significa que la estrategia está activada y 0 significa que está desactivada
            individuo = [random.choice([0, 1]) for _ in range(3)]
            poblacion.append(individuo)
        return poblacion

    # Método para que la IA defensora elija una estrategia en función de su combinación de estrategias
    def elegir_estrategia(self, individuo):
        # Comprobamos qué estrategia está activada (1) en el individuo
        estrategias_activas = [i for i, activo in enumerate(individuo) if activo == 1]
        
        # Si hay estrategias activas, seleccionamos una al azar de las activadas
        if estrategias_activas:
            estrategia_seleccionada = random.choice(estrategias_activas)
            return self.estrategias[estrategia_seleccionada]
        else:
            return None  # Si ninguna estrategia está activada, no hace nada

    # Reacciona al ataque cerrando los puertos y abriendo otros 3, según la estrategia seleccionada
    def reaccionar_ataque(self, individuo):
        self.red.cerrar_todos()
        estrategia = self.elegir_estrategia(individuo)
        if estrategia:
            self.estrategia_actual = estrategia.__name__
            estrategia()

    # Evaluación del rendimiento
    def evaluar_rendimiento(self, ia_atacante):
        # Evaluamos el rendimiento comparando el número de errores del atacante
        exitoso = len(ia_atacante.errores) <= 3
        delta_def = 1.0 if not exitoso else -1
        return delta_def

    #------Estrategias------
    def abrir_puertos_al_inicio(self):
        self.red.abrir_puertos([1, 2, 3])

    def abrir_puertos_al_final(self):
        self.red.abrir_puertos([self.red.total_puertos - 2, self.red.total_puertos - 1, self.red.total_puertos])

    def abrir_puertos_aleatorios(self):
        disponibles = list(range(1, self.red.total_puertos + 1))
        abiertos = random.sample(disponibles, 3)
        self.red.abrir_puertos(abiertos)

    # Método para seleccionar el mejor individuo de la población según el rendimiento
    def seleccionar_mejor_individuo(self, ia_atacante):
        # Aquí seleccionamos el mejor individuo en función de su rendimiento con la IA atacante
        mejor_individuo = min(self.poblacion, key=lambda individuo: self.evaluar_rendimiento_con_ia(ia_atacante, individuo))
        return mejor_individuo

    # Evaluación del rendimiento de un individuo con la IA atacante
    def evaluar_rendimiento_con_ia(self, ia_atacante, individuo):
        # Hacemos que la IA defensora reaccione con la estrategia de este individuo y luego evaluamos
        self.reaccionar_ataque(individuo)
        ia_atacante.escanear()
        return len(ia_atacante.errores)  # Retornamos el número de errores del atacante

    # Evolucionar la población (copiar al mejor individuo)
    def evolucionar(self, ia_atacante):
        if self.turno_actual % 15 == 0:
            print(f"Evolución después de {self.turno_actual} turnos...")

            # Seleccionamos el mejor individuo usando la IA atacante para la evaluación
            mejor_individuo = self.seleccionar_mejor_individuo(ia_atacante)

            # Actualizamos mejor_estrategia y mejor_fitness
            self.mejor_estrategia = mejor_individuo
            self.mejor_fitness = self.evaluar_rendimiento_con_ia(ia_atacante, mejor_individuo)

            # Reemplazamos toda la población con copias del mejor individuo
            self.poblacion = [mejor_individuo for _ in range(len(self.poblacion))]

            # Imprimir un resumen de la evolución
            print(f"Mejor estrategia seleccionada: {mejor_individuo}")


    def aumentar_turno(self):
        self.turno_actual += 1

    def obtener_resumen(self):
        # Mostrar el resumen después de cada ciclo de evolución
        for ciclo in self.resumen:
            print(f"Turno {ciclo['turno']}: Estrategia Evolutiva: {ciclo['estrategia']} | Rendimiento: {ciclo['rendimiento']}")
