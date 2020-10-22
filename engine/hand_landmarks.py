from __future__ import print_function
from imutils import face_utils
import numpy as np
import imutils
import cv2
import dlib

cap = cv2.VideoCapture(0)

detector = dlib.fhog_object_detector('../resources/HandDetector.svm')
predictor = dlib.shape_predictor("../resources/Hand_9_Landmarks_Detector.dat")

while cap.isOpened():

    ret, image = cap.read()

    image = cv2.flip(image, 1)

    detections = detector(image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)

    for (i, rect) in enumerate(rects):
        l = int(rect.left())
        r = int(rect.right())
        t = int(rect.top())
        center = (round(l + ((r - l)/2)), t)

        print(center)

    cv2.imshow('Recognition Laboratory', image)

    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
