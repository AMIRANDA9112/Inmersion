import base64
from imutils import face_utils
import imutils
import dlib
import cv2
from threading import Thread
import numpy as np
import cv2.aruco as aruco
from collections import deque


class Makeup_artist(object):
    def __init__(self):
        pass

    def antimirror(self, b, part_face):
        for l in part_face:
            for r in l:
                r[0] = b - r[0]
        return part_face

    def apply_makeup(self, image, handdetector, face, landmark, background, count, max, r1, r2):

        detector = face
        predictor = landmark
        handpredictor = handdetector

        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

        bg = background

        gn = (0, 255, 0)
        rd = (0, 0, 255)
        bl = (255, 0, 0)
        bk = (0, 0, 0)
        wt = (255, 255, 255)

        a1, b1, c1 = image.shape

        beforey = round((a1 / 100) * 60)
        beforex = round((b1 / 100) * 40)

        nexty = round((a1 / 100) * 60)
        nextx = round((b1 / 100) * 60)

        im = count
        center = None
        r = 8
        r1 = 0
        r2 = 0

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        handrects = handpredictor(gray, 1)
        rects = detector(gray, 1)

        for (i, rect) in enumerate(rects):

            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            mouth = shape[mStart:mEnd]

            Mouth = cv2.convexHull(mouth)
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)

            Mouth = self.antimirror(b1, Mouth)

            leftEyeHull = self.antimirror(b1, leftEyeHull)

            rightEyeHull = self.antimirror(b1, rightEyeHull)

            x1 = Thread(target=cv2.drawContours, args=(bg, [Mouth], 0, bk, -1))

            x2 = Thread(target=cv2.drawContours, args=(bg, [leftEyeHull], 0, bl, -1))

            x3 = Thread(target=cv2.drawContours, args=(bg, [rightEyeHull], 0, bl, -1))
            x3.start()
            x1.start()
            x2.start()

            c = 0
            for (x, y) in shape:
                c += 1
                if c in [18, 19, 20, 21, 22, 23, 24, 25, 26, 27]:
                    cv2.circle(bg, ((b1 - x), y), 1, bk, -1)

                if c in [28, 29, 30, 31, 32, 33, 34, 35, 36]:
                    cv2.circle(bg, ((b1 - x), y), 1, rd, -1)

                if c in [61, 62, 63, 64, 65, 66, 67, 68]:
                    cv2.circle(bg, ((b1 - x), y), 1, wt, -1)

        if handrects:

            for (i, hrect) in enumerate(handrects):
                l = int(hrect.left())
                r = int(hrect.right())
                t = int(hrect.top())
                center = (b1 - round(l + (r - l) / 2), t)
                cv2.circle(bg, center, 4, rd, -1)

        _, im_arr = cv2.imencode('.jpg', bg)  # im_arr: image in Numpy one-dim array format.

        r3 = 0
        if center:
            axix, axiy = center

            if beforex < axix < nextx:
                r1 = 0

            if 0 < axix < beforex or nextx < axix < b1:
                if beforey > axiy:
                    r1 = 0

            if nextx < axix < b1 and nexty < axiy < a1:

                r3 = 1
                r1 += 1

                if im <= max and r1 == 1 and r2 == 0:
                    im += 1
                    r2 = 1

                if im <= max and r1 > r:
                    r1 = 0
                    r2 = 1
                    im += 1

            # Laser section

            if 0 < axix < beforex and beforey < axiy < a1:
                r3 = 1
                r1 += 1

                if im > 1 and r1 == 1 and r2 == 0:
                    r2 = 1
                    im -= 1

                if im > 0 and r1 > r:
                    r1 = 0
                    r2 = 1
                    im -= 1

            if r2 == 1 and r3 == 0:
                r2 = 0

        return im_arr, im, r1, r2
