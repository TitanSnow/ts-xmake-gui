#!/usr/bin/env python

import Tkinter as tk
import tkFileDialog
import os
import terminal
from shutil import rmtree
import conf_parse as cp
import json
from tkMessageBox import showinfo,showerror
from threading import Timer

tiped_exception=set()
def error_handle(func):
    def _func(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception,err:
            if not err in tiped_exception:showerror("Internal Exception","Sorry, there is an internal exception happened\n\nDetail:\n"+str(err))
            tiped_exception.add(err)
            raise
        except:
            showerror("Internal Exception","Sorry, there is an unknown internal exception happened")
            raise
    return _func

class MainWin(tk.Frame):
    @error_handle
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.pack()
        self.createWidgets()
        self.option_verbose=False
        self.option_backtrace=False

    @error_handle
    def createWidgets(self):
        self.label_project=tk.Label(self,text="Project")
        self.label_project.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=0,column=0,columnspan=6)

        self.projectdir_input_content=tk.StringVar()
        self.projectdir_input_content.set(os.getenv("HOME"))
        self.projectdir_input=tk.Entry(self,textvariable=self.projectdir_input_content)
        self.projectdir_input.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=1,column=0,columnspan=4)
        self.projectdir_input.bind("<Return>",self.callback_projectdir_input_return)

        self.browse_projectdir=tk.Button(self,text="Browse Project Dir",command=self.action_browse_projectdir)
        self.browse_projectdir.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=1,column=4,columnspan=2)

        self.label_action=tk.Label(self,text="Action")
        self.label_action.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=2,column=0,columnspan=6)

        self.config=tk.Button(self,text="Config",command=self.action_config,width=10)
        self.config.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=3,column=0)

        self.build=tk.Button(self,text="Build",command=self.action_build,width=20)
        self.build.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=3,column=1,columnspan=2)

        self.rebuild=tk.Button(self,text="Rebuild",command=self.action_rebuild,width=10)
        self.rebuild.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=3,column=3)

        self.clean=tk.Button(self,text="Clean",command=self.action_clean,width=10)
        self.clean.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=3,column=4)

        self.distclean=tk.Button(self,text="Distclean",command=self.action_distclean,width=10)
        self.distclean.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=3,column=5)

        self.label_target=tk.Label(self,text="Target")
        self.label_target.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=4,column=0,columnspan=2)

        self.target_list=tk.Listbox(self,width=0)
        self.target_list.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=5,column=0,columnspan=2,rowspan=2)
        self.target_list.bind("<ButtonRelease-1>",self.callback_target_list_click)
        self.target_list.bind("<Return>",self.callback_target_list_click)

        self.label_config=tk.Label(self,text="Config")
        self.label_config.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=4,column=2,columnspan=4)

        self.reload_conf=tk.Button(self,text="Load",command=self.action_reload_conf)
        self.reload_conf.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=5,column=2,columnspan=2)

        self.reconfig=tk.Button(self,text="Config",command=self.action_config)
        self.reconfig.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=5,column=4,columnspan=2)

        self.configarea=tk.Text(self,width=0)
        self.configarea.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=6,column=2,columnspan=4)

        self.label_status=tk.Label(self,text="Status")
        self.label_status.grid(sticky=tk.W,row=7,columnspan=6)

        self.label_xmake_path=tk.Label(self,text="xmake path: xmake\t..Checking...")
        self.label_xmake_path.grid(sticky=tk.W,row=8,columnspan=6)

        self.reflesh_target_list()
        self.reflesh_configarea()

    @error_handle
    def action_browse_projectdir(self):
        self.projectdir_input_content.set(tkFileDialog.askdirectory(parent=self,initialdir=self.projectdir_input_content.get(),title="Browse Project Dir"))
        self.reflesh_target_list()
        self.reflesh_configarea()

    @error_handle
    def action_common(self,action):
        os.chdir(self.projectdir_input_content.get())
        target=self.target_list.curselection()
        if not target:
            target=""
        else:
            target=self.targets[target[0]]
        target="--all" if target=="all" else target
        target="" if target=="--all" and action[:len("config")]=="config" else target
        args=[]
        if self.option_verbose:
            args.append("--verbose")
        if self.option_backtrace:
            args.append("--backtrace")
        args=' '.join(args)
        terminal.run_keep_window(self.get_xmake_path()+" "+action+" "+args+" "+target)
        self.reflesh_target_list()
        self.reflesh_configarea()

    @error_handle
    def action_build(self):
        self.action_common("build")

    @error_handle
    def action_rebuild(self):
        self.action_common("build -r")

    @error_handle
    def action_clean(self):
        self.action_common("clean")

    @error_handle
    def action_distclean(self):
        self.action_common("clean")
        rmtree(".xmake")
        self.reflesh_target_list()
        self.reflesh_configarea()

    @error_handle
    def action_config(self):
        st=self.configarea.get(1.0,tk.END)
        tarconf=None
        try:
            tarconf=json.loads(st)
            if not self.origin_config:
                raise()
        except:
            self.action_common("config")
            return
        cfs=[]
        for key,value in tarconf.items():
            key=str(key)
            value=str(value)
            cfs.append(" '--%s=%s'"%(key.replace("'","\\'"),value.replace("'","\\'")))
        self.action_common("config "+''.join(cfs))

    @error_handle
    def action_reload_conf(self):
        self.reflesh_configarea()

    @error_handle
    def read_conf(self):
        try:
            os.chdir(self.projectdir_input_content.get())
            f=open(".xmake/xmake.conf","r")
            configs=cp.loads(f.read())
            f.close()
            return configs
        except:
            return

    @error_handle
    def reflesh_target_list(self):
        configs=self.read_conf() or {}
        targets={}
        if "_TARGETS" in configs:
            targets=configs["_TARGETS"]
        self.target_list.delete(0,tk.END)
        for key in targets:
            self.target_list.insert(tk.END,key)
        self.targets=[key for key in targets]

    @error_handle
    def reflesh_configarea(self):
        self.configarea.delete(1.0,tk.END)
        target=self.target_list.curselection()
        if target:
            target=self.targets[target[0]]
            configs=self.read_conf()
            if configs and "_TARGETS" in configs and target in configs["_TARGETS"]:
                tarconf=configs["_TARGETS"][target]
                st=json.dumps(tarconf,indent=4,separators=(',',': '))
                self.configarea.insert(tk.END,st)
                self.origin_config=tarconf

    @error_handle
    def askpath(self,title):
        return tkFileDialog.askopenfilename(parent=self,title=title)

    @error_handle
    def test_xmake_path(self):
        return os.system(self.get_xmake_path()+" --version")==0

    @error_handle
    def config_xmake_path(self):
        self.xmake_path=self.askpath("Browse xmake path")
        if not self.test_xmake_path():
            self.label_xmake_path["text"]="xmake_path: "+self.get_xmake_path()+"\t..FAIL!"
            showerror("Error","xmake not found!\n\nIf you're sure you have installed xmake, please config xmake path manually\nOtherwise, goto github.com/tboox/xmake to get one")
        else:
            self.label_xmake_path["text"]="xmake_path: "+self.get_xmake_path()+"\t..OK"

    @error_handle
    def get_xmake_path(self):
        try:
            return self.xmake_path
        except:
            return "xmake"

    @error_handle
    def callback_projectdir_input_return(self,event):
        self.reflesh_target_list()
        self.reflesh_configarea()

    @error_handle
    def callback_target_list_click(self,event):
        self.reflesh_configarea()

    @error_handle
    def toggle_verbose(self):
        self.option_verbose=not self.option_verbose

    @error_handle
    def toggle_backtrace(self):
        self.option_backtrace=not self.option_backtrace

