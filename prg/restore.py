#!/usr/bin/python3
import os
from parseCLI import parseCLI
from ImageRestore import ImageRestore

def main():
    args = parseCLI()
    inputFilePath = (getattr(args, 'input file path')[0])
    outputFilePath = (getattr(args, 'output file path')[0])
    outputSize = (getattr(args, 'size'))
    ir = ImageRestore()
    if (ir.prepare(inputFilePath, outputSize) < 0):
        return -1
    #call machine learning method
    ir.outputImage(outputFilePath)
    print(args)
    print("End of main")        #debug

if __name__ == "__main__":
    main()

