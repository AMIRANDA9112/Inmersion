import threading
import binascii
from time import sleep
from utils import base64_to_pil_image, pil_image_to_base64
import base64
import numpy as np
import cv2
import dlib
import cv2.aruco as aruco
from collections import deque


class Camera(object):
    def __init__(self, makeup_artist):
        self.to_process = []
        self.to_output = []
        self.makeup_artist = makeup_artist
        self.face_detector = dlib.get_frontal_face_detector()
        self.landmark_detector = dlib.shape_predictor("./resources/shape_68_dots.dat")
        self.handetector = dlib.fhog_object_detector('./resources/HandDetector.svm')
        self.pts = deque(maxlen=4)

        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

    def process_one(self):
        if not self.to_process:
            return

        input_str = self.to_process.pop(0)

        im_bytes = base64.b64decode(input_str)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
        input_str = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

        output_img = self.makeup_artist.apply_makeup(input_str, self.handetector, self.pts, self.face_detector, self.landmark_detector)

        self.pts = output_img[1]

        im_bytes = output_img[0].tobytes()

        imgf = base64.b64encode(im_bytes)

        self.to_output.append(binascii.a2b_base64(imgf))

    def keep_processing(self):
        while True:
            self.process_one()
            sleep(0.01)

    def enqueue_input(self, input):
        self.to_process.append(input)

    def get_frame(self):
        while not self.to_output:
            sleep(0.05)
        return self.to_output.pop(0)
