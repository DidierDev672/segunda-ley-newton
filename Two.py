
#! Calcular el desplazamiento de un objecto en acelaración
# Los dragsters pueden alcanzar una aceleración media de 26,0 m/s2. Supongamos que un dragster acelera desde el reposo a esta tasa durante 5,56.
# ¿Qué distancia recorre en este tiempo?

def calcular_aceleracion(velocidadInicial,tiempo):
    t = tiempo * tiempo
    a = velocidadInicial * t
    result = (0.5 * a)
    print(f"Tiempo: {t}")
    print(f"Aceleración: {a}")
    return result


print(f"Distancia recorrida: {calcular_aceleracion(26.0,5.56)} m/s2");