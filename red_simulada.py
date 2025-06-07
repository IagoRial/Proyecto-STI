import random

class RedSimulada:
    def __init__(self, total_puertos=10):
        self.total_puertos = total_puertos
        self.puertos = {i: False for i in range(1, total_puertos + 1)}
        self.puertos_abiertos = []
        self.abrir_puertos_iniciales()
        
    #Abre 3 puertos aleatorios al principio de cada simulación
    def abrir_puertos_iniciales(self):
        self.abrir_puertos(random.sample(range(1, self.total_puertos + 1), 3))

    #Función que cierra todos los puertos
    def cerrar_todos(self):
        for puerto in self.puertos:
            self.puertos[puerto] = False
        self.actualizar_puertos_abiertos()

    #Recorre todos los puertos y guarda aquellos que esstén abiertos
    def actualizar_puertos_abiertos(self):
        self.puertos_abiertos = [p for p, abierto in self.puertos.items() if abierto]

    #Devuelve el valor de todos los puertos, es decir, nos muestra el estado de la red
    def obtener_estado_red(self):
        return self.puertos
    
    # Función genérica para abrir puertos
    def abrir_puertos(self, lista_puertos):
        for p in lista_puertos:
            self.puertos[p] = True
        self.actualizar_puertos_abiertos()

