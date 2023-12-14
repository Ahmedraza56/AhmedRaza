from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Form se data nikalo
        user_name = request.form['user_name']
        return render_template('index.html', user_name=user_name)
    return render_template('index.html')

if __name__ == '_main_':
    app.run(debug=True)
