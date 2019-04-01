"""
randomFile.py: The Random File Opener
I built this application to get more enjoyment out of my video library, 
and also as a practice project. 
Usage is fairly self-explanatory, and a help button is included.
To start from command line:
$ python3 /path/to/RandomFile.py 
"""

import os
import sys
import subprocess
import random
import functools
import tkinter as tk
from tkinter.filedialog import askdirectory


def go(Notice, Inclusivity, Extensions):
    inclusivity = Inclusivity.get()
    extensions = Extensions.get().split()
    files = []
    options = []

    # Check all entries to verify they are real directories
    global branches
    notdirs = []
    limbs = {}
    index = 0
    for x in branches.keys():
        index += 1
        if os.path.isdir(x.get()):
            limbs[x.get()] = branches[x].get()
        else:
            notdirs.append(x.get() + ' is not a directory')
            if index == len(branches):
                warning(Notice, notdirs, type=1)

    # Get full paths to all files from all real directories
    for limb in limbs.keys():
        if limbs[limb]:
            for root, subdirectories, collections in os.walk(limb):
                for item in collections:
                    files.append(os.path.join(root, item))
        else:
            for x in os.listdir(limb):
                if os.path.isfile(os.path.join(limb, x)):
                    files.append(os.path.join(limb, x))

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

    # Choose at random from the list of options and open it
    target = random.choice(options)
    if sys.platform.lower().startswith('win'):
        try:
            os.startfile(target)
        except Exception:
            warning(Notice, None, type=2)
    elif sys.platform.lower().startswith('dar'):
        try:
            subprocess.run(['open', target])
        except Exception:
            warning(Notice, None, type=3)
    else:
        try:
            subprocess.run(['xdg-open', target])
        except Exception:
            warning(Notice, None, type=4)

def add_branch(Tree):
    # Add a tk.Frame called Branch with fields for user to fill out
    global branches
    global rownum
    rownum += 1
    Branch = tk.Frame(Tree)
    Depth = tk.IntVar()
    
    tk.Checkbutton(Branch, text='Search Sub-Folders?', variable=Depth,
        onvalue=1, offvalue=0).grid(row=rownum, column=0)
    Entry = tk.Entry(Branch, width=50)
    Entry.grid(row=rownum, column=1)
    Entry.focus_set()
    tk.Button(Branch, text='Browse', command=(
        lambda x=Entry:[x.delete(0, len(x.get())),
        x.insert(0, askdirectory())])).grid(row=rownum, column=2)
    Branch.grid(row=rownum)
    Twig = tk.Frame(Tree)
    Adder = tk.Button(Twig)
    Adder.config(text='Add Folder', command=lambda x=Tree: add_branch(x))
    Adder.grid(row=rownum+1, column=1)
    if rownum > 1:
        Pruner = tk.Button(Twig)
        Pruner.config(text='Remove Previous', command=lambda: [
            prune(Entry), Branch.grid_forget(), Twig.grid_forget()])
        Pruner.grid(row=rownum+1, column=2)
    Twig.grid(row=rownum+1)

    branches[Entry] = Depth


def prune(Entry):
    # Move up one row and delete the previous Entry
    global rownum
    global branches
    rownum -= 1
    del branches[Entry]


def clear(Inclusivity, Extensions):
    # Clear/Reset all fields
    global branches
    for x in branches.keys():
        x.delete(0, len(x.get()))
        branches[x].set(0)
    Inclusivity.set(2)
    Extensions.config(state='normal')
    Extensions.delete(0, len(Extensions.get()))
    Extensions.config(state='disabled')


