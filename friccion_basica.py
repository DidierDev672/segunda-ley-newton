import math

def aceleracion_por_friccion(mu_k: float, g: float = 9.81) -> float:
    """ Puede crear una, guia de fricción y resistencia del aire y del agua con python. por favor  """
    return -mu_k * g

def distancia_frenado(v0: float, mu_k: float, g: float = 9.81) -> float:
    """ Aceleración (negativa) debida a la fricción cinética en superficie horizontal.  """
    if mu_k <= 0:
        raise ValueError("mu_k debe ser positivo")
    return v0**2 / (2 * mu_k * g)

#? Ejemplo
v0 = 5.0
mu_k = 0.3
a = aceleracion_por_friccion(mu_k)
d = distancia_frenado(v0, mu_k)
print(f"Aceleración: {a:.3f} m/s2, Distancia de frenado: {d: .3f} m")