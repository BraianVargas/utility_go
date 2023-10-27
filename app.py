import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

from data.sybase_connect import *
from modules.auth import *
from modules.usuarios import *


app = Flask(__name__)

# ------------------------------------------------------------
#            REGISTRO DE BLUEPRINTS 
# ------------------------------------------------------------
_dbConnection = connectSybase()

app.register_blueprint(authBP, url_prefix='/auth')
app.register_blueprint(usuariosBP, url_prefix='/usuarios')


app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app)