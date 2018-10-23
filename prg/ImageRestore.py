#!/bin/python3

import numpy as np
from PIL import Image

class ImageRestore:
    def __init__(self):
        self.inImage = Image.new('RGBA', [0, 0])
        self.outImage = Image.new('RGBA', [0, 0])
        self.pixelArray = np.empty((0,0), np.int8)

    def prepare(self, filename):
        self.openImage(filename)
        self.convertToGreyscale()
        self.createPixelArray()

    def openImage(self, filename):
        try:
            self.inImage = Image.open(filename)
        except IOError:
            print("Error:  Input file path not valid")
            return -1
    
    def convertToGreyscale(self):
        self.inImage = self.inImage.convert('L')

    def createPixelArray(self):
        self.pixelArray = np.fromstring(self.inImage.tobytes(), dtype=np.uint8)
        self.pixelArray = self.pixelArray.reshape((self.inImage.size[0], self.inImage.size[1]))
        for i in self.pixelArray:
            print(i)
