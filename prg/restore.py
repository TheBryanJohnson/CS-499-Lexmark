#!/usr/bin/python3
import os
from parseCLI import parseCLI

def main():
    args = parseCLI()
    print(args)
    print("Hello, World!")

if __name__ == "__main__":
    main()

