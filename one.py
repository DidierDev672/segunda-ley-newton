
#! Calcular la velocidad final
# Un avión aterriza a una velocidad inicial de 70,0 m/s y luego desacelera a 1,50 m/s2 durante 40,0s. ¿Cual es su velocidad final?

def calcular_valocidad_final(velocidad: float,aceleracion: float,tiempo: float):
    return velocidad + (-aceleracion) * tiempo

print(f"Velocidad final:  {calcular_valocidad_final(70.0, 1.50, 40.0)} m/s2")