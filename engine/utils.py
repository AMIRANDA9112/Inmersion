import base64
from io import BytesIO
from PIL import Image

"""
Scripts wih two functions, one to convert PIL_image object to base64 and other make the
inverse transformation
"""


def pil_image_to_base64(pil_image):
    """Function that translate string image to bite image"""
    buf = BytesIO()
    pil_image.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue())


def base64_to_pil_image(base64_img):
    """Function that translate bite image to string image"""
    return Image.open(BytesIO(base64.b64decode(base64_img)))
