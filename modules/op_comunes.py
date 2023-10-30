from flask import jsonify, session
import jwt
from datetime import datetime, timedelta

from data.env_data import *

def genera_token(data:dict):
    expiracion = datetime.utcnow() + timedelta(hours=24)
    token = jwt.encode({**data, "expiracion": expiracion.timestamp()}, data['api_secret'], algorithm='HS256')
    tiempo_faltante = int((expiracion - datetime.utcnow()).total_seconds())

    response = {
        "token": token,
        "expiracion": tiempo_faltante
    }
    return response

def verifica_api_key(_api_key):
    if _api_key == API_KEY:
        return True
    else:
        return False

def verifica_api_secret(_api_secret):
    if _api_secret == SECRET_KEY:
        return True
    else:
        return False

def verifica_headers(_headers):
    if _headers['Content-Type'] == HEADERS['Content-Type'] and _headers['Authorization'] == HEADERS['Authorization']:
        return True
    else:
        return False

def valida_token(token, output=False):
    try:
        if output == True:
            return jwt.decode(token,key=SECRET_KEY, algorithm='HS256')
    except:
        return jsonify({"mensaje": "Credenciales inválidas"}),401