from flask import Blueprint

compressor_bp = Blueprint('compressor', __name__)

from .routes import *  # Importa las rutas para registrarlas en el Blueprint
