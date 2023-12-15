from flask import Flask, request,render_template,Blueprint

test_app = Blueprint('test',__name__)

@test_app.route('/')
def index():
    return render_template('test.html') 



