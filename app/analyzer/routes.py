from flask import render_template, request, jsonify, Blueprint
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote, urljoin

analyzer_bp = Blueprint('analyzer', __name__)

def extract_real_image_url(image_url):
    """ Extrae la URL real de una imagen si está encapsulada en un parámetro `url=` """
    parsed_url = urlparse(image_url)
    query_params = parse_qs(parsed_url.query)

    if "url" in query_params:
        return unquote(query_params["url"][0])  # Decodificar la URL real de la imagen

    return image_url  # Si no está en `url=`, devolver la URL original

def get_images_from_page(url):
    """Extrae todas las imágenes de una página web."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        images = [urljoin(url, img['src']) for img in soup.find_all("img") if "src" in img.attrs]
        return images
    except requests.exceptions.RequestException:
        return []

def get_image_type(image_url):
    """Obtiene el tipo de imagen desde el Content-Type de la cabecera HTTP."""
    headers = {"User-Agent": "Mozilla/5.0"}

    # 🔹 Extraer la URL real antes de procesarla
    image_url = extract_real_image_url(image_url)

    try:
        response = requests.head(image_url, headers=headers, timeout=3)
        content_type = response.headers.get("Content-Type", "")

        # Si no hay Content-Type, intentamos con GET
        if not content_type:
            response = requests.get(image_url, headers=headers, timeout=3, stream=True)
            content_type = response.headers.get("Content-Type", "")

        print(f"📸 {image_url} → Content-Type: {content_type}")  # ✅ Debug

        if "jpeg" in content_type:
            return "jpg"
        elif "png" in content_type:
            return "png"
        elif "webp" in content_type:
            return "webp"
        elif "svg" in content_type:
            return "svg"
        elif "avif" in content_type:
            return "avif"
        elif "image" in content_type:
            return "other"
        else:
            return "unknown"
    except requests.exceptions.RequestException:
        return "unknown"

def crawl_site(start_url, max_pages=10):
    """Realiza un crawleo básico en el sitio y analiza múltiples páginas."""
    visited = set()
    to_visit = [start_url]
    all_images = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue

        visited.add(url)
        images = get_images_from_page(url)

        # ✅ Debug: Ver cuántas imágenes tiene la página y las primeras 10 URLs
        print(f"🔍 {url} → {len(images)} imágenes encontradas")
        for img in images[:10]:  # Solo las primeras 10 para no saturar la consola
            ext = img.split(".")[-1].lower()
            print(f"🖼️ {img} → Extensión detectada: {ext}")

        all_images.extend(images)

        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a", href=True):
                absolute_url = urljoin(url, link["href"])
                if urlparse(absolute_url).netloc == urlparse(start_url).netloc and absolute_url not in visited:
                    to_visit.append(absolute_url)
        except requests.exceptions.RequestException:
            continue

    return all_images

def normalize_url(url):
    """Asegura que la URL tenga un esquema válido (https:// o http://)"""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url  # Se asume HTTPS por defecto
    return url

def format_size(size_kb):
    """Convierte KB a MB siempre"""
    return f"{round(size_kb / 1024, 2)} MB"

def get_site_diagnosis(total_weight_mb):
    """Genera un diagnóstico basado en el peso total de imágenes"""
    if total_weight_mb < 10:
        return "✅ Excelente: Tus imágenes están bien optimizadas."
    elif total_weight_mb < 15:
        return "🟡 Aceptable: Tus imágenes están en un rango razonable."
    elif total_weight_mb < 20:
        return "⚠️ Pesado: Tus imágenes podrían estar ralentizando la carga de la web."
    else:
        return "🚨 Crítico: Tus imágenes son muy pesadas y afectan seriamente la velocidad."

@analyzer_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("websiteUrl")
        url = normalize_url(url)
        images = crawl_site(url, max_pages=2)

        formats = {"jpg": 0, "png": 0, "webp": 0, "other": 0, "unknown": 0}  # Aseguramos que 'other' exista
        total_weight_before = 0
        total_weight_after = 0
        valid_images = 0  # Contamos solo imágenes válidas

        weight_estimates = {
            "jpg": {"before": 300, "after": 210},
            "png": {"before": 500, "after": 250},
            "webp": {"before": 250, "after": 250},
            "svg": {"before": 400, "after": 400},  # SVG entra en "other"
            "other": {"before": 400, "after": 400},
            "unknown": {"before": 400, "after": 400},
        }

        for img in images:
            if not img:  # Evitar URLs vacías
                continue

            img_type = get_image_type(img)

            # Si el formato no es reconocido, agrégalo como "other"
            if img_type not in formats:
                img_type = "other"

            formats[img_type] += 1
            total_weight_before += weight_estimates.get(img_type, weight_estimates["other"])["before"] * 1024
            total_weight_after += weight_estimates.get(img_type, weight_estimates["other"])["after"] * 1024
            valid_images += 1

        # Convertir pesos a MB
        total_weight_before_mb = total_weight_before / 1024 / 1024
        total_weight_after_mb = total_weight_after / 1024 / 1024
        diagnosis = get_site_diagnosis(total_weight_before_mb)

        reduction_percentage = ((total_weight_before - total_weight_after) / total_weight_before) * 100 if total_weight_before > 0 else 0
        avg_weight_before = total_weight_before / valid_images if valid_images else 0
        avg_weight_after = total_weight_after / valid_images if valid_images else 0

        return jsonify({
            "formats": formats,
            "total_images": valid_images,
            "total_weight_before": round(total_weight_before_mb,2),
            "total_weight_after": round(total_weight_after_mb, 2),
            "avg_weight_before": format_size(avg_weight_before / 1024),
            "avg_weight_after": format_size(avg_weight_after / 1024),
            "reduction_percentage": round(reduction_percentage, 2),
            "diagnosis": diagnosis
        })

    return render_template("analizador.html")
