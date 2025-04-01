from flask import render_template
from . import blog_bp

@blog_bp.route('/')
def blog_index():
    posts = [
        {
            "title": "¿Qué es WebP y por qué debería importarte en 2025?",
            "slug": "que-es-webp",
            "excerpt": "Descubre cómo una buena compresión puede mejorar la velocidad, SEO y experiencia de usuario.",
            "date": "2025-04-01",
            "author": "Emilio Llavallol"
        },
        {
            "title": "SEO para Ecommerce: Cómo optimizar imágenes para posicionar mejor tus productos",
            "slug": "seo-para-ecommerce",
            "excerpt": "Cuando gestionas un ecommerce, sabes que aparecer en los primeros resultados de Google es fundamental para atraer tráfico cualificado y aumentar las ventas.",
            "date": "2025-04-01",
            "author": "Emilio Llavallol"
        }
    ]
    return render_template("blog_index.html", posts=posts)

@blog_bp.route('/<slug>')
def blog_post(slug):
    return render_template(f"blog_post_{slug}.html")
