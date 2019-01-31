#!/usr/bin/python3

# randomFileOpener.py

"""
Designed for unix-like systems with python 3.X and BASH installed.
Usage is self-explanatory.
A work in progress...
"""

from subprocess import call
from random import choice
from os import listdir

choosing = True

while choosing == True:
    directory = input('Enter the full, absolute path of the directory you wish to make a random selection from:\n')
    _file = str(choice(listdir(directory)))
    target = directory + '/' + _file

    call(['xdg-open', target])

    response = input('Would you like to make another random selection? Enter "y" to continue:\t')
    if response.upper() != 'Y':
        choosing = False
