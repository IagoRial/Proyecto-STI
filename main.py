from red_simulada import RedSimulada
from ia_atacante import IAAttacker
from ia_defensora import IADefensora
from ia_defensora_evolutiva import IADefensoraEvolutiva  # Importamos la IA defensora evolutiva

# Función para imprimir el resumen de cada ciclo de 15 turnos
def print_resumen(turno, red, ia_atacante, ia_defensora_qlearning, ia_defensora_evolutiva):
    # Estrategia y errores del atacante
    estrategia_atk = ia_atacante.ultimo_estrategia_usada
    errores_atk = ia_atacante.errores  # Mostramos los errores del atacante

    # Estrategia y rendimiento de la defensora Q-Learning
    estrategia_def_qlearning = ia_defensora_qlearning.estrategia_actual
    rendimiento_def_qlearning = ia_defensora_qlearning.rendimiento.get(estrategia_def_qlearning, 0)

    # Estrategia y rendimiento de la defensora evolutiva
    if ia_defensora_evolutiva.mejor_estrategia:
        estrategia_def_evolutiva = ia_defensora_evolutiva.mejor_estrategia
        rendimiento_def_evolutiva = ia_defensora_evolutiva.mejor_fitness
    else:
        estrategia_def_evolutiva = "Sin evolución aún"
        rendimiento_def_evolutiva = "N/A"

    # Mostrar los resultados del resumen solo después de cada ciclo de 15 turnos
    print(f"\n--- Resumen después de {turno} turnos ---")
    print(f"[Red] Puertos abiertos: {sorted(red.puertos_abiertos)}")
    print(f"[Atacante] Estrategia: {estrategia_atk} | Errores: {len(errores_atk)}")
    print(f"[Defensora Q-Learning] Estrategia: {estrategia_def_qlearning} | Rendimiento: {rendimiento_def_qlearning:.2f}")
    print(f"[Defensora Evolutiva] Estrategia: {estrategia_def_evolutiva} | Rendimiento: {rendimiento_def_evolutiva}")

# Crear la red simulada y las instancias de las IA
red = RedSimulada(total_puertos=10)
ia_atacante = IAAttacker(red)
ia_defensora_qlearning = IADefensora(red)
ia_defensora_evolutiva = IADefensoraEvolutiva(red)

# Bucle principal del programa
turno = 1
while True:
    # La defensora Q-Learning reacciona al ataque
    ia_defensora_qlearning.reaccionar_ataque()
    ia_atacante.escanear()
    ia_defensora_qlearning.evaluar_rendimiento(ia_atacante)

    # La defensora Evolutiva evalúa su rendimiento y evoluciona cada ciclo
    ia_defensora_evolutiva.evolucionar(ia_atacante)  # Aquí pasamos la instancia de IAAtacante

    # Si llegamos al ciclo de 15 turnos, mostramos el resumen
    if turno % 15 == 0:
        print_resumen(turno, red, ia_atacante, ia_defensora_qlearning, ia_defensora_evolutiva)

    # Pedir confirmación en cada ciclo
    continuar = input("\n¿Continuar con la siguiente iteración? (y/n): ")
    if continuar.lower() != 'y':
        print("Simulación finalizada.")
        break

    turno += 1
