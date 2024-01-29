from flask import Flask, render_template, redirect, url_for, request
from PDF_functions import *
from flask_sqlalchemy import SQLAlchemy
'''
Lets make stright functionality before visual
'''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is the key baby!'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

# Columns: id, filename, data
'''
Current Implementation: Storing the data diretly to the db, may not perform so well
Future implementation: Store this on a file system or S3, and store metadata on the db
'''
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary) # Store arbitrary binary


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('index_coffee.html')

@app.route('/upload', methods=['GET', 'POST'])
def new_page():
    if request.method == 'POST':
        file = request.files['file']
        print(file.filename)
        return f'Uploaded {file.filename}'
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)