#!/bin/python3

import numpy as np
from PIL import Image

class ImageRestore:
    
    resolutions = { 
        "150" : (1650, 1275),
        "200" : (2200, 1700),
        "300" : (3300, 2550)
    }

    filters = {
        "nearest" : Image.NEAREST,
        "box" : Image.BOX,
        "bilinear" : Image.BILINEAR,
        "hamming" : Image.HAMMING,
        "bicubic" : Image.BICUBIC,
        "lanczos" : Image.LANCZOS
    }

    def __init__(self):
        self.inImage = Image.new('RGBA', [0, 0])
        self.outImage = Image.new('L', [0, 0])
        self.pixelArray = np.empty((0,0), np.uint8)
        self.outputSize = "300"

    def prepare(self, filename, size, resample, filterName):
        if (self.openImage(filename) < 0):
            return -1
        self.setOutputResolution(size)
        self.convertToGreyscale()
        if resample:
            self.resizeImage(filterName)
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
    
    def setOutputResolution(self, size):
        if size in self.resolutions:
            self.outputSize = size
            return
        for name, coord in sorted(self.resolutions.items()):
            print(self.inImage.size, '\t', coord)       #debug
            
            if self.inImage.size <= coord:
                self.outputSize = name
                return
        self.outputSize = "300"     #image is too large

    def convertToGreyscale(self):
        self.inImage = self.inImage.convert('L')

    def resizeImage(self, filterName):
        self.inImage = self.inImage.resize((self.resolutions[self.outputSize][1], self.resolutions[self.outputSize][0]), self.filters[filterName])
        print(self.inImage.size)

    def createPixelArray(self):
        self.pixelArray = np.fromstring(self.inImage.tobytes(), dtype=np.uint8)
        self.pixelArray.shape = (self.inImage.size[1], self.inImage.size[0])

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
        for i in self.pixelArray[0:10]:       #debug
            print(i[0:10])