@error_handle
def main():
    win=MainWin()
    win.master.title("xmake")
    menubar=tk.Menu(win.master)
    def show_about():
        showinfo("About","ts-xmake-gui\nAn ugly xmake gui\n\nMaintained by TitanSnow\nLicensed under The Unlicense\nHosted on github.com/TitanSnow/ts-xmake-gui")
    mn_option=tk.Menu(win.master)
    mn_option.add_command(label="xmake path",command=win.config_xmake_path)
    mn_option.add_checkbutton(label="verbose",command=win.toggle_verbose)
    mn_option.add_checkbutton(label="backtrace",command=win.toggle_backtrace)
    menubar.add_cascade(label="Option",menu=mn_option)
    menubar.add_command(label="About",command=show_about)
    win.master.config(menu=menubar)
    if not win.test_xmake_path():
        win.label_xmake_path["text"]="xmake_path: "+win.get_xmake_path()+"\t..FAIL!"
        showerror("Error","xmake not found!\n\nIf you're sure you have installed xmake, please config xmake path manually\nOtherwise, goto github.com/tboox/xmake to get one")
    else:
        win.label_xmake_path["text"]="xmake_path: "+win.get_xmake_path()+"\t..OK"
    def clear_tiped_exception():
        tiped_exception=set()
    Timer(60,clear_tiped_exception).start()
    win.mainloop()
if __name__=="__main__":
    main()
