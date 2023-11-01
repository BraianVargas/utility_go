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
def identificacion():
    values = request.get_json()
    method_name = 'web_UserVerificaIdentificacion'
    response = ejec_store_procedure(method_name, [values['email'],values['proveedor'],values['uid']], ["message"])
    if response['message']=="Usuario ya registrado.":
        return jsonify(response),422
    else:
        return jsonify(),200


# ----------- D.2 verificar --------------
@usuariosBP.route('/verificar', methods=['POST'])
def verifica_usuario():
    values = request.get_json()
    method_name = 'web_UserVerificaExistencia'
    response = ejec_store_procedure(method_name, [values['email'], values['telefono'], values['proveedor'], values['uid']], ["usuario_id", "email", "confirmado"])

    if len(response) == 1:
        return jsonify({"mensaje": response['usuario_id']}), 404
    else:
        return jsonify({k: response[k] for k in ["usuario_id", "email", "confirmado"]}), 200
