from flask import Flask, render_template, request, send_file, Blueprint
from rembg import remove
from PIL import Image
import io

bgremove_app = Blueprint("bgremove", __name__)

@bgremove_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded file
        uploaded_file = request.files['file']

        if uploaded_file:
            # Remove the background of the image
            try:
                input_image = Image.open(uploaded_file)
                input_image_bytes = io.BytesIO()
                input_image.save(input_image_bytes, format=input_image.format)

                result_bytes = remove(input_image_bytes.getvalue())

                result_image = Image.open(io.BytesIO(result_bytes))
                result_image.save("static/bg_removed.png")

                return render_template('bgremove.html', result_image='bg_removed.png')
            except Exception as e:
                error_message = f'An error occurred: {str(e)}'
                return render_template('bgremove.html', error_message=error_message)

    return render_template('bgremove.html', result_image=None, error_message=None)

@bgremove_app.route('/download')
def download():
    return send_file('static/bg_removed.png', as_attachment=True)

