#!/bin/python3
import numpy as np
from PIL import Image

class ImageRestore:
    
    #list of resolutions, used to translate between dpi and image size, 
    #assuming letter sized paper
    resolutions = { 
        "150" : (1650, 1275),
        "200" : (2200, 1700),
        "300" : (3300, 2550)
    }

    #list of pixels, used to select method to resample if option is selected
    filters = {
        "nearest"   : Image.NEAREST,
        "box"       : Image.BOX,
        "bilinear"  : Image.BILINEAR,
        "hamming"   : Image.HAMMING,
        "bicubic"   : Image.BICUBIC,
        "lanczos"   : Image.LANCZOS
    }

    def __init__(self):
        '''
        Constructor
            Input: none
            Output: a new object of this class
        All values set should be overwritten later
        '''
        self.inImage = Image.new('RGBA', [0, 0])    #input image loaded from file
        self.outImage = Image.new('L', [0, 0])      #output image created
        self.pixelArray = np.empty((0,0), np.uint8) #image being processed 
                                                    #stored in a numpy array
        self.outputSize = "300"                     #sets output size in dpi

    def prepare(self, filename, size, resample=False, filterName="bicubic"):
        '''
        prepares image for machine learning module
            Input: 
                filename: string file path to input image, 
                size: in dpi as a string, 
                resample: bool selecting if image should be resampled,
                filtername: string used to select filter to be used in resampling
            Output:
                0 if successful, -1 if not
        Calls all functions needed to prepare an image for the machine learning 
        model in order
        '''
        if (self.openImage(filename) < 0):
            return -1
        self.setOutputResolution(size)
        self.convertToGreyscale()
        if resample:
            self.resizeImage(filterName)
        self.createPixelArray()
        self.padImage()
        return 0

    def outputImage(self, filename):
        '''
        calls functions required to prepare image to be saved and then saves the
        image
            Input:
                filename: string file path indicating where to save image
            Output:
                0 if successful, -1 if not
        '''
        self.pixelArrayToImage()
        return self.saveOutputImage(filename)

    def openImage(self, filename):
        '''
        Opens image at filename
            Input:
                filename: string file path to input image
            Output:
                0 if successful, -1 if not
        '''
        try:
            self.inImage = Image.open(filename)
            return 0

        except IOError:
            print("Error:  Input file path not valid")
            return -1
    
    def setOutputResolution(self, size):
        '''
        Sets output size to specified size
            Input:
                size: in dpi as a string or orig to autodetect
            Output:
                none
        '''
        #check if valid dpi is specified
        if size in self.resolutions:
            self.outputSize = size
            return

        #autodetect resolution by selecting lowest dpi setting that is at least 
        #as large as input
        for name, coord in sorted(self.resolutions.items()):
            if self.inImage.size <= coord:
                self.outputSize = name
                return
        self.outputSize = "300"     #image is too large so default to 300

    def convertToGreyscale(self):
        '''
        Converts inImage to greyscale
            Input:
                none
            Output:
                none
        '''
        self.inImage = self.inImage.convert('L')    #use PIL convert function

    def resizeImage(self, filterName):
        '''
        Resizes input image to specified output size
            Input:
                filtername: string used to select filter to be used in resampling
            Output:
                none
        '''
        self.inImage = self.inImage.resize((
            self.resolutions[self.outputSize][1],   #coordinates are reversed
            self.resolutions[self.outputSize][0]), 
            self.filters[filterName])

    def createPixelArray(self):
        '''
        Creates a pixel array from inImage
            Input:
                none
            Output:
                none
        '''
        self.pixelArray = np.fromstring(self.inImage.tobytes(), dtype=np.uint8)
        self.pixelArray.shape = (self.inImage.size[1], self.inImage.size[0])

    def padImage(self):
        '''
        Pads pixelArray to conform with model if needed
            Input:
                none
            Output:
                none
        '''
        #check if shape is already correct
        if self.pixelArray.shape == self.resolutions[self.outputSize]:
            return
        #create a new array that is the correct size full of pad value
        newArr = np.zeros(self.resolutions[self.outputSize], dtype=np.uint8)
        #copy pixelArray to new array, extra spaces are padded
        for i in range(self.pixelArray.shape[0]):
            for j in range(self.pixelArray[i].size):
                newArr[i][j] = self.pixelArray[i][j]
        #set pixelArray to newArr
        self.pixelArray = newArr

    def pixelArrayToImage(self):
        '''
        Converts pixelArray to a greyscale PIL image
            Input:
                none
            Output:
                none
        '''
        self.outImage = Image.fromarray(self.pixelArray, 'L')   #use PIL method 
                                                                #to convert

    def saveOutputImage(self, filename):
        '''
        Saves image to specified filename
            Input:
                filename: string file path indicating where to save image
            Output:
                0 if successful, -1 if not
        '''
        try:
            self.outImage.save(filename)
            return 0
        except IOError:
            print("Error:  Image could not be saved")
            return -1

    def printArray(self):
        '''
        Method used for debugging. Prints a portion of pixelArray
            Input:
                none
            Output:
                none
        '''
        for i in self.pixelArray[0:10]:
            print(i[0:10])
