from modules import *
from modules.usuarios import usuariosBP
from modules.usuarios import usuariosBP
from modules.op_comunes import *
from .controller import *
from data.env_data import *

import requests
import flask
from flask import request

@usuariosBP.before_request
def verifica_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    response = valida_token(token, output=True)
    if isinstance(response,flask.wrappers.Response):
        return(response)
    else:
        pass
    

# --------- B.1 verificar. ----------
@usuariosBP.route('/identificacion', methods=['POST'])
def registra_usuario():
    print("# Se va a registrar el usuario")


    return jsonify(1)
