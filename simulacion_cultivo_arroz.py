import numpy as np
import matplotlib.pyplot as plt

def simulacion_arroz(masa, fuerza_motor, fuerza_resistencia, tiempo_total, paso_t):
    """
    Simula el movimiento de una sembradora de arroz aplicando la segunda ley de Newton.
    F = m * a
    """

    #? Incialización
    tiempos = np.arange(0, tiempo_total + paso_t, paso_t)
    velocidad = np.zeros_like(tiempos)
    posicion = np.zeros_like(tiempos)
    aceleracion = np.zeros_like(tiempos)

    for i in range(1, len(tiempos)):
        #! Fuerza neta = motor - resistencia
        F_neta = fuerza_motor - fuerza_resistencia

        #! Acelaración
        a = F_neta / masa
        aceleracion[i] = a

        #! Integrar velocidad y posición
        velocidad[i] = velocidad[i-1] + a * paso_t
        posicion[i] = posicion[i-1] + velocidad[i-1] * paso_t + 0.5 * a * paso_t**2

    return tiempos, aceleracion, velocidad, posicion

#? Parámetros del modelo
masa = 800 #! kg
fuerza_motor = 2000 #! N
fuerza_resistencia = 600 #! N
tiempo_total = 10 #! Segundos
paso_t = 0.5 #! Segundos

t, a, v, x = simulacion_arroz(masa, fuerza_motor, fuerza_resistencia, tiempo_total, paso_t)

#? Resultados.
print(f"Aceleración media: {np.mean(a): .2f} m/s2")
print(f"Velocidad final: {v[-1]:.2f} m/s")
print(f"Distancia recorrida: {x[-1]:.2f} m")

#? Graficas
plt.figure(figsize=(10, 6))

plt.subplot(3, 1, 1)
plt.plot(t, a, color="red", label="Aceleración (m/s²)")
plt.legend(); plt.grid()

plt.subplot(3, 1, 2)
plt.plot(t, v, color="blue", label="Velocidad (m/s)")
plt.legend(); plt.grid()

plt.subplot(3, 1, 3)
plt.plot(t, x, color="green", label="Posición (m)")
plt.legend(); plt.grid()

plt.suptitle("Simulación de Movimiento de Sembradora de Arroz (Segunda Ley de Newton)")
plt.tight_layout()
plt.show()