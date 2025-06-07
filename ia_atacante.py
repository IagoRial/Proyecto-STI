class IAAttacker:
    # Inicializador, con referencia a la red
    def __init__(self, red):
        self.red = red
        self.estrategias = [self.escaneo_lineal, self.escaneo_inverso, self.escaneo_saltado]
        self.estrategia_actual = None
        self.turno = 0  # Contador de turnos para ciclo de estrategias
        self.errores = []  # Lista para registrar los errores del atacante
        self.ultimo_estrategia_usada = None  # Inicializamos la variable

    # Función para seleccionar la estrategia de manera cíclica, con 3 turnos por estrategia
    def seleccionar_estrategia(self):
        # Cambiar de estrategia cada 3 turnos (cuando el turno sea divisible por 3)
        estrategia = self.estrategias[self.turno // 5 % 3]  # Usa el turno dividido entre 3
        self.ultimo_estrategia_usada = estrategia.__name__  # Actualizamos la estrategia utilizada
        return estrategia

    # Escanea los puertos de la red, registrando los errores cuando encuentra puertos cerrados
    def escanear(self):
        estrategia = self.seleccionar_estrategia()  # Selección de estrategia cíclica
        self.estrategia_actual = estrategia.__name__ 
        orden_puertos = estrategia()  # Obtenemos el orden de puertos según la estrategia
        estado = self.red.obtener_estado_red()
        self.errores = []  # Limpiamos los errores anteriores

        # Recorremos los puertos según la estrategia
        for puerto in orden_puertos:
            if estado[puerto]:  # Si el puerto está abierto, consideramos el ataque exitoso
                break  # Deja de escanear en cuanto se encuentra un puerto abierto
            else:
                self.errores.append(puerto)  # Si el puerto está cerrado, es un error

        self.turno += 1  # Incrementamos el contador de turnos
        return self.errores
    
    #------Estrategias------
    def escaneo_lineal(self):
        # Estrategia de escaneo lineal: de 1 al total de puertos
        return list(range(1, self.red.total_puertos + 1))

    def escaneo_inverso(self):
        # Estrategia de escaneo inverso: del total de puertos a 1
        return list(range(self.red.total_puertos, 0, -1))

    def escaneo_saltado(self):
        # Estrategia de escaneo saltado: puertos impares primero, luego pares
        return list(range(1, self.red.total_puertos + 1, 2)) + list(range(2, self.red.total_puertos + 1, 2))
