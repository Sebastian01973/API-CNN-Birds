# -*- coding: utf-8 -*-
"""Test_CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qE_R7UoiDw5w6tPCMs4zC1RRd-wGTSSg

## Clasificador de imagenes
"""

# !pip install opendatasets

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
import seaborn as sns
import random
from tqdm import tqdm 
import cv2
import os

from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D,Dropout,Flatten, Dense, Activation, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping,ReduceLROnPlateau
import keras_tuner as kt
from tensorflow import keras

import opendatasets as od
od.download("https://www.kaggle.com/datasets/gpiosenka/100-bird-species")

class_names= ['AFRICAN EMERALD CUCKOO',
 'AFRICAN OYSTER CATCHER',
 'AMERICAN COOT',
 'AMERICAN KESTREL',
 'ANDEAN SISKIN',
 'ANHINGA',
 'APAPANE',
 'APOSTLEBIRD',
 'ASIAN CRESTED IBIS',
 'AUSTRAL CANASTERO',
 ]
class_names_label={class_names:i for i, class_names in enumerate(class_names)}

# path_actual = os.getcwd()
# ruta = f'{path_actual}/dataset/valid'

# import shutil
# for nombre_carpeta in os.listdir(ruta):
#     ruta_carpeta = os.path.join(ruta, nombre_carpeta)
#     if nombre_carpeta not in class_names:
#         # Eliminar la carpeta y su contenido
#         shutil.rmtree(ruta_carpeta)

FAST_RUN =False
IMAGE_WIDTH=224
IMAGE_HEIGHT=224
IMAGE_SIZE=(IMAGE_WIDTH,IMAGE_HEIGHT)
IMAGE_CHANNELS=3  #3 para imagenes con color y 1 para blanco y negro
BATCH_SIZE=32
EPOCHS=20 #Maximo 20 empezar en 5
if FAST_RUN:
  EPOCHS=5

"""## Cargar el Dataset"""

def load_data():
  datasets=["/content/dataset/train",
            "/content/dataset/valid",
            "/content/dataset/test"]
  output=[]

  for dataset in datasets:

    images=[]
    labels=[]
    print("Loading {}".format(dataset))

    for folder in os.listdir(dataset):
      label = class_names_label[folder]
      for file in tqdm(os.listdir(os.path.join(dataset,folder))):
        img_path = os.path.join(os.path.join(dataset,folder),file)
        image = cv2.imread(img_path,cv2.IMREAD_COLOR)
        if image is None:
          continue
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        image = cv2.resize(image,IMAGE_SIZE)
        images.append(image)
        labels.append(label)
    images = np.array(images)
    labels = np.array(labels)
    output.append((images,labels))
  return output

"""## Generador de imágenes (entrenamiento y validación)"""

(train_images,train_labels),(val_images,val_labels),(test_images,test_labels)=load_data()

print(train_images.shape)
print(train_labels.shape)
print(val_images.shape)
print(val_labels.shape)
print(test_images.shape)
print(test_labels.shape)

"""## Mostrar las imagenes"""

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(14,10))
for n in range(1,31):
  fig.add_subplot(5, 6, n)
  img = train_images[n]
  plt.imshow(img)
  plt.title(class_names[train_labels[n]])
  plt.axis('off')

from tensorflow.keras.utils import to_categorical
train_labels=to_categorical(train_labels,0)
val_labels=to_categorical(val_labels,0)
test_labels=to_categorical(test_labels,0)

train_labels[100:1005]

train_images, train_labels = shuffle(train_images,train_labels,random_state=42)
val_images, val_labels = shuffle(val_images, val_labels, random_state=42)
test_images, test_labels = shuffle(test_images, test_labels, random_state=42)

path_actual = os.getcwd()
train_dir = f'{path_actual}/dataset/train'
test_dir = f'{path_actual}/dataset/test'

train_datagen = ImageDataGenerator(
    rescale=1./255,
    # rotation_range=15,
    # shear_range=0.1,
    # zoom_range=0.2,
    # horizontal_flip=True,
    # width_shift_range=0.1,
    # height_shift_range=0.1
)

test_datagen = ImageDataGenerator(rescale=1/255.)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    batch_size=BATCH_SIZE,
    target_size=(224, 224), 
    class_mode="categorical",
    seed=42
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    batch_size=BATCH_SIZE,
    target_size=(224, 224), 
    class_mode="categorical",
    seed=42
)

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(14,10))
for n in range(1,31):
  fig.add_subplot(5, 6, n)
  img = train_images[n]
  
  plt.imshow(img)
  plt.axis('off')

