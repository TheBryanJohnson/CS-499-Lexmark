#!/usr/bin/python3
import argparse

def parseCLI():
    parser = argparse.ArgumentParser(description="Improve the quality of a compressed image.")
    parser.add_argument("input file path", metavar="Input", type=str, nargs=1, help="An image file that you wish to process.")
    parser.add_argument("output file path", metavar="Output", type=str, nargs=1, help="The location where you would like the output saved")
    parser.add_argument("-s", "--size", metavar="Size", choices=["orig", "100", "150", "300"], default="300",
    help="Specifies the size of the output image in dots per inch (dpi).  Options are 100, 150, 300, and orig.  orig will use the original size.  The default is 300.")
    parser.add_argument("-r", "--resample", action="store_true", help="Sets teh image to be resampled using the filter selected with -f or --filter.")
    parser.add_argument("-f", "--filter", metavar="Filter", choices=["nearest", "box", "bilinear", "hamming", "bicubic",
    "lanczos"], default="nearest", help="Selects a filter to use for resizing the image.  Only used when -r or --resample is specified.  choices are nearest, box, bilinear, hamming, bicubic, and lanczos.  The default is nearest.")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1")
    args = parser.parse_args()
    return args

