from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import cv2, base64
import numpy as np
from focus_detect import focus

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
#app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///penis.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:harshil@35.202.242.209/main'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password_hash = db.Column(db.String(256))
    score = db.Column(db.Integer)
    def __repr__(self):
        return username

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Re-enter Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Create Account")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET'])
def index():
    return render_template('mainpage.html')

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    users = User.query.order_by(desc(User.score))
    return render_template('leaderboard.html', users=users)

@app.route('/home', methods=['GET'])
def home():
    return render_template('tool.html')

@app.route('/points', methods=['POST'])
def points():
    user = load_user(current_user.id)
    user.score = user.score + int(request.values['points'])
    db.session.commit()
    return 'owo'
    
@app.route('/predict', methods=['POST'])
def predict():
    data_url = request.values['file']
    img_bytes = base64.b64decode(data_url)
    img = np.asarray(bytearray(img_bytes), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    eyes = eyeCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2, minSize=(40, 40))

    print("[INFO] Found {0} eyes.".format(len(eyes)))

    eye = (0, 0, 0, 0)
    for (x, y, w, h) in eyes:
        if w > eye[2] and h > eye[3]:            
            eye = (x, y, w, h)

    roi_color = img[eye[1]:eye[1] + eye[3], eye[0]:eye[0] + eye[2]]
    
    roi_color = cv2.resize(roi_color, (100, 100))
    #print("[INFO] Object found. Saving locally.")
    cv2.imwrite('file.jpg', roi_color)

    hi = focus('file.jpg')
    return hi

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password_hash, form.password.data):  
            login_user(user)
            return redirect(url_for('home', _external=True, _scheme='http'))
        else:
            error = "invalid credentials"
    else:
        flash(form.errors)

    return render_template('login.html', users=User.query.all(), form=LoginForm(), error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).count() > 0:
            error = "User already exists"
        else:
            try:
                db.session.add(User(username=form.username.data, password_hash=generate_password_hash(form.password.data), score=0))
                db.session.commit()
                return redirect(url_for('login', _external=True, _scheme='http'))
            except:
                db.session.rollback()
    else:
        flash(form.errors)

    return render_template('register.html', users=User.query.all(), form=RegisterForm(), error=error)
    
if __name__ == "__main__": 
    app.run()

