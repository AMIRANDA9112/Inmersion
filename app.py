from camera import Camera
import celery
import cv2
from country_list import countries_for_language
from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO
import logging
from makeup_artist import Makeup_artist
import numpy
import os
import pdf2image
from sys import stdout
import time
import threading
from utils import base64_to_pil_image, pil_image_to_base64


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
app.logger.addHandler(logging.StreamHandler(stdout))
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)
UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
camera = Camera(Makeup_artist())


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


@app.route('/streaming', methods=['GET', 'POST'])
def upload_file():
    file = request.files['file']
    file = file.raw.read()
    pil_image = to_pil.delay(file)
    camera.max = save_img.delay(pil_image)
    camera.charge = True

    return render_template('index.html')


@celery.task
def to_pil(slides):
    slides = pdf2image.convert_from_bytes(file, dpi=200, fmt='png', thread_count=1,
                                          size=(640, 480), poppler_path=None)
    return slides


@celery.task
def save_img(pil_images):
    index = 1
    for image in pil_images:
        image.save("/tmp/page_" + str(index) + ".png")
        index += 1
    return index

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
