from flask import Flask, render_template
from app.compressor import compressor_bp
from app.analyzer import analyzer_bp
from app.contacto import contacto_bp
from app.blog import blog_bp

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your_secret_key_here'

    # Registrar los Blueprints
    app.register_blueprint(compressor_bp, url_prefix='/comprimir')
    app.register_blueprint(analyzer_bp, url_prefix='/analizar')
    app.register_blueprint(contacto_bp, url_prefix='/contacto')
    app.register_blueprint(blog_bp, url_prefix='/blog')

    @app.route('/')
    def home():
        return render_template('home.html')

    return app
