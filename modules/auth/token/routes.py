from modules.auth.token import tokenBP
from flask import Flask, jsonify, request, send_file
from .controller import *
from ...op_comunes import *

import requests, json

@tokenBP.route('/', methods=['POST'])
def get_token():
    if request.method == 'POST':
        values = request.get_json()
        if verifica_api_key(values['api_key']) and verifica_api_secret(values['api_secret']): # API KEY Y SECRET correctas
            response = jsonify(genera_token(data=values))
            response.headers['Authorization'] = 'JWT'
            return (response),200
        else:
            return jsonify({"mensaje": "Credenciales inválidas"}),401
    