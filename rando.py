"""
Finds files in directories included in the branches argument, which is to be a list of tuples.
The first item of the branches tuple is to be a string containing the full path to the directory,
the second item of the branches tuple is to be either 0 or 1 to indicate whether (1) or not (0) to
search the directory's subdirectories for files.

Inclusivity is to equal either 2, 1, or 0. 
A value of 2 indicates that all filetypes are to be included.
A value of 1 indicates that all files with extensions in the extensions list are to be excluded.
A value of 0 indicates that only files with extensions in the extensions list are to be included.

The interface and notice arguments are used internally and supplied by gui.py and cli.py if needed.

It is simpler to run gui.py or cli.py as top level modules than to import rando manually.
If run as a top level module it simply imports cli.py and runs as though the user had run cli.py.
"""

import os
import sys
import subprocess
import random


def rando(branches, inclusivity, extensions, interface=None, notice=None):
    # Initialize a list for all files (files), another for files to choose from (options):
    files = []
    options = []

    # Check all entries to verify they are real directories, unless gui already did this:
    limbs = []
    if interface == None:
        for x in branches:
            if os.path.isdir(x[0]):
                limbs.append(x)
            else:
                print('\n' + x + ' is not a directory!\n')
    else:
        limbs = branches

    # Get full paths to all files from all real directories:
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

    # Weed out any files not to be included due to their extensions:
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

    # Choose at random from the list of options and open it with the proper method:
    target = random.choice(options)
    if sys.platform.lower().startswith('win'):
        try:
            os.startfile(target)
        except OSError:
            text = ('Failed to open ' + target + '\nNo application associated '
                'with files ending in .' + target.split('.')[-1]
            )
            if interface not in [None, 'cli']:
                interface.warning(notice, text, 2)
            else:
                print(text)
        except Exception:
            if interface not in [None, 'cli']:
                interface.warning(notice, sys.exc_info(), 2)
            else:
                print(sys.exc_info())
    elif sys.platform.lower().startswith('dar'):
        # I haven't tested on any Macs yet. This *might* work:
        try:
            subprocess.run(['open', target])
        except Exception:
            if interface not in [None, 'cli']:
                interface.warning(notice, None, 3)
            else:
                print('\nFailed to open ' + target)
                print('This program has not yet been tested on Macs')
                print(sys.exc_info())
    else:
        try:
            subprocess.run(['xdg-open', target])
        except Exception:
            if interface not in [None, 'cli']:
                interface.warning(notice, None, 4)
            else:
                print('\nFailed to open ' + target)
                print('This program requires xdg-open to be installed to work')
                print('Installing the xdg-utils package may solve the problem.')
                print(sys.exc_info())

if __name__ == '__main__':
    import cli
    cli.cli_mode()