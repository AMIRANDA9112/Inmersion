import binascii
import base64
from collections import deque
import cv2
import dlib
import numpy as np
import threading
from time import sleep

"""
Create Class Camera that receive, transform and send the frames from client in API
"""


class Camera(object):
    def __init__(self, makeup_artist):
        self.to_process = deque(maxlen=2)
        self.to_output = deque(maxlen=2)
        self.makeup_artist = makeup_artist
        self.face_detector = dlib.get_frontal_face_detector()
        self.landmark_detector = dlib.shape_predictor("./resources/shape_68_dots.dat")
        self.handetector = dlib.fhog_object_detector('./resources/HandDetector.svm')
        self.count = 0
        self.max = 0
        self.charge = False
        self.user = "None"
        self.background = cv2.imread("./media/home1.png")
        self.r1 = 0
        self.r2 = 0

        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

    def process_one(self):
        """
        This method transform image string-bit-string and app the makeup_artist
        function


        :return: Slide with avatar
        """
        if not self.to_process:
            return

        input_str = self.to_process.popleft()

        im_bytes = base64.b64decode(input_str)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
        input_str = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

        if self.charge:
            self.background = cv2.imread("/tmp/page_" + str(self.user) + str(self.count) + ".png")
            print("image read")
        else:
            print("image no read")

        if self.background is None:
            self.background = cv2.imread("./media/home1.png")

        output_img = self.makeup_artist.apply_makeup(input_str, self.handetector, self.face_detector,
                                                     self.landmark_detector, self.background, self.count, self.max,
                                                     self.r1, self.r2)

        self.r1 = output_img[2]
        self.r2 = output_img[3]
        self.count = output_img[1]

        print("fps No: " + str(self.r1) + "slide No: " + str(self.count) + "buttom activate: " + str(self.r2))
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
        return self.to_output.popleft()
