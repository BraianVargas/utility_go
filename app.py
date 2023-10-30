import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

from data.sybase_connect import *
from modules.token import *
from modules.usuarios import *


app = Flask(__name__)

# ------------------------------------------------------------
#            REGISTRO DE BLUEPRINTS 
# ------------------------------------------------------------
# _dbConnection = connectSybase()

CORS(app)
app.register_blueprint(tokenBP, url_prefix='/token')
app.register_blueprint(usuariosBP, url_prefix='/usuarios')

app.config['CORS_HEADERS'] = 'Content-Type'


if __name__ =='__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")