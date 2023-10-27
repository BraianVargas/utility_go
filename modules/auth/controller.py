from flask import jsonify
import requests
import json

from data.env_data import *

def get_token_controller():
     response = requests.post(
        f'{base_url}/token',
        data={
            "api_key": api_key,
            "api_secret": api_secret
        },
        headers=headers)
     response_dict = response.json()
     if int(response_dict['expiracion']) > 0:
          return response_dict['token']
     else:
          return response_dict['mensaje']
