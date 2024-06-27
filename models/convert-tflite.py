import tensorflow as tf
from tensorflow.keras.models import load_model
import tensorflow as tf
import glob

# Obtén la lista de archivos .keras en el directorio actual
keras_files = glob.glob('/Volumes/Bodega/Proyectos/github/py-tfe/models/*.keras')

for keras_file in keras_files:
    # Carga el modelo Keras
    model = load_model(keras_file)

    # Convierte el modelo
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    # Guarda el modelo
    tflite_file = keras_file.replace('.keras', '.tflite')
    with open(tflite_file, 'wb') as f:
        f.write(tflite_model)
