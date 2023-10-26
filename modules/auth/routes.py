from modules.auth import authBP
from flask import Flask, jsonify, request, send_file
from .controller import *
from data.env_data import *

import requests



values = '''{
  "api_key": "aaapppiiikkkeeyyy123",
  "api_secret": "aaapppiiikkkeeyyy---111!!"
}'''


@authBP.route('/', methods=['GET', 'POST'])
def index():
    response = requests.post(f'{base_url}/token', data=values, headers=headers)
    print(response.json())
    return jsonify(
        {
            "status_code":response.status_code,
            "headers":response.headers,
            "data":response.json()
        }
    )


@authBP.route('/valida/mail', methods=['GET', 'POST'])
def valida_mail():
    _email = request.args.get('email')
    print(f'{base_url}/validar_email'+'{?'+f'{_email}'+'}')
    response = requests.post(f'{base_url}/validar_email'+'{?'+f'{_email}'+'}', data=values, headers=headers)

    # print(response.status_code)
    # print(response.headers)
    # print(response.url)
    print(response.text)
    input()
    return (
        {
            "status_code":response.status_code,
            "headers":response.headers,
            "data":response.text
        }
    )