from imutils import face_utils
import dlib
import cv2
from threading import Thread
import numpy as np
from collections import deque
import pyfakewebcam


def antimirror(b, part_face):
    for l in part_face:
        for r in l:
            r[0] = b - r[0]
    return part_face


cap = cv2.VideoCapture(0)

camera = pyfakewebcam.FakeWebcam('/dev/video2', 640, 480)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("../resources/shape_68_dots.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

bag = None
init = "../media/home1.png"

gn = (0, 255, 0)
rd = (0, 0, 255)
nr = (255, 165, 0)
bk = (0, 0, 0)
wt = (255, 255, 255)

im = 1

ret, image = cap.read()
a1, b1, c1 = image.shape

beforey = round((a1 / 100) * 60)
beforex = round((b1 / 100) * 40)

nexty = round((a1 / 100) * 60)
nextx = round((b1 / 100) * 60)

center = None
r = 8
r1 = 0
r2 = 0

r3 = 0

while cap.isOpened():

    ret, image = cap.read()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    rects = detector(gray, 1)

    bg = np.zeros((480, 640, 3), dtype=np.uint8)
    a, b, c = bg.shape

    for (i, rect) in enumerate(rects):

        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        mouth = shape[mStart:mEnd]

        Mouth = cv2.convexHull(mouth)
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)

        Mouth = antimirror(b, Mouth)

        leftEyeHull = antimirror(b, leftEyeHull)

        rightEyeHul = antimirror(b, rightEyeHull)

        x1 = Thread(target=cv2.drawContours, args=(bg, [Mouth], 0, nr, -1))

        x2 = Thread(target=cv2.drawContours, args=(bg, [leftEyeHull], 0, nr, -1))

        x3 = Thread(target=cv2.drawContours, args=(bg, [rightEyeHull], 0, nr, -1))

        c = 0
        for (x, y) in shape:
            c += 1
            if c in [18, 19, 20, 21, 22, 23, 24, 25, 26, 27]:
                cv2.circle(bg, ((b - x), y), 1, wt, -1)

            if c in [28, 29, 30, 31, 32, 33, 34, 35, 36]:
                cv2.circle(bg, ((b - x), y), 1, wt, -1)

            if c in [61, 62, 63, 64, 65, 66, 67, 68]:
                cv2.circle(bg, ((b - x), y), 0, wt, -1)

        x1.start()
        x2.start()
        x3.start()

        pues
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
