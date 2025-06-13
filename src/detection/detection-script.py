import os

def es_linea_de_deteccion(linea):
    return len(linea.strip().split()) == 5

def buscar_txt_con_deteccion(carpeta_labels):
    archivos_con_deteccion = []

    for archivo in os.listdir(carpeta_labels):
        if archivo.endswith('.txt'):
            ruta = os.path.join(carpeta_labels, archivo)
            with open(ruta, 'r') as f:
                lineas = f.readlines()
                for linea in lineas:
                    if es_linea_de_deteccion(linea):
                        archivos_con_deteccion.append(archivo)
                        break  # basta con una línea para marcarlo

    return archivos_con_deteccion

# Cambia esta ruta según tu estructura
ruta_labels = r'C:\Users\Usuario\Desktop\urban_route_optimization\dataset\test\labels'
resultados = buscar_txt_con_deteccion(ruta_labels)

print("Archivos que contienen al menos una detección (no segmentación):")
for archivo in resultados:
    print(archivo)
