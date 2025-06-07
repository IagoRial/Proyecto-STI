class Evaluador:
    #Inicializador 
    def __init__(self, ia_atacante, ia_defensora):
        self.ia_atacante = ia_atacante
        self.ia_defensora = ia_defensora
        self.estrategia_defensora_anterior = None
    #Guardamos la estretgia defensora anterior para evaluarla 
    def guardar_estrategia_defensora(self, estrategia):
        self.estrategia_defensora_anterior = estrategia

    def evaluar(self):
        estrategia_atk = self.ia_atacante.ultimo_estrategia_usada
        estrategia_def = self.estrategia_defensora_anterior if self.estrategia_defensora_anterior else None

        #Determinar si el ataque fue exitoso o no (<= 3 fallos, exitoso)
        exitoso = len(self.ia_atacante.errores) <= 3
        delta_atk = 1.0 if exitoso else -0.5
        delta_def = -0.5 if exitoso else 1.0

        # Actualizar puntuaciones
        self.ia_atacante.rendimiento[estrategia_atk] += delta_atk
        if estrategia_def:
            self.ia_defensora.rendimiento[estrategia_def] += delta_def

        return delta_atk, delta_def