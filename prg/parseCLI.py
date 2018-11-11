#!/usr/bin/python3
import argparse

def parseCLI():
    '''
    Function used to parse the command line options
        input:  none (should find CLI arguments passed into main)
        output: a namespace object containing formatted arguments
                Access arguments using getAttr()
    '''
    parser = argparse.ArgumentParser(description="Improve the quality of a compressed image.")
    
    #argument used to specify input file path
    parser.add_argument("input file path", 
        metavar="Input", 
        type=str, 
        nargs=1, 
        help="An image file that you wish to process.")
    
    #argument used to specify output file path
    parser.add_argument("output file path", 
        metavar="Output", 
        type=str, 
        nargs=1, 
        help="The location where you would like the output saved")

    '''
    #specifies size of output image
    parser.add_argument("-s", "--size", 
        metavar="Size", 
        choices=["orig", "100", "150", "300"], 
        default="300",
        help="Specifies the size of the output image in dots per inch (dpi).  Options are 100, 150, 300, and orig.  orig will use the original size.  The default is 300.")
    
    #select whether to resample if image is resized as opposed to padding
    parser.add_argument("-r", "--resample", 
        action="store_true", 
        help="Sets the image to be resampled using the filter selected with -f or --filter.")
    
    #used to specify the filter to be used if resample is selected, ignored otherwise
    parser.add_argument("-f", "--filter", 
        metavar="Filter", 
        choices=["nearest", "box", "bilinear", "hamming", "bicubic", "lanczos"], 
        default="nearest", 
        help="Selects a filter to use for resizing the image.  Only used when -r or --resample is specified.  choices are nearest, box, bilinear, hamming, bicubic, and lanczos.  The default is nearest.")
    '''

    parser.add_argument("-m", "--use-machine-learning", 
        action="store_true",
        help="Include flag in order to use the experimental machine learning model in deciding output.")
    #displays version of program
    parser.add_argument("--version", 
        action="version", 
        version="%(prog)s 1.0")
    
    #call that actually parsed the above arguments
    args = parser.parse_args()
    return args

