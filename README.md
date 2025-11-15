# Sistema IoT de Monitoreo de Humedad para Agricultura de Precision

Proyecto completo de optimizacion para despliegue de sistema IoT en campo de paltas (208 hectareas), combinando:
1. **Optimizacion de Gateways LoRa** mediante Programacion Lineal Entera (PLE)
2. **Despliegue estrategico de Sensores de Humedad** basado en principios agronomicos

## Descripcion del Proyecto

Este proyecto resuelve dos problemas complementarios para implementar un sistema IoT de monitoreo de humedad de suelo:

### Problema 1: Optimizacion de Gateways LoRa (Set Cover Problem)

Minimizar el numero de gateways LoRa necesarios para garantizar cobertura RF completa del campo, considerando:
- Modelo de propagacion path-loss realista
- Interferencia y obstrucciones (zona campesina poblada)
- Diferenciacion entre campo abierto (n=2.0) y zona obstruida (n=3.5)

**Resultado:** Solo **2 gateways LoRa** necesarios para cubrir 208 hectareas

### Problema 2: Despliegue de Sensores de Humedad

Determinar cantidad y ubicacion optima de sensores de humedad de suelo basado en:
- Requerimientos agronomicos (densidad por hectarea)
- Cobertura de variabilidad espacial del suelo
- Asignacion eficiente a gateways disponibles

**Resultado:** **153 sensores de humedad** distribuidos en grid de 120m

## Arquitectura del Sistema (Two-Tier)

```
TIER 1: Gateways LoRa (2 unidades)
   |
   +-- Gateway 1 (1525m, 525m) --> 87 sensores
   +-- Gateway 2 (225m, 675m)  --> 62 sensores

TIER 2: Sensores de Humedad (153 unidades)
   |
   +-- Miden humedad cada 30-60 min
   +-- Transmiten via LoRa a gateway asignado
   +-- Autonomia: >1 ano con sleep mode
```

## Parametros del Campo

| Parametro | Valor | Descripcion |
|-----------|-------|-------------|
| Area Total | 2,080,000 m2 | 208 hectareas |
| Dimensiones | 2000m x 1040m | Campo rectangular |
| Cultivo | Paltas | Aguacate |
| Ubicacion | Zona campesina poblada | Con casas y vegetacion densa |

## Resultados Principales

### Optimizacion de Gateways LoRa

**Metodo:** Set Cover Problem mediante PLE (PuLP + CBC solver)

**Parametros de Radio:**
- Frecuencia: 915 MHz (banda ISM America)
- Potencia TX: 14 dBm
- Sensibilidad RX: -137 dBm
- Rango efectivo: ~750m (con obstrucciones)

**Solucion Optima:**
- **N_optimo = 2 gateways**
- Tiempo de calculo: 5.98 segundos
- Cobertura: 100% del campo
- Densidad: 0.01 gateways/hectarea

### Despliegue de Sensores de Humedad

**Estrategia Seleccionada:** Precision Media

**Parametros:**
- Densidad: 0.67 sensores/hectarea
- Espaciado: 120m entre sensores
- Total: 153 sensores
- Profundidad: 20-30 cm (zona radicular)

**Asignaciones:**
- Gateway 1: 87 sensores (lado este del campo)
- Gateway 2: 62 sensores (lado oeste del campo)
- 4 sensores requieren ajuste menor (fuera de rango por <80m)

## Instalacion

### Requisitos Previos

```bash
# Software
- Python 3.8+
- pip
- Jupyter Notebook

# Opcional (mejor rendimiento)
- CBC solver
```

### Instalacion Rapida

```bash
# 1. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Instalar CBC solver (opcional pero recomendado)
brew install coin-or-tools/coinor/cbc  # macOS
# sudo apt-get install coinor-cbc      # Linux
```

### Dependencias Principales

- `pulp>=2.7.0` - Solver de programacion lineal entera
- `numpy>=1.24.0` - Calculos numericos
- `matplotlib>=3.7.0` - Visualizacion
- `jupyter>=1.0.0` - Notebooks interactivos

## Uso

### 1. Optimizacion de Gateways LoRa

```bash
# Activar entorno virtual
source venv/bin/activate

# Abrir y ejecutar notebook
jupyter notebook notebooks/sensor_optimization.ipynb
```

El notebook ejecuta:
1. Carga de parametros desde `config.json`
2. Generacion de puntos de demanda (grid 50x50m)
3. Calculo de modelo path-loss
4. Creacion de matriz de cobertura binaria
5. Formulacion del Set Cover Problem
6. Resolucion con PuLP + CBC
7. Visualizacion de resultados

