import numpy as np
import matplotlib.pyplot as plt

def simulacion_variable(masa, tiempo_total, paso_t=0.1):
    tiempos = np.arange(0, tiempo_total, paso_t)
    fuerza = 10 + 2 * np.sin(tiempos) #! Fuerza oscilante
    acelaracion = fuerza / masa

    velocidad = np.cumsum(acelaracion) * paso_t
    posicion = np.cumsum(velocidad) * paso_t

    return tiempos, fuerza, acelaracion, velocidad, posicion


t, F, a, v, x = simulacion_variable(masa=2, tiempo_total=10)

plt.figure(figsize=(10, 6))
plt.subplot(3,1,1)
plt.plot(t, F, label="Fuerza (N)")
plt.legend()
plt.grid()

plt.subplot(3,1,2)
plt.plot(t, a, label="Aceleración (m/s2)", color="red")
plt.legend();
plt.grid()

plt.subplot(3,1,3)
plt.plot(t, v, label="Velocidad (m/s2)", color="green")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()