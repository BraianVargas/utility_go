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
# ------------- F3. Actualizar (alias de usuario) --------------
#
@perfilBP.route('/asociasiones',methods=['PUT'])
def actualiza_alias():
    values = request.get_json()
    method_name='web_UserActualizaAliasSum'
    params = [values[k] for k in values.keys()]
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
        response = jsonify(response)
        response.headers["Authorization"] = 'JWT'
        return response,404

#
# ------------- F1. Obtener (cuentas) --------------
#
@perfilBP.route('/asociasiones',methods=['GET'])
def obtener_cuentas():
    values = request.args.to_dict()
    method_name='web_UserObtieneCuentas'
    params = [values[k] for k in values.keys()]
    outputs = ['cuenta_id','titular','direccion']
    response = ejec_store_procedure(method_name, params, outputs)
    
    if "no existe" in response[0]['cuenta_id'] or "No existen" in response[0]['cuenta_id'] :
        response = jsonify({"mensaje":response[0]['cuenta_id']})
        response.headers["Authorization"] = 'JWT'
        return response, 404
    else:
        if "ya existe" in response[0]['cuenta_id']:
            response = jsonify({"mensaje":response[0]['cuenta_id']})
            response.headers["Authorization"] = 'JWT'
            return response, 422
        else:
            return response