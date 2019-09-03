"""
cli.py is designed for command-line use:

Usage:
$ python3 /path/to/cli.py /path/to/directory1 [/path/to/directory2 /path/to/directory3 ...] \
[-e|-i] [ext1 ext2 ext3 ...]

cli.py will summon rando.py to search directories supplied as arguments and their subdirectories
for files.

Certain filetypes may be excluded with the -e or -i option, only one of which should be used.
The -e option excludes all files with extensions matching those supplied by the user
The -i option excludes all files not having extensions matching those supplied by the user.
Extensions should be supplied as a space-separated list following the -e or -i option.
"""

import os
import argparse
import rando


def cli_mode():
    # Create the ArgumentParser;
    # Add arguments for directories and filetypes to be included or excluded:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'directories', type=str, nargs='*', metavar='/path/to/dir1 /path/to/dir2 ...',
        help='Enter a space-separated list of all directories you want to include.\nExample: '
        '$ python3 randomFile.py /path/to/directory/one /path/to/directory/two'
    )
    parser.add_argument(
        '-e', nargs='*', help='Enter a space-separated list of all file extensions'
        ' you want to exclude.\nExample: $ python3 randomFile.py /path/to/dir1 -e bmp avi wav'
    )
    parser.add_argument(
        '-i', nargs='*', help='Enter a space-separated list of all file extensions you want to '
        'include.\nExample: $ python3 randomFile.py /path/to/dir1 -i mp3 mp4 jpeg jpg png'
    )

    # Parse the arguments, default inclusivity to highest level, initialize branches:
    args = parser.parse_args()
    branches = []
    inclusivity = 2

    # Add valid directory paths to the branches list:
    for x in args.directories:
        if os.path.isdir(x):
            branches.append((x, 1))
        else:
            print(x, 'is not a directory.')
    if len(branches) == 0:
        exit()

    # If the -e or -i options were selected, add file extensions to be in/excluded;
    # Priority is given to the most restrictive option (-i):
    if args.e != None:
        extensions = []
        inclusivity = 1
        for x in args.e:
            extensions.append(x)
    elif args.i != None:
        extensions = []
        inclusivity = 0
        for x in args.i:
            extensions.append(x)
    else:
        extensions = []

    # Run the rando function:
    rando.rando(branches, inclusivity, extensions, 'cli')


if __name__ == '__main__':
    cli_mode()