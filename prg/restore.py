#!/usr/bin/python3
import os
from parseCLI import parseCLI
from ImageRestore import ImageRestore

def main():
    args = parseCLI()
    print(args)
    ir = ImageRestore()
    ir.prepare("test.png")
    print("Hello, World!")

if __name__ == "__main__":
    main()

