from flask import Flask, render_template, redirect, url_for, request
from PDF_functions import *
from flask_sqlalchemy import SQLAlchemy
'''
Lets make stright functionality before visual
'''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is the key baby!'

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('index_coffee.html')

@app.route('/upload', methods=['GET', 'POST'])
def new_page():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)