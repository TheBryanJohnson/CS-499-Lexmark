#!/usr/bin/python3
import argparse

def parseCLI():
    parser = argparse.ArgumentParser(description="Improve the quality of a compressed image.")
    parser.add_argument("input file path", metavar="Input", type=str, nargs=1, help="An image file that you wish to process.")
    parser.add_argument("output file path", metavar="Output", type=str, nargs=1, help="The location where you would like the output saved")
    args = parser.parse_args()
    return args

