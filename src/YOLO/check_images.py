import cv2
import os

# Configuración
base_dir = r'C:\Users\Usuario\Desktop\urban_route_optimization\dataset'
split = 'valid'
images_dir = os.path.join(base_dir, split, 'images')
labels_dir = os.path.join(base_dir, split, 'labels')

# Diccionario de clases
class_names = {
    '0': 'Semáforo',
    '1': 'Stop'
}

# Función para convertir de coordenadas YOLO a (x1, y1, x2, y2)
def yolo_to_pixel_coords(x_c, y_c, w, h, img_w, img_h):
    x1 = int((x_c - w / 2) * img_w)
    y1 = int((y_c - h / 2) * img_h)
    x2 = int((x_c + w / 2) * img_w)
    y2 = int((y_c + h / 2) * img_h)
    return x1, y1, x2, y2

# Mostrar imagen redimensionada con sus labels
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
                if len(partes) != 5:
                    continue

                clase, x, y, w, h = partes
                x, y, w, h = float(x), float(y), float(w), float(h)
                x1, y1, x2, y2 = yolo_to_pixel_coords(x, y, w, h, w_img, h_img)

                color = (0, 255, 0) if clase == '0' else (0, 0, 255)
                etiqueta = class_names.get(clase, 'Clase desconocida')

                cv2.rectangle(imagen, (x1, y1), (x2, y2), color, 2)
                cv2.putText(imagen, etiqueta, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    max_width = 800
    if imagen.shape[1] > max_width:
        scale = max_width / imagen.shape[1]
        new_size = (int(imagen.shape[1] * scale), int(imagen.shape[0] * scale))
        imagen = cv2.resize(imagen, new_size)

    cv2.imshow('Imagen con etiquetas', imagen)
    print(f"Mostrando: {nombre_imagen} (presiona una tecla para continuar, ESC para salir)")

    key = cv2.waitKey(0)
    cv2.destroyAllWindows()

    if key == 27:  # Tecla ESC
        return False
    return True

# Mostrar todas las imágenes del conjunto
for archivo in sorted(os.listdir(images_dir)):
    if archivo.endswith('.jpg'):
        continuar = mostrar_imagen(archivo)
        if not continuar:
            break
