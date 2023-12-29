from flask import Blueprint

gestion_facturasBP = Blueprint('gestion_facturasBP', __name__)

from . import routes