**Salida:**
- N_optimo y coordenadas de gateways
- Visualizacion: `results/visualizations/distribucion_sensores_pathloss.png`
- Reporte: `results/reports/reporte_optimizacion.txt`

### 2. Analisis de Sensores de Humedad

```bash
# Ejecutar script de deployment
python scripts/humidity_sensor_deployment.py
```

El script calcula:
1. Requerimientos agronomicos de sensores
2. Grid optimo de ubicaciones
3. Asignacion sensor → gateway
4. Verificacion de cobertura RF
5. Estimacion de costos

**Salida:**
- Visualizacion: `results/visualizations/two_tier_architecture.png`
- Guia completa: `results/reports/deployment_guide.txt`

## Estructura del Proyecto

```
set-cover-problem/
|
├── README.md                           # Este archivo
├── config.json                         # Parametros configurables
├── requirements.txt                    # Dependencias Python
|
├── notebooks/                          # Jupyter notebooks
│   ├── sensor_optimization.ipynb       # Optimizacion gateways LoRa
│   └── sensor_optimization_executed.ipynb
|
├── scripts/                            # Scripts Python
│   └── humidity_sensor_deployment.py   # Analisis sensores humedad
|
├── results/                            # Resultados generados
│   ├── visualizations/
│   │   ├── distribucion_sensores_pathloss.png  # Mapa gateways
│   │   └── two_tier_architecture.png           # Sistema completo
│   └── reports/
│       ├── reporte_optimizacion.txt            # Reporte tecnico
│       └── deployment_guide.txt                # Guia de instalacion
|
└── venv/                               # Entorno virtual (local)
```

## Configuracion

Editar `config.json` para ajustar parametros:

### Parametros del Campo

```json
{
  "campo": {
    "dimension_x_m": 2000,
    "dimension_y_m": 1040,
    "area_total_m2": 2080000
  }
}
```

### Modelo de Propagacion

```json
{
  "propagacion": {
    "frecuencia_mhz": 915,
    "potencia_tx_dbm": 14,
    "sensibilidad_rx_dbm": -137,
    "exponente_path_loss_abierto": 2.0,
    "exponente_path_loss_obstruido": 3.5,
    "margen_desvanecimiento_db": 10
  }
}
```

### Escenario de Interferencia

```json
{
  "escenario": {
    "tipo": "zona_campesina_poblada",
    "porcentaje_area_obstruida": 35
  }
}
```

### Discretizacion

```json
{
  "discretizacion": {
    "celda_x_m": 50,
    "celda_y_m": 50
  }
}
```

## Formulacion Matematica

### Set Cover Problem (Gateways LoRa)

**Variables de Decision:**
```
x_i ∈ {0, 1}  para cada ubicacion i ∈ I
```

**Funcion Objetivo:**
```
Minimizar: Σ x_i  (i ∈ I)
```

**Restricciones:**
```
Σ a_ij * x_i >= 1   para todo j ∈ J (puntos de demanda)
x_i ∈ {0, 1}        para todo i ∈ I
```

Donde:
- `a_ij = 1` si el enlace (i,j) es viable segun modelo path-loss
- `a_ij = 0` en caso contrario

### Modelo de Path-Loss

```
PL(d) = PL(d0) + 10 * n * log10(d/d0)
```

**Viabilidad del Enlace:**
```
P_rx = P_tx - PL(d) >= Sensibilidad_rx + Margen
```

**Rangos Calculados:**
- Campo abierto (n=2.0): ~500m
- Zona obstruida (n=3.5): ~150m
- Reduccion por obstruccion: 70%

## Especificaciones Tecnicas

### Hardware - Gateway LoRa

- Modulo LoRa 915 MHz (ej: RFM95, SX1276)
- Microcontrolador (ESP32, Raspberry Pi, etc.)
- Antena omnidireccional 3-5 dBi
- Alimentacion: Panel solar + bateria o AC
- Conectividad uplink: WiFi/Ethernet/4G
- Altura instalacion: 3-5 metros

### Hardware - Sensor de Humedad

- Sensor capacitivo de humedad de suelo
- Microcontrolador: ESP32
- Modulo LoRa: SX1276 o RFM95
- Bateria LiPo + panel solar pequeno
- Carcasa impermeable IP67
- Profundidad instalacion: 20-30 cm

### Configuracion LoRa Recomendada

