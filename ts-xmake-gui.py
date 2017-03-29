#!/usr/bin/env python

import Tkinter as tk
import tkFileDialog
import os
import terminal
from shutil import rmtree

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

        self.config=tk.Button(self,text="Configure",command=self.action_config)
        self.config.pack()

        self.build=tk.Button(self,text="Build",command=self.action_build)
        self.build.pack()

        self.clean=tk.Button(self,text="Clean",command=self.action_clean)
        self.clean.pack()

        self.distclean=tk.Button(self,text="Distclean",command=self.action_distclean)
        self.distclean.pack()

    def action_browse_projectdir(self):
        self.projectdir_input_content.set(tkFileDialog.askdirectory(parent=self,initialdir=self.projectdir_input_content.get(),title="Browse Project Dir"))

    def action_common(self,action,after_script=""):
        os.chdir(self.projectdir_input_content.get())
        if after_script:
            after_script=";"+after_script
        terminal.run_keep_window("xmake "+action+after_script)

    def action_build(self):
        self.action_common("build")

    def action_clean(self):
        self.action_common("clean")

    def action_distclean(self):
        self.action_common("clean")
        rmtree(".xmake")

    def action_config(self):
        self.action_common("config")

win=MainWin()
win.master.title("xmake")
win.mainloop()
