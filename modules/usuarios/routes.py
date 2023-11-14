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
    response = ejec_store_procedure(method_name, params, ["message"])[0]
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
    response = ejec_store_procedure(method_name, params, ["usuario_id", "email", "confirmado"])[0]


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
    response = ejec_store_procedure(method_name, params, ["usuario_id"])[0]
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
    response = ejec_store_procedure(method_name, params, ['mensaje'])[0]
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
    response = ejec_store_procedure(method_name, params, ['mensaje'])[0]
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
    response = ejec_store_procedure(method_name, params, outputs)[0]
    if len(response)>1:
        response = jsonify(response)
        response.headers['Authorization'] = 'JWT'
        return (response),200
    else:
        response = jsonify({"mensaje":response['usuario_id']})
        response.headers['Authorization'] = 'JWT'
        return (response),404


#
# --------- E1. Mostrar ----------
#
@usuariosBP.route('/<string:usuario_id>',methods=["GET"])
def mostrar_perfil(usuario_id):
    method_name = "web_UserMuestraPerfil"
    params = [usuario_id]
    outputs=["email","uid","proveedor","nombre","apellido","alias","genero","tipo_documento","numero_documento","telefono","perfil_actualizado","confirmado"]
    response = ejec_store_procedure(method_name, params, outputs)[0]
    if len(response)>1:
        response = jsonify(response)
        response.headers['Authorization'] = 'JWT'
        return (response),200
    else:
        response = jsonify({"mensaje":response['email']})
        response.headers['Authorization'] = 'JWT'
        return (response),404
    
#
# --------- E3. Actualizar (contraseña) ----------
#
@usuariosBP.route('/<string:usuario_id>/password',methods=["PUT"])
def update_password(usuario_id):
    method_name = "web_UserCambiaPassword"
    values = request.get_json()
    params = [values[k] for k in values.keys()]
    params.insert(0,usuario_id)
    outputs=["mensaje"]
    response = ejec_store_procedure(method_name, params, outputs)[0]
    if ("incorrecta" not in response):
        response = jsonify(response)
        response.headers['Authorization'] = 'JWT'
        return (response),200
    else:
        response = jsonify(response)
        response.headers['Authorization'] = 'JWT'
        return (response),404
    

#
# --------- E4. Iniciar (Baja de usuarios)----------
#
@usuariosBP.route('/<string:usuario_id>/baja',methods=["POST"])
def baja_usuario(usuario_id):
    method_name='web_UserBaja'
    params = [usuario_id]
    outputs = ['mensaje']
    try:
        response = ejec_store_procedure(method_name, params, outputs)[0]
    except:
        return jsonify({"error": "Ha ocurrido un error en la consulta, reintente"}),500
    
    if ("inició el proceso" in response['mensaje']):
        response = jsonify(response)
        response.headers["Authorization"] = 'JWT'
        return response,200
    else:
        if ("error" not in response["mensaje"]):
            response = jsonify({"error": response['mensaje']})
            response.headers["Authorization"] = 'JWT'
            return response,404
        else:
            response = jsonify({"error": response['mensaje']})
            response.headers["Authorization"] = 'JWT'
            return response,422

#
# --------- E2. Actualizar (Perfil de usuarios)----------
#
@usuariosBP.route('/<string:usuario_id>',methods=["PUT"])
def actualiza_usuario(usuario_id):
    values = request.get_json()
    method_name='web_UserActualizaPerfil'
    params = [int(values[k]) if isinstance(values[k], bool) else values[k] for k in values.keys()]
    params.insert(0,usuario_id)
    outputs = ['mensaje']
    try:
        response = ejec_store_procedure(method_name, params, outputs)[0]
    except:
        return jsonify({"error": "Ha ocurrido un error en la consulta, reintente"}),500
    if ("correctamente" in response['mensaje']):
        response = jsonify(response)
        response.headers["Authorization"] = 'JWT'
        return response,200
    else:
        if ("inexistente" in response["mensaje"]):
            response = jsonify(response)
            response.headers["Authorization"] = 'JWT'
            return response,404
        else:
            response = jsonify({"error": response['mensaje']})
            response.headers["Authorization"] = 'JWT'
            return response,422
        