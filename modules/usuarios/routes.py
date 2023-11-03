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
    
#
# --------- B1. verificar. ----------
#
@usuariosBP.route('/identificacion', methods=['POST'])
def identificacion():
    values = request.get_json()
    method_name = 'web_UserVerificaIdentificacion'
    params=list(values.values())
    response = ejec_store_procedure(method_name, params, ["message"])
    if response['message']=="Usuario ya registrado.":
        return jsonify(response),422
    else:
        return jsonify(),200

#
# ----------- D2. verificar --------------
#
@usuariosBP.route('/verificar', methods=['POST'])
def verifica_usuario():
    values = request.get_json()
    method_name = 'web_UserVerificaExistencia'

# [values["email"],values["telefono"],values["proveedor"],values["uid"]]

    params=list(values.values())
    print(params)
    response = ejec_store_procedure(method_name, params, ["usuario_id", "email", "confirmado"])


    if len(response) == 1:
        return jsonify({"mensaje": response['usuario_id']}), 404
    else:
        return jsonify({k: response[k] for k in ["usuario_id", "email", "confirmado"]}), 200

#
# ----------- B4. Generar --------------
#
@usuariosBP.route('/', methods=['POST'])
def generar_usuario():
    values = request.get_json()
    method_name = 'web_UserGeneraRegistro'
    params = [int(values[k]) if isinstance(values[k], bool) else values[k] for k in values.keys()]
    response = ejec_store_procedure(method_name, params, ["usuario_id"])
    try:
        return jsonify({"usuario_id":int(response['usuario_id'])}), 200
    except:
        return jsonify({"mensaje": response['usuario_id']}), 404

