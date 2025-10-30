def segunda_ley_newton(fuerza, masa):
    """
        Calcula la aceleración según la segunda ley de Newton.
    """
    if masa <= 0:
        raise ValueError("La masa debe ser mayor que cero.")
    aceleracion = fuerza / masa
    return aceleracion

#? Ejemplo de uso:
fuerza = 20 #! Newtons
masa = 5 #! Kg

aceleracion = segunda_ley_newton(fuerza, masa)
print(f"Aceleración: {aceleracion: .2f} m/s2")