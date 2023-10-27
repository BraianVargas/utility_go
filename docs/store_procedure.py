#--1� CREAR 
class intnet_fadigital_obtenerdtoscontactoObject(object):
    def on_post(self, req, resp):
          cnx = conexionGesto()
          cnx.autocommit = True
          metodo = 'fd_obtiene_datos_contacto'
          credentials = json.loads(req.stream.read())        
          suministro = credentials['data']['suministro']
          parametros = [suministro]
          listaSalida = ['suministro','nombres', 'apellidos', 'celular', 'email']
          salida = consulta(metodo, parametros, listaSalida, cnx)
          resp.body = json.dumps(salida)

api.add_route('/intnet_fadigital_obtenerdtoscontacto/', intnet_fadigital_obtenerdtoscontactoObject())

