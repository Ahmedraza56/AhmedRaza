from flask import Flask, render_template, request, send_file ,Blueprint
from PIL import Image
import os

mbtokb_app = Blueprint("mbtokb",__name__)

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
        return None

    return output_path

@mbtokb_app.route('/', methods=['GET', 'POST'])
def index():
    download_button_visible = False  # Flag to determine if the "Download" button should be visible

    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            target_size_kb = 100
            output_path = "static/converted_image.jpg"
            uploaded_file_path = f"static/{uploaded_file.filename}"

            uploaded_file.save(uploaded_file_path)

            converted_path = mb_to_kb_converter(uploaded_file_path, output_path, target_size_kb)

            if converted_path:
                download_button_visible = True
                return render_template('mbtokb.html', original_image=uploaded_file_path,
                                       converted_image=converted_path,
                                       download_button_visible=download_button_visible)

    return render_template('mbtokb.html', download_button_visible=download_button_visible)

@mbtokb_app.route('/download')
def download():
    return send_file('static/converted_image.jpg', as_attachment=True)

