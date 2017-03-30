#!/usr/bin/env python

import Tkinter as tk
import tkFileDialog
import os
import terminal
from shutil import rmtree
import conf_parse as cp

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

        self.rebuild=tk.Button(self,text="Rebuild",command=self.action_rebuild)
        self.rebuild.pack()

        self.clean=tk.Button(self,text="Clean",command=self.action_clean)
        self.clean.pack()

        self.distclean=tk.Button(self,text="Distclean",command=self.action_distclean)
        self.distclean.pack()

        self.label_target=tk.Label(self,text="Target")
        self.label_target.pack()

        self.target_list=tk.Listbox(self)
        self.target_list.pack()

        self.reflesh_target_list()

    def action_browse_projectdir(self):
        self.projectdir_input_content.set(tkFileDialog.askdirectory(parent=self,initialdir=self.projectdir_input_content.get(),title="Browse Project Dir"))
        self.reflesh_target_list()

    def action_common(self,action,after_script=""):
        os.chdir(self.projectdir_input_content.get())
        if after_script:
            after_script=";"+after_script
        target=self.target_list.curselection()
        if not target:
            target=""
        else:
            target=self.targets[target[0]]
        terminal.run_keep_window("xmake "+action+" "+target+after_script)
        self.reflesh_target_list()

    def action_build(self):
        self.action_common("build")

    def action_rebuild(self):
        self.action_common("build -r")

    def action_clean(self):
        self.action_common("clean")

    def action_distclean(self):
        self.action_common("clean")
        rmtree(".xmake")
        self.reflesh_target_list()

    def action_config(self):
        self.action_common("config")

    def read_conf(self):
        try:
            os.chdir(self.projectdir_input_content.get())
            f=open(".xmake/xmake.conf","r")
            configs=cp.loads(f.read())
            f.close()
            return configs
        except:
            return

    def reflesh_target_list(self):
        configs=self.read_conf() or {}
        targets={}
        if "_TARGETS" in configs:
            targets=configs["_TARGETS"]
        self.target_list.delete(0,tk.END)
        for key in targets:
            self.target_list.insert(tk.END,key)
        self.targets=[key for key in targets]

win=MainWin()
win.master.title("xmake")
win.mainloop()
