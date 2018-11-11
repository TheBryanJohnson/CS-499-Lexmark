#!/usr/bin/python3
from parseCLI import parseCLI
from ImageRestore import ImageRestore

def main():
    #get arguments from CLI
    args = parseCLI()
    if __debug__:
        print(args)

    #store arguments into variables for future usage
    inputFilePath = getattr(args, 'input file path')[0]
    outputFilePath = getattr(args, 'output file path')[0]
    #outputSize = getattr(args, 'size')
    #resample = getattr(args, 'resample')
    #filterName = getattr(args, "filter")
    useML = getattr(args, "use_machine_learning")

    #instantiate image restore object
    ir = ImageRestore()

    #image preprocessing, exits program if image fails to load properly
    try:
        ir.openImage(inputFilePath)
    except IOError:
        print("Cannot open file: ", inputFilePath)

    #call machine learning method
    ir.restore(useMachineLearning=useML)
    try:
        ir.saveOutputImage(outputFilePath)
    except IOError:
        print("Cannot save file: ", outputFilePath)
        return
    if __debug__:
        print(args)                 #debug
        print("End of main")        #debug

if __name__ == "__main__":
    main()



