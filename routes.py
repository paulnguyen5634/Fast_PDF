from io import BytesIO # Allows us to take the binary from the db and convert to a format that flask can use to regen data

from flask import Flask, render_template, redirect, url_for, request, send_file
from PDF_functions import *
from PDF_functions.Image_to_PDF import image_to_pdf, convert_image_to_pdf
from flask_sqlalchemy import SQLAlchemy
from reportlab.pdfgen import canvas
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

ToDo: Add another database to store loggedin users, track their pdf attachments, 1 to many relationship
'''

# One to many relationship
class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary) # Store arbitrary binary
    # A pdf can have 1 or many modfied files 
    posts = db.relationship('Child', backref='parent', lazy=True)

class Child(db.Model): # Will hold modified PDF for downloading, composit key
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary) # Store arbitrary binary
    user_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=False) # Looks to backref (parent) and checks the id

# Relational DB, primary: pdf#, fori

def upload_data(data):
    db.session.add(data)
    db.session.commit()
    return

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('index_coffee.html')

@app.route('/upload', methods=['GET', 'POST'])
def new_page():
    if request.method == 'POST':
        file = request.files['file']
        
        # Uploading the data onto the database
        upload = Parent(filename=file.filename, data = file.read())
        db.session.add(upload)
        db.session.commit()

        return f'Uploaded {file.filename}'
    
    return render_template('upload.html')

@app.route('/merge', methods=['GET', 'POST'])
def merge():
    if request.method == 'POST':
        file = request.files['file']
        
        # Uploading the data onto the database
        upload = Parent(filename=file.filename, data = file.read())
        upload_data(upload)

        return f'Uploaded {file.filename}'
    
    return render_template('merge_pdf.html')

@app.route('/image-to-pdf', methods=['GET', 'POST'])
def IMG_to_PDF():
    if request.method == 'POST':
        file = request.files['file']
        
        # Uploading the data onto the database
        upload = Parent(filename=file.filename, data = file.read())
        upload_data(upload)

        pdf_id = upload.id
        pdf_data = convert_image_to_pdf(upload.data)

        # Pass the bytes of the PDF data to the Child model
        modupload = Child(data=pdf_data.read(), user_id=pdf_id)
        upload_data(modupload)

        return redirect(url_for('download_child', upload_id=modupload.id))
    
    return render_template('img_to_pdf.html')

# TODO: Make a redirect to a new page for downloading data -> Save altered pdf_id into the session as to redirect to download
@app.route('/download/<upload_id>')
def download(upload_id):
    upload = Parent.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), download_name=upload.filename, as_attachment=True)

@app.route('/download_child/<upload_id>')
def download_child(upload_id):
    upload = Child.query.filter_by(id=upload_id).first()

    if not upload:
        return "File not found"

    # Convert upload.id to a string for download_name
    download_name = str(upload.id)

    return send_file(BytesIO(upload.data), download_name=f'{download_name}.pdf', as_attachment=True)

@app.route('/downloads')
def downloadsPage():
    return render_template('download.html')

if __name__ == '__main__':
    # Create the database tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)