def help():
    # Display basic usage instructions in a popup window
    Help = tk.Toplevel()
    Help.title('Help')
    tk.Label(Help, text='Usage:\n\n'
        'Enter the full absolute paths of folders you want to pick from in '
        'the top section.\n'
        'In Windows this usually begins with C:\\ \n'
        'In Mac OS and Linux it begins with / \n'
        'Use the browse button if you need help finding the path of a given '
        'folder.\n'
        'Mark the checkbox if you want to include sub-folders of these in '
        'your search.\n\n'
        'In the bottom section, decide if you want to exclude certain '
        'filetypes,\n'
        'include only certain filetypes, or run a fully inclusive search '
        'of everything,\n'
        'and mark the corresponding radio button.\n'
        'Type the list of extensions of the filetypes you want to \n'
        'exclude from or restrict your search to without commas.\n\n'
        'Examples of common extensions for various filetypes:\n'
        'Video: .mp4 .avi .m4v .mov .mpg .wmv\n'
        'Picture: .jpg .jpeg .gif .png .bmp .svg\n'
        'Music: .m4a .mid .mp3 .mpa .wav .wma\n\n'
        'Click the "Go!" button to run the search,\n'
        '"Clear All" to clear all fields,\n'
        'and "Exit" to close the program.').pack(ipadx=15)
    tk.Button(Help, text='OK', command=Help.destroy).pack()
    Help()
        
    
def warning(Notice, x, type=0):
    # If there was a problem, inform the user of what went wrong
    if type == 0:
        tk.Label(Root, text='Sorry, an unknown error occurred. This '
        'program is still under development.', fg='red').pack(ipadx=10)
    if type == 1:
        Notice.config(text='\n'.join(x), fg='red')
    if type == 2:
        Failure = tk.Toplevel()
        Failure.title('Failed to open file')
        tk.Label(Failure, text='Windows failed to open the file.', fg='red')
        tk.Button(Failure, text='OK', command=Failure.destroy).pack()
        Failure()
    if type == 3:
        Failure = tk.Toplevel()
        Failure.title('Failed to open file')
        tk.Label(Failure, text='Mac failed to open the file.', fg='red')
        tk.Button(Failure, text='OK', command=Failure.destroy).pack()
        Failure()
    if type == 4:
        Failure = tk.Toplevel()
        Failure.title('Failed to open file')
        tk.Label(Failure, text='Failed to open file.\n'
            'Program requires xdg-open.', fg='red')
        tk.Button(Failure, text='OK', command=Failure.destroy).pack()
        Failure()


# Build and start the GUI
Root = tk.Tk()
Root.title('Random File Opener')

global rownum
rownum = 0
global branches
branches = dict()

Tree = tk.Frame(Root)
Instructions = tk.Label(Tree, text=
    'Enter the path of a directory to choose from:', font=('tk.TkDefaultFont', 12)).grid(row=rownum)
add_branch(Tree)
Tree.pack(ipadx=10, ipady=5)

Filetypes = tk.Frame(Root)
tk.Label(Filetypes, text='Choose whether to exclude certain '
    'file based on type:', font=('tk.TkDefaultFont', 12)).grid(row=0)
Inclusivity = tk.IntVar()
Extensions = tk.Entry(Filetypes, text='File extensions',
    width=25, state='disabled')
tk.Radiobutton(Filetypes, text='All-Inclusive', value=2, 
    variable=Inclusivity, command=(lambda x=Extensions: 
    x.config(state='disabled'))).grid(row=1)
tk.Radiobutton(Filetypes, text='Exclude:', value=1, 
    variable=Inclusivity, command=(lambda x=Extensions: 
    x.config(state='normal'))).grid(row=2)
tk.Radiobutton(Filetypes, text='Only Include:', value=0, 
    variable=Inclusivity, command=(lambda x=Extensions: 
    x.config(state='normal'))).grid(row=3)
Inclusivity.set(2)
Extensions.grid(row=4)
Filetypes.pack(ipadx=10, ipady=5)

Problems = tk.Frame(Root).pack(ipadx=10)
Notice = tk.Label(Problems)
Notice.pack()

Buttons = tk.Frame(Root)
tk.Button(Buttons, text='Go!', command=functools.partial(
    go, Notice, Inclusivity, Extensions)).grid(row=0, column=1)
tk.Button(Buttons, text='Clear All', command=functools.partial(
    clear, Inclusivity, Extensions)).grid(row=0, column=2)
tk.Button(Buttons, text='Help', command=help).grid(row=0, column=3)
tk.Button(Buttons, text='Exit', command=Root.quit).grid(row=0, column=4)
Buttons.pack(ipadx=10, ipady=5)

if __name__ == '__main__':
    Root.mainloop()
