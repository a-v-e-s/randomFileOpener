#!/usr/bin/python3
# randomFile.py

"""
I developed this program so that I could get more enjoyment out of my own media libraries.
The usage is self-explanatory. This is a work in progress. 
It has been tested on Debian Linux and Windows 10 with Python 3.X and should work with these.
GUI and other features still to come.
"""

import os, sys, subprocess, random
global files

def main():
    # Add one or more directories to search for files and decide whether or not to search their subdirectories
    adding = True
    branches = {}
    while adding == True:
        directory = input('\nEnter the full, absolute path of a directory you wish to make a random selection from:\n')
        if not os.path.isdir(directory):
            print('\n', directory, ' is not a valid directory. Please try again and make sure to enter the full, absolute path\n')
            continue
        deep = False
        if input('\nWould you like to include subdirectories of this directory in your search?\nEnter "y" if yes:\n').lower() == 'y':
            deep = True
        branches[directory] = deep
        if input('\nWould you like to add another directory to your search?\nEnter "y" to add more:\n').lower() != 'y':
            adding = False

    # Decide whether to exclude certain filetypes, only include certain filetypes, or include all filetypes (the default)
    included = []
    excluded = []
    exin = input('\nWould you like to restrict your search to only certain file types or exclude any filetypes?\nEnter "i" to run an inclusive search with only certain filetypes, "e" to run an exclusive search excluding certain filetypes, or anything else to run a fully inclusive search of all files:\n')
    if exin.lower() == 'i':
        included = input('\nEnter the file extensions you would like to restrict your search to separated by spaces without any commas:\n').lower().split()
    if exin.lower() == 'e':
        excluded = input('\nEnter the file extensions you would like to exclude from your search separated by spaces without any commas:\n').lower().split()

    # Build a the list of files in the (sub-)directories
    global files
    files = []
    for x in branches.keys():
        if branches[x] == False:
            for y in os.listdir(x):
                if os.path.isfile(x + '/' + y):
                    files.append(x + '/' + y)
        else:
            # I could have used os.walk here, but I built the descend function before I learned about os.walk
            descend(x)
    
    # If the user wanted to exclude or only include certain filetypes, 
    # decide if the files in the files list are options based on their extensions
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

    # Open files from the constructed list of options for as long as the user wants to repeat the process
    repeat = True
    while repeat == True:
        target = random.choice(options)
        if sys.platform.lower().startswith('win'):
            os.startfile(target)
        elif sys.platform.lower().startswith('dar'):
            # I don't have a Mac so I haven't been able to develop support for them. This *might* work...
            try:
                subprocess.run(['open', target])
            except:
                print('\nSorry, support for Macs has not yet been developed.\n')
                exit()
        else:
            try: 
                subprocess.run(['xdg-open', target])
            except:
                print('\nSorry, it seems that your system is not supported at this time.\nIf you can install xdg-open, this problem should be resolved.\n')
                exit()
        response = input('\nWould you like to make another selection?\nEnter "r" to repeat a selection from the same directory or directories, "d" to make a selection from different directories, or anything else to exit the program:\n')
        if response.lower() == 'r':
            pass
        elif response.lower() == 'd':
            repeat = False
            main()
        else:
            exit()

def descend(directory): 
    # Add files within directory to global files list, build lists of directories within the directory, 
    # then recursively call this function to do the same in all subdirectories.
    global files
    os.chdir(directory)
    subBranches = []
    baseList = os.listdir(directory)
    for x in baseList:
        if os.path.isfile(x) == True:
            path = directory + '/' + x
            files.append(path)
        elif os.path.isdir(x) == True:
            subBranches.append(x)
    for x in subBranches:
        nextdir = directory + '/' + x
        descend(nextdir)

if __name__ == '__main__':
    main()
