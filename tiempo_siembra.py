"""
    Simulación estimada del tiempo hasta cosecha combinando:
    - Newton (Para operaciones de maquinaria y compactación).
    - Crecimiento logístico (biológico) para la planta

    Salida:
    - Tiempo de preparación/siembra (s)
    - Tiempo biológico hasta alcanzar fracción objectivo de biomasa (días).
    - Tiempo total aproximado hasta cosecha
"""

import numpy as np
import matplotlib.pyplot as plt

G = 9.81 #! Gravedad m/s^2

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

    #! aceleración inicial que puede producir la fuerza neta
    a = net_force_N / mass_tractor_kg
    if a <= 0:
        t_acc = np.inf
        d_acc = 0
    else:
        t_acc = v_target_m_s / a
        d_acc = 0.5 * a * t_acc**2

    #? Area cubierta por segundo una vez a velocidad objectivo
    area_por_segundo = implement_width_m * v_target_m_s * seed_efficiency
    if area_por_segundo <= 0:
        return np.inf

    tiempo_operacion_seg = field_area_m2 / area_por_segundo

    #! Consideramos el tiempo total de operación + tiempo de aceleración.
    tiempo_total_s = tiempo_operacion_seg + t_acc
    return tiempo_total_s

def compaction_factor(mass_tractor_kg, contact_area_m2, threshold_pressure_pa=10000, k_compaction=0.5):
    """
        Estima un factor de compactación (0..1) en función de la presión del eje/rueda.
        - contact_area_m2: área de contacto de las ruedas/implementos (m^2)
        - threshold_pressure_pa: presión por debajo de la cual no hay daño significativo
        - k_compaction: factor de sensibilidad (máx reducción proporcional)
        Retorna factor en [0,1] que representará la reducción relativa en la tasa de crecimiento.
    """

    if contact_area_m2 <= 0:
        return 0.0
    pressure = (mass_tractor_kg * G) / contact_area_m2
    excess = max(0.0, pressure - threshold_pressure_pa)

    p_ref = threshold_pressure_pa * 4
    comp = (excess / max(1e-9, p_ref))
    comp = np.clip(comp * k_compaction, 0.0, k_compaction)
    return comp

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
    r_eff = r_base_per_day * (1.0 - compaction_effect)  # reducción por compactación
    if r_eff <= 0:
        return np.inf, None, None

    # Analítica del modelo logístico: x(t) = K / (1 + A * exp(-r t)), con A = (K - x0)/x0
    x0 = initial_fraction * K
    A = (K - x0) / x0
    # queremos t tal que x(t) = target_fraction * K
    target = target_fraction * K
    # target = K / (1 + A * exp(-r t)) => 1 + A e^{-r t} = K / target => e^{-r t} = (K/target - 1)/A
    ratio = (K/target - 1.0) / A
    if ratio <= 0:
        return 0.0, r_eff, x0
    t_days = - (1.0 / r_eff) * np.log(ratio)
    if t_days < 0:
        t_days = 0.0
    return t_days, r_eff, x0