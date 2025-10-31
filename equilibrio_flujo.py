import numpy as np
import matplotlib.pyplot as plt

m = 0.002 #! Masa promedio de particula (kg)
aceleracion = np.linspace(0.1, 5, 50) #! Aceleraciones posibles del flujo (m/s2)

fuerza = m * aceleracion

#? Heurística: Se considera "óptima" cuando la fuerza está entre 0.004 y 0.007 N
f_optima_min, f_option_max = 0.004, 0.007

#? Visualización
plt.figure(figsize=(8, 5))
plt.plot(aceleracion, fuerza, label="F = m * a", color="blue")
plt.axhspan(f_optima_min, f_option_max, color="green", alpha=0.2, label="Zona óptima de fuerza")
plt.title("Heurística de equilibrio del flujo de riesgo (Ley de Newton II)")
plt.xlabel("Aceleración del agua (m/s2)")
plt.ylabel("Fuerza sobre partícula (N)")
plt.legend()
plt.grid(True)
plt.show()