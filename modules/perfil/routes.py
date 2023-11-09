from flask import request, jsonify, wrappers

from modules.perfil import *
from modules.stores_procedures import *
from modules.op_comunes import *

# 
# --------- B.1 Verifica que se haya enviado el token por medio del header. ----------
# 
@perfilBP.before_request
def verifica_token_middleware():
    try:
        token = request.headers['Authorization'].split(" ")[1]
    except:
        response = jsonify({"mensaje": "Credenciales inválidas"})
        response.status_code = 401
        return response
    response = valida_token(token, output=True)
    if isinstance(response,wrappers.Response):
        return(response)
    else:
        pass

#
# --------- E1. Mostrar ----------
#
@perfilBP.route('/<string:usuario_id>',methods=["GET"])
def mostrar_perfil(usuario_id):
    method_name = "web_UserMuestraPerfil"
    params = [usuario_id]
    outputs=["email","uid","proveedor","nombre","apellido","alias","genero","tipo_documento","numero_documento","telefono","perfil_actualizado","confirmado"]
    response = ejec_store_procedure(method_name, params, outputs)
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
@perfilBP.route('/<string:usuario_id>/password',methods=["PUT"])
def update_password(usuario_id):
    method_name = "web_UserCambiaPassword"
    values = request.get_json()
    params = [values[k] for k in values.keys()]
    params.insert(0,usuario_id)
    outputs=["mensaje"]
    response = ejec_store_procedure(method_name, params, outputs)
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
@perfilBP.route('/<string:usuario_id>/baja',methods=["POST"])
def baja_usuario(usuario_id):
    method_name='web_UserBaja'
    params = [usuario_id]
    outputs = ['mensaje']
    try:
        response = ejec_store_procedure(method_name, params, outputs)
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
@perfilBP.route('/<string:usuario_id>',methods=["PUT"])
def actualiza_usuario(usuario_id):
    values = request.get_json()
    method_name='web_UserActualizaPerfil'
    params = [int(values[k]) if isinstance(values[k], bool) else values[k] for k in values.keys()]
    params.insert(0,usuario_id)
    outputs = ['mensaje']
    try:
        response = ejec_store_procedure(method_name, params, outputs)
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