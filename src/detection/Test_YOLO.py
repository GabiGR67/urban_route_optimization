import os
import cv2
import numpy as np
from ultralytics import YOLO

# Rutas
MODEL_PATH = r'C:\Users\Usuario\Desktop\urban_route_optimization\runs\segment\train\weights\best.pt'
IMG_DIR = r'C:\Users\Usuario\Desktop\urban_route_optimization\dataset\test\images'
LABEL_DIR = r'C:\Users\Usuario\Desktop\urban_route_optimization\dataset\test\labels'

# Cargar modelo
model = YOLO(MODEL_PATH)

# Colores
COLOR_GT = (0, 255, 0)       # Verde para ground truth
COLOR_PRED = (0, 0, 255)     # Rojo para predicción

# Iterar sobre imágenes
for img_file in os.listdir(IMG_DIR):
    if not img_file.lower().endswith(('.jpg', '.png', '.jpeg')):
        continue

    img_path = os.path.join(IMG_DIR, img_file)
    label_path = os.path.join(LABEL_DIR, os.path.splitext(img_file)[0] + '.txt')

    img = cv2.imread(img_path)
    if img is None:
        continue
    h, w = img.shape[:2]

    # Dibujar ground truth
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            for line in f:
                parts = list(map(float, line.strip().split()))
                cls = int(parts[0])
                if len(parts[1:]) % 2 != 0:
                    continue
                points = np.array(parts[1:], dtype=np.float32).reshape(-1, 2)
                abs_points = (points * np.array([[w, h]])).astype(int)
                cv2.polylines(img, [abs_points], isClosed=True, color=COLOR_GT, thickness=2)

    # Predicción
    results = model(img_path)[0]
    if results.masks is not None:
        for seg in results.masks.xy:
            cv2.polylines(img, [np.array(seg, dtype=np.int32)], isClosed=True, color=COLOR_PRED, thickness=2)

    # Redimensionar imagen si es necesario
    max_width = 900
    if img.shape[1] > max_width:
        scale = max_width / img.shape[1]
        new_size = (max_width, int(img.shape[0] * scale))
        img = cv2.resize(img, new_size)

    # Mostrar imagen
    cv2.imshow('Predicción vs Ground Truth', img)
    key = cv2.waitKey(0)
    if key == 27:  # ESC
        print("Proceso interrumpido por el usuario.")
        break

cv2.destroyAllWindows()
