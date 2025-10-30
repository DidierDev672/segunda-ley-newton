import numpy as np
import matplotlib.pyplot as plt

def movimiento(fuerza, masa, tiempo_total, peso_t=0.1):
    a = fuerza / masa
    tiempos = np.arange(0, tiempo_total + peso_t, peso_t)
    velocidades = a * tiempos
    posiciones = 0.5 * a * tiempos**2
    return tiempos, velocidades, posiciones

#? Parametros
F = 10 #! N
m = 2 #! kg
t_total = 5 #! segundos

t, v, x = movimiento(F, m, t_total)

#? Graficos
plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
plt.plot(t, v, label="Velocidad (m/s)")
plt.title("Velocidad vs Tiempo")
plt.xlabel("Tiempo (s)")
plt.ylabel("Velocidad (m/s)")
plt.grid(True)
plt.legend()

plt.subplot(1, 2,2)
plt.plot(t, x, label="Posición (m)", color='orange')
plt.title("Posición vs Tiempo")
plt.ylabel("Posición (m)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()