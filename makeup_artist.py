import base64
import cv2
import numpy as np


class Makeup_artist(object):
    def __init__(self):
        pass

    def apply_makeup(self, img):
        print(img, "inputmakeup")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, im_arr = cv2.imencode('.jpg', gray)  # im_arr: image in Numpy one-dim array format.

        print(im_arr, "outputmakeup")

        return im_arr
