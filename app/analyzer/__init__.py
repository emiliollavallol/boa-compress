from flask import Blueprint

analyzer_bp = Blueprint('analyzer', __name__)

from .routes import *  # Importa las rutas para registrarlas en el Blueprint
