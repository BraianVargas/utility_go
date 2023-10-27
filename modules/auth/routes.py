from modules.auth import authBP
from flask import Flask, jsonify, request, send_file
from .controller import *
from data.env_data import *

import requests, json


@authBP.route('/get_token', methods=['GET', 'POST'])
def get_token():
    try:
        resp = get_token_controller()
        if type(resp) == bool:
            pass
        else:
            pass
    except Exception as e:
        return jsonify(
            {KeyError:ValueError}
        )
    
    return resp
    
