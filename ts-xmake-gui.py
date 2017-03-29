#!/usr/bin/env python

import Tkinter as tk
import tkFileDialog
import os
import terminal

class MainWin(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.label_project=tk.Label(self,text="Project")
        self.label_project.pack()

        self.projectdir_input_content=tk.StringVar()
        self.projectdir_input_content.set(os.getenv("HOME"))
        self.projectdir_input=tk.Entry(self,textvariable=self.projectdir_input_content)
        self.projectdir_input.pack()

        self.browse_projectdir=tk.Button(self,text="Browse Project Dir",command=self.action_browse_projectdir)
        self.browse_projectdir.pack()

        self.label_action=tk.Label(self,text="Action")
        self.label_action.pack()

        self.build=tk.Button(self,text="Build!",command=self.action_build)
        self.build.pack()

        self.clean=tk.Button(self,text="Clean",command=self.action_clean)
        self.clean.pack()

    def action_browse_projectdir(self):
        self.projectdir_input_content.set(tkFileDialog.askdirectory(parent=self,initialdir=self.projectdir_input_content.get(),title="Browse Project Dir"))

    def action_common(self,action):
        os.chdir(self.projectdir_input_content.get())
        terminal.run_keep_window("xmake "+action)

    def action_build(self):
        self.action_common("build")

    def action_clean(self):
        self.action_common("clean")

win=MainWin()
win.master.title("xmake")
win.mainloop()
