from flask import request, wrappers

from modules.stores_procedures import ejec_store_procedure
from modules.op_comunes import * 


from modules.emails import emailBP
from .controller import *

# 
# --------- B.1 Verifica que se haya enviado el token por medio del header. ----------
#
@emailBP.before_request
def verifica_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    response = valida_token(token, output=True)
    if isinstance(response,wrappers.Response):
        return(response)
    else:
        pass

#
# ----------- B5. Enviar --------------
#
@emailBP.route('/registro', methods=['POST'])
def generar_usuario():
    values = request.get_json()
    method_name = 'web_UserEnviaCodVerificacion'
    params = [values[k] for k in values.keys()]
    response = ejec_store_procedure(method_name, params, ["mensaje"])[0]
    try:
        if (values['email'] in response['mensaje']):
            status = envia_mail_codigo(values['email'],values['codigo_verificacion'])
            if status==True:
                return jsonify({"mensaje":(response['mensaje'])}), 200
        else:
            return jsonify({"mensaje": response['mensaje']}), 404
    except Exception as e:
        return jsonify({"Server Error": e}), 500