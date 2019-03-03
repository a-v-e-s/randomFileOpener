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

global files

def main():
    adding = True
    branches = {}
    while adding == True:
        directory = input('\nEnter the full, absolute path of a directory you wish to make a random selection from:\n')
        if not os.path.isdir(directory):
            print('\n', directory, ' is not a valid directory. Please try again and make sure to enter the full, absolute path\n')
            continue
        try:
            depth = abs(int(input('\nWould you like to include sub-directories?\nEnter any non-zero integer to include up to that many levels of subdirectories.\nEnter "0" to search only in that directory:\n')))
        except (ValueError):
            depth = abs(int(input('\nInvalid input: Make sure you enter an integer and nothing else:\n')))
        branches[directory] = depth
        if input('\nWould you like to add another directory to your search?\nEnter "y" to add more:\n').lower() != 'y':
            adding = False

    included = []
    excluded = []
    exin = input('\nWould you like to restrict your search to only certain file types or exclude any filetypes?\nEnter "i" to run an inclusive search with only certain filetypes, "e" to run an exclusive search excluding certain filetypes, or anything else to run a fully inclusive search of all files:\n')
    if exin.lower() == 'i':
        included = input('\nEnter the file extensions you would like to restrict your search to separated by spaces without any commas:\n').lower().split()
    if exin.lower() == 'e':
        excluded = input('\nEnter the file extensions you would like to exclude from your search separated by spaces without any commas:\n').lower().split()

    global files
    files = []
    for x in branches.keys():
        if branches[x] == 0:
            for y in os.listdir(x):
                files.append(x + '/' + y)
        else:
            descend(x, branches[x])
    
    options = []
    if len(included) != 0:
        for f in files:
            for i in included:
                if f.lower().endswith(i):
                    options.append(f)
                    break
    elif len(excluded) != 0:
        for f in files:
            index = 0
            for e in excluded:
                index += 1
                if f.lower().endswith(e):
                    break
                if index == len(excluded):
                    options.append(f)
    else:
        options = files

    repeat = True
    while repeat == True:
        target = random.choice(options)
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
    global files
    os.chdir(directory)
    subBranches = []
    baseList = os.listdir(directory)
    if dive < depth:
        dive += 1
        for x in baseList:
            if os.path.isfile(x) == True:
                path = directory + '/' + x
                files.append(path)
            elif os.path.isdir(x) == True:
                subBranches.append(x)
        for x in subBranches:
            nextdir = directory + '/' + x
            descend(nextdir, depth, dive)

if __name__ == '__main__':
    main()
