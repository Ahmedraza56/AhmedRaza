from flask import Flask, render_template, request
from bgremove import bgremove_app
from text_to_speech import text_to_speech_app
from textDetector import textDetector_app
from WebScrapingTool import WebScrapingTool_app
from webtopng import webtopng_app
from mbtokb import mbtokb_app
from VideoAudioSplitter import VideoAudioSplitter_app
from ImageDownloader import ImageDownloader_app

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 


@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(bgremove_app, url_prefix='/bgremove')
app.register_blueprint(text_to_speech_app, url_prefix='/text_to_speech')
app.register_blueprint(textDetector_app, url_prefix='/textDetector')
app.register_blueprint(WebScrapingTool_app, url_prefix='/WebScrapingTool')
app.register_blueprint(webtopng_app, url_prefix='/webtopng')
app.register_blueprint(mbtokb_app, url_prefix='/mbtokb')  
app.register_blueprint(VideoAudioSplitter_app, url_prefix='/VideoAudioSplitter')  
app.register_blueprint(ImageDownloader_app, url_prefix='/ImageDownloader')

if __name__ == '__main__':
    app.run(port=8002)