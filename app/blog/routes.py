from flask import render_template
from . import blog_bp

@blog_bp.route('/')
def blog_index():
    posts = [
        {
            "title": "La guía definitiva sobre formatos de imágenes para tu web: JPEG, PNG, GIF, SVG, WebP y cuándo usar cada uno",
            "slug": "guia-definitiva-sobre-formatos-de-imagenes-para-tu-web",
            "excerpt": "Las imágenes son fundamentales para cualquier página web: enriquecen el contenido, mejoran la experiencia del usuario y ayudan al SEO. Sin embargo, elegir el formato adecuado puede marcar la diferencia en rendimiento, calidad visual y velocidad. ",
            "date": "2025-04-16",
            "author": "Emilio Llavallol"
        },
        {
            "title": "Guía práctica para mejorar tu catálogo online con imágenes optimizadas",
            "slug": "guia-practica-para-mejorar-tu-catalogo-online",
            "excerpt": "El catálogo online es la vidriera de tu ecommerce. Imágenes atractivas y optimizadas son fundamentales para captar la atención de tus visitantes y aumentar la conversión.",
            "date": "2025-04-16",
            "author": "Emilio Llavallol"
        },
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
