from flask import Flask, render_template, request

from test import test_app


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(test_app, url_prefix='/test')


if __name__ == '__main__':
    app.run(port=8002,debug=True)