from io import BytesIO # Allows us to take the binary from the db and convert to a format that flask can use to regen data

from flask import Flask, render_template, redirect, url_for, request, send_file, session, flash
from PDF_functions import *
from PDF_functions.Image_to_PDF import image_to_pdf, convert_image_to_pdf
from flask_sqlalchemy import SQLAlchemy
from reportlab.pdfgen import canvas
from datetime import timedelta
'''
Lets make stright functionality before visual
'''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is the key baby!'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.permanent_session_lifetime = timedelta(minutes=5) 

db = SQLAlchemy(app)

# Columns: id, filename, data
'''
Current Implementation: Storing the data diretly to the db, may not perform so well
Future implementation: Store this on a file system or S3, and store metadata on the db

ToDo: Add another database to store loggedin users, track their pdf attachments, 1 to many relationship
'''

# One to many relationship
# One to many relationship
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50))
    name = db.Column(db.String(50))
    password = db.Column(db.String(50)) # String or soemthing similar, make sure to hash this for security reasons and add SALT (Boi's got salt)
    # A pdf can have 1 or many modfied files 
    posts = db.relationship('Parent', backref='user', lazy=True) #The relational connection from one db to another

class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
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
    return render_template('homepage.html')

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

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    # Submit should be GET, create should be POST
    if 'signup' in request.form:
        nonmatch = None
        username = request.form["username"] 
        password = request.form["password"]
        email = request.form["email"]
        name = request.form["name"]
        confirm_password = request.form["confirm_password"]
        if confirm_password != password:
            nonmatch  = "Passwords do not match"
            return render_template('login_signup.html', nonmatch=nonmatch)
        print(username)
        print(password)
        session['username'] = username
        upload = users(name=name, username=username, password=password, email=email)
        upload_data(upload)
        return redirect(url_for('home'))
    elif 'login' in request.form:
        error = None
        username = request.form.get('username')
        password = request.form.get('password')
        print(username)
        print(password)
        # Check if passwords and username exists
        upload = users.query.filter_by(username=username).first()
        if upload:
        # User with the specified username exists
        # Perform further actions
            if upload.password == password:
                session['username'] = username
            else:
                error = "Invalid username or password"
                return render_template('login_signup.html', error=error)
        else:
            # User with the specified username doesn't exist
            # Handle this case accordingly
            error = "Invalid username or password"
            return render_template('login_signup.html', error=error)
    
    return render_template('login_signup.html')

# Recombine this with user_login section, but with different post request naming variables
@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    error = None
    username = request.form.get('username')
    password = request.form.get('password')
    print(username)
    print(password)
    
    # Check if passwords and username exists
    upload = users.query.filter_by(username=username).first()
    if upload:
    # User with the specified username exists
    # Perform further actions
        if upload.password == password:
            session['username'] = username
    else:
        # User with the specified username doesn't exist
        # Handle this case accordingly
        error = "Invalid username or password"
        return render_template('login_signup.html', error=error)

if __name__ == '__main__':
    # Create the database tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)