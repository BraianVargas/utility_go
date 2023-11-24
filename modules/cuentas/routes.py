from flask import request, jsonify, wrappers, abort

from modules.cuentas import *
from modules.stores_procedures import *
from modules.op_comunes import *

# 
# --------- B.1 Verifica que se haya enviado el token por medio del header. ----------
# 
@cuentasBP.before_request
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
# ---------------- G2. Muestra CUENTAS ----------------
#
@cuentasBP.route('/<string:usuario_id>', methods=['GET'])
def mostrar_cuentas(usuario_id):
    try:
        method_name = 'web_UserMuestraCuenta'
        params= [usuario_id]
        outputs = ["cuenta_id","adherido_debito_automatico","adherido_factura_digital","tarifa","tarifa_normalizada","medidor_inteligente","premium","titular","direccion","localidad","partido","latitud","longitud","saldo_total","tipo_demanda","descripcion_estado","estado","es_electrodependiente","emails_factura_digital","codigo_segmentacion_electrica","consumo_tiempo_real","url_consumo_tiempo_real","tope_subsidio_provincial","valor_tope_subsidio_provincial","persona_id","atributos_adicionales","empadronado_segmentacion_electrica"]
        response = ejec_store_procedure(method_name, params, outputs)[0]
        if len(response)>1:
            return jsonify(response),200
        else:
            return jsonify({"mensaje":response['cuenta_id']}),404
    except:
        return jsonify({"error":"Hubo un problema al ejecutar 'Listar cuentas'."}),500





