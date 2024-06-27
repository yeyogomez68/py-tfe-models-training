import numpy as np
from tensorflow.keras.applications import ResNet152V2, VGG16, DenseNet121, EfficientNetB7
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
#from keras.optimizers import Adam
from tensorflow.keras.optimizers import Adam, SGD, RMSprop, Adagrad
import matplotlib.pyplot as plt

models = [ResNet152V2, VGG16, DenseNet121, EfficientNetB7]
model_names = ['ResNet152V2', 'VGG16', 'DenseNet121', 'EfficientNetB7']

models = [ResNet152V2, VGG16, DenseNet121]
model_names = ['ResNet152V2', 'VGG16', 'DenseNet121']

colors = ['b', 'g', 'r', 'c']

# Almacena las métricas de todos los modelos
all_accuracy = [[] for _ in range(len(models))]
all_val_accuracy = [[] for _ in range(len(models))]
all_loss = [[] for _ in range(len(models))]
all_val_loss = [[] for _ in range(len(models))]

batch_size = 32

for i, model_func in enumerate(models):
    # Carga la arquitectura del modelo con pesos preentrenados en ImageNet
    base_model = model_func(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

    # Congela las capas del modelo base para no entrenarlas
    for layer in base_model.layers:
        layer.trainable = False

    # Añade nuevas capas al final del modelo
    model = Sequential([
        base_model,
        Flatten(),
        Dense(7, activation='softmax')  # Asume que hay 7 tipos diferentes de árboles/plantas
    ])

    # Compila el modelo
    model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

    # Genera datos de entrenamiento, validacion y pruebas a partir de las imágenes en la carpeta 'dataset'
    train_datagen = ImageDataGenerator(rescale=1./255, rotation_range=20)
    train_generator = train_datagen.flow_from_directory('dataset/train', target_size=(224, 224), batch_size=batch_size, class_mode='categorical')

    validation_datagen = ImageDataGenerator(rescale=1./255)
    validation_generator = validation_datagen.flow_from_directory('dataset/train', target_size=(224, 224), batch_size=batch_size, class_mode='categorical')

    test_datagen = ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_directory('dataset/test', target_size=(224, 224), batch_size=batch_size, class_mode='categorical')

    # Entrena el modelo
    history = model.fit(
        train_generator,
        validation_data=validation_generator,
        epochs=3
    )

    # Almacena las métricas por epoch
    all_accuracy[i] = history.history['accuracy']
    all_val_accuracy[i] = history.history['val_accuracy']
    all_loss[i] = history.history['loss']
    all_val_loss[i] = history.history['val_loss']

    #save model
    model.save(f'{model_names[i]}.keras')

# Grafica la precisión de entrenamiento y validación de todos los modelos
plt.figure()
for i in range(len(models)):
    epochs = range(len(all_accuracy[i]))
    plt.plot(epochs, all_accuracy[i], colors[i], label=f'Training accuracy for {model_names[i]}')
    plt.plot(epochs, all_val_accuracy[i], colors[i], linestyle='--', label=f'Validation accuracy for {model_names[i]}')
plt.title('Training and validation accuracy for all models')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Grafica la pérdida de entrenamiento y validación de todos los modelos
plt.figure()
for i in range(len(models)):
    epochs = range(len(all_loss[i]))
    plt.plot(epochs, all_loss[i], colors[i], label=f'Training loss for {model_names[i]}')
    plt.plot(epochs, all_val_loss[i], colors[i], linestyle='--', label=f'Validation loss for {model_names[i]}')
plt.title('Training and validation loss for all models')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

print(history.history.keys())