| Parametro | Valor | Notas |
|-----------|-------|-------|
| Frecuencia | 915 MHz | Banda ISM America |
| Spreading Factor | SF7-SF9 | Balance alcance/velocidad |
| Bandwidth | 125 kHz | Estandar |
| Coding Rate | 4/5 | Buena correccion de errores |
| Potencia TX | 14 dBm | Ambos gateways y sensores |
| Tiempo en aire | 50-200ms | Por mensaje |
| Payload | 20-30 bytes | ID + humedad + bat + temp |

## Estimacion de Costos

### Hardware

| Componente | Cantidad | Costo Unitario | Subtotal |
|------------|----------|----------------|----------|
| Gateway LoRa | 2 | $150 | $300 |
| Sensor Humedad + LoRa | 153 | $45 | $6,885 |
| **Total Hardware** | | | **$7,185** |

### Instalacion

| Item | Cantidad | Costo Unitario | Subtotal |
|------|----------|----------------|----------|
| Instalacion Gateway | 2 | $200 | $400 |
| Instalacion Sensor | 153 | $10 | $1,530 |
| **Total Instalacion** | | | **$1,930** |

### Resumen

- **Costo Total:** ~$9,115 USD
- **Costo por Hectarea:** ~$44/ha
- **Costo por Sensor:** ~$60 (hardware + instalacion)

## Guia de Deployment

### Fase 1: Instalacion de Gateways (2 unidades)

1. Marcar ubicaciones:
   - Gateway 1: (1525m, 525m)
   - Gateway 2: (225m, 675m)

2. Instalar postes/estructuras (3-5m altura)

3. Montar gateways y antenas

4. Configurar parametros LoRa

5. Conectar uplink a internet

6. Test de alcance con sensor movil

### Fase 2: Instalacion de Sensores (153 unidades)

1. Marcar grid de 120m con GPS/estacas

2. Instalar sensores a 20-30cm profundidad

3. Programar Device ID y gateway asignado

4. Verificar transmision exitosa

5. Registrar ubicacion en base de datos

### Fase 3: Puesta en Marcha

1. Verificar recepcion de todos los sensores

2. Calibrar umbrales segun tipo de suelo

3. Configurar dashboard y alarmas

4. Entrenar personal

5. Documentar y crear plan de mantenimiento

## Personalizacion

### Ajustar Obstruccion

Para campos con mas o menos obstrucciones:

```json
"escenario": {
  "porcentaje_area_obstruida": 50  // Aumentar para mas casas/arboles
}
```

### Cambiar Potencia LoRa

Para mayor alcance:

```json
"propagacion": {
  "potencia_tx_dbm": 20,           // Aumentar potencia (max ~20 dBm)
  "margen_desvanecimiento_db": 5   // Reducir margen (mas agresivo)
}
```

### Modificar Densidad de Sensores

Editar `scripts/humidity_sensor_deployment.py`:

```python
# Linea ~75-95: Seleccionar otra estrategia
estrategia_seleccionada = estrategia_alta   # Alta precision (1 sensor/ha)
# estrategia_seleccionada = estrategia_media # Media (0.67 sensor/ha)
# estrategia_seleccionada = estrategia_baja  # Basica (0.5 sensor/ha)
```

### Ajustar Discretizacion

Para campos mas pequenos o mayor precision:

```json
"discretizacion": {
  "celda_x_m": 30,  // Celdas mas pequenas = mas precision
  "celda_y_m": 30   // Pero aumenta tiempo de computo
}
```

**Guia de tamano de celda:**
- Campo pequeno (< 20 ha): 20m x 20m
- Campo mediano (20-100 ha): 30m x 30m
- Campo grande (100-300 ha): 50m x 50m
- Campo muy grande (> 300 ha): 60m x 60m o dividir en sectores

## Resultados Obtenidos

### Gateways LoRa

```
N_optimo = 2 gateways
Tiempo de resolucion: 5.98 segundos
Cobertura RF: 100% del campo
Densidad: 0.01 gateways/hectarea

Coordenadas:
  Gateway 1: (1525.0, 525.0) m
  Gateway 2: (225.0, 675.0) m
```

### Sensores de Humedad

```
Total sensores: 153 unidades
Densidad: 0.67 sensores/hectarea
Espaciado: 120 m
Estrategia: Precision Media

Asignaciones:
  Gateway 1: 87 sensores
  Gateway 2: 62 sensores
  Fuera de rango: 4 sensores (ajuste menor requerido)
```

