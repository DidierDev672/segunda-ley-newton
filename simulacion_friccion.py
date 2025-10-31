import numpy as np

def simular_deslizamiento(v0, mu_k, m, dt=0.01, g=9.81, max_t=30.0):
    """
    Simula la velocidad y posición de un cuerpo que desliza bajo fricción cinética constante.
    Devuelve arrays de tiempo, velocidad, posición y aceleración.
    """
    N = m * g
    Fk = mu_k * N
    a = -Fk / m  # constante

    times = [0.0]
    v = [v0]
    x = [0.0]
    a_list = [a]

    t = 0.0
    while t < max_t and abs(v[-1]) > 1e-4:
        t += dt
        v_new = v[-1] + a * dt
        # evitar cambiar de signo: si sobrepasa 0, poner 0
        if v_new * v0 < 0:
            v_new = 0.0
        x_new = x[-1] + v[-1] * dt + 0.5 * a * dt**2
        times.append(t)
        v.append(v_new)
        x.append(x_new)
        a_list.append(a)
    return np.array(times), np.array(v), np.array(x), np.array(a_list)

if __name__ == "__main__":
    t, v, x, a = simular_deslizamiento(5.0, 0.25, 50.0)
    print(f"Tiempo final: {t[-1]:.2f}s, Distancia: {x[-1]:.2f} m")