import random
class IAAttacker:
    #Inicializador, con referencia a la red
    def __init__(self, red):
        self.red = red
        self.estrategias = [self.escaneo_lineal, self.escaneo_inverso, self.escaneo_saltado]
        self.rendimiento = {estr.__name__: 1.0 for estr in self.estrategias}
        self.aciertos = []
        self.errores = []
        self.ultimo_estrategia_usada = None

    #Función utilizada para seleccionar estrategia en base a su rendimiento
    def seleccionar_estrategia(self):
        max_rend = max(self.rendimiento.values())
        
        mejores = [estr for estr in self.estrategias
                   if self.rendimiento[estr.__name__] == max_rend]
        
        elegida = random.choice(mejores)
        self.ultimo_estrategia_usada = elegida.__name__
        return elegida
    #Escanea los puertos de la red en el orden dictado por la estrategia, registrando los errores con append, y parando en cuanto encuentra un puerto abierto
    def escanear(self):
        estrategia = self.seleccionar_estrategia()
        self.ultimo_estrategia_usada = estrategia.__name__ 
        orden_puertos = estrategia()
        estado = self.red.obtener_estado_red()
        self.aciertos = []
        self.errores = []
        self.ultimo_puerto_objetivo = None

        for puerto in orden_puertos:
            if estado[puerto]:
                self.aciertos.append(puerto)
                self.ultimo_puerto_objetivo = puerto
                break
            else:
                self.errores.append(puerto)

        return self.aciertos
    
    #------Estrategias------
    def escaneo_lineal(self):
        return list(range(1, self.red.total_puertos + 1))

    def escaneo_inverso(self):
        return list(range(self.red.total_puertos, 0, -1))

    def escaneo_saltado(self):
        return list(range(1, self.red.total_puertos + 1, 2)) + list(range(2, self.red.total_puertos + 1, 2))