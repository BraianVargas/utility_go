from flask import request, jsonify, wrappers, abort

from modules.gestion_facturas import *
from modules.gestion_facturas.controller import *
from modules.stores_procedures import *
from modules.op_comunes import *
from modules.op_comunes import *

# 
# --------- B.1 Verifica que se haya enviado el token por medio del header. ----------
# 
@gestion_facturasBP.before_request
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
# --------- H.2 Factua en pdf - Descargar ----------
# 
@gestion_facturasBP.route('/<string:cuenta_id>/facturas/<string:factura_id>/pdf', methods=['GET'])
def descarga_factura(cuenta_id, factura_id):
     try:   
        method_name = 'web_FacturaObtienePath'
        params= [cuenta_id, factura_id]
        outputs = ["path_factura"]
        response = ejec_store_procedure(method_name, params, outputs)[0]
        if len(response)>=1:
            pdf_base64=pdf_to_base64(pdf_path = response['path_factura'])
            return jsonify({"base64":pdf_base64}),200
        else:
            return jsonify({"mensaje":response['cuenta_id']}),404
     except:
          return jsonify({"error":"Hubo un problema al ejecutar 'Descarga de pdf'."}),500

