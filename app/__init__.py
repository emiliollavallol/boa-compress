from flask import Flask, render_template, send_from_directory
from app.compressor import compressor_bp
from app.analyzer import analyzer_bp
from app.contacto import contacto_bp
from app.blog import blog_bp
import os

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback_key')

    # Rutas para robots.txt y sitemap.xml
    @app.route('/robots.txt')
    def robots_txt():
        return send_from_directory(app.root_path, 'robots.txt', mimetype='text/plain')

    @app.route('/sitemap.xml')
    def sitemap_xml():
        return send_from_directory(app.root_path, 'sitemap.xml', mimetype='application/xml')

    # Registrar los Blueprints
    app.register_blueprint(compressor_bp, url_prefix='/comprimir')
    app.register_blueprint(analyzer_bp, url_prefix='/analizar')
    app.register_blueprint(contacto_bp, url_prefix='/contacto')
    app.register_blueprint(blog_bp, url_prefix='/blog')

    @app.route('/')
    def home():
        return render_template('home.html')

    return app
