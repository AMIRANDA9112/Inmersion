import base64
import cv2
import numpy as np


class Makeup_artist(object):
    def __init__(self):
        pass

    def apply_makeup(self, img):

        im_bytes = base64.b64decode(img)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, im_arr = cv2.imencode('.jpg', gray)  # im_arr: image in Numpy one-dim array format.
        im_bytes = im_arr.tobytes()

        imgf = base64.b64encode(im_bytes)

        return imgf
