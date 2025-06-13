import cv2
import os
import numpy as np

# Configuración
base_dir = r'C:\Users\Usuario\Desktop\urban_route_optimization\dataset'
split = 'test'  # Cambia a 'valid' o 'test' si quieres
images_dir = os.path.join(base_dir, split, 'images')
labels_dir = os.path.join(base_dir, split, 'labels')

class_names = {
    '0': 'Stop sign',
    '1': 'Traffic light'
}

def yolo_bbox_to_pixels(x_c, y_c, w, h, img_w, img_h):
    x1 = int((x_c - w / 2) * img_w)
    y1 = int((y_c - h / 2) * img_h)
    x2 = int((x_c + w / 2) * img_w)
    y2 = int((y_c + h / 2) * img_h)
    return x1, y1, x2, y2

def normalizados_a_pixeles(puntos, img_w, img_h):
    coords = []
    for i in range(0, len(puntos), 2):
        x = int(float(puntos[i]) * img_w)
        y = int(float(puntos[i + 1]) * img_h)
        coords.append([x, y])
    return np.array(coords, dtype=np.int32)

def mostrar_imagen(nombre_imagen):
    ruta_imagen = os.path.join(images_dir, nombre_imagen)
    ruta_label = os.path.join(labels_dir, nombre_imagen.replace('.jpg', '.txt'))

    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print(f"No se pudo leer la imagen: {ruta_imagen}")
        return

    h_img, w_img = imagen.shape[:2]

    if os.path.exists(ruta_label):
        with open(ruta_label, 'r') as f:
            for linea in f:
                partes = linea.strip().split()
                if len(partes) < 5:
                    continue

                clase = partes[0]
                puntos = partes[1:]
                color = (0, 255, 0) if clase == '0' else (0, 0, 255)
                etiqueta = class_names.get(clase, 'Clase desconocida')

                if len(puntos) == 4:
                    # Bounding box
                    x_c, y_c, w, h = map(float, puntos)
                    x1, y1, x2, y2 = yolo_bbox_to_pixels(x_c, y_c, w, h, w_img, h_img)
                    cv2.rectangle(imagen, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(imagen, etiqueta, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                elif len(puntos) % 2 == 0:
                    # Polígono
                    coords = normalizados_a_pixeles(puntos, w_img, h_img)
                    cv2.polylines(imagen, [coords], isClosed=True, color=color, thickness=2)
                    x_text, y_text = coords[0]
                    cv2.putText(imagen, etiqueta, (x_text, y_text - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                else:
                    print(f"Línea inválida (número impar de coordenadas): {linea}")

    # Redimensionar si es muy grande
    max_width = 900
    if imagen.shape[1] > max_width:
        scale = max_width / imagen.shape[1]
        new_size = (int(imagen.shape[1] * scale), int(imagen.shape[0] * scale))
        imagen = cv2.resize(imagen, new_size)

    cv2.imshow('Imagen con anotaciones', imagen)
    print(f"Mostrando: {nombre_imagen} — Presiona una tecla para continuar, ESC para salir")

    key = cv2.waitKey(0)
    cv2.destroyAllWindows()

    if key == 27:  # ESC
        return False
    return True

for archivo in sorted(os.listdir(images_dir)):
    if archivo.endswith('.jpg'):
        continuar = mostrar_imagen(archivo)
        if not continuar:
            break