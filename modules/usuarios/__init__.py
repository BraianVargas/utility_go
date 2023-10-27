from flask import Blueprint

usuariosBP=Blueprint('usuariosBP',__name__)

from . import routes
