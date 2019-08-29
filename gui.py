import os
import sys
import subprocess
import random
import functools
import threading
import argparse
import tkinter as tk
from tkinter.filedialog import askdirectory
import rando


class Gui():
    def __init__(self):
        # Build and launch the GUI
        Root = tk.Tk()
        Root.title('Random File Opener')

        self.rownum = 0
        self.branches = []

        Tree = tk.Frame(Root)
        dir_label = tk.Label(
            Tree, text='Enter the path of a folder to choose from:',
            font=('tk.TkDefaultFont', 12)
        )
        dir_label.grid(row=self.rownum)
        self.add_branch(Tree)
        Tree.pack(ipadx=10, ipady=5)
        
        Top = tk.Frame(Root)
        Adder = tk.Button(Top, text='Add Folder', font=('tk.TkDefaultFont', 12), command=lambda x=Tree: self.add_branch(x))
        Adder.grid(row=1, column=1)
        self.Pruner = tk.Button(
            Top, text='Remove Previous', font=('tk.TkDefaultFont', 12), state='disabled',
            command=lambda: self.prune()
        )
        self.Pruner.grid(row=1, column=2)
        Top.pack(ipadx=10, ipady=10)

        Filetypes = tk.Frame(Root)
        exts = tk.Label(
            Filetypes, text='Choose whether to exclude certain file based on type:',
            font=('tk.TkDefaultFont', 12)
        )
        exts.grid(row=0)
        Inclusivity = tk.IntVar()
        Extensions = tk.Entry(Filetypes, text='File extensions', width=25, state='disabled')
        all_incl = tk.Radiobutton(
            Filetypes, text='All-Inclusive', value=2, variable=Inclusivity,
            command=(lambda x=Extensions: x.config(state='disabled'))
        )
        all_incl.grid(row=1)
        exclusive = tk.Radiobutton(
            Filetypes, text='Exclude:', value=1, variable=Inclusivity,
            command=(lambda x=Extensions: x.config(state='normal'))
        )
        exclusive.grid(row=2)
        very_exclusive = tk.Radiobutton(
            Filetypes, text='Only Include:', value=0, variable=Inclusivity,
            command=(lambda x=Extensions: x.config(state='normal'))
        )
        very_exclusive.grid(row=3)
        Inclusivity.set(2)
        Extensions.grid(row=4)
        Filetypes.pack(ipadx=10, ipady=5)

        Problems = tk.Frame(Root).pack(ipadx=10)
        Notice = tk.Label(Problems)
        Notice.pack()

        Buttons = tk.Frame(Root)
        go = tk.Button(
            Buttons, text='Go!', command=(lambda: threading.Thread(
                None, self.go, args=(
                    self.branches, Inclusivity.get(), Extensions.get().split(), Notice
                )
            ).run())
        )
        go.grid(row=0, column=1)
        clear = tk.Button(
            Buttons, text='Clear All',
            command=functools.partial(self.clear, Inclusivity, Extensions)
        )
        clear.grid(row=0, column=2)
        hlp = tk.Button(Buttons, text='Help', command=self.help_)
        hlp.grid(row=0, column=3)
        qit = tk.Button(Buttons, text='Quit', command=Root.destroy)
        qit.grid(row=0, column=4)
        Buttons.pack(ipadx=10, ipady=5)
        Root.bind(
            sequence='<Return>', func=(
                lambda x: threading.Thread(None, self.go, args=(
                    self.branches, Inclusivity.get(), Extensions.get().split(), Notice
                )).run()
            )
        )
        Root.bind(sequence='<Control-KeyPress-n>', func=(lambda x: self.add_branch(Tree)))
        Root.bind(sequence='<Control-KeyPress-d>', func=(lambda x: self.prune()))
        Root.bind(sequence='<Control-KeyPress-h>', func=(lambda x: self.help_()))
        Root.bind(sequence='<Control-KeyPress-q>', func=(lambda x: Root.destroy()))
        Root.bind(sequence='<Control-KeyPress-l>', func=(lambda x: self.clear(Inclusivity, Extensions)))
        Root.mainloop()


    def add_branch(self, Tree):
        # Add a tk.Frame called Branch with fields for user to fill out
        self.rownum += 1
        Branch = tk.Frame(Tree)
        Depth = tk.IntVar()

        depth = tk.Checkbutton(
            Branch, text='Search Sub-Folders?', variable=Depth, onvalue=1, offvalue=0
        )
        depth.grid(row=self.rownum, column=0)
        Entry = tk.Entry(Branch, width=50)
        Entry.grid(row=self.rownum, column=1)
        Entry.focus_set()
        browse = tk.Button(
            Branch, text='Browse', command=(
                lambda x=Entry:[x.delete(0, len(x.get())), x.insert(0, askdirectory())]
            )
        )
        browse.grid(row=self.rownum, column=2)
        Branch.grid(row=self.rownum)
        self.branches.append((Entry, Depth, depth, browse))

        if self.rownum > 1:
            self.Pruner.configure(state='active')


    def prune(self):
        # Move up one row and delete the previous Entry
        if self.rownum > 1:
            self.rownum -= 1
            forgets = [0, 2, 3]
            for x in forgets:
                self.branches[-1][x].grid_remove()
            del self.branches[-1]
        if self.rownum == 1:
            self.Pruner.configure(state='disabled')


    def clear(self, Inclusivity, Extensions):
        # Clear/Reset all fields
        for x in range(1, len(self.branches)):
            self.prune()
        x = self.branches[0]
        x[0].delete(0, len(x[0].get()))
        x[1].set(0)
        Inclusivity.set(2)
        Extensions.config(state='normal')
        Extensions.delete(0, len(Extensions.get()))
        Extensions.config(state='disabled')


    def warning(self, Notice, x, type=0):
        # If there was a problem, inform the user of what went wrong
        if type == 1:
            Notice.config(text=''.join(x), fg='red')
            return None
        else:
            Failure = tk.Toplevel()
            Failure.title('Failed to open file')
        if type == 2:
            reason = tk.Label(
                Failure, fg='red',
                text='Windows failed to open the file.\n'
                'Your version of Windows or Python may be incompatible'
            )
            reason.pack()
        if type == 3:
            reason = tk.Label(
                Failure, fg='red',
                text='Mac failed to open the file.\n'
                'This program has not yet been tested on Macs.'
            )
            reason.pack()
        if type == 4:
            reason = tk.Label(
                Failure, fg='red',
                text='Failed to open file.\nProgram requires xdg-open.\n'
                'Installing the xdg-utils package may solve this problem'
            )
        reason.pack()
        quit_warn = tk.Button(Failure, text='OK', command=Failure.destroy)
        quit_warn.pack()
        Failure.mainloop()


    def help_(self):
        # Display basic usage instructions in a popup window
        help_ = tk.Toplevel()
        help_.title('Help')
        help_text = tk.Label(
            help_, text='Usage:\n\n'
            'Enter the full absolute paths of folders you want to pick from in the top section.\n'
            'In Windows this usually begins with C:\\ \n'
            'In Mac OS and Linux it begins with / \n'
            'Use the browse button if you need help finding the path of a given folder.\n'
            'Mark the checkbox if you want to include sub-folders of these in your search.\n\n'
            'In the bottom section, decide if you want to exclude certain filetypes,\n'
            'include only certain filetypes, or run a fully inclusive search of everything,\n'
            'and mark the corresponding radio button.\n'
            'Type the list of extensions of the filetypes you want to \n'
            'exclude from or restrict your search to without commas.\n\n'
            'Examples of common extensions for various filetypes:\n'
            'Video: .mp4 .avi .m4v .mov .mpg .wmv\n'
            'Picture: .jpg .jpeg .gif .png .bmp .svg\n'
            'Music: .m4a .mid .mp3 .mpa .wav .wma\n\n'
            'Click the "Go!" button to run the search,\n'
            '"Clear All" to clear all fields,\n'
            'and "Exit" to close the program.')
        help_text.pack(ipadx=15)
        help_quit = tk.Button(help_, text='OK', command=help_.destroy)
        help_quit.pack()
        help_.bind(sequence='<Return>', func=(lambda x: help_.destroy()))
        help_.mainloop()


    def go(self, branches, inclusivity, extensions, Notice):
        limbs = []
        not_dirs = []
        for x in self.branches:
            psbl_dir = x[0].get()
            if os.path.isdir(psbl_dir):
                limbs.append((psbl_dir, x[1]))
            else:
                not_dirs.append('Not a directory: ' + psbl_dir + '\n')

        if len(not_dirs) > 0:
            self.warning(Notice, not_dirs, type=1)

        rando.rando(limbs, inclusivity, extensions, self, Notice)


if __name__ == '__main__':
    Gui()