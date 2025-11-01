import matplotlib.pyplot as plt
from simulacion_friccion import simular_deslizamiento

t, v, x, a = simular_deslizamiento(v0=6.0, mu_k=0.3, m=100.0, dt=0.01)

plt.figure(figsize=(10,6))
plt.subplot(2,1,1)
plt.plot(t, v, label="Velocidad (m/s)")
plt.ylabel("Velocidad (m/s)")
plt.grid(True)
plt.legend()

plt.subplot(2,1,2)
plt.plot(t, x, label="Posición (m)", color='green')
plt.xlabel("Tiempo (s)")
plt.ylabel("Posición (m)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
