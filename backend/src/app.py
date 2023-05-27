from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Server Run!'})
  


if __name__ == '__main__':
    app.run(debug=True, port=5000)   