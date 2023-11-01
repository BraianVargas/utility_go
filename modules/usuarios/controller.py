from data.sybase_connect import connectSybase



def consulta_select(query):
    cnx = connectSybase()
    cnx.autocommit = True
    response = cnx.execute(query)
    return(response.fetchall())
