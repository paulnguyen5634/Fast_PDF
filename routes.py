from io import BytesIO # Allows us to take the binary from the db and convert to a format that flask can use to regen data

from flask import Flask, render_template, redirect, url_for, request, send_file
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
        
        # Uploading the data onto the database
        upload = Upload(filename=file.filename, data = file.read())
        db.session.add(upload)
        db.session.commit()

        return f'Uploaded {file.filename}'
    
    return render_template('upload.html')

@app.route('/merge', methods=['GET', 'POST'])
def merge():
    if request.method == 'POST':
        file = request.files['file']
        
        # Uploading the data onto the database
        upload = Upload(filename=file.filename, data = file.read())
        db.session.add(upload)
        db.session.commit()

        return f'Uploaded {file.filename}'
    
    return render_template('merge_pdf.html')

# TODO: Make a redirect to a new page for downloading data -> Save altered pdf_id into the session as to redirect to download
@app.route('/download/<upload_id>')
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), download_name=upload.filename, as_attachment=True)

if __name__ == '__main__':
    # Create the database tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)