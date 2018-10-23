#!/bin/python3

from PIL import Image

class ImageRestore:
    inImage
    outImage

    def openImage(filename):
        try:
            inImage = Image.open(filename)
        except IOError:
            print("Error:  Input file path not valid")
            return -1
    
    def convertToGreyscale():
        inImage = inImage.convert('L')

    
