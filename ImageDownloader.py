from flask import Flask, render_template, request, send_file, Blueprint
import requests
from PIL import Image
import io
import base64

ImageDownloader_app = Blueprint("ImageDownloader", __name__)

def download_image(url):
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    try:
        image = Image.open(io.BytesIO(response.content))
        # Check the image format (e.g., JPEG, PNG)
        image.verify()
        return image
    except Exception as e:
        raise ValueError(f'Invalid image format: {e}')

@ImageDownloader_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            image = download_image(url)

            if image:
                img_byte_arr = io.BytesIO()
                # Save the image explicitly in PNG format
                image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()

                img_str = base64.b64encode(img_byte_arr).decode('utf-8')

                return render_template('ImageDownloader.html', image=img_str, error_message=None)
            else:
                error_message = 'Invalid image format'
                return render_template('ImageDownloader.html', error_message=error_message)

        except ValueError as ve:
            error_message = str(ve)
            return render_template('ImageDownloader.html', error_message=error_message)
        except Exception as e:
            error_message = f'Error: {e}'
            return render_template('ImageDownloader.html', error_message=error_message)

    return render_template('ImageDownloader.html', error_message=None)

@ImageDownloader_app.route('/download', methods=['GET'])
def download():
    try:
        url = request.args.get('url')
        image = download_image(url)

        if image:
            img_byte_arr = io.BytesIO()
            # Save the image explicitly in PNG format
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            return send_file(
                io.BytesIO(img_byte_arr),
                mimetype='image/png',
                as_attachment=True,
                download_name='downloaded_image.png'
            )
        else:
            error_message = 'Invalid image format'
            return render_template('ImageDownloader.html', error_message=error_message)

    except ValueError as ve:
        error_message = str(ve)
        return render_template('ImageDownloader.html', error_message=error_message)
    except Exception as e:
        error_message = f'Error downloading image: {e}'
        return render_template('ImageDownloader.html', error_message=error_message)

app = Flask(__name__)
app.register_blueprint(ImageDownloader_app, url_prefix='/imagedownloader')
