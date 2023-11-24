from flask import request, jsonify, wrappers, abort

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
@perfilBP.route('/asociaciones',methods=['PUT'])
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
@perfilBP.route('/asociaciones',methods=['GET'])
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

#
# ------------- F2. Asociar (suministros) --------------
#

@perfilBP.route('/asociaciones', methods=['post'])
def asocia_cuentas():
    try:
        values = request.get_json()
        method_name = 'web_UserAsociaCuentas'
        params = [values['usuario_id']]
        outputs = ['cuenta_id', 'direccion', 'cuenta_asociada', 'mensaje']
        cuentas = values.get('cuentas', [])
        final_response = []

        for cuenta in cuentas:
            params.extend(str(cuenta.get(key, '')) if cuenta.get(key) is not None else '' for key in cuenta)
            response = ejec_store_procedure(method_name, params, outputs)
            final_response.append(response[0])
            params[1:] = []

        return jsonify(final_response), 200

    except Exception as e:
        mensaje_error = "Hubo un error al procesar la asociación de cuentas. Por favor, inténtelo nuevamente más tarde."
        abort(422, description=mensaje_error)



#
# ------------- F4. Desasociar (Suministros) --------------
#
@perfilBP.route('/asociaciones', methods=['DELETE'])
def desasocia_cuenta():
    try:
        values = request.get_json()
        method_name = "web_UserDesasociarCuentas"
        params = [values[k] for k in values.keys()]
        outputs = ["mensaje"]
        response = ejec_store_procedure(method_name, params, outputs)[0]
        if "inexistente" not in response['mensaje']:
            return jsonify(response),200
        else:
            return jsonify(response),404
    except:
        return jsonify({"error":"Error interno de servidor. Metodo: Desasociar Cuentas."}),500