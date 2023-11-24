from flask import Blueprint

cuentasBP = Blueprint('cuentas_BP', __name__)

from . import routes