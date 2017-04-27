#!/usr/bin/env python

import tk
from tkFileDialog import askdirectory,askopenfilename
import os
import terminal
from shutil import rmtree
import conf_parse as cp
import json
from tkMessageBox import showinfo,showerror,askokcancel
import subprocess as sp
import re
import webbrowser as wb
from unnamed_exception import *
from os import path
from tkSimpleDialog import askstring

min_xmake_ver=20000100003L
VER="2d170418 (posix)"

tiped_exception=set()
def error_handle(func):
    def _func(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception as err:
            if not err in tiped_exception:showerror("Internal Exception","Sorry, there is an internal exception happened\n\nDetail:\n"+str(err)+"\n\nBug report:\ngithub.com/TitanSnow/ts-xmake-gui/issues")
            tiped_exception.add(err)
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
        self.projectdir_input_content.set(os.getcwd())
        self.projectdir_input=tk.Entry(self,textvariable=self.projectdir_input_content)
        self.projectdir_input.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=1,column=0,columnspan=4)
        self.projectdir_input.bind("<Return>",self.callback_projectdir_input_return)

        self.browse_projectdir=tk.Button(self,text="Browse Project Dir",command=self.action_browse_projectdir)
        self.browse_projectdir.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=1,column=4,columnspan=2)

        self.label_action=tk.Label(self,text="Action")
        self.label_action.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=2,column=0,columnspan=6)

        self.btnconfig=tk.Button(self,text="Config",command=self.action_config,width=10)
        self.btnconfig.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=3,column=0)

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

        self.target_list=tk.Listbox(self,width=0,height=0)
        self.target_list.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=5,column=0,columnspan=2,rowspan=2)
        self.target_list.bind("<ButtonRelease-1>",self.callback_target_list_click)
        self.target_list.bind("<Return>",self.callback_target_list_click)

        self.label_config=tk.Label(self,text="Config")
        self.label_config.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=4,column=2,columnspan=4)

        self.reload_conf=tk.Button(self,text="Load",command=self.action_reload_conf)
        self.reload_conf.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=5,column=4)

        self.reconfig=tk.Button(self,text="Config",command=self.action_config)
        self.reconfig.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=5,column=5)

        self.configarea=tk.Text(self,width=0,height=10)
        self.configarea.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=6,column=2,columnspan=4)

        self.label_status=tk.Label(self,text="Status")
        self.label_status.grid(sticky=tk.W,row=10,columnspan=6)

        self.label_xmake_path=tk.Label(self,text="xmake path: xmake\t..Checking...")
        self.label_xmake_path.grid(sticky=tk.W,row=11,columnspan=6)

        self.label_console=tk.Label(self,text="Console")
        self.label_console.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=9,columnspan=3)

        self.console=tk.Text(self,state=tk.DISABLED,width=0,height=15)
        self.console.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=7,columnspan=6)
        self.console.insert_queue=[]
        self.console.bind("<<insert>>",self.console_insert)
        self.console.bind("<<ask>>",self.console_ask)

        self.progress=tk.Progressbar(self,length=0)
        self.progress.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=8,columnspan=3)

        self.inputbar_text=tk.StringVar()
        self.inputbar=tk.Entry(self,width=0,textvariable=self.inputbar_text,state=tk.DISABLED)
        self.inputbar.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=8,column=3,columnspan=3)
        self.inputbar.bind("<Return>",lambda e:self.console_sendinput())

        self.btnsend=tk.Button(self,text="Send Input",width=0,command=self.console_sendinput,state=tk.DISABLED)
        self.btnsend.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=9,column=5)

        self.btnshut=tk.Button(self,text="Shut Input",width=0,state=tk.DISABLED,command=self.console_shut)
        self.btnshut.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=9,column=4)

        self.btnkill=tk.Button(self,text="Kill",width=0,state=tk.DISABLED,command=self.console_kill)
        self.btnkill.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=9,column=3)

        self.verlabel=tk.Label(self,text=VER,fg="Darkblue")
        self.verlabel.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=5,column=2,columnspan=2)

        self.reflesh_target_list()
        self.reflesh_configarea()

    @error_handle
    def action_browse_projectdir(self):
        self.projectdir_input_content.set(askdirectory(parent=self,initialdir=self.projectdir_input_content.get(),title="Browse Project Dir"))
        self.reflesh_target_list()
        self.reflesh_configarea()

    @error_handle
    def action_common(self,action,callback=None):
        if isinstance(action,str):
            action=[action]
        os.chdir(self.projectdir_input_content.get())
        target=self.target_list.curselection()
        if not target:
            target=""
        else:
            target=self.targets[target[0]]
        target="--all" if target=="all" else target
        target="" if target=="--all" and action[0][:len("config")]=="config" else target
        args=[]
        if self.option_verbose:
            args.append("--verbose")
        if self.option_backtrace:
            args.append("--backtrace")
        arglist=[self.get_xmake_path()]+action+args
        if target:
            arglist.append(target)
        def reflesh():
            self.enable_all()
            self.reflesh_target_list()
            self.reflesh_configarea()
            self.fd=None
            if callback:
                callback()
        self.disable_all()
        self.pid,self.fd=terminal.run_in_async(self.console,arglist,reflesh)

    @error_handle
    def disable_all(self):
        for child in self.winfo_children():
            try:
                child.config(state=tk.DISABLED)
            except tk.TclError:
                pass
        self.inputbar.config(state=tk.NORMAL)
        self.btnsend.config(state=tk.NORMAL)
        self.btnshut.config(state=tk.NORMAL)
        self.btnkill.config(state=tk.NORMAL)

    @error_handle
    def enable_all(self):
        for child in self.winfo_children():
            try:
                child.config(state=tk.NORMAL)
            except tk.TclError:
                pass
        self.console.config(state=tk.DISABLED)
        self.inputbar.config(state=tk.DISABLED)
        self.btnsend.config(state=tk.DISABLED)
        self.btnshut.config(state=tk.DISABLED)
        self.btnkill.config(state=tk.DISABLED)

    @error_handle
    def action_build(self):
        self.action_common("build")

    @error_handle
    def action_rebuild(self):
        self.action_common(["build","-r"])

    @error_handle
    def action_clean(self):
        self.action_common("clean")

    @error_handle
    def action_distclean(self):
        def cb():
            rmtree(".xmake")
            self.reflesh_target_list()
            self.reflesh_configarea()
        self.action_common("clean",cb)

    @error_handle
    def action_config(self):
        st=self.configarea.get(1.0,tk.END)
        tarconf=None
        try:
            tarconf=json.loads(st)
        except ValueError:
            self.action_common("config")
            return
        cfs=[]
        for key,value in tarconf.items():
            if isinstance(key,str) and isinstance(value,str) or isinstance(key,unicode) and isinstance(value,unicode):
                cfs.append("--%s=%s"%(key,value))
        self.action_common(["config"]+cfs)

    @error_handle
    def action_reload_conf(self):
        self.reflesh_configarea()

    @error_handle
    def read_conf(self):
        try:
            os.chdir(self.projectdir_input_content.get())
            with open(path.join(".xmake","xmake.conf"),"r") as f:
                configs=cp.loads(f.read())
            return configs
        except (OSError,IOError,ValueError):
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

    @error_handle
    def askpath(self,title):
        return askopenfilename(parent=self,title=title)

    @error_handle
    def test_xmake_path(self):
        try:
            out=sp.check_output([self.get_xmake_path(),"--version"])
            rst=re.search(r'(\d+)\.(\d+)\.(\d+)',out)
            ver=rst.groups()
            self.xmake_version='.'.join(ver)
            ver=long(''.join(["%05d"%int(x) for x in ver]))
            if ver>=min_xmake_ver:
                return True
            raise UnnamedException()
        except (OSError,sp.CalledProcessError,AttributeError,UnnamedException):
            return False

    @error_handle
    def get_xmake_version(self):
        try:
            return self.xmake_version
        except AttributeError:
            self.test_xmake_path()
            return self.xmake_version

    @error_handle
    def config_xmake_path(self):
        self.xmake_path=self.askpath("Browse xmake path")
        if not self.test_xmake_path():
            self.label_xmake_path["text"]="xmake_path: "+self.get_xmake_path()+"\t..FAIL!"
            showerror("Error","xmake not found!\n\nIf you're sure you have installed xmake, please config xmake path manually\nOtherwise, goto github.com/tboox/xmake to get one")
        else:
            self.label_xmake_path["text"]="xmake_path: "+self.get_xmake_path()+"\t.. "+self.get_xmake_version()

    @error_handle
    def get_xmake_path(self):
        try:
            return self.xmake_path
        except AttributeError:
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
    def action_package(self):
        self.action_common("package")

    @error_handle
    def action_run(self):
        if askokcancel("Warning","Weak terminal emulation. Continue?"):
            self.action_common("run")

    @error_handle
    def action_global(self):
        self.action_common("global")

    @error_handle
    def action_install(self):
        self.action_common("install")

    @error_handle
    def action_uninstall(self):
        self.action_common("uninstall")

    @error_handle
    def action_create(self):
        self.action_common("create")

    @error_handle
    def action_doxygen(self):
        self.action_common("doxygen")

    @error_handle
    def action_project(self):
        self.action_common("project")

    @error_handle
    def action_hello(self):
        self.action_common("hello")

    @error_handle
    def action_version(self):
        self.action_common("--version")

    @error_handle
    def action_help(self):
        self.action_common("--help")

    @error_handle
    def action_shell(self):
        if askokcancel("Warning","Weak terminal emulation. Continue?"):
            def reflesh():
                self.enable_all()
                self.reflesh_target_list()
                self.reflesh_configarea()
                self.fd=None
            self.disable_all()
            self.pid,self.fd=terminal.run_in_async(self.console,["/bin/sh"],reflesh)

    @error_handle
    def console_insert(self,e):
        console=self.console
        if console.insert_queue:
            console.config(state=tk.NORMAL)
            while console.insert_queue:
                st=console.insert_queue.pop(0)
                console.insert(tk.END,st)
                rst=re.search(r'^\[(\d{2,3})%\]',st)
                if rst:
                    val=int(rst.groups()[0])
                    self.progress.config(value=val)
            console.see(tk.END)
            console.config(state=tk.DISABLED)

    @error_handle
    def console_ask(self,e):
        self.console.ask_result=askstring(*self.console.ask_param)
        self.console.ask_event.set()

    @error_handle
    def console_sendinput(self):
        os.write(self.fd,self.inputbar_text.get()+'\n')
        self.inputbar_text.set("")

    @error_handle
    def console_shut(self):
        os.write(self.fd,'\04')

    @error_handle
    def console_kill(self):
        os.kill(self.pid,15)

