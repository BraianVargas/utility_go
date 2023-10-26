from flask import Blueprint

authBP=Blueprint('authBP',__name__)

from . import routes
