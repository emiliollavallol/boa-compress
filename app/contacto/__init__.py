from flask import Blueprint

contacto_bp = Blueprint('contacto', __name__)

from . import routes  # importa las rutas al registrar el blueprint
