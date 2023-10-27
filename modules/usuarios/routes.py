from modules.auth import authBP
from flask import Flask, jsonify, request, send_file
from .controller import *
from data.env_data import *

import requests

@authBP.route('/register', methods=['GET', 'POST'])
def registra_usuario():
    response = requests.post(f'{base_url}/token', data={"api_key":api_key, "api_secret": api_secret}, headers=headers)
    print(response.json())
    return jsonify(
        {
            "status_code":response.status_code,
            "headers":response.headers,
            "data":response.json()
        }
    )

