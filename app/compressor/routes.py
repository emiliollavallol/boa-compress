from flask import render_template, request, send_file, Blueprint
from PIL import Image
import io
import os
import pillow_heif  # ✅ Import HEIC support

compressor_bp = Blueprint('compressor', __name__)

@compressor_bp.route('/')
def index():
    return render_template("conversor.html")

@compressor_bp.route("/convert", methods=["POST"])
def convert_image():
    if "image" not in request.files:
        return "No file uploaded", 400

    file = request.files["image"]

    try:
        # Detect HEIC and convert it to PIL Image
        if file.filename.lower().endswith(".heic"):
            heif_image = pillow_heif.open_heif(file.stream)
            image = Image.frombytes(
                heif_image.mode, heif_image.size, heif_image.data
            )
        else:
            image = Image.open(file.stream)

        # Convert to RGB if needed (WebP doesn't support all color modes)
        if image.mode in ("RGBA", "P", "CMYK"):
            image = image.convert("RGB")

        output = io.BytesIO()
        image.save(output, format="WEBP", quality=80)  # ✅ Ensure WebP conversion
        output.seek(0)

        return send_file(output, mimetype="image/webp", as_attachment=True,
                         download_name=f"{os.path.splitext(file.filename)[0]}.webp")

    except Exception as e:
        return f"Error processing image: {str(e)}", 500