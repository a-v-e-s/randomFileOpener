#!/usr/bin/python3

# randomFileOpener.py

"""
Designed for unix-like systems with python 3.X and BASH installed.
Usage is self-explanatory.
A work in progress...
"""

from subprocess import call     # for passing commands to a sub-shell
from random import choice       # for choosing a file at random
from os import listdir          # for getting a list of files from a given directory

choosing = True
repeat = False

while choosing == True:     # while we are still running the program
    if repeat == False:     # if we are not running the exact same search and selection
        directory = input('Enter the full, absolute path of the directory you wish to make a random selection from:\n')     # get a new directory to choose from
    _file = str(choice(listdir(directory)))     # choose a filename at random from that directory
    target = directory + '/' + _file            # stick that filename onto the full directory path

    call(['xdg-open', target])                  # and pass it to a sub-shell to be opened with xdg-open

    response = input('Would you like to make another random selection? Enter "y" to continue: ')    # go again?
    if response.upper() != 'Y':     # if no
        choosing = False            # stop the program
    else:                           # if yes
        response = input('Would you like to repeat the random selection in the same directory? Enter "y" to repeat: ')  #do you want to select randomly from the same directory?
        if response.upper() == 'Y':     # if yes
            repeat = True               # repeat the exact same random search
        else:                           # if no
            repeat = False              # don't
