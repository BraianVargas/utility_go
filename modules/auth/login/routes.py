from modules.auth.login import loginBP
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
    try:
        token = request.headers['Authorization'].split(" ")[1]
    except:
        response = jsonify({"mensaje": "Credenciales inválidas"})
        response.status_code = 401
        return response
    response = valida_token(token, output=True)
    if isinstance(response,flask.wrappers.Response):
        return(response)
    else:
        pass

#
# ------------ D1. Ingresar ------------
#
@loginBP.route('/login',methods=['POST'])
def login():
    values = request.get_json()
    method_name = "web_UserIngresaLogin"
    params = [values[k] for k in values.keys()]
    outputs = ["usuario_id","confirmado","perfil_actualizado"]
    response = ejec_store_procedure(method_name, params, outputs)[0]
    if len(response) == 1:
        return jsonify({"mensaje":response['usuario_id']}),401
    else:
        return jsonify(response),200

