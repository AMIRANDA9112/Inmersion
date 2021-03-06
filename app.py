from country_list import countries_for_language
from engine.camera import Camera
from engine.makeup_artist import Makeup_artist
from flask_socketio import SocketIO
from flask_cors import CORS
from flask import Flask, render_template, Response, request
from flask_sqlalchemy import SQLAlchemy
import logging
import os
import pdf2image
from sys import stdout

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_data.db'
db = SQLAlchemy(app)
app.logger.addHandler(logging.StreamHandler(stdout))
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)
camera = Camera(Makeup_artist())


class User(db.Model):
    """Model for Users"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    country = db.Column(db.String)


db.create_all()


@socketio.on('input image', namespace='/test')
def test_message(input):
    input = input.split(",")[1]
    camera.enqueue_input(input)


@socketio.on('connect', namespace='/test')
def test_connect():
    app.logger.info("client connected")


@app.route('/', methods=['GET', 'POST'])
def home():
    """Home page method"""
    return render_template('home.html')


def gen():
    """Video streaming generator function."""
    app.logger.info("starting to generate frames!")
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/streaming')
def index():
    """Video streaming home page."""
    return render_template('index.html')


@app.route('/upload_page', methods=['GET', 'POST'])
def upload_file():
    """Page (Route) for uploading a PDF document"""
    if request.method == "POST":
        file = request.files['file']
        file = file.raw.read()
        pil_image = to_pil(file)
        camera.max = save_img(pil_image)
        camera.charge = True
        return render_template('index.html')
    return render_template('upload_pag.html')


def to_pil(slides):
    """
    Funtion that convert slides from pdf to png format
    :param slides: pdf file
    :return: png images files
    """
    slides = pdf2image.convert_from_bytes(slides, dpi=200,
                                          fmt='png', thread_count=1,
                                          size=(640, 480), poppler_path=None)
    return slides


def save_img(pil_images):

    """
    Function that save images
    :param pil_images: images to save
    :return: number of images
    """
    index = 0
    for image in pil_images:
        image.save("/tmp/page_" + str(camera.user) + str(index) + ".png")
        index += 1
        print("chargue slide No: ", index)
    return index


@app.route('/login', methods=['GET', 'POST'])
def signin():
    """Sign In page route"""
    if request.method == "POST":
        email = request.form["email"]
        camera.user = str(email)
        password = request.form["pswd"]
        if not email:
            message = 'Please fill out this field.'
            return render_template('login.html', message=message)
        if not password:
            return render_template(
                'login.html', message_p='Please fill out this field.')
        user = User.query.filter_by(email=email, password=password).first()
        if user is None:
            return render_template(
                "login.html",
                message_failure="Wrong Credentials. Please Try Again.")
        else:
            return render_template(
                'login.html', message_success="Successful login!!")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Sign Up page route"""
    countries = dict(countries_for_language('en'))
    if request.method == "POST":
        req = request.form
        missing = []
        for field, input in req.items():
            if input == "":
                missing.append(field)

        if missing:
            feedback = " {}".format(', '.join(missing))
            return render_template('signup.html', countries=countries,
                                   feedback=feedback)
        if req["Email"] != req["Confirm email"]:
            return render_template('signup.html', countries=countries,
                                   dont_match="Emails don't match")
        if req["Password"] != req["Confirm password"]:
            return render_template('signup.html', countries=countries,
                                   dont_match="Passwords don't match")
        """adding data to database in SQLAlquemy"""
        new_user = User(first_name=req["First name"], last_name=req["Last name"],
                        email=req["Email"], password=req["Password"],
                        country=req["countries"])
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("signup.html", countries=countries,
                                   feedback="email already exists")
        finally:
            db.session.close()
            return render_template("signup.html", countries=countries,
                                   success="Successful Registration")
    return render_template('signup.html', countries=countries)


@app.route('/about', methods=['GET', 'POST'])
def about():
    """About Us page route"""
    return render_template('about.html')


if __name__ == '__main__':
    socketio.run(app)
