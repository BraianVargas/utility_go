# #--1� CREAR 
# class intnet_fadigital_obtenerdtoscontactoObject(object):
#     def on_post(self, req, resp):
#         cnx = conexionGesto()
#         cnx.autocommit = True
#         metodo = 'fd_obtiene_datos_contacto'
#         credentials = json.loads(req.stream.read())        
#         suministro = credentials['data']['suministro']
#         parametros = [suministro]
#         listaSalida = ['suministro','nombres', 'apellidos', 'celular', 'email']
#         salida = consulta(metodo, parametros, listaSalida, cnx)
#         resp.body = json.dumps(salida)

# api.add_route('/intnet_fadigital_obtenerdtoscontacto/', intnet_fadigital_obtenerdtoscontactoObject())


# WEB SERVICE
def diccionario(listaCampos, resultados):
    nroCampos = len(listaCampos)
    salida = []
    for dato in resultados:
        doc = {}
        for c in range(nroCampos):
            doc[listaCampos[c]] =  '{}'.format(dato[c])
        salida.append(doc)
    return salida

def formarSP(metodo, parametros):
    inicial = ' "'
    separador = '","'
    ultimo = len(parametros)
    contador = 0
    if ultimo >0:
        exe = metodo + inicial
        for parametro in parametros:
            p = str(parametro)
            contador = contador + 1
            if p[:1] == '&':
                p = p[1:]
                exe = exe[:-1] # QUITAR doble comilla 
                exe += p
                if contador < ultimo:
                    exe += ',"'
            else:
                exe += p + separador
                if contador == ultimo:
                    exe = exe[:-2]
        sp = exe
    else:
        sp = metodo
    return(sp)

def consulta(metodo, parametros, listaSalida,cnx):
    procedimiento = formarSP(metodo, parametros)
    #print(procedimiento)
    resultados = cnx.execute(procedimiento)
    salida = diccionario(listaSalida, resultados)
    return salida