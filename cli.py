import os
import argparse
import rando


def cli_mode():
    branches = []

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

    args = parser.parse_args()
    inclusivity = 2
    extensions = []

    for x in args.directories:
        if os.path.isdir(x):
            branches.append((x, 1))
        else:
            print(x, 'is not a directory.')
    if len(branches) == 0:
        exit()
    if args.e != None:
        inclusivity = 1
        for x in args.e:
            extensions.append(x)
    elif args.i != None:
        inclusivity = 0
        for x in args.i:
            extensions.append(x)

    rando.rando(branches, inclusivity, extensions)


if __name__ == '__main__':
    cli_mode()