from red_simulada import RedSimulada
from ia_atacante import IAAttacker
from ia_defensora import IADefensora
from evaluador import Evaluador
import logging

# Configuración del log
logging.basicConfig(
    filename='registro_simulacion.log',
    level=logging.INFO,
    format='%(message)s',
    filemode='w'  # Reescribe el archivo cada vez que se ejecuta
)

TURNOS_AUTO = 20  # 0 = manual, otro número, x turnos, automático (ej: 50)

# Función que imprime el resumen del turno
def print_turno_resumen(turno, red, ia_atacante, ia_defensora, delta_atk, delta_def):
    estrategia_atk = max(ia_atacante.rendimiento, key=ia_atacante.rendimiento.get)
    puntuacion_atk = ia_atacante.rendimiento[estrategia_atk]

    estrategia_def = max(ia_defensora.rendimiento, key=ia_defensora.rendimiento.get)
    puntuacion_def = ia_defensora.rendimiento[estrategia_def]

    print(f"\n--- Turno {turno} ---")
    print(f"[Red] Puertos abiertos: {sorted(red.puertos_abiertos)}")
    print(f"[Atacante] Estrategia: {ia_atacante.ultimo_estrategia_usada} | Aciertos: {len(ia_atacante.aciertos)} | Errores: {len(ia_atacante.errores)}")
    print(f"[Defensora] Estrategia: {ia_defensora.estrategia_actual}")
    print(f"[Evaluación] Atacante {delta_atk:+.1f} | Defensora {delta_def:+.1f}")
    print(f"[Rendimiento] Mejor estrategia atacante: {estrategia_atk} ({puntuacion_atk:.2f}) | Mejor defensora: {estrategia_def} ({puntuacion_def:.2f})")

# Crear instancias
red = RedSimulada(total_puertos=10)
ia_atacante = IAAttacker(red)
ia_defensora = IADefensora(red)
evaluador = Evaluador(ia_atacante, ia_defensora)

# Bucle de simulación
turno = 1
while True:
    ia_defensora.reaccionar_ataque()
    evaluador.estrategia_defensora_anterior = ia_defensora.estrategia_actual
    ia_atacante.escanear()
    delta_atk, delta_def = evaluador.evaluar()

    # Guardar datos en log
    estrategia = ia_defensora.estrategia_actual
    rendimiento = ia_defensora.rendimiento[estrategia] if estrategia else 0.0
    logging.info(f"{turno},{len(ia_atacante.errores)},{rendimiento:.2f}")

    # Mostrar en pantalla
    print_turno_resumen(turno, red, ia_atacante, ia_defensora, delta_atk, delta_def)

    if TURNOS_AUTO > 0:
        if turno >= TURNOS_AUTO:
            print("\nSimulación automática finalizada.")
            break
    else:
        continuar = input("\n¿Continuar con la siguiente iteración? (y/n): ")
        if continuar.lower() != 'y':
            print("Simulación finalizada.")
            break

    turno += 1
