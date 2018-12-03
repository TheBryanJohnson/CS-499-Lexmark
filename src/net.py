
import numpy
numpy.random.seed(1)
from PIL import Image
from PIL import ImageFilter
from keras.layers import *#Input, Conv2D
from keras.models import *#Sequential, load_model
import os
import sys

class Restorer:
    def __init__(self):
        self.modelFilename = '300-300.model'
        self.pixelsPerInch = 300

        if (self.modelFilename in os.listdir('.')):
            # load net from file
            self.net = load_model(self.modelFilename)
            if __debug__:
                kernel = self.net.get_weights()[0]
                print('kernel:')
                print(numpy.reshape(kernel, (3,3)))
        else:
            # create net
            # get pixel dimensions
            letterPaperWidthInches, letterPaperLengthInches = (8.5, 11)
            widthPixels = int(letterPaperWidthInches * self.pixelsPerInch)
            lengthPixels = int(letterPaperLengthInches * self.pixelsPerInch)
            # initialize neural network
            self.net = Sequential()
            self.net.add(
                Conv2D(
                    1, # dimensionality of output space: grayscale
                    (3, 3), # kernel size
                    input_shape = (lengthPixels, widthPixels, 1), # 1 dimension (grayscale)
                    padding = "SAME",
                    data_format = "channels_last"
                )
            )
            self.net.add(Activation('relu'))
            self.net.compile(
                optimizer = "sgd",
                loss = "mse",
                metrics = ["binary_accuracy"]
            )

    def __threshold(p):
        if 0 <= p < 120:
            return 0
        elif 120 <= p < 140:
            return 120
        elif 140 <= p < 160:
            return 140
        elif 160 <= p < 180:
            return 160
        else:
            return 255

    def restore(self, image):
        # image preprocessing
        # convert to grayscale
        image = image.convert('L')
        # perform a Gaussian Blur with a 3x3 pixel kernel
        image = image.filter(ImageFilter.GaussianBlur(1))
        # perform thresholding
        image = image.point(Restorer.__threshold)
        # resize the image to the size required by the neural network
        width = int(self.pixelsPerInch * 8.5)
        height = int(self.pixelsPerInch * 11)
        image = image.resize(
            (width, height),
            Image.LANCZOS
        )
        # get pixels
        pixels = list(image.getdata())
        # convert to numpy array
        pixels = numpy.float32(pixels)
        # normalize
        pixels = numpy.divide(pixels, 255)
        # reshape
        pixels = numpy.reshape(
            pixels,
            (1, height, width, 1)
        )
        # predict
        out = self.net.predict(pixels, batch_size=1)
        # reshape
        out = numpy.reshape(out, (height, width))
        # de-normalize: convert pixel values back to the range [0, 255]
        out = numpy.multiply(out, 255.0)
        # Pillow expects pixel values to be integer values
        out = numpy.uint8(out)
        # convert back to image
        image = Image.fromarray(out)
        # return
        return image



    def _train(self):
        inputData = []
        expectedOutput = []
        # if the training data exists in the current directory, then there's
        #   no need to recompute it
        if 'inputTrainingData.npy' in os.listdir('.'):
            print('loading training data')
            inputData = numpy.load('inputTrainingData.npy')#, mmap_mode='r')
        if 'expectedOutputData.npy' in os.listdir('.'):
            print('loading label data')
            expectedOutput = numpy.load('expectedOutputData.npy')#, mmap_mode='r')
        # If either the input or output training data was not in the current directory
        #   then compute the data
        if [] == inputData or [] == expectedOutput:
            # get training data
            trainingDataPath = 'trainingData/'
            trainingData = {}
            # prepare the list of files in which the training data is located
            files = [ f for f in sorted(os.listdir(trainingDataPath)) if '.npy' in f ]
            for filename in files:
                print(filename)
                # get the full path to the training file
                filepath = trainingDataPath + filename
                # load the pixel data from the file
                pixels = numpy.load(filepath)#, mmap_mode='r')
                # remove the file extension
                filedata = filename[:-4].split('-')
                # get the page number from the file name
                pageNumber = filedata[2]
                # if the page hasn't been processed yet, add it
                if None == trainingData.get(pageNumber):
                    trainingData[pageNumber] = []
                trainingData[pageNumber].append(pixels)
            '''
            inputData = numpy.memmap(
                'inputTrainingData',
                dtype='float32',
                mode='w+',
                shape=(len(files), )
            )
            '''
            # get label data
            labelDataPath = 'labelData/'
            labelData = {}
            # list of label files
            files = [ f for f in sorted(os.listdir(labelDataPath)) if '.npy' in f ]
            for filename in files:
                print(filename)
                # remove file extension
                filedata = filename[:-4].split('-')
                # get page number from file
                pageNumber = filedata[1]
                # save the pixel data
                # BUG HERE... doesn't load pixel data
                labelData[pageNumber] = pixels
            # generate data sets
            inputData = []
            expectedOutput = []
            # pair each input image with its expects output
            for pageNumber in trainingData.keys():
                for pixels in trainingData[pageNumber]:
                    inputData.append(pixels)
                    expectedOutput.append(labelData[pageNumber])
            # prepare for net
            print('numpy-ifying')
            # turn the list of input images into a numpy array
            inputData = numpy.array(inputData, copy=False)
            print('reshaping')
            # convert the array into the shape expected by Keras
            inputData = numpy.reshape(
                inputData,
                (
                    len(inputData),
                    len(inputData[0]),
                    len(inputData[0][0]),
                    1
                )
            )
            if __debug__:
                print('numpy-ifying')
            # save the combined input data into a file for convenience
            numpy.save('inputTrainingData', inputData)
            expectedOutput = numpy.array(expectedOutput, copy=False)
            if __debug__:
                print('reshaping')
            # reshape to dimensionality expected by Keras
            expectedOutput = numpy.reshape(
                expectedOutput,
                (
                    len(expectedOutput),
                    len(expectedOutput[0]),
                    len(expectedOutput[0][0]),
                    1
                )
            )
            # save for later convenience
            numpy.save('expectedOutputData', expectedOutput)
        if __debug__:
            print('fitting')
        # train the neural network with the data
        self.net.fit(inputData, expectedOutput, epochs=1, batch_size=1)
        # save the network in a file so that it doesn't need recomputed
        self.net.save(self.modelFilename)

    def _test(self):
        if not self.modelFilename in os.listdir('.'):
            self._train()

        # load the image with the specified properties
        path = 'trainingData/'
        dpi = 300
        qf = 20
        pn = 30
        filename = '{}dpi-{}qf-{}.npy'.format(dpi, qf, pn)
        filepath = path + filename
        if __debug__:
            print('loading image')
        data = numpy.load(filepath)
        # prepare for net
        # reshape
        data = numpy.reshape(data, (1, int(300 * 11), int(300 * 8.5), 1))
        if __debug__:
            print('predict')
        # get network's output
        out = self.net.predict(data, batch_size=1)
        # reshape
        out = numpy.reshape(out, (len(out[0]), len(out[0][0])))
        # prepare to save output
        if __debug__:
            print('postprocess')
        # de-normalize
        out = numpy.multiply(out, 255.0)
        out = numpy.uint8(out)
        # convert back to image
        out = Image.fromarray(out)
        # apply threshold to each pixel
        out = out.point(Restorer.__threshold)
        # save to output
        outfilename = 'out-{}dpi-{}qf-{}.png'.format(dpi, qf, pn)
        out.save(outfilename)
        print('saved to {}'.format(outfilename))

if __name__ == "__main__":
    main()
    res = Restorer()
    res._test()

