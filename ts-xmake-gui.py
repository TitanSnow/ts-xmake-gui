#!/usr/bin/env python

import Tkinter as tk
import tkFileDialog
import os
import subprocess as sp

class MainWin(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.projectdir_input_content=tk.StringVar()
        self.projectdir_input_content.set(os.getenv("HOME"))
        self.projectdir_input=tk.Entry(self,textvariable=self.projectdir_input_content)
        self.projectdir_input.pack()

        self.browse_projectdir=tk.Button(self,text="Browse Project Dir",command=self.action_browse_projectdir)
        self.browse_projectdir.pack()

        self.make=tk.Button(self,text="Make!",command=self.action_make)
        self.make.pack()

    def action_browse_projectdir(self):
        self.projectdir_input_content.set(tkFileDialog.askdirectory(parent=self,initialdir=self.projectdir_input_content.get(),title="Browse Project Dir"))

    def action_make(self):
        os.chdir(self.projectdir_input_content.get())
        sp.Popen(["xterm","-e","xmake;python -c 'raw_input()'"])

win=MainWin()
win.master.title("xmake")
win.mainloop()
