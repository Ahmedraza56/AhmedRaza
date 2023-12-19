from flask import Flask, render_template, request, send_file, Blueprint
from PIL import Image
from io import BytesIO
import os

webtopng_app = Blueprint("webtopng", __name__)

@webtopng_app.route('/', methods=['GET', 'POST'])
def main():
    converted_image = None
    if request.method == 'POST':
        try:
            uploaded_file = request.files['file']
            if uploaded_file and allowed_file(uploaded_file.filename):
                converted_image = convert_to_png(uploaded_file)
        except Exception as e:
            return render_template('webtopng.html', error=f"An error occurred: {str(e)}")

    return render_template('webtopng.html', converted_image=converted_image)

@webtopng_app.route('/convert', methods=['POST'])
def convert():
    try:
        uploaded_file = request.files['file']
        if uploaded_file and allowed_file(uploaded_file.filename):
            converted_image_path = convert_to_png(uploaded_file)
            return render_template('webtopng.html', converted_image=converted_image_path)
    except Exception as e:
        return render_template('webtopng.html', error=f"An error occurred: {str(e)}")

    return render_template('webtopng.html')

@webtopng_app.route('/download', methods=['GET'])
def download():
    try:
        filename = request.args.get('filename')
        return send_file(filename, as_attachment=True, download_name="converted_image.png")
    except Exception as e:
        return render_template('webtopng.html', error=f"An error occurred: {str(e)}")

def convert_to_png(image_file):
    try:
        img = Image.open(image_file)
        img_png = img.convert("RGBA")

        img_bytes = BytesIO()
        img_png.save(img_bytes, format="PNG")

        # Save the BytesIO content to a temporary file
        temp_filename = "/tmp/converted_image.png"
        with open(temp_filename, "wb") as temp_file:
            temp_file.write(img_bytes.getvalue())

        return temp_filename
    except Exception as e:
        raise e  # You might want to handle this exception differently based on your application's needs

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'webp'}
