#!/usr/bin/env python3

"""
This module contains everything needed for Random File Opener's graphical interface.
If run as the top level module it initializes the gui.
It has no real utility otherwise.
"""

import os
import threading
import tkinter as tk
from tkinter.filedialog import askdirectory
import rando


class Gui():
    def __init__(self):
        # Initialize the Tk widget, rownum variable and the psbl_brnchs list for the class
        self.root = tk.Tk()
        self.root.title('Random File Opener')
        self.rownum = 0
        self.psbl_brnchs = []

        # Create the tree frame, and create its first branch:
        self.tree = tk.Frame(self.root)
        self.dir_label = tk.Label(
            self.tree, text='Enter the path of a folder to choose from:',
            font=('tk.TkDefaultFont', 12)
        )
        self.dir_label.grid(row=self.rownum)
        self.add_limb()
        self.tree.pack(ipadx=10, ipady=5)

        # Create the (tree)top Frame, and the adder and pruner buttons:
        self.top = tk.Frame(self.root)
        self.adder = tk.Button(
            self.top, text='Add Folder', font=('tk.TkDefaultFont', 12),
            command=lambda: self.add_limb()
        )
        self.adder.grid(row=1, column=1)
        self.pruner = tk.Button(
            self.top, text='Remove Previous', font=('tk.TkDefaultFont', 12), state='disabled',
            command=lambda: self.prune()
        )
        self.pruner.grid(row=1, column=2)
        self.top.pack(ipadx=10, ipady=10)

        # Create the filetypes Frame for excluding or including certain filetypes:
        self.filetypes = tk.Frame(self.root)
        self.incls = tk.Label(
            self.filetypes, text='Choose whether to exclude certain file based on type:',
            font=('tk.TkDefaultFont', 12)
        )
        self.incls.grid(row=0)
        self.inclusivity = tk.IntVar()
        self.extensions = tk.Entry(
            self.filetypes, text='File extensions', width=25, state='disabled'
        )
        self.all_incl = tk.Radiobutton(
            self.filetypes, text='All-Inclusive', value=2, variable=self.inclusivity,
            command=(lambda x=self.extensions: x.config(state='disabled'))
        )
        self.all_incl.grid(row=1)
        self.exclusive = tk.Radiobutton(
            self.filetypes, text='Exclude:', value=1, variable=self.inclusivity,
            command=(lambda x=self.extensions: x.config(state='normal'))
        )
        self.exclusive.grid(row=2)
        self.only_include = tk.Radiobutton(
            self.filetypes, text='Only Include:', value=0, variable=self.inclusivity,
            command=(lambda x=self.extensions: x.config(state='normal'))
        )
        self.only_include.grid(row=3)
        self.inclusivity.set(2)
        self.exts = tk.Label(
            self.filetypes, font=('tk.TkDefaultFont', 11),
            text='Enter the file extensions here if your search is not all-inclusive:'
        )
        self.exts.grid(row=4)
        self.extensions.grid(row=5)
        self.filetypes.pack(ipadx=10, ipady=5)

        # Create a Frame to notify the user of any problems that occur:
        self.problems = tk.Frame(self.root)
        self.problems.pack(ipadx=10)
        self.notice = tk.Label(self.problems)
        self.notice.pack()

        # Create the control buttons:
        self.buttons = tk.Frame(self.root)
        self.goh = tk.Button(
            self.buttons, text='Go!', command=(
                lambda: threading.Thread(None, self.go).run()
            )
        )
        self.goh.grid(row=0, column=1)
        self.clr = tk.Button(
            self.buttons, text='Clear All',
            command=self.clear
        )
        self.clr.grid(row=0, column=2)
        self.hlp = tk.Button(self.buttons, text='Help', command=self.help_)
        self.hlp.grid(row=0, column=3)
        self.qit = tk.Button(self.buttons, text='Quit', command=self.root.destroy)
        self.qit.grid(row=0, column=4)
        self.buttons.pack(ipadx=10, ipady=5)

        # Bind certain keys to certain functions:
        self.root.bind(
            sequence='<Return>', func=(lambda x: threading.Thread(None, self.go).run())
        )
        self.root.bind(sequence='<Control-KeyPress-n>', func=(lambda x: self.add_limb()))
        self.root.bind(sequence='<Control-KeyPress-d>', func=(lambda x: self.prune()))
        self.root.bind(sequence='<Control-KeyPress-h>', func=(lambda x: self.help_()))
        self.root.bind(sequence='<Control-KeyPress-q>', func=(lambda x: self.root.destroy()))
        self.root.bind(sequence='<Control-KeyPress-l>', func=(lambda x: self.clear()))

        # Start the Gui:
        self.root.mainloop()


    def add_limb(self):
        # Add a tk.Frame called limb with fields for user to fill out
        # Increase the rownum, Initialize the Depth Variable:
        self.rownum += 1
        self.limb = tk.Frame(self.tree)
        self.depth = tk.IntVar()

        # Create all the widgets the user will interact with:
        self.dpth = tk.Checkbutton(
            self.limb, text='Search Sub-Folders?', variable=self.depth, onvalue=1, offvalue=0
        )
        self.dpth.grid(row=0, column=0)
        self.entry = tk.Entry(self.limb, width=50)
        self.entry.grid(row=0, column=1)
        self.entry.focus_set()
        self.browse = tk.Button(
            self.limb, text='Browse', command=(
                lambda x=self.entry:[x.delete(0, len(x.get())), x.insert(0, askdirectory())]
            )
        )
        self.browse.grid(row=0, column=2)
        self.limb.grid(row=self.rownum)
        self.psbl_brnchs.append((self.entry, self.depth, self.dpth, self.browse, self.limb))

        # If this is not the first limb, activate the pruner button:
        if self.rownum > 1:
            self.pruner.configure(state='active')


    def prune(self):
        # Move up one row, remove all widgets from the grid, then delete the limb:
        if self.rownum > 1:
            self.rownum -= 1
            remove_these = [0, 2, 3, 4]
            for x in remove_these:
                self.psbl_brnchs[-1][x].grid_remove()
            del self.psbl_brnchs[-1]
        if self.rownum == 1:
            self.pruner.configure(state='disabled')


    def clear(self):
        # Reset/Delete all fields:
        for x in range(1, len(self.psbl_brnchs)):
            self.prune()
        x = self.psbl_brnchs[0]
        x[0].delete(0, len(x[0].get()))
        x[1].set(0)
        self.inclusivity.set(2)
        self.extensions.config(state='normal')
        self.extensions.delete(0, len(self.extensions.get()))
        self.extensions.config(state='disabled')
        self.notice.config(text='')


    def warning(self, notice, problem, type=0):
        # If there was a problem, inform the user of what went wrong;
        # Type 1 configures the notice widget of the Gui.
        if type == 1:
            self.notice.config(text=''.join(problem), fg='red')
            return None

        # Other error types create their own popup window describing the issue.
        failure = tk.Toplevel()
        failure.title('Failed to open file')
        if type == 2:
            reason = tk.Label(failure, fg='red', text=str(problem))
        if type == 3:
            reason = tk.Label(failure, fg='red', text=str(problem))
        if type == 4:
            reason = tk.Label(failure, fg='red', text=str(problem))
        reason.pack()
        quit_warn = tk.Button(failure, text='OK', command=failure.destroy)
        quit_warn.pack()
        failure.mainloop()


    def help_(self):
        # Display basic usage instructions in a popup window:
        help_ = tk.Toplevel()
        help_.title('Help')
        help_text = tk.Label(
            help_, text='Important:\n'
            'Source code: https://github.com/a-v-e-s/randomFileOpener\n'
            'License: https://github.com/a-v-e-s/randomFileOpener/blob/master/LICENSE.md\n'
            'Random File Opener is open source software and comes with No Warranty!\n\n'
            'Usage:\n\n'
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
            'and "Exit" to close the program.\n\n'
            'Keyboard Shortcuts:\n'
            '<Return> runs the program\'s main function.\n'
            '<Ctrl>+n adds a directory\n'
            '<Ctrl>+d removes the last directory.\n'
            '<Ctrl>+l clears all user-supplied information.\n'
            '<Ctrl>+h displays this help message.\n'
            '<Ctrl>+q quits the program.')
        help_text.pack(ipadx=15)
        help_quit = tk.Button(help_, text='OK', command=help_.destroy)
        help_quit.pack()
        help_.bind(sequence='<Return>', func=(lambda x: help_.destroy()))
        help_.mainloop()


    def go(self):
        # Process the entry widgets to ensure they contain valid directories;
        # Alert user of any invalid input, pass valid input to the rando module:
        branches = []
        not_dirs = []
        for x in self.psbl_brnchs:
            psbl_dir = x[0].get()
            if os.path.isdir(psbl_dir):
                branches.append((psbl_dir, x[1].get()))
            else:
                not_dirs.append('Not a directory: ' + psbl_dir + '\n')

        if len(not_dirs) > 0:
            self.warning(self.notice, not_dirs, type=1)

        rando.rando(branches, self.inclusivity.get(), self.extensions.get().split(), self)


if __name__ == '__main__':
    # If this is the top-level module, initialize the Gui:
    Gui()