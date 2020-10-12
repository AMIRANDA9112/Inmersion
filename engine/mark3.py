"""
An example of using ArUco markers with OpenCV.
"""

import cv2
import cv2.aruco as aruco
import numpy as np

cap = cv2.VideoCapture(0)



fn = 0


while cap.isOpened():
    fn += 1

    im_src = cv2.imread('../media/icon2.png')
    # Capture frame-by-frame

    ret, frame = cap.read()

    org_frame = frame
    # Check if frame is not empty


    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters_create()
    corners, ids, _ = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
    if np.all(ids is not None):

        # print(np.array(corners))
        # print(corners)
        print(ids)
        for c in corners:
            x1 = (c[0][0][0], c[0][0][1])
            x2 = (c[0][1][0], c[0][1][1])
            x3 = (c[0][2][0], c[0][2][1])
            x4 = (c[0][3][0], c[0][3][1])
            im_dst = frame

            size = im_src.shape
            pts_dst = np.array([x1, x2, x3, x4])
            print(pts_dst)
            pts_src = np.array(
                [
                    [0, 0],
                    [size[1] - 1, 0],
                    [size[1] - 1, size[0] - 1],
                    [0, size[0] - 1]
                ], dtype=float
            )

            h, status = cv2.findHomography(pts_src, pts_dst)

            # project corners into frame
            temp = cv2.warpPerspective(im_src.copy(), h, (org_frame.shape[1], org_frame.shape[0]))
            cv2.fillConvexPoly(org_frame, pts_dst.astype(int), 0, 16)

            org_frame = cv2.add(org_frame, temp)
            org_frame = cv2.flip(org_frame, 1)

        cv2.imshow('frame', org_frame)

    else:
        frame = cv2.flip(frame, 1)
        cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
