#!/usr/bin/env python3
"""
Análisis de Deployment de Sensores de Humedad
Two-Tier Architecture: Pocos Gateways LoRa + Muchos Sensores de Humedad
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from datetime import datetime

# ============================================================================
# 1. CARGAR CONFIGURACIÓN Y RESULTADOS DE OPTIMIZACIÓN
# ============================================================================

print("="*80)
print("ANÁLISIS DE DEPLOYMENT: SENSORES DE HUMEDAD DE SUELO")
print("="*80)
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Cargar configuración
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

L_x = config['campo']['dimension_x_m']
L_y = config['campo']['dimension_y_m']
A_total = config['campo']['area_total_m2']

# Resultados de la optimización LoRa (del notebook ejecutado)
N_gateways = 2
gateway_coords = [
    (1525.0, 525.0),  # Gateway 1
    (225.0, 675.0)     # Gateway 2
]

# Rango efectivo de LoRa (conservador, considerando obstrucciones)
R_lora_efectivo = 750  # metros (rango típico en zona con obstrucciones)

print("RESULTADOS DE OPTIMIZACIÓN LoRa:")
print("-"*80)
print(f"Número de Gateways LoRa: {N_gateways}")
print(f"Coordenadas de Gateways:")
for idx, (x, y) in enumerate(gateway_coords, 1):
    print(f"  Gateway {idx}: ({x:.1f} m, {y:.1f} m)")
print(f"\nRango efectivo por gateway: {R_lora_efectivo} m")
print(f"Área del campo: {A_total:,.0f} m² ({A_total/10000:.1f} hectáreas)")

# ============================================================================
# 2. CALCULAR REQUERIMIENTOS DE SENSORES DE HUMEDAD
# ============================================================================

print("\n" + "="*80)
print("CÁLCULO DE SENSORES DE HUMEDAD")
print("="*80)

# Parámetros agronómicos para paltas
espaciado_arboles_m = 6  # Típico: 6-8m entre árboles de palta
densidad_arboles_por_ha = 10000 / (espaciado_arboles_m ** 2)
total_arboles_estimado = int(densidad_arboles_por_ha * (A_total / 10000))

# Estrategias de monitoreo
print("\nPARÁMETROS AGRONÓMICOS:")
print(f"  Espaciado típico entre árboles: {espaciado_arboles_m} m")
print(f"  Densidad de plantación: {densidad_arboles_por_ha:.0f} árboles/ha")
print(f"  Total árboles estimado: {total_arboles_estimado:,}")

print("\nESTRATEGIAS DE MONITOREO DE HUMEDAD:")
print("-"*80)

# Estrategia 1: Alta densidad (1 sensor por 1 ha)
estrategia_alta = {
    'nombre': 'Alta Precisión',
    'sensores_por_ha': 1.0,
    'descripcion': '1 sensor por hectárea - Máxima precisión',
    'spacing_m': 100
}
estrategia_alta['n_sensores'] = int(estrategia_alta['sensores_por_ha'] * A_total / 10000)

# Estrategia 2: Densidad media (1 sensor por 1.5 ha)
estrategia_media = {
    'nombre': 'Precisión Media',
    'sensores_por_ha': 0.67,
    'descripcion': '1 sensor por 1.5 hectáreas - Balance costo/precisión',
    'spacing_m': 120
}
estrategia_media['n_sensores'] = int(estrategia_media['sensores_por_ha'] * A_total / 10000)

# Estrategia 3: Densidad baja (1 sensor por 2 ha)
estrategia_baja = {
    'nombre': 'Cobertura Básica',
    'sensores_por_ha': 0.5,
    'descripcion': '1 sensor por 2 hectáreas - Mínimo viable',
    'spacing_m': 140
}
estrategia_baja['n_sensores'] = int(estrategia_baja['sensores_por_ha'] * A_total / 10000)

estrategias = [estrategia_alta, estrategia_media, estrategia_baja]

for est in estrategias:
    print(f"\n{est['nombre']}:")
    print(f"  {est['descripcion']}")
    print(f"  Densidad: {est['sensores_por_ha']:.2f} sensores/ha")
    print(f"  Espaciado de grid: ~{est['spacing_m']} m")
    print(f"  Total sensores: {est['n_sensores']}")
    print(f"  Costo relativo: {'$$$' if est['sensores_por_ha'] >= 1 else '$$' if est['sensores_por_ha'] >= 0.6 else '$'}")

# Seleccionar estrategia recomendada (media)
estrategia_seleccionada = estrategia_media
N_sensores = estrategia_seleccionada['n_sensores']
spacing_sensores = estrategia_seleccionada['spacing_m']

print("\n" + "="*80)
print(f"ESTRATEGIA RECOMENDADA: {estrategia_seleccionada['nombre']}")
print(f"Total sensores de humedad: {N_sensores}")
print("="*80)

# ============================================================================
# 3. GENERAR GRID DE SENSORES DE HUMEDAD
# ============================================================================

print("\nGenerando grid de sensores de humedad...")

# Crear grid regular de sensores de humedad
sensor_coords = []
x_offset = spacing_sensores / 2
y_offset = spacing_sensores / 2

y = y_offset
while y < L_y:
    x = x_offset
    while x < L_x:
        sensor_coords.append((x, y))
        x += spacing_sensores
    y += spacing_sensores

sensor_coords = np.array(sensor_coords)
N_sensores_real = len(sensor_coords)

print(f"Sensores de humedad generados: {N_sensores_real}")
print(f"Espaciado del grid: {spacing_sensores} m")

# ============================================================================
# 4. ASIGNAR SENSORES A GATEWAYS
# ============================================================================

print("\nAsignando sensores a gateways...")

def calcular_distancia(p1, p2):
    """Calcula distancia euclidiana entre dos puntos."""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Asignar cada sensor al gateway más cercano
asignaciones = []
sensores_por_gateway = {i: [] for i in range(N_gateways)}
sensores_fuera_rango = []

for idx, (sx, sy) in enumerate(sensor_coords):
    distancias = [calcular_distancia((sx, sy), gw) for gw in gateway_coords]
    gateway_mas_cercano = np.argmin(distancias)
    distancia_minima = distancias[gateway_mas_cercano]

    asignaciones.append({
        'sensor_id': idx,
        'coords': (sx, sy),
        'gateway': gateway_mas_cercano,
        'distancia': distancia_minima,
        'dentro_rango': distancia_minima <= R_lora_efectivo
    })

    if distancia_minima <= R_lora_efectivo:
        sensores_por_gateway[gateway_mas_cercano].append(idx)
    else:
        sensores_fuera_rango.append(idx)

print("\nRESULTADO DE ASIGNACIONES:")
print("-"*80)
for gw_id in range(N_gateways):
    n_asignados = len(sensores_por_gateway[gw_id])
    print(f"Gateway {gw_id + 1}: {n_asignados} sensores asignados")

if sensores_fuera_rango:
    print(f"\n⚠️  ADVERTENCIA: {len(sensores_fuera_rango)} sensores fuera del rango de {R_lora_efectivo}m")
    print("   Considere: aumentar potencia LoRa o agregar gateway adicional")
else:
    print(f"\n✓ Todos los {N_sensores_real} sensores están dentro del rango de cobertura")

# ============================================================================
# 5. VISUALIZACIÓN - TWO-TIER ARCHITECTURE
# ============================================================================

print("\nGenerando visualización...")

fig, ax = plt.subplots(figsize=(18, 14))

# Configurar límites y aspecto
ax.set_xlim(-50, L_x + 50)
ax.set_ylim(-50, L_y + 50)
ax.set_aspect('equal')

# Dibujar contorno del campo
from matplotlib.patches import Rectangle
ax.add_patch(Rectangle((0, 0), L_x, L_y,
                        fill=False, edgecolor='black', linewidth=3))

# Colores para cada gateway
colores_gw = ['#FF6B6B', '#4ECDC4']

# Dibujar círculos de cobertura de gateways
for idx, (gx, gy) in enumerate(gateway_coords):
    circle = Circle((gx, gy), R_lora_efectivo,
                   color=colores_gw[idx], alpha=0.08,
                   linestyle='--', linewidth=2, zorder=1)
    ax.add_patch(circle)

# Dibujar sensores de humedad (pequeños puntos)
for asig in asignaciones:
    sx, sy = asig['coords']
    gw_id = asig['gateway']
    dentro_rango = asig['dentro_rango']

    if dentro_rango:
        ax.scatter(sx, sy, c=colores_gw[gw_id], s=20, alpha=0.6,
                  edgecolors='none', zorder=3)
    else:
        ax.scatter(sx, sy, c='gray', s=20, alpha=0.4,
                  marker='x', zorder=3)

# Dibujar gateways LoRa (estrellas grandes)
for idx, (gx, gy) in enumerate(gateway_coords):
    ax.scatter(gx, gy, c=colores_gw[idx], s=800, marker='*',
              edgecolors='darkred', linewidth=3, zorder=5,
              label=f'Gateway LoRa {idx+1}')

    # Etiqueta del gateway
    ax.text(gx, gy - 30, f'GW{idx+1}',
           ha='center', va='top', fontsize=14, fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                    edgecolor=colores_gw[idx], linewidth=2))

# Configurar título y etiquetas
ax.set_xlabel('X (metros)', fontsize=14, fontweight='bold')
ax.set_ylabel('Y (metros)', fontsize=14, fontweight='bold')

titulo = f"Two-Tier Architecture: {N_gateways} Gateways LoRa + {N_sensores_real} Sensores de Humedad\n"
titulo += f"Campo: {L_x}m × {L_y}m ({A_total/10000:.1f} ha) | "
titulo += f"Densidad: {estrategia_seleccionada['sensores_por_ha']:.2f} sensores/ha"
ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)

# Leyenda personalizada
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='*', color='w', markerfacecolor='red',
           markeredgecolor='darkred', markeredgewidth=2,
           markersize=20, label=f'Gateways LoRa (N={N_gateways})'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colores_gw[0],
           markersize=8, alpha=0.7, label=f'Sensores Humedad GW1 ({len(sensores_por_gateway[0])})'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colores_gw[1],
           markersize=8, alpha=0.7, label=f'Sensores Humedad GW2 ({len(sensores_por_gateway[1])})'),
    Patch(facecolor='gray', alpha=0.2, linestyle='--',
          label=f'Cobertura LoRa ({R_lora_efectivo}m)')
]

if sensores_fuera_rango:
    legend_elements.append(
        Line2D([0], [0], marker='x', color='gray',
               markersize=8, linestyle='None',
               label=f'Fuera de rango ({len(sensores_fuera_rango)})')
    )

ax.legend(handles=legend_elements, loc='upper right', fontsize=12,
         framealpha=0.95, edgecolor='black', fancybox=True)
ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)

plt.tight_layout()

# Guardar en nueva ubicacion organizada
output_path = 'results/visualizations/two_tier_architecture.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Visualización guardada como '{output_path}'")

# ============================================================================
# 6. GENERAR REPORTE DE DEPLOYMENT
# ============================================================================

print("\nGenerando reporte de deployment...")

# Guardar en nueva ubicacion organizada
output_path = 'results/reports/deployment_guide.txt'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("GUÍA DE DEPLOYMENT - SISTEMA IoT DE MONITOREO DE HUMEDAD\n")
    f.write("Two-Tier Architecture: Gateways LoRa + Sensores de Humedad\n")
    f.write("="*80 + "\n\n")

    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    f.write("-"*80 + "\n")
    f.write("1. RESUMEN EJECUTIVO\n")
    f.write("-"*80 + "\n")
    f.write(f"Campo: {A_total/10000:.1f} hectáreas ({L_x}m × {L_y}m)\n")
    f.write(f"Cultivo: Paltas (aguacate)\n")
    f.write(f"Tecnología: LoRa 915 MHz + Sensores capacitivos de humedad\n\n")
    f.write(f"COMPONENTES DEL SISTEMA:\n")
    f.write(f"  • Gateways LoRa: {N_gateways} unidades\n")
    f.write(f"  • Sensores de humedad: {N_sensores_real} unidades\n")
    f.write(f"  • Densidad de monitoreo: {estrategia_seleccionada['sensores_por_ha']:.2f} sensores/hectárea\n")
    f.write(f"  • Estrategia: {estrategia_seleccionada['nombre']}\n\n")

    f.write("-"*80 + "\n")
    f.write("2. UBICACIÓN DE GATEWAYS LoRa\n")
    f.write("-"*80 + "\n")
    f.write(f"{'Gateway':<12} {'X (m)':<12} {'Y (m)':<12} {'Sensores':<12}\n")
    f.write("-"*80 + "\n")
    for idx, (gx, gy) in enumerate(gateway_coords):
        n_sens = len(sensores_por_gateway[idx])
        f.write(f"Gateway {idx+1:<4} {gx:<12.1f} {gy:<12.1f} {n_sens:<12}\n")
    f.write("\nREQUISITOS POR GATEWAY:\n")
    f.write("  • Módulo LoRa (915 MHz, potencia configurada 14 dBm)\n")
    f.write("  • Antena omnidireccional 3-5 dBi\n")
    f.write("  • Alimentación: Panel solar + batería o conexión AC\n")
    f.write("  • Altura de instalación recomendada: 3-5 metros\n")
    f.write("  • Conectividad: WiFi/Ethernet/Celular para uplink a cloud\n\n")

    f.write("-"*80 + "\n")
    f.write("3. GRID DE SENSORES DE HUMEDAD\n")
    f.write("-"*80 + "\n")
    f.write(f"Espaciado del grid: {spacing_sensores} m\n")
    f.write(f"Total de sensores: {N_sensores_real}\n")
    f.write(f"Profundidad de medición: 20-30 cm (zona radicular)\n\n")

    f.write("ESPECIFICACIONES DEL SENSOR:\n")
    f.write("  • Tipo: Sensor capacitivo de humedad de suelo\n")
    f.write("  • Módulo: ESP32 + LoRa (SX1276/RFM95)\n")
    f.write("  • Rango de medición: 0-100% VWC\n")
    f.write("  • Frecuencia de muestreo: Cada 30-60 minutos\n")
    f.write("  • Alimentación: Baterías + panel solar pequeño\n")
    f.write("  • Autonomía esperada: >1 año con sleep mode\n\n")

    f.write("-"*80 + "\n")
    f.write("4. ASIGNACIÓN SENSOR → GATEWAY\n")
    f.write("-"*80 + "\n")

    for gw_id in range(N_gateways):
        f.write(f"\nGateway {gw_id + 1} ({gateway_coords[gw_id][0]:.1f}, {gateway_coords[gw_id][1]:.1f}):\n")
        f.write(f"  Sensores asignados: {len(sensores_por_gateway[gw_id])}\n")
        f.write(f"  Primeros 10 sensores:\n")

        for i, sensor_id in enumerate(sensores_por_gateway[gw_id][:10]):
            asig = asignaciones[sensor_id]
            sx, sy = asig['coords']
            dist = asig['distancia']
            f.write(f"    Sensor {sensor_id:3d}: ({sx:7.1f}, {sy:7.1f}) - {dist:6.1f}m\n")

        if len(sensores_por_gateway[gw_id]) > 10:
            f.write(f"    ... y {len(sensores_por_gateway[gw_id]) - 10} sensores más\n")

    if sensores_fuera_rango:
        f.write(f"\n⚠️  SENSORES FUERA DE RANGO ({len(sensores_fuera_rango)}):\n")
        for sensor_id in sensores_fuera_rango[:5]:
            asig = asignaciones[sensor_id]
            sx, sy = asig['coords']
            dist = asig['distancia']
            f.write(f"    Sensor {sensor_id:3d}: ({sx:7.1f}, {sy:7.1f}) - {dist:6.1f}m del gateway más cercano\n")
        f.write("  ACCIÓN: Considerar agregar gateway adicional o aumentar potencia TX\n")

    f.write("\n" + "-"*80 + "\n")
    f.write("5. PROTOCOLO DE INSTALACIÓN\n")
    f.write("-"*80 + "\n")
    f.write("\nFASE 1 - INSTALACIÓN DE GATEWAYS:\n")
    f.write("  1. Instalar gateways en posiciones especificadas\n")
    f.write("  2. Orientar antenas verticalmente (polarización)\n")
    f.write("  3. Configurar parámetros LoRa (SF, BW, CR)\n")
    f.write("  4. Verificar conectividad a cloud/servidor\n")
    f.write("  5. Realizar test de alcance con sensor móvil\n")

    f.write("\nFASE 2 - DESPLIEGUE DE SENSORES:\n")
    f.write("  1. Marcar posiciones del grid con estacas\n")
    f.write("  2. Instalar sensores a profundidad especificada (20-30cm)\n")
    f.write("  3. Programar Device ID y Gateway asignado en cada sensor\n")
    f.write("  4. Verificar transmisión de datos\n")
    f.write("  5. Registrar ubicación en base de datos\n")

    f.write("\nFASE 3 - VALIDACIÓN Y PUESTA EN MARCHA:\n")
    f.write("  1. Verificar recepción de datos de todos los sensores\n")
    f.write("  2. Calibrar umbrales de humedad según tipo de suelo\n")
    f.write("  3. Configurar alarmas y notificaciones\n")
    f.write("  4. Entrenar al personal en mantenimiento\n")
    f.write("  5. Documentar sistema y crear plan de mantenimiento\n")

    f.write("\n" + "-"*80 + "\n")
    f.write("6. CONFIGURACIÓN LORA RECOMENDADA\n")
    f.write("-"*80 + "\n")
    f.write("Frecuencia: 915 MHz (ISM Band América)\n")
    f.write("Spreading Factor (SF): 7-9 (balance alcance/velocidad)\n")
    f.write("Bandwidth (BW): 125 kHz\n")
    f.write("Coding Rate (CR): 4/5\n")
    f.write("Potencia TX: 14 dBm (gateways), 14 dBm (sensores)\n")
    f.write("Tiempo en aire: ~50-200ms por mensaje\n")
    f.write("Payload: 20-30 bytes (ID + humedad + batería + temperatura)\n\n")

    f.write("-"*80 + "\n")
    f.write("7. ESTIMACIÓN DE COSTOS (USD)\n")
    f.write("-"*80 + "\n")
    f.write(f"Gateways LoRa ({N_gateways} unidades):\n")
    f.write(f"  • Hardware: ${N_gateways * 150:.0f} ($150/unidad)\n")
    f.write(f"  • Instalación: ${N_gateways * 200:.0f} ($200/unidad)\n")
    f.write(f"  • Subtotal gateways: ${N_gateways * 350:.0f}\n\n")

    f.write(f"Sensores de Humedad ({N_sensores_real} unidades):\n")
    f.write(f"  • Hardware: ${N_sensores_real * 45:.0f} ($45/unidad)\n")
    f.write(f"  • Instalación: ${N_sensores_real * 10:.0f} ($10/unidad)\n")
    f.write(f"  • Subtotal sensores: ${N_sensores_real * 55:.0f}\n\n")

    total_costo = N_gateways * 350 + N_sensores_real * 55
    f.write(f"COSTO TOTAL ESTIMADO: ${total_costo:,.0f}\n")
    f.write(f"Costo por hectárea: ${total_costo / (A_total/10000):,.0f}/ha\n")

    f.write("\n" + "="*80 + "\n")
    f.write("FIN DEL REPORTE\n")
    f.write("="*80 + "\n")

print(f"✓ Reporte de deployment guardado como '{output_path}'")

# ============================================================================
# 7. RESUMEN A CONSOLA
# ============================================================================

print("\n" + "="*80)
print("RESUMEN - TWO-TIER ARCHITECTURE")
print("="*80)
print(f"\n📡 TIER 1 - GATEWAYS LoRa:")
print(f"   Cantidad: {N_gateways} gateways")
print(f"   Ubicaciones: ver archivo de reporte")
print(f"   Función: Recibir datos y enviar a cloud")

print(f"\n💧 TIER 2 - SENSORES DE HUMEDAD:")
print(f"   Cantidad: {N_sensores_real} sensores")
print(f"   Densidad: {estrategia_seleccionada['sensores_por_ha']:.2f} sensores/hectárea")
print(f"   Espaciado: {spacing_sensores} m")
print(f"   Función: Medir humedad a nivel radicular (20-30cm)")

print(f"\n📊 ASIGNACIONES:")
for gw_id in range(N_gateways):
    print(f"   Gateway {gw_id + 1}: {len(sensores_por_gateway[gw_id])} sensores")

print(f"\n💰 COSTO ESTIMADO: ${total_costo:,.0f}")

print(f"\n📁 ARCHIVOS GENERADOS:")
print("   • results/visualizations/two_tier_architecture.png (mapa visual)")
print("   • results/reports/deployment_guide.txt (guía completa de instalación)")

print("\n" + "="*80)
print("✅ ANÁLISIS COMPLETADO")
print("="*80)
