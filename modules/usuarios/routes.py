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

#
# ------------ B6. Confirmar -----------
#
@usuariosBP.route('/<string:usuario_id>/confirmacion', methods=['POST'])
def confirmacion_usuario(usuario_id):
    values = request.get_json()
    method_name = "web_UserConfirmaRegistracion"
    params = [usuario_id]
    params.append(values[k] for k in values.keys())
    response = ejec_store_procedure(method_name, params, ['mensaje'])
    if response['mensaje'] == ' ':
        return jsonify(),200
    else:
        if response['mensaje'] == "Usuario inexistente.":
            return jsonify(response),404
        if response['mensaje'] == "Usuario ya confirmado.": 
            return jsonify(response),422

#
# ------------ C2. Generar -----------
#
@usuariosBP.route('/<string:usuario_id>/recuperacion_password', methods=['POST'])
def forgot_password(usuario_id):
    values = request.get_json()
    method_name = "web_UserGeneraNuevaPassword"
    params = [usuario_id,values['password'],values['token']]
    response = ejec_store_procedure(method_name, params, ['mensaje'])
    if "actualizada" in response['mensaje']:
        return jsonify(response),200
    else:
        return jsonify(response),422
    
#
# ------------ D3. Obtener Pista -----------
#
@usuariosBP.route('/recuperacion', methods=['GET'])
def recupera_usuario():
    values = request.args.to_dict()
    method_name = "web_UserObtieneMail"
    params = [values[k] for k in values.keys()]
    outputs=["usuario_id","email","proveedor"]
    response = ejec_store_procedure(method_name, params, outputs)
    if len(response)>1:
        response = jsonify(response)
        response.headers['Authorization'] = 'JWT'
        return (response),200
    else:
        response = jsonify({"mensaje":response['usuario_id']})
        response.headers['Authorization'] = 'JWT'
        return (response),404
    