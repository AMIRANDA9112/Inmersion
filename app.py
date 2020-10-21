from sys import stdout
from makeup_artist import Makeup_artist
import logging
from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO
from camera import Camera
from utils import base64_to_pil_image, pil_image_to_base64
from country_list import countries_for_language
import pdf2image
import time
import cv2
import os


app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(stdout))
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)
UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
PIL_IMAGE = []
base_image = cv2.imread("./media/home1.png")
PIL_IMAGE.append(base_image)
MAX = 1
camera = Camera(Makeup_artist(), PIL_IMAGE, MAX)


@socketio.on('input image', namespace='/test')
def test_message(input):
    input = input.split(",")[1]
    camera.enqueue_input(input)


@socketio.on('connect', namespace='/test')
def test_connect():
    app.logger.info("client connected")


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/streaming')
def index():
    """Video streaming home page."""
    return render_template('index.html')


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

@app.route('/upload_page')
def start_page():
    """Slides upload section"""
    return render_template('upload_pag.html')


@app.route('/upload', methods=['POST'])
def upload_file():

    file = request.files['slide']

    PIL_IMAGE = pdf2image.convert_from_bytes(file, dpi=200, fmt='png', thread_count=1, size=(640, 480))
    index = 0
    for image in pil_images:
        index += 1
    MAX = index
    return inrender_template('upload_pag.html', slides=str(index))

    # Save file
    # filename = 'static/' + file.filename
    # file.save(filename)


@app.route('/login', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["pswd"]
        if not email:
            message = 'Please fill out this field.'
            return render_template('login.html', message=message)
        if not password:
            return render_template('login.html', message_p='Please fill out this field.')
        return render_template('login.html', message_success="Successful login!!")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    countries = dict(countries_for_language('en'))
    if request.method == "POST":
        name = request.form["name"]

        if name:
            return render_template('signup.html', name="Please fill out this field.")
    return render_template('signup.html', countries=countries)


if __name__ == '__main__':
    socketio.run(app)
