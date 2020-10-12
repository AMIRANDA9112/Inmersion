import cv2
import numpy as np
import cv2.aruco as aruco

cap = cv2.VideoCapture(0)

# Colores para pintar
colorBlue = (255, 0, 0)
colorYellow = (89, 222, 255)
colorRed = (0, 0, 255)
colorGreen = (0, 255, 0)
ColorWhite = (0, 0, 0)


WlineBlue = 6
WlineYellow = 2
WlineRed = 2
WlineGreen = 2


lineMin = 1
lineMid = 3
LineBig = 4


color = colorBlue  # Color
wLine = 3  # Grosor

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()
x1 = None
y1 = None
imAux = None

while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break

    frameb = frame
    frame = cv2.flip(frame, 1)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if imAux is None:
        imAux = np.zeros(frame.shape, dtype=np.uint8)

    corners, ids, _ = aruco.detectMarkers(frameb, aruco_dict, parameters=parameters)

    # color
    cv2.rectangle(frame, (0, 0), (50, 50), colorYellow, WlineYellow)
    cv2.rectangle(frame, (50, 0), (100, 50), colorRed, WlineRed)
    cv2.rectangle(frame, (100, 0), (150, 50), colorGreen, WlineGreen)
    cv2.rectangle(frame, (150, 0), (200, 50), colorBlue, WlineBlue)

    # limpiar la pantalla
    cv2.rectangle(frame, (300, 0), (400, 50), ColorWhite, 1)
    cv2.putText(frame, 'Restart', (320, 20), 6, 0.6, ColorWhite, 1, cv2.LINE_AA)
    cv2.putText(frame, 'SCREEN', (320, 40), 6, 0.6, ColorWhite, 1, cv2.LINE_AA)

    # grosor
    cv2.rectangle(frame, (490, 0), (540, 50), (0, 0, 0), lineMin)
    cv2.circle(frame, (515, 25), 3, (0, 0, 0), -1)
    cv2.rectangle(frame, (540, 0), (590, 50), (0, 0, 0), lineMid)
    cv2.circle(frame, (565, 25), 7, (0, 0, 0), -1)
    cv2.rectangle(frame, (590, 0), (640, 50), (0, 0, 0), LineBig)
    cv2.circle(frame, (615, 25), 11, (0, 0, 0), -1)

    if np.all(ids is not None):

        for c in corners:
            m1 = (c[0][0][0], c[0][0][1])
            x2 = int(640 - m1[0])
            y2 = int(m1[1])

        if x1 is not None:

            if 0 < x2 < 50 and 0 < y2 < 50:
                color = colorYellow  # Color
                WlineYellow = 6
                WlineRed = 2
                WlineGreen = 2
                WlineBlue = 2

            if 100 > x2 > 50 > y2 > 0:
                color = colorRed  # Color
                WlineYellow = 2
                WlineRed = 6
                WlineGreen = 2
                WlineBlue = 2
            if 100 < x2 < 150 and 0 < y2 < 50:
                color = colorGreen  # Color
                WlineYellow = 2
                WlineRed = 2
                WlineGreen = 6
                WlineBlue = 2
            if 150 < x2 < 200 and 0 < y2 < 50:
                color = colorBlue  # Color
                WlineYellow = 2
                WlineRed = 2
                WlineGreen = 2
                WlineBlue = 6
            if 490 < x2 < 540 and 0 < y2 < 50:
                wLine = 3  # Grosor
                lineMin = 6
                lineMid = 1
                LineBig = 1
            if 540 < x2 < 590 and 0 < y2 < 50:
                wLine = 7  # Grosor
                lineMin = 1
                lineMid = 6
                LineBig = 1
            if 590 < x2 < 640 and 0 < y2 < 50:
                wLine = 11  # Grosor
                lineMin = 1
                lineMid = 1
                LineBig = 6
            if 300 < x2 < 400 and 0 < y2 < 50:
                cv2.rectangle(frame, (300, 0), (400, 50), ColorWhite, 2)
                cv2.putText(frame, 'Restart', (320, 20), 6, 0.6, ColorWhite, 2, cv2.LINE_AA)
                cv2.putText(frame, 'Screen', (320, 40), 6, 0.6, ColorWhite, 2, cv2.LINE_AA)
                imAux = np.zeros(frame.shape, dtype=np.uint8)
            if 0 < y2 < 60 or 0 < y1 < 60:
                imAux = imAux
            else:

                imAux = cv2.line(imAux, (x1, y1), (x2, y2), color, wLine)
        cv2.circle(frame, (x2, y2), wLine, color, 3)
        x1 = x2
        y1 = y2
    else:

        x1, y1 = None, None

    imAuxGray = cv2.cvtColor(imAux, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(imAuxGray, 10, 255, cv2.THRESH_BINARY)
    thInv = cv2.bitwise_not(th)
    frame = cv2.bitwise_and(frame, frame, mask=thInv)
    frame = cv2.add(frame, imAux)

    cv2.imshow('imAux', imAux)
    cv2.imshow('frame', frame)

    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
