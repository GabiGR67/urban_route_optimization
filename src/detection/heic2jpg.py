import os
from pillow_heif import register_heif_opener
from PIL import Image
import piexif

# 🗂 Cambia estas rutas según tus carpetas
ORIGEN = r"C:\Users\Usuario\Downloads\Imagenes3"
DESTINO = r"C:\Users\Usuario\Downloads\Imagenes_jpg"

# 🔧 Crear carpeta de destino si no existe
os.makedirs(DESTINO, exist_ok=True)

# 📦 Registrar compatibilidad HEIC
register_heif_opener()

# 🚀 Convertir todos los .heic a .jpg
for archivo in os.listdir(ORIGEN):
    if archivo.lower().endswith(".heic"):
        ruta_origen = os.path.join(ORIGEN, archivo)
        nombre_sin_ext = os.path.splitext(archivo)[0]
        ruta_destino = os.path.join(DESTINO, f"{nombre_sin_ext}.jpg")

        print(f"Procesando: {archivo}...")

        # Abrir imagen HEIC
        imagen = Image.open(ruta_origen)

        # Extraer metadatos EXIF (si los tiene)
        exif_bytes = imagen.info.get("exif")

        # Guardar como JPG con metadatos
        if exif_bytes:
            imagen.save(ruta_destino, "JPEG", exif=exif_bytes)
        else:
            imagen.save(ruta_destino, "JPEG")

print("✅ Conversión completada sin perder metadatos.")
