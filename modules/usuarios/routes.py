from modules.usuarios import usuariosBP
from modules.stores_procedures import *
from modules.op_comunes import *
from .controller import *
from data.env_data import *

import requests
import flask
from flask import request

# 
# --------- B.1 Verifica que se haya enviado el token por medio del header. ----------
# 
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
    values = request.get_json()
    method_name = 'web_UserVerificaIdentificacion'
    response = ejec_store_procedure(method_name, [values['email'],values['proveedor'],values['uid']], ["message"])
    if response['message']=="Usuario ya registrado.":
        return jsonify(response),422
    else:
        return jsonify(),200
