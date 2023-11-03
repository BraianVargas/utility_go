import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

from data.sybase_connect import *
from modules.token import *
from modules.usuarios import *
from modules.emails import *


app = Flask(__name__)

# ------------------------------------------------------------
#            REGISTRO DE BLUEPRINTS 
# ------------------------------------------------------------
CORS(app)
app.register_blueprint(tokenBP, url_prefix='/token')
app.register_blueprint(usuariosBP, url_prefix='/usuarios')
app.register_blueprint(emailBP, url_prefix='/emails')

app.config['CORS_HEADERS'] = 'Content-Type'


if __name__ =='__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")