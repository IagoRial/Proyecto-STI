import random

class IADefensora:
    # Inicializador con referencia a la red
    def __init__(self, red):
        self.red = red
        self.estrategias = [self.abrir_puertos_al_inicio, self.abrir_puertos_al_final, self.abrir_puertos_aleatorios]
        self.rendimiento = {estr.__name__: 1.0 for estr in self.estrategias}
        self.estrategia_actual = None
        self.turno = 0  # Contador de turnos

    # Reacciona al ataque cerrando los puertos y abriendo otros 3, según la estrategia seleccionada
    def reaccionar_ataque(self):
        self.red.cerrar_todos()
        estrategia = self.elegir_estrategia()
        self.estrategia_actual = estrategia.__name__
        estrategia()


    # Elige la estrategia con mayor rendimiento
    def elegir_estrategia(self):
        mejor_estrategia = max(self.rendimiento, key=self.rendimiento.get)
        return getattr(self, mejor_estrategia)

    # Función de evaluación del rendimiento
    def evaluar_rendimiento(self, ia_atacante):
        # Determinar si el ataque fue exitoso o no (<= 3 fallos, exitoso)
        exitoso = len(ia_atacante.errores) <= 3
        delta_def = 1.0 if not exitoso else -1

        # Actualizar puntuaciones
        estrategia_def = self.estrategia_actual
        self.rendimiento[estrategia_def] += delta_def
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
