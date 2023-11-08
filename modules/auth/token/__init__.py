from flask import Blueprint

tokenBP=Blueprint('tokenBP',__name__)

from . import routes
