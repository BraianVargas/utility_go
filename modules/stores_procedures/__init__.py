from data.sybase_connect import connectSybase

def diccionario(output_list, responses):
    return [dict(zip(output_list, map(str, dato))) for dato in responses]

def formarSP(metodo, parametros):
    sp = metodo
    if parametros:
        sp += ' "' + '","'.join(str(p).lstrip('&') for p in parametros) + '"'
    return sp

def ejec_store_procedure(method_name, params, output_list):
    cnx = connectSybase()
    cnx.autocommit = True
    procedimiento = formarSP(method_name, params)
    response = cnx.execute(procedimiento)
    if not response:
        return None
    salida = diccionario(output_list,response)
    return(salida[0])

