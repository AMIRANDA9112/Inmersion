from imutils import face_utils
import dlib
import cv2
from threading import Thread
import numpy as np
import cv2.aruco as aruco
from collections import deque


def antimirror(b, part_face):
    for l in part_face:
        for r in l:
            r[0] = b - r[0]
    return part_face


cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("../resources/shape_68_dots.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

init = "../media/home1.png"

gn = (0, 255, 0)
rd = (0, 0, 255)
bl = (255, 0, 0)
bk = (0, 0, 0)
wt = (255, 255, 255)

im = 1

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()
pts = deque(maxlen=4)

ret, image = cap.read()
a1, b1, c1 = image.shape

beforey = round((a1 / 100) * 60)
beforex = round((b1 / 100) * 40)

nexty = round((a1 / 100) * 60)
nextx = round((b1 / 100) * 60)

center = None
r = 15
r1 = 0
r2 = 0

r3 = 0

while cap.isOpened():

    ret, image = cap.read()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    rects = detector(gray, 1)

    bg = cv2.imread(init)
    a, b, c = bg.shape
    corners, ids, _ = aruco.detectMarkers(image, aruco_dict, parameters=parameters)

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

        x1 = Thread(target=cv2.drawContours, args=(bg, [Mouth], 0, bk, -1))
        x1.start()
        x2 = Thread(target=cv2.drawContours, args=(bg, [leftEyeHull], 0, bl, -1))
        x2.start()
        x3 = Thread(target=cv2.drawContours, args=(bg, [rightEyeHull], 0, bl, -1))
        x3.start()

        c = 0
        for (x, y) in shape:
            c += 1
            if c in [18, 19, 20, 21, 22, 23, 24, 25, 26, 27]:
                cv2.circle(bg, ((b - x), y), 1, bk, -1)

            if c in [28, 29, 30, 31, 32, 33, 34, 35, 36]:
                cv2.circle(bg, ((b - x), y), 1, rd, -1)

            if c in [61, 62, 63, 64, 65, 66, 67, 68]:
                cv2.circle(bg, ((b - x), y), 0, wt, -1)

    if np.all(ids is not None):

        for c in corners:
            m1 = (c[0][0][0], c[0][0][1])
            x2 = int(b1 - m1[0])
            y2 = int(m1[1])
            center = (x2, y2)
            pts.appendleft(center)

    for i in range(1, len(pts)):

        if pts[i - 1] is None or pts[i] is None:

            continue

        thick = int(np.sqrt(len(pts) / float(i + 1)) * 2.5)
        cv2.line(bg, pts[i - 1], pts[i], (0, 0, 225), thick)

    cv2.imshow('Recognition Laboratory', bg)

    r3 = 0
    if center:
        x3, y3 = center

        if beforex < x3 < nextx:
            r1 = 0

        if 0 < x3 < beforex or nextx < x3 < b1:
            if beforey > y3:
                r1 = 0

        if nextx < x3 < b1 and nexty < y3 < a1:

            r3 = 1
            r1 += 1

            if im <= 3 and r1 == 1 and r2 == 0:
                r1 = 0
                im += 1
                r2 = 1
                sim = str(im)
                init = "../media/home" + sim + ".png"

            if im <= 3 and r1 > r:
                r1 = 0
                r2 = 1
                im += 1
                sim = str(im)
                init = "../media/home" + sim + ".png"

        # Laser section

        if 0 < x3 < beforex and beforey < y3 < a1:
            r3 = 1
            r1 += 1

            if im > 1 and r1 == 1 and r2 == 0:
                r1 = 0
                r2 = 1
                im -= 1
                sim = str(im)
                init = "media/home" + sim + ".png"

            if im > 1 and r1 > r:
                r1 = 0
                r2 = 1
                im -= 1
                sim = str(im)
                init = "../media/home" + sim + ".png"

        if r2 == 1 and r3 == 0:
            r2 = 0
