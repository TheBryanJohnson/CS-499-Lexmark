#!/usr/bin/python3
import os
from parseCLI import parseCLI
from ImageRestore import ImageRestore

def main():
    args = parseCLI()
    inputFilePath = (getattr(args, 'input file path')[0])
    outputFilePath = (getattr(args, 'output file path')[0])
    ir = ImageRestore()
    if (ir.prepare(inputFilePath) < 0):
        return -1
    #call machine learning method
    ir.outputImage(outputFilePath)
    print("End of main")        #debug

if __name__ == "__main__":
    main()

