"""
Simulación estimada del tiempo hasta cosecha combinando:
- Newton (para operaciones de maquinaria y compactación)
- Crecimiento logístico (biológico) para la planta

Salida:
- tiempo de preparación/siembra (s)
- tiempo biológico hasta alcanzar fracción objetivo de biomasa (días)
- tiempo total aproximado hasta cosecha
"""

import numpy as np
import matplotlib.pyplot as plt

G = 9.81  #! gravedad m/s^2


def tiempo_siembra(field_area_m2, implement_width_m, v_target_m_s, mass_tractor_kg, net_force_N, seed_efficiency=1.0):
    """
    Calcula el tiempo (s) necesario para sembrar el campo.
    - field_area_m2: superficie a sembrar (m^2)
    - implement_width_m: ancho de trabajo de la sembradora (m)
    - v_target_m_s: velocidad de trabajo objetivo (m/s)
    - mass_tractor_kg: masa del tractor (kg)
    - net_force_N: fuerza neta de tracción disponible (N)
    - seed_efficiency: fracción efectiva (0..1) que reduce tiempo por solapamiento/eficiencia
    """
    #? aceleración inicial que puede producir la fuerza neta
    a = net_force_N / mass_tractor_kg  # m/s^2
    if a <= 0:
        t_acc = np.inf
        d_acc = 0
    else:
        t_acc = v_target_m_s / a
        d_acc = 0.5 * a * t_acc**2

    #? área cubierta por segundo una vez a velocidad objetivo
    area_por_segundo = implement_width_m * v_target_m_s * seed_efficiency
    if area_por_segundo <= 0:
        return np.inf

    tiempo_operacion_seg = field_area_m2 / area_por_segundo

    #? Consideramos el tiempo total como tiempo de operación + tiempo de aceleración
    tiempo_total_s = tiempo_operacion_seg + t_acc
    return tiempo_total_s, a, d_acc


def compactacion_factor(mass_tractor_kg, contact_area_m2, threshold_pressure_pa=10000, k_compaction=0.5):
    """
    Estima un factor de compactación (0..1) en función de la presión del eje/rueda.
    - contact_area_m2: área de contacto de las ruedas/implementos (m^2)
    - threshold_pressure_pa: presión por debajo de la cual no hay daño significativo
    - k_compaction: factor de sensibilidad (máx reducción proporcional)
    Retorna factor en [0,1] que representará la reducción relativa en la tasa de crecimiento.
    """
    if contact_area_m2 <= 0:
        return 0.0
    pressure = (mass_tractor_kg * G) / contact_area_m2  # Pa ~ N/m2
    excess = max(0.0, pressure - threshold_pressure_pa)
    #? normalizamos: una presión alta produce hasta k_compaction reducción (p. ej. 50%)
    #? elegimos una escala de referencia para normalizar (p_ref)
    p_ref = threshold_pressure_pa * 4  # a 4x el threshold llegamos al máximo efecto
    comp = (excess / max(1e-9, p_ref))
    comp = np.clip(comp * k_compaction, 0.0, k_compaction)
    return comp  # valor entre 0 y k_compaction


def tiempo_hasta_cosecha_logistico(r_base_per_day, K, initial_fraction, compaction_effect, target_fraction=0.9):
    """
    Resuelve el modelo logístico dx/dt = r * x * (1 - x/K)
    r_base_per_day: tasa intrínseca de crecimiento por día
    compaction_effect: fracción (0..k) que reduce r (ej. 0.2 reduce r a 0.8*r)
    initial_fraction: biomasa inicial / K (0..1)
    target_fraction: fracción de K para cosecha (ej. 0.9)
    Devuelve tiempo en días para que x >= target_fraction * K
    """
    if initial_fraction <= 0:
        initial_fraction = 1e-6
    #? reducción por compactación
    r_eff = r_base_per_day * (1.0 - compaction_effect)
    if r_eff <= 0:
        return np.inf, None, None

    #? Analítica del modelo logístico: x(t) = K / (1 + A * exp(-r t)), con A = (K - x0)/x0
    x0 = initial_fraction * K
    A = (K - x0) / x0
    #? queremos t tal que x(t) = target_fraction * K
    target = target_fraction * K
    #? target = K / (1 + A * exp(-r t)) => 1 + A e^{-r t} = K / target => e^{-r t} = (K/target - 1)/A
    ratio = (K/target - 1.0) / A
    if ratio <= 0:
        return 0.0, r_eff, x0
    t_days = - (1.0 / r_eff) * np.log(ratio)
    if t_days < 0:
        t_days = 0.0
    return t_days, r_eff, x0

