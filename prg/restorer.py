<<<<<<< HEAD

from PIL import Image
from PIL import ImageFilter
=======
#!/usr/bin/python3
from parseCLI import parseCLI
from ImageRestore import ImageRestore

def main():
    #get arguments from CLI
    args = parseCLI()

    #store arguments into variables for future usage
    inputFilePath = getattr(args, 'input file path')[0]
    outputFilePath = getattr(args, 'output file path')[0]
    outputSize = getattr(args, 'size')
    resample = getattr(args, 'resample')
    filterName = getattr(args, "filter")

    #instantiate image restore object
    ir = ImageRestore()

    #image preprocessing, exits program if image fails to load properly
    if (ir.prepare(inputFilePath, outputSize, resample, filterName) < 0):
        return -1

    #call machine learning method
    ir.outputImage(outputFilePath)

    #print(args)                 #debug
    #print("End of main")        #debug
>>>>>>> f447455e00fa953e27ab5b7e63f5408f93668df4

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

