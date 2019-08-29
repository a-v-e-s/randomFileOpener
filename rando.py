import os
import sys
import subprocess
import random


def rando(branches, inclusivity, extensions, gui=None, Notice=None):
    files = []
    options = []

    # Check all entries to verify they are real directories
    limbs = []
    if gui == None:
        for x in branches:
            if os.path.isdir(x[0]):
                limbs.append(x)
            else:
                print('\n' + x + ' is not a directory!\n')
    else:
        limbs = branches

    # Get full paths to all files from all real directories
    for limb in limbs:
        if limb[1]:
            for root, subdirectories, collections in os.walk(limb[0]):
                for item in collections:
                    files.append(os.path.join(root, item))
        else:
            for x in os.listdir(limb[0]):
                y = os.path.join(limb[0], x)
                if os.path.isfile(y):
                    files.append(y)

    # Weed out any files not to be included due to their extensions
    if inclusivity == 2:
        options = files
    elif inclusivity == 1:
        for f in files:
            index = 0
            for excluded in extensions:
                index += 1
                if f.lower().endswith(excluded.lower()):
                    break
                if index == len(extensions):
                    options.append(f)
    else:
        for f in files:
            for included in extensions:
                if f.lower().endswith(included.lower()):
                    options.append(f)
                    break
    del files

    # Choose at random from the list of options and open it
    target = random.choice(options)
    if sys.platform.lower().startswith('win'):
        try:
            os.startfile(target)
        except Exception:
            if gui:
                gui.warning(Notice, None, 2)
            else:
                print('\nFailed to open ' + target)
                print('Your version of Windows or Python may not be supported')
                print(sys.exc_info())
    elif sys.platform.lower().startswith('dar'):
        # I haven't tested on any Macs yet. This *might* work
        try:
            subprocess.run(['open', target])
        except Exception:
            if gui:
                gui.warning(Notice, None, 3)
            else:
                print('\nFailed to open ' + target)
                print('This program has not yet been tested on Macs')
                print(sys.exc_info())
    else:
        try:
            subprocess.run(['xdg-open', target])
        except Exception:
            if gui:
                gui.warning(Notice, None, 4)
            else:
                print('\nFailed to open ' + target)
                print('This program requires xdg-open to be installed to work')
                print('Installing the xdg-utils package may solve the problem.')
                print(sys.exc_info())