#* ----------------------- Ejemplo con valores representativos -----------------------


def ejemplo_simulacion():
    #? Parámetros del terreno y maquinaria
    field_area_ha = 1.0                 #! hectáreas
    field_area_m2 = field_area_ha * 10_000
    implement_width_m = 3.0             #! ancho trabajo (m)
    v_target_kmh = 5.0                  #! velocidad de trabajo (km/h)
    v_target_m_s = v_target_kmh / 3.6
    mass_tractor_kg = 800.0             #! masa total (kg)
    net_force_N = 2000.0                #! fuerza neta disponible (N)
    contact_area_m2 = 0.5               #! área de contacto total efectiva (m^2)

    #? Parámetros biológicos (arroz)
    #? tasa intrínseca diaria (ej: 8% por día)
    r_base_per_day = 0.08
    K = 1.0                             #! normalizamos biomasa a K=1 (fracción)
    initial_fraction = 0.02             #! 2% de biomasa inicial
    target_fraction = 0.9               #! cosechar al 90% de K

    #? 1) Tiempo de siembra
    tiempo_siembra_s, a, d_acc = tiempo_siembra(field_area_m2, implement_width_m, v_target_m_s,
                                                mass_tractor_kg, net_force_N, seed_efficiency=0.95)
    tiempo_siembra_h = tiempo_siembra_s / 3600

    #? 2) Compactación estimada
    comp = compactacion_factor(mass_tractor_kg, contact_area_m2,
                               threshold_pressure_pa=15000, k_compaction=0.5)

    #? 3) Tiempo biológico hasta cosecha (días)
    tiempo_biologico_dias, r_eff, x0 = tiempo_hasta_cosecha_logistico(r_base_per_day, K,
                                                                      initial_fraction, comp,
                                                                      target_fraction=target_fraction)

    #? 4) Resumen
    print("=== Resumen de la simulación ===")
    print(f"Área de campo: {field_area_ha:.2f} ha ({field_area_m2:.0f} m²)")
    print(
        f"Ancho implemento: {implement_width_m:.2f} m, velocidad objetivo: {v_target_kmh:.2f} km/h")
    print(
        f"Tiempo de siembra (estimado): {tiempo_siembra_h:.2f} horas ({tiempo_siembra_s:.0f} s)")
    print(
        f"Aceleración inicial posible: {a:.3f} m/s², distancia de aceleración: {d_acc:.2f} m")
    print(
        f"Presión de contacto estimada -> factor de compactación: {comp:.3f} (reduce r a {100*(1-comp):.1f}% de r_base)")
    if np.isfinite(tiempo_biologico_dias):
        print(
            f"Tiempo biológico hasta {int(100*target_fraction)}% de madurez: {tiempo_biologico_dias:.1f} días")
        print(
            f"Tiempo total aproximado (siembra + crecimiento): {tiempo_biologico_dias + tiempo_siembra_h/24:.1f} días")
    else:
        print("Con los parámetros dados, la tasa efectiva de crecimiento es <= 0; no alcanzará la madurez.")

    #? 5) Graficar evolución logísitica
    if np.isfinite(tiempo_biologico_dias):
        t_plot = np.linspace(0, tiempo_biologico_dias, 200)
        r = r_eff
        A = (K - x0) / x0
        x_t = K / (1 + A * np.exp(-r * t_plot))
        plt.figure(figsize=(8, 4))
        plt.plot(t_plot, x_t, label="Biomasa relativa (x/K)")
        plt.axhline(target_fraction, color='red', linestyle='--',
                    label=f"Objetivo {int(100*target_fraction)}%")
        plt.xlabel("Días desde siembra")
        plt.ylabel("Fracción de biomasa (x/K)")
        plt.title(
            "Evolución del cultivo (modelo logístico modificado por compactación)")
        plt.grid(True)
        plt.legend()
        plt.show()


if __name__ == "__main__":
    ejemplo_simulacion()
