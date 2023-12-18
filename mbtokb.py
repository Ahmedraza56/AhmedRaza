from flask import Blueprint, render_template, request, send_file, url_for
from PIL import Image
import os

mbtokb_app = Blueprint("mbtokb", __name__)

def mb_to_kb_converter(image_path, output_path, target_size_kb):
    try:
        with Image.open(image_path) as img:
            target_size_bytes = target_size_kb * 1024
            img.thumbnail((300, 300))
            img.save(output_path, format="JPEG", quality=85)

            while os.path.getsize(output_path) > target_size_bytes:
                img.thumbnail((img.width // 2, img.height // 2))
                img.save(output_path, format="JPEG", quality=85)

    except Exception as e:
        print(f"Error during image conversion: {e}")
        return None

    return output_path

def get_static_path(filename):
    return os.path.join("static", filename)

@mbtokb_app.route('/', methods=['GET', 'POST'])
def index():
    download_button_visible = False

    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file:
            target_size_kb = 100
            output_path = get_static_path("converted_image.jpg")
            uploaded_file_path = get_static_path(uploaded_file.filename)

            uploaded_file.save(uploaded_file_path)

            converted_path = mb_to_kb_converter(uploaded_file_path, output_path, target_size_kb)

            if converted_path:
                download_button_visible = True
                return render_template('mbtokb.html', original_image=url_for('static', filename=uploaded_file.filename),
                                       converted_image=url_for('static', filename='converted_image.jpg'),
                                       download_button_visible=download_button_visible)

    return render_template('mbtokb.html', download_button_visible=download_button_visible)

@mbtokb_app.route('/download')
def download():
    return send_file(get_static_path("converted_image.jpg"), as_attachment=True)
