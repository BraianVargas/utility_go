from flask import jsonify, session
import jwt
from jwt import exceptions, encode, decode
from datetime import datetime, timedelta

from data.env_data import *


def genera_token(data:dict):
    def expire_date(time:int):
        now = datetime.now() 
        new_date = now + timedelta(hours=time)
        return new_date
    token = encode(
        payload={**data, "expiracion": expire_date(24).timestamp()},
        key= data['api_secret'], 
        algorithm='HS256')
    expiracion = expire_date(24)
    tiempo_faltante = int((expiracion - datetime.now()).total_seconds())
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
        if output:
            response = decode(token,key=SECRET_KEY, algorithms='HS256')
            return response
    except exceptions.DecodeError:
        response = jsonify({"mensaje": "Credenciales inválidas"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"mensaje": "Credenciales inválidas"})
        response.status_code = 401
        return response