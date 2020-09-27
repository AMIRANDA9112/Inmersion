import cv2
import numpy as np

def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(encoded_data.decode('base64'), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

data_uri = "data:image/jpeg;base64,/9j/4AAQ..."
img = data_uri_to_cv2_img(data_uri)
cv2.imshow(img)
