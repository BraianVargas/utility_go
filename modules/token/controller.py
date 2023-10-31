import string, secrets
from datetime import datetime, timedelta
from jwt import encode
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
