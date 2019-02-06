#!/usr/bin/python3

# randomFileOpener.py

"""
Designed for unix-like systems with python 3.X and BASH installed.
I developed this program so that I could get more enjoyment out of my own media libraries.
The usage is self-explanatory.
This is a work in progress...
"""

import os
from subprocess import run
from random import choice

possibilities = []

def flatRandom():
    choosing = True
    repeat = False

    while choosing == True:
        if repeat == False:
            directory = input('Enter the full, absolute path of the directory you wish to make a random selection from:\n')
        _file = str(choice(os.listdir(directory)))
        target = directory + '/' + _file

        run(['xdg-open', target])

        response = input('Would you like to make another random selection? Enter "y" to continue: ')
        if response.upper() != 'Y':
            choosing = False
        else:
            response = input('Would you like to repeat the random selection in the same directory? Enter "y" to repeat: ')
            if response.upper() == 'Y':
                repeat = True
            else:
                flatOrDeep()

def deepRandom(depth):
    choosing = True
    repeat = False
    
    while choosing == True:     
        if repeat == False:     
            directory = input('Enter the full, absolute path of the top-level directory you wish to start the random selection search from:\n')
            
        target = descend(directory, depth)
        
        run(['xdg-open', target])

        response = input('Would you like to make another random selection? Enter "y" to continue: ')    
        if response.upper() != 'Y':     
            choosing = False            
        else:                           
            response = input('Would you like a different random selection from the same directories? Enter "y" to repeat: ')   
            if response.upper() == 'Y':    
                repeat = True               
            else:             
                flatOrDeep()

def descend(directory, depth, dive = -1):
    os.chdir(directory)
    dirlist = []
    global possibilities
    baseList = os.listdir(directory)

    if dive < depth:
        dive += 1
        for x in baseList:
            if os.path.isfile(x) == True: 
                _path = directory + '/' + x
                possibilities.append(_path)
            elif os.path.isdir(x) == True: 
                dirlist.append(x)
        for x in dirlist: 
            nextdir = directory + '/' + dirlist.pop()
            descend(nextdir, depth, dive)

    target = str(choice(possibilities))
    return target

def flatOrDeep():
    depth = input('Would you like to pick randomly from a single directory?\nEnter "y" for a single directory or any other non-negative number to include up to that many levels of subdirectories:\n')
    if depth == 'y': 
        flatRandom()
    elif depth != 'y':
        depth = int(depth)
        deepRandom(depth)
    else: flatOrDeep() 
        
if __name__ == '__main__':
    flatOrDeep()
