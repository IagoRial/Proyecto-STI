import matplotlib.pyplot as plt
import pandas as pd

# Leer el archivo log (tiene: turno, errores, rendimiento)
df = pd.read_csv("registro_simulacion.log", names=["turno", "errores", "rendimiento"])

# Crear gráfica
plt.figure(figsize=(10, 5))
plt.plot(df["turno"], df["errores"], label="Errores del atacante", marker='o')
plt.plot(df["turno"], df["rendimiento"], label="Rendimiento de la defensora", marker='x')
plt.title("Evolución del ataque y defensa")
plt.xlabel("Turno")
plt.ylabel("Valor")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