@error_handle
def main():
    root=tk.Tk()
    win=MainWin(root)
    root.title("xmake")
    @error_handle
    def show_about():
        showinfo("About","ts-xmake-gui\nAn ugly xmake gui\n\nMaintained by TitanSnow\nLicensed under The Unlicense\nHosted on github.com/TitanSnow/ts-xmake-gui")
    @error_handle
    def show_help():
        wb.open("https://github.com/TitanSnow/ts-xmake-gui/blob/master/README.md",1,True)
    @error_handle
    def stop_all():
        root.quit()
    menubar=tk.Menu(root)
    mn_chores=tk.Menu(root)
    mn_chores.add_command(label="Package",command=win.action_package)
    mn_chores.add_command(label="Run",command=win.action_run)
    mn_chores.add_command(label="Global",command=win.action_global)
    mn_chores.add_command(label="Install",command=win.action_install)
    mn_chores.add_command(label="Uninstall",command=win.action_uninstall)
    mn_chores.add_command(label="Create",command=win.action_create)
    mn_chores.add_separator()
    mn_chores.add_command(label="Doxygen",command=win.action_doxygen)
    mn_chores.add_command(label="Project",command=win.action_project)
    mn_chores.add_command(label="Hello",command=win.action_hello)
    mn_chores.add_separator()
    mn_chores.add_command(label="Version",command=win.action_version)
    mn_chores.add_command(label="Help",command=win.action_help)
    mn_chores.add_separator()
    mn_chores.add_command(label="Shell",command=win.action_shell)
    mn_chores.add_command(label="Exit",command=stop_all)
    menubar.add_cascade(label="Chores",menu=mn_chores)
    mn_option=tk.Menu(root)
    mn_option.add_command(label="xmake path",command=win.config_xmake_path)
    mn_option.add_separator()
    mn_option.add_checkbutton(label="verbose",command=win.toggle_verbose)
    mn_option.add_checkbutton(label="backtrace",command=win.toggle_backtrace)
    menubar.add_cascade(label="Option",menu=mn_option)
    mn_help=tk.Menu(root)
    mn_help.add_command(label="Help",command=show_help)
    mn_help.add_command(label="About",command=show_about)
    menubar.add_cascade(label="Help",menu=mn_help)
    root.config(menu=menubar)
    if not win.test_xmake_path():
        win.label_xmake_path["text"]="xmake_path: "+win.get_xmake_path()+"\t..FAIL!"
        showerror("Error","xmake not found or version is too low!\n\nIf you're sure you have installed xmake 2.1.3+, please config xmake path manually\nOtherwise, goto github.com/tboox/xmake to get one")
    else:
        win.label_xmake_path["text"]="xmake_path: "+win.get_xmake_path()+"\t.. "+win.get_xmake_version()
    @error_handle
    def clear_tiped_exception():
        global tiped_exception
        tiped_exception=set()
        root.after(60000,clear_tiped_exception)
    clear_tiped_exception()
    win.mainloop()
if __name__=="__main__":
    main()
