from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model

import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

print("Cargo Dependencias")

width_shape = 224
height_shape = 224

names = ['AFRICAN EMERALD CUCKOO', 'AFRICAN OYSTER CATCHER', 'AMERICAN COOT',
         'AMERICAN KESTREL', 'ANDEAN SISKIN', 'ANHINGA', 'APAPANE',
         'APOSTLEBIRD', 'ASIAN CRESTED IBIS', 'AUSTRAL CANASTERO',
         ]

path_actual = os.path.dirname(os.path.abspath(__file__))
print(path_actual)

modelt = load_model(f"{path_actual}/models/model.h5")

print("Modelo cargado exitosamente")

imaget_path = f"{path_actual}/tests/imageTest.jpg"

imaget = cv2.resize(cv2.imread(imaget_path), (width_shape,
                    height_shape), interpolation=cv2.INTER_AREA)

xt = np.asarray(imaget)
xt = preprocess_input(xt)
xt = np.expand_dims(xt, axis=0)


print("Predicción")
preds = modelt.predict(xt)

print("Predicción:", names[np.argmax(preds)])
plt.imshow(cv2.cvtColor(np.asarray(imaget), cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
