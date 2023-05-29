import os
import numpy as np
import cv2
# Import Flask
from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
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
CORS(app, supports_credentials=True)

path_actual = os.path.dirname(os.path.abspath(__file__))
model = load_model(f"{path_actual}/models/model.h5")
print('Modelo cargado exitosamente.')


# Realizamos la predicción usando la imagen cargada y el modelo
def model_predict(img_path, model):
    img = cv2.resize(cv2.imread(img_path), (width_shape,
                     height_shape), interpolation=cv2.INTER_AREA)
    x = np.asarray(img)
    x = preprocess_input(x)
    x = np.expand_dims(x, axis=0)

    preds = model.predict(x)
    return preds


### ENDPOINTS ###
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Server Run!'})


@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello World!'})


@cross_origin
@app.route('/upload', methods=['POST'])
def load_image(): 
    data = request.files['image']
    
    # Graba el archivo en ./uploads
    basepath = os.path.dirname(__file__)

    file_path = os.path.join(
        basepath, 'uploads', secure_filename(data.filename))
    data.save(file_path)

    # Predicción
    preds = model_predict(file_path, model)
    result = str(names[np.argmax(preds)])

    return jsonify({'result': result})
    


@app.route('/clean_uploads', methods=['GET'])
def clean():
    # Elimina los archivos de ./uploads
    # Falta probarlo en el servidor
    basepath = os.path.dirname(__file__)
    file_path = os.path.join(basepath, 'uploads')
    for file in os.listdir(file_path):
        os.remove(os.path.join(file_path, file))

    return jsonify({'message': 'Clean Uploads!'}), 200


def create_app():
    return app


if __name__ == '__main__':
    port = os.getenv('PORT')
    if(port == None):
        print("Error on $PORT env variable")
    else:
        app.run(host="0.0.0.0", port=int(port), debug=True)
