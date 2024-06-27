import os
from PIL import Image

# Define la carpeta de origen y destino
src_folder = 'dataset/firebase'
dst_folder = 'dataset/224'

# Define el tamaño del recorte
crop_size = (224, 224)

# Recorre todas las subcarpetas y archivos en la carpeta de origen
for subdir, dirs, files in os.walk(src_folder):
    for filename in files:
        if filename.endswith('.jpg') or filename.endswith('.png'):  # Asume que las imágenes son .jpg o .png
            # Crea la carpeta de destino correspondiente si no existe
            dst_subdir = subdir.replace(src_folder, dst_folder)
            os.makedirs(dst_subdir, exist_ok=True)
            
            # Abre la imagen
            img = Image.open(os.path.join(subdir, filename))
            
            # Obtiene las dimensiones de la imagen
            width, height = img.size            
            

            # Define el nuevo ancho
            new_width = 224
            # Calcula la nueva altura proporcionalmente
            new_height = int(height * new_width / width)
            # Redimensiona la imagen
            img_resized = img.resize((new_width, new_height))
            # Guarda la imagen redimensionada en la carpeta de destino correspondiente
            #img_resized.save(os.path.join(dst_subdir, f'{filename}_w224.jpg'))
            # Define el número de recortes
            num_crops = 4
            # Calcula el tamaño de los recortes
            # Define el tamaño de los recortes
            crop_size = 224            
            #iTops new_height/num_crops
            separador = new_height/num_crops
            separador = int(separador/4)
            iTops = [separador*0, separador*1, separador*2, separador*3, separador*4]            
            #replace < 0 with 0
            iTops = [0 if i < 0 else i for i in iTops]
            #order the list
            iTops.sort()
            # Recorre la imagen haciendo recortes
            for i in iTops:
                # Define las coordenadas del recorte
                box = (0, i, 224, i + 224)
                # Recorta la imagen
                img_cropped = img_resized.crop(box)
                # Guarda la imagen recortada en la carpeta de destino correspondiente
                img_cropped.save(os.path.join(dst_subdir, f'{filename}_w{i}.jpg'))
                

print('Todos los recortes de las imágenes han sido creados.')

#crea una carpeta dataset/train y dataset/test con 80% y 20% de las imagenes respectivamente
import os
import shutil
import random

# Define la carpeta de origen y destino
src_folder = 'dataset/224'
train_folder = 'dataset/train'
test_folder = 'dataset/test'

# Crea las carpetas de entrenamiento y prueba si no existen
os.makedirs(train_folder, exist_ok=True)
os.makedirs(test_folder, exist_ok=True)

# Recorre todas las subcarpetas y archivos en la carpeta de origen
for subdir, dirs, files in os.walk(src_folder):
    for filename in files:
        if filename.endswith('.jpg'):  # Asume que las imágenes son .jpg
            # Obtiene el nombre de la subcarpeta
            subfolder_name = os.path.basename(subdir)
            
            # Crea la carpeta de destino correspondiente si no existe
            if random.random() < 0.8:
                dst_folder = os.path.join(train_folder, subfolder_name)
            else:
                dst_folder = os.path.join(test_folder, subfolder_name)
            
            os.makedirs(dst_folder, exist_ok=True)
            
            # Copia la imagen a la carpeta de destino correspondiente
            shutil.copy(os.path.join(subdir, filename), os.path.join(dst_folder, filename))

print('Las imágenes han sido divididas en las carpetas de entrenamiento y prueba.')