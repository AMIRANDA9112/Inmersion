import cv2


class Makeup_artist(object):
    def __init__(self):
        pass

    def apply_makeup(self, img):

        image = cv2.imread(cv2.flip(img, 0))
        return image
