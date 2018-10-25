#!/bin/python3

import numpy as np
from PIL import Image

class ImageRestore:
    
    resolutions = { 
        "150" : (1275, 1650),
        "200" : (1700, 2200),
        "300" : (2550, 3300)
    }

    def __init__(self):
        self.inImage = Image.new('RGBA', [0, 0])
        self.outImage = Image.new('L', [0, 0])
        self.pixelArray = np.empty((0,0), np.uint8)
        self.outputSize = "300"

    def prepare(self, filename):
        if (self.openImage(filename) < 0):
            return -1
        self.convertToGreyscale()
        self.createPixelArray()
        self.padImage()
        self.printArray()
        return 0

    def outputImage(self, filename):
        self.pixelArrayToImage()
        return self.saveOutputImage(filename)

    def openImage(self, filename):
        try:
            self.inImage = Image.open(filename)
            return 0
        except IOError:
            print("Error:  Input file path not valid")
            return -1
    
    def convertToGreyscale(self):
        self.inImage = self.inImage.convert('L')

    def createPixelArray(self):
        self.pixelArray = np.fromstring(self.inImage.tobytes(), dtype=np.uint8)
        self.pixelArray.shape = (self.inImage.size[0], self.inImage.size[1])

    def padImage(self):
        if self.pixelArray.shape == self.resolutions[self.outputSize]:
            return
        newArr = np.zeros(self.resolutions[self.outputSize], dtype=np.uint8)
        for i in range(self.pixelArray.shape[0]):
            for j in range(self.pixelArray[i].size):
                newArr[i][j] = self.pixelArray[i][j]
        self.pixelArray = newArr

    def pixelArrayToImage(self):
        self.outImage = Image.fromarray(self.pixelArray, 'L')

    def saveOutputImage(self, filename):
        try:
            self.outImage.save(filename)
            return 0
        except IOError:
            print("Error:  Image could not be saved")
            return -1

    def printArray(self):
        for i in self.pixelArray[0:20]:       #debug
            print(i[0:20])
