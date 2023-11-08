from flask import Blueprint

loginBP=Blueprint('loginBP',__name__)

from . import routes
