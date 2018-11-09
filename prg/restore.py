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

if __name__ == "__main__":
    main()

