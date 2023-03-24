import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from google.cloud import storage
from models import db

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

csrf = CSRFProtect(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'

# Set your environment variable with your Google Cloud JSON key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./storage-key.json"

# Set your Google Cloud Storage bucket name
BUCKET_NAME = "moni-lab-tests"

storage_client = storage.Client()
bucket = storage_client.get_bucket(BUCKET_NAME)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Log In')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Sign Up')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def home():
    return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file part'})
        
        file = request.files['file']

        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No selected file'})

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Save the file to Google Cloud Storage
            blob = bucket.blob(filename)
            blob.upload_from_string(
                file.read(),
                content_type=file.content_type
            )
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'File type not allowed'})

    return render_template('upload.html')

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@app.route('/login_action', methods=['POST'])
def login_action():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid username or password'})
    else:
        return jsonify({'status': 'error', 'message': 'Form validation failed'})
    

@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')


@app.route('/signup_action', methods=['POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if User.query.filter_by(username=username).first():
            return jsonify({'status': 'error', 'message': 'Username already exists. Please choose a different one.'})

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Form validation failed'})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
