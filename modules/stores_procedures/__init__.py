from data.sybase_connect import connectSybase

def diccionario_1(output_list,responses):
    return_list = []
    for response in responses:
        for i in range(len(response)):
            try:
                response[i] = bool(response[i]) if response[i] in (0,1) else response[i]
            except:
                pass
        return_list.append(dict(zip(output_list, map(str, response))))
    return return_list

def formarSP(metodo, parametros):
    sp = metodo
    if parametros:
        param_strings = []
        for p in parametros:
            if isinstance(p, int):
                param_strings.append(str(p))
            else:
                param_strings.append(f'"{p}"')
        sp += ' ' + ','.join(param_strings)
    return sp

def ejec_store_procedure(method_name, params, output_list):
    cnx = connectSybase()
    cnx.autocommit = True
    procedimiento = formarSP(method_name, params)
    response = cnx.execute(procedimiento)
    response = (response.fetchall())
    if not response:
        return None
    salida = diccionario_1(output_list,response)
    return(salida)

