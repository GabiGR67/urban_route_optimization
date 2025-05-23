# Optimización de Rutas Urbanas Basada en Visión Artificial

Este proyecto forma parte del Trabajo Fin de Máster (TFM) del Máster en Inteligencia Artificial de la Universidad Internacional de La Rioja (UNIR). El objetivo es desarrollar un sistema inteligente capaz de detectar señales de tráfico urbanas mediante visión por computador y utilizar esta información para calcular rutas óptimas, considerando no solo la distancia sino también restricciones viales como semáforos y señales de stop o ceda el paso.

---

## Objetivos del Proyecto

- Detectar señales de tráfico relevantes a partir de imágenes capturadas.
- Construir un grafo vial que represente calles e intersecciones.
- Asignar penalizaciones dinámicas a tramos del grafo en función de las señales detectadas.
- Calcular rutas óptimas mediante algoritmos clásicos (A*, Dijkstra), adaptados al entorno urbano real.

---

##  Estructura del Proyecto

```bash
urban_route_optimization/
├── data/                      # Datos crudos y procesados
│   ├── raw/                   # Imágenes originales
│   ├── processed/             # Recortes de señales
│   ├── graph_data/            # Mapas o grafos exportados
│   └── results/               # Salidas de rutas y evaluaciones
│
├── models/
│   ├── yolo/                  # Modelo YOLO entrenado (best.pt)
│   └── checkpoints/           # (opcional) Pesos intermedios
│
├── notebooks/                 # Exploraciones, pruebas y validaciones
│   ├── 01_signal_detection.ipynb
│   ├── 02_graph_building.ipynb
│   └── 03_path_planning.ipynb
│
├── src/                       # Código fuente organizado por módulos
│   ├── detection/             # Detección de señales con YOLO
│   ├── preprocessing/         # Mejora y segmentación de imágenes
│   ├── graph/                 # Construcción del grafo vial
│   ├── routing/               # Algoritmo de rutas
│   └── config.py              # Configuración global del proyecto
│
├── main.py                    # Ejecución del pipeline completo
├── requirements.txt           # Dependencias necesarias
└── README.md                  # Este archivo

```

---

## Instalación

1. Clona el repositorio
```bash
git clone https://github.com/tu_usuario/urban_route_optimization.git
cd urban_route_optimization


2. Crea un entorno virtual
python3.10 -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate.bat     # Windows

3. Instala las dependencias
pip install -r requirements.txt
```

Coloca tu modelo YOLO entrenado en la siguiente ruta:

```bash
models/yolo/best.pt
Puedes entrenarlo tú mismo con Ultralytics YOLO o usar uno descargado desde Roboflow Universe.
```

Para ejecutar el sistema completo:

```bash
python main.py
```

También puedes trabajar por módulos accediendo a los notebooks en la carpeta notebooks/.

## Resultados Esperados

- Visualización de señales detectadas en imágenes urbanas.

- Construcción de grafo urbano con penalizaciones dinámicas.

- Comparativa entre rutas optimizadas vs. rutas estándar (distancia, tiempo, número de paradas).

- Posible integración futura con sistemas de navegación reales o simulados.

## Créditos

- **Autores:** Gabriel Gállego Grau, Marcos Caballero Cortes, Keila Gomez Rodriguez
- **Universidad:** Universidad Internacional de La Rioja (UNIR)
- **Máster:** Máster en Inteligencia Artificial
- **Año:** 2025
- **Asesor:** Ainhoa García Sánchez

## Licencia

Este proyecto está bajo la Licencia MIT. El uso comercial requiere autorización expresa del autor.
