from modules import *
from modules.usuarios import usuariosBP
from modules.usuarios import usuariosBP
from modules.op_comunes import *

from .controller import *
from data.env_data import *


import requests
@usuariosBP.before_request
def verifica_token_middleware():
    token = requests.headers['Authorization'].split(' ')[1]
    valida_token(token)
    

@usuariosBP.route('/registrar', methods=['GET', 'POST'])
def registra_usuario():
    print("# Se va a registrar el usuario")