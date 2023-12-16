from flask import Flask, render_template, request
from bgremove import bgremove_app
from text_to_speech import text_to_speech_app
from textDetector import textDetector_app
from WebScrapingTool import WebScrapingTool_app
from webtopng import webtopng_app

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(bgremove_app, url_prefix='/bgremove')
app.register_blueprint(text_to_speech_app, url_prefix='/text_to_speech')
app.register_blueprint(textDetector_app, url_prefix='/textDetector')
app.register_blueprint(WebScrapingTool_app, url_prefix='/WebScrapingTool')
app.register_blueprint(webtopng_app, url_prefix='/webtopng')

if __name__ == '__main__':
    app.run(port=8002,debug=True)