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

def flat():
    choosing = True
    repeat = False

    while choosing:
        if repeat == False:
            directory = input('Enter the full, absolute path of the directory you wish to make a random selection from:\n')
        try:
            file = str(random.choice(os.listdir(directory)))
        except FileNotFoundError:
            retry = input('No such directory: %s\nEnter "y" to try again:' % directory)
            if retry.lower() == 'y':
                flat()
            else:
                exit()
        else:
            target = directory + '/' + file
            subprocess.run(['xdg-open', target])

        repeat = redo()

def deep(depth, possibilities):
    choosing = True
    repeat = False
    
    while choosing:     
        if repeat == False:     
            directory = input('Enter the full, absolute path of the top-level directory you wish to start the random selection search from:\n')
            
        possibilities = []
        try:
            target = descend(directory, depth, possibilities)
        except FileNotFoundError:
            retry = input('No such directory: %s\nEnter "y" to try again:' % directory)
            if retry.lower() == 'y':
                deep(depth, possibilities)
            else:
                exit()
        else:
            subprocess.run(['xdg-open', target])

        repeat = redo()

def descend(directory, depth, possibilities, dive = -1,):
    os.chdir(directory)
    dirlist = []
    baseList = os.listdir(directory)

    if dive < depth:
        dive += 1
        for x in baseList:
            if os.path.isfile(x) == True: 
                path = directory + '/' + x
                possibilities.append(path)
            elif os.path.isdir(x) == True: 
                dirlist.append(x)
        for x in dirlist: 
            nextdir = directory + '/' + dirlist.pop()
            descend(nextdir, depth, possibilities, dive)

    if dive == 0:
        target = random.choice(possibilities)
        return target

def redo():
    response = input('Would you like to make another selection? Enter "r" to make a different selection from the same directory or directories, "d" to make a different random selection, or anything else to exit the program: ')
    if response.lower() == 'r':
        repeat = True
        return repeat
    elif response.lower() == 'd':
        main()
    else:
        exit()

def main():
    try:
        depth = abs(int(input('Would you like to pick randomly from a single directory?\nEnter 1 for a single directory or any other non-zero integer to include up to that many levels of subdirectories:\n')))
        if depth == 0:
            raise Shallow()
    except (ValueError, Shallow):
        retry = input('Invalid input: Make sure you enter a non-zero integer and nothing else.\nEnter "y" to try again:\n')
        if retry.lower() == 'y': 
            main()
        else:
            exit()
    else:
        if depth == 1: 
            flat()
        elif depth != 1:
            possibilities = []
            deep(depth, possibilities)

class Shallow(Exception): pass
        
if __name__ == '__main__':
    main()
