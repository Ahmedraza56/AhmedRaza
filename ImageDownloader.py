from flask import Flask, render_template, request, send_file, Blueprint
import requests
from PIL import Image
from io import BytesIO
import base64

ImageDownloader_app = Blueprint("ImageDownloader", __name__)

def download_image(url):
    if url.startswith("data:image"):
        _, encoded = url.split(",", 1)
        img_data = base64.b64decode(encoded)
        img = Image.open(BytesIO(img_data))
    else:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        img = Image.open(BytesIO(response.content))
    return img

@ImageDownloader_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            image = download_image(url)

            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            img_str = base64.b64encode(img_byte_arr).decode('utf-8')

            return render_template('ImageDownloader.html', image=img_str, error_message=None)

        except Exception as e:
            error_message = f'Error: {e}'
            return render_template('ImageDownloader.html', error_message=error_message)

    return render_template('ImageDownloader.html', error_message=None)

@ImageDownloader_app.route('/download', methods=['GET'])
def download():
    try:
        url = request.args.get('url')
        image = download_image(url)

        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        return send_file(
            BytesIO(img_byte_arr),
            mimetype='image/png',
            as_attachment=True,
            download_name='downloaded_image.png'
        )

    except Exception as e:
        error_message = f'Error: {e}'
        return render_template('ImageDownloader.html', error_message=error_message)

app = Flask(__name__)
app.register_blueprint(ImageDownloader_app, url_prefix='/imagedownloader')

    
