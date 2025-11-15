#!/usr/bin/env python3
"""
Script para crear un mapa de ubicación del campo
Muestra el contexto geográfico y dimensiones del campo de paltas
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle
import json

# Cargar configuración
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Parámetros del campo
L_x = config['campo']['dimension_x_m']
L_y = config['campo']['dimension_y_m']
A_total = config['campo']['area_total_m2']
elevacion_min = config['campo']['elevacion_min_m']
elevacion_max = config['campo']['elevacion_max_m']
elevacion_mediana = config['campo']['elevacion_mediana_m']

# Crear figura
fig, ax = plt.subplots(figsize=(14, 10))
ax.set_aspect('equal')

# Fondo (contexto de área más grande)
contexto_size = 3000  # 3 km x 3 km de contexto
ax.set_xlim(-500, contexto_size - 500)
ax.set_ylim(-500, contexto_size - 500)

# Dibujar área de contexto (fondo)
ax.add_patch(Rectangle((0, 0), contexto_size, contexto_size,
                       facecolor='#E8F5E9', edgecolor='none', alpha=0.3, zorder=0))

# Dibujar el campo principal
campo_x_offset = (contexto_size - L_x) / 2
campo_y_offset = (contexto_size - L_y) / 2

# Sombra del campo
ax.add_patch(Rectangle((campo_x_offset + 20, campo_y_offset - 20), L_x, L_y,
                       facecolor='gray', alpha=0.2, zorder=1))

# Campo principal
ax.add_patch(FancyBboxPatch((campo_x_offset, campo_y_offset), L_x, L_y,
                           boxstyle="round,pad=10",
                           facecolor='#4CAF50', edgecolor='#2E7D32',
                           linewidth=4, alpha=0.6, zorder=2))

# Texto con información del campo
info_text = f"Campo de Paltas\n{A_total/10000:.1f} hectareas\n{L_x}m × {L_y}m"
ax.text(campo_x_offset + L_x/2, campo_y_offset + L_y/2,
       info_text,
       fontsize=24, fontweight='bold', ha='center', va='center',
       bbox=dict(boxstyle='round,pad=1', facecolor='white',
                edgecolor='#2E7D32', linewidth=2, alpha=0.95),
       zorder=5)

# Dimensiones
# Dimension horizontal
ax.annotate('', xy=(campo_x_offset + L_x, campo_y_offset - 150),
           xytext=(campo_x_offset, campo_y_offset - 150),
           arrowprops=dict(arrowstyle='<->', lw=2, color='black'))
ax.text(campo_x_offset + L_x/2, campo_y_offset - 200,
       f'{L_x} m',
       fontsize=14, ha='center', fontweight='bold',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9))

# Dimension vertical
ax.annotate('', xy=(campo_x_offset - 150, campo_y_offset + L_y),
           xytext=(campo_x_offset - 150, campo_y_offset),
           arrowprops=dict(arrowstyle='<->', lw=2, color='black'))
ax.text(campo_x_offset - 250, campo_y_offset + L_y/2,
       f'{L_y} m',
       fontsize=14, ha='center', va='center', rotation=90, fontweight='bold',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9))

# Brújula (Norte)
compass_x = campo_x_offset + L_x + 300
compass_y = campo_y_offset + L_y - 200
ax.arrow(compass_x, compass_y, 0, 100,
        head_width=30, head_length=30, fc='red', ec='darkred', lw=2, zorder=6)
ax.text(compass_x, compass_y + 150, 'N',
       fontsize=20, fontweight='bold', ha='center', color='darkred')

# Escala
scale_x = campo_x_offset
scale_y = campo_y_offset - 350
scale_length = 500  # 500 metros
ax.plot([scale_x, scale_x + scale_length],
       [scale_y, scale_y],
       'k-', lw=4, zorder=6)
ax.plot([scale_x, scale_x], [scale_y - 20, scale_y + 20], 'k-', lw=2)
ax.plot([scale_x + scale_length, scale_x + scale_length],
       [scale_y - 20, scale_y + 20], 'k-', lw=2)
ax.text(scale_x + scale_length/2, scale_y - 60,
       f'{scale_length} m',
       fontsize=12, ha='center', fontweight='bold',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9))

# Información adicional
info_box_text = f"Area: {A_total:,.0f} m² ({A_total/10000:.2f} ha)\n"
info_box_text += f"Perimetro: ~{2*(L_x + L_y):.0f} m\n"
info_box_text += f"Elevacion: {elevacion_min:.1f}-{elevacion_max:.1f} m\n"
info_box_text += f"(mediana: {elevacion_mediana:.0f} m)\n"
info_box_text += f"\nZona: Campesina poblada\n"
info_box_text += f"Cultivo: Paltas (Persea americana)"

ax.text(campo_x_offset + L_x + 100, campo_y_offset + 100,
       info_box_text,
       fontsize=11, va='bottom', ha='left',
       bbox=dict(boxstyle='round,pad=0.8', facecolor='lightyellow',
                edgecolor='#F57C00', linewidth=2, alpha=0.95),
       family='monospace', zorder=5)

# Título
ax.text(contexto_size/2, contexto_size - 150,
       'Mapa de Ubicacion - Campo de Paltas',
       fontsize=20, fontweight='bold', ha='center',
       bbox=dict(boxstyle='round,pad=1', facecolor='white',
                edgecolor='black', linewidth=2, alpha=0.95))

# Subtítulo
ax.text(contexto_size/2, contexto_size - 250,
       'Sistema IoT de Monitoreo de Humedad - Two-Tier Architecture',
       fontsize=12, ha='center', style='italic',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))

# Configurar ejes
ax.set_xlabel('Distancia (metros)', fontsize=12, fontweight='bold')
ax.set_ylabel('Distancia (metros)', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
ax.set_facecolor('#F5F5DC')  # Color beige claro

# Remover marco
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()

# Guardar
output_path = 'results/visualizations/location_map.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Mapa de ubicacion guardado como '{output_path}'")

# Mostrar
# plt.show()

print("\n" + "="*60)
print("MAPA DE UBICACIÓN GENERADO")
print("="*60)
print(f"Campo: {A_total/10000:.1f} hectareas ({L_x}m × {L_y}m)")
print(f"Archivo: {output_path}")
print("="*60)
