
from PIL import Image
from PIL import ImageFilter

def threshold(p):
    if 0 <= p < 120:
        return 0
    elif 120 <= p < 140:
        return 120
    elif 140 <= p < 160:
        return 140
    elif 160 <= p < 180:
        return 160
    elif 180 <= p < 200:
        return 180
    else:
        return 255

def restore(image):
    # convert to grayscale
    image = image.convert('L')
    # resize to 300 DPI
    image = image.resize((2550, 3300), Image.LANCZOS)
    # image preprocessing
    image = image.filter(ImageFilter.GaussianBlur(1))
    image = image.point(threshold)
    return image

