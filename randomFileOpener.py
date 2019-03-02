#!/usr/bin/python3
# randomFile.py

"""
Designed for unix-like systems with python 3.7 and BASH installed.
I developed this program so that I could get more enjoyment out of my own media libraries.
The usage is self-explanatory.
This is a work in progress...
"""

import os
import subprocess
import random
import copy

global deepfiles

def main():
    directory = input('\nEnter the full, absolute path of the directory you wish to make a random selection from:\n')
    try:
        depth = abs(int(input('\nWould you like to include sub-directories?\nEnter any non-zero integer to include up to that many levels of subdirectories.\nEnter "0" to search only a single directory:\n')))
    except (ValueError):
        depth = abs(int(input('\nInvalid input: Make sure you enter an integer and nothing else:\n')))

    included = []
    excluded = []

    exin = input('\nWould you like to restrict your search to only certain file types or exclude any filetypes?\nEnter "i" to run an inclusive search with only certain filetypes, "e" to run an exclusive search excluding certain filetypes, or anything else to run a fully inclusive search of all files:\n')
    if exin.lower() == 'i':
        included = input('\nEnter the file extensions you would like to restrict your search to separated by spaces without any commas:\n').lower().split()
    if exin.lower() == 'e':
        excluded = input('\nEnter the file extensions you would like to exclude from your search separated by spaces without any commas:\n').lower().split()

    files = []

    if depth == 0:
        files = os.listdir(directory)
    else:
        global deepfiles
        deepfiles = []
        descend(directory, depth)
        files = deepfiles
    
    options = []

    if len(included) != 0:
        for p in files:
            for i in included:
                if p.lower().endswith(i):
                    options.append(p)
                    break
    elif len(excluded) != 0:
        for p in files:
            index = 0
            for e in excluded:
                index += 1
                if p.lower().endswith(e):
                    break
                if index == len(excluded):
                    options.append(p)
    else:
        options = files

    repeat = True
    while repeat == True:
        target = random.choice(options)
        if depth == 0:
            target = directory + '/' + target

        subprocess.run(['xdg-open', target])
        
        response = input('\nWould you like to make another selection?\nEnter "r" to make a selection from the same directory or directories.\n Enter "d" to make a selection from different directories, or anything else to exit the program:\n')
        if response.lower() == 'r':
            pass
        elif response.lower() == 'd':
            repeat = False
            main()
        else:
            exit()

def descend(directory, depth, dive=-1): 
    global deepfiles
    os.chdir(directory)
    dirlist = []
    baseList = os.listdir(directory)

    if dive < depth:
        dive += 1

        for x in baseList:
            if os.path.isfile(x) == True:
                path = directory + '/' + x
                deepfiles.append(path)
            elif os.path.isdir(x) == True:
                dirlist.append(x)

        for x in dirlist:
            nextdir = directory + '/' + x
            descend(nextdir, depth, dive)

if __name__ == '__main__':
    main()
