#!/usr/bin/python3
import os
from parseCLI import parseCLI
from ImageRestore import ImageRestore

def main():
    args = parseCLI()
    inputFilePath = (getattr(args, 'input file path')[0])
    ir = ImageRestore()
    ir.prepare(inputFilePath)
    print("End of main")        #debug

if __name__ == "__main__":
    main()

