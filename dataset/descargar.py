import os
import re
from firebase_admin import credentials, initialize_app, storage

# Inicializa Firebase con tus credenciales
cred = credentials.Certificate('tfm-admin-bf396-firebase-adminsdk-cyiz5-a22e476635.json')
app = initialize_app(cred, {'storageBucket': 'gs://tfm-admin-bf396.appspot.com'})

# Descarga las imágenes de la carpeta "Buganbil, veranera"
bucket = storage.bucket('tfm-admin-bf396.appspot.com', app=app)
blobs = bucket.list_blobs()
for blob in blobs:
    # Extrae la estructura de carpetas del nombre de archivo
    folder_structure = os.path.dirname(blob.name)

    # Crea las carpetas necesarias si no existen
    try:
        os.makedirs(os.path.join('firebase', folder_structure), exist_ok=True)
    except OSError as e:
        if e.errno != os.errno.EEXIST:  # Ignore "file already exists" errors
            print(f"Error creando directorio: {e}")
        continue

    # Sanitiza el nombre de archivo para Windows
    invalid_chars = r"[\\/*:\?\"<>]"
    sanitized_filename = re.sub(invalid_chars, "_", blob.name)

    # Descarga el archivo a la carpeta correspondiente
    download_path = os.path.join('firebase', folder_structure, sanitized_filename)
    blob.download_to_filename(download_path)
    print(f"Descargada {download_path}")

# Función para sanitizar el nombre de archivo
def sanitize_filename(filename):
    # Replace invalid characters with underscores
    invalid_chars = r"[\\/*:\?\"<>]"
    filename = re.sub(invalid_chars, "_", filename)
    return filename
