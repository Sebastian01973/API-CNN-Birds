from flask import Flask,jsonify, request
from flask_cors import CORS


import os
import numpy as np
import cv2

# Keras
from keras.models import load_model
from keras.applications.imagenet_utils import preprocess_input

from werkzeug.utils import secure_filename


width_shape = 224
height_shape = 224
names = ['AFRICAN EMERALD CUCKOO', 'AFRICAN OYSTER CATCHER', 'AMERICAN COOT',
         'AMERICAN KESTREL', 'ANDEAN SISKIN', 'ANHINGA', 'APAPANE',
         'APOSTLEBIRD', 'ASIAN CRESTED IBIS', 'AUSTRAL CANASTERO',
         ]


app = Flask(__name__)
CORS(app)


path_actual = os.path.dirname(os.path.abspath(__file__))


model = load_model(f"{path_actual}/models/model.h5")

print('Modelo cargado exitosamente. Verificar en consola.')

# Realizamos la predicción usando la imagen cargada y el modelo
def model_predict(img_path, model):

    img=cv2.resize(cv2.imread(img_path), (width_shape, height_shape), interpolation = cv2.INTER_AREA)
    x=np.asarray(img)
    x=preprocess_input(x)
    x = np.expand_dims(x,axis=0)
    
    preds = model.predict(x)
    return preds

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Obtiene el archivo del request
        f = request.files['file']

        # Graba el archivo en ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Predicción
        preds = model_predict(file_path, model)

        print('PREDICCIÓN', names[np.argmax(preds)])
        
        # Enviamos el resultado de la predicción
        result = str(names[np.argmax(preds)])              
        return result
    return None

### ENDPOINTS ###

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Server Run!'})
  



if __name__ == '__main__':
    app.run(debug=True, port=5000)   