### Metricas del Sistema

- **Cobertura agronomica:** 1 sensor cada 1.5 ha
- **Autonomia sensores:** >1 ano con sleep mode
- **Frecuencia muestreo:** Cada 30-60 minutos
- **Latencia datos:** <5 minutos (sensor → cloud)
- **Escalabilidad:** Facil agregar mas sensores

## Solucion de Problemas

### Error: "No module named 'pulp'"

```bash
pip install pulp numpy matplotlib
```

### Solver muy lento

- Instalar CBC solver (ver seccion Instalacion)
- Aumentar tamano de celda (50m → 60m)
- Reducir area o dividir en sectores

### Sensores fuera de rango

Si muchos sensores quedan fuera del rango de 750m:

1. Aumentar potencia TX a 20 dBm en `config.json`
2. Usar Spreading Factor mas alto (SF10-12)
3. Reducir margen de desvanecimiento a 5 dB
4. Considerar agregar un tercer gateway

### Puntos sin cobertura RF

Si el modelo indica "puntos sin cobertura":

- Aumentar `potencia_tx_dbm` (ej: 20 dBm)
- Reducir `margen_desvanecimiento_db` (ej: 5 dB)
- Verificar parametros de propagacion

### Memoria insuficiente

Para campos muy grandes (>500 ha):

- Aumentar tamano de celda (80m o 100m)
- Dividir campo en 2-4 sectores
- Procesar cada sector independientemente

## Archivos Generados

### Visualizaciones

- `results/visualizations/distribucion_sensores_pathloss.png`
  - Mapa de gateways LoRa con circulos de cobertura
  - Campo abierto vs. zona obstruida

- `results/visualizations/two_tier_architecture.png`
  - Sistema completo: gateways + sensores
  - Asignaciones por colores
  - Zonas de cobertura

### Reportes

- `results/reports/reporte_optimizacion.txt`
  - Analisis tecnico completo
  - Parametros del modelo path-loss
  - Metricas de cobertura RF
  - Estadisticas de enlaces

- `results/reports/deployment_guide.txt`
  - Guia paso a paso de instalacion
  - Especificaciones de hardware
  - Protocolo de deployment
  - Asignaciones sensor → gateway
  - Estimacion de costos detallada

## Limitaciones y Consideraciones

### Modelo de Propagacion

- Simplificacion log-distance (no multitrayecto complejo)
- Obstruccion modelada probabilisticamente
- Terreno asumido plano (no considera topografia)

### Simplificaciones

- Cobertura circular isotropica (antenas omnidireccionales)
- Ubicaciones discretas en grid regular
- No considera interferencia entre gateways

### Recomendaciones para Implementacion Real

1. **Validar con mediciones en campo**
   - Realizar site survey con analizador de espectro
   - Medir RSSI real en puntos clave

2. **Ajustar parametros**
   - Calibrar exponentes n segun mediciones
   - Considerar margenes adicionales (15-20 dB)

3. **Considerar topografia**
   - Usar modelo DEM si hay desnivel significativo
   - Ajustar alturas de instalacion segun terreno

4. **Planificar mantenimiento**
   - Programa de cambio de baterias
   - Limpieza de paneles solares
   - Verificacion periodica de conectividad

## Referencias

- [PuLP Documentation](https://coin-or.github.io/pulp/)
- [Set Cover Problem - Wikipedia](https://en.wikipedia.org/wiki/Set_cover_problem)
- [LoRa Path Loss Models](https://ieeexplore.ieee.org/document/8030482)
- [Log-Distance Path Loss Model](https://en.wikipedia.org/wiki/Log-distance_path_loss_model)
- [LoRaWAN Specification](https://lora-alliance.org/resource_hub/lorawan-specification-v1-1/)

## Licencia

Este proyecto esta disponible para uso academico y de investigacion.

## Autor

Proyecto de optimizacion para aplicaciones agricolas IoT con:
- Modelo de propagacion path-loss realista
- Set Cover Problem mediante PLE
- Two-tier architecture (Gateways + Sensores)

## Contribuciones

Las contribuciones son bienvenidas:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Contacto y Soporte

Para preguntas o problemas:
- Revisa la seccion "Solucion de Problemas"
- Consulta los reportes generados en `results/reports/`
- Verifica configuracion en `config.json`

---

**Proyecto desarrollado para optimizacion de sistemas IoT agricolas con LoRa**

**Version:** 2.0 (Two-Tier Architecture)

**Ultima actualizacion:** 2025-11-14
