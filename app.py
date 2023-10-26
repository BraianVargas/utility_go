import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

from modules.auth import *
from modules.registro_usuarios import *


app = Flask(__name__)

# ------------------------------------------------------------
#            REGISTRO DE BLUEPRINTS 
# ------------------------------------------------------------

app.register_blueprint(authBP, url_prefix='/auth')


app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app)