"""## Creando el modelo de redes convolucionales"""

model = Sequential()

# Convolution layers

model.add(Conv2D(32,(3, 3),input_shape=(IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D((2,2)))

model.add(Conv2D(64,(3, 3)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(128, (3, 3)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D((2, 2)))


model.add(Conv2D(256, (3, 3)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D((2, 2)))


model.add(Flatten())
model.add(Dropout(0.5))

model.add(Dense(10))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.2))

model.add(Dense(10))
model.add(BatchNormalization())
model.add(Activation('softmax'))


# Compile the model
model.compile(loss = "categorical_crossentropy",
                optimizer = "adam",
                metrics = ["accuracy"])

#Early stopping
callback = EarlyStopping(monitor='val_loss', patience=3, verbose=1, restore_best_weights=True)

"""## Entrenar el model"""

history = model.fit(train_generator, epochs=100, callbacks=[callback], validation_data = test_generator)

"""## Probar el modelo"""

model.evaluate(test_generator)

"""### Guardar el modelo entrenado"""

model.save(os.path.join('models','newImage.h5'))

"""### Observar las predicciones"""

y_pred = model.predict(test_generator)
y_pred[:5]

y_pred = y_pred.argmax(axis=1)
y_pred[:5]

"""## Gráficas de entrenamiento y validación (accuracy - loss)"""

def plotTraining(hist, epochs, typeData):
    
    if typeData=="loss":
        plt.figure(1,figsize=(10,5))
        yc=hist.history['loss']
        xc=range(epochs)
        plt.ylabel('Loss', fontsize=24)
        plt.plot(xc,yc,'-r',label='Loss Training')
    if typeData=="accuracy":
        plt.figure(2,figsize=(10,5))
        yc=hist.history['accuracy']
        for i in range(0, len(yc)):
            yc[i]=100*yc[i]
        xc=range(epochs)
        plt.ylabel('Accuracy (%)', fontsize=24)
        plt.plot(xc,yc,'-r',label='Accuracy Training')
    if typeData=="val_loss":
        plt.figure(1,figsize=(10,5))
        yc=hist.history['val_loss']
        xc=range(epochs)
        plt.ylabel('Loss', fontsize=24)
        plt.plot(xc,yc,'--b',label='Loss Validate')
    if typeData=="val_accuracy":
        plt.figure(2,figsize=(10,5))
        yc=hist.history['val_accuracy']
        for i in range(0, len(yc)):
            yc[i]=100*yc[i]
        xc=range(epochs)
        plt.ylabel('Accuracy (%)', fontsize=24)
        plt.plot(xc,yc,'--b',label='Training Validate')
        

    plt.rc('xtick',labelsize=24)
    plt.rc('ytick',labelsize=24)
    plt.rc('legend', fontsize=18) 
    plt.legend()
    plt.xlabel('Number of Epochs',fontsize=24)
    plt.grid(True)

plotTraining(history,10,"loss")
plotTraining(history,10,"accuracy")
plotTraining(history,10,"val_loss")
plotTraining(history,10,"val_accuracy")

"""## Prueba del modelo cargando una imagen"""

from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.utils import np_utils
from tensorflow.keras.models import load_model # type: ignore

names= ['AFRICAN EMERALD CUCKOO',
 'AFRICAN OYSTER CATCHER',
 'AMERICAN COOT',
 'AMERICAN KESTREL',
 'ANDEAN SISKIN',
 'ANHINGA',
 'APAPANE',
 'APOSTLEBIRD',
 'ASIAN CRESTED IBIS',
 'AUSTRAL CANASTERO',
 ]

modelt = load_model("/content/models/newImage.h5",
                    custom_objects={'KerasLayer':hub.KerasLayer})
#modelt = custom_vgg_model

imaget_path = "/content/dataset/valid/ASIAN CRESTED IBIS/4.jpg"
imaget=cv2.resize(cv2.imread(imaget_path), (IMAGE_WIDTH, IMAGE_HEIGHT), interpolation = cv2.INTER_AREA)
xt = np.asarray(imaget)
xt=preprocess_input(xt)
xt = np.expand_dims(xt,axis=0)
preds = modelt.predict(xt)

print(names[np.argmax(preds)])
plt.imshow(cv2.cvtColor(np.asarray(imaget),cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()