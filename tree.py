import tk
import os
class TreeDialog:
    def __init__(self,root,error_handle=lambda f:f):
        try:
            tk.DirTree
        except AttributeError:
            return
        self.menu=tk.Menu(root)
        self.win=tk.Toplevel(root,menu=self.menu)
        self.tree=tk.DirTree(self.win,width=200,height=400)
        self.tree.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=0)
        self.flst=tk.Listbox(self.win,width=0,height=10)
        self.flst.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=1)
        self.showhidden=False
        self.cwd=os.getcwd()
        @error_handle
        def list_file():
            self.flst.delete(0,tk.END)
            for item in filter(lambda item:(item[0]!='.' or self.showhidden) and os.path.isfile(os.path.join(self.cwd,item)),os.listdir(self.cwd)):
                self.flst.insert(tk.END,item)
        @error_handle
        def toggle_showhidden():
            self.showhidden=not self.showhidden
            list_file()
        mn_file=tk.Menu(root)
        mn_file.add_checkbutton(label="Show hidden files",command=toggle_showhidden)
        mn_file.add_separator()
        mn_file.add_command(label="Close",command=lambda :self.win.destroy())
        mn_file.add_command(label="Exit",command=lambda :root.quit())
        self.menu.add_cascade(label="File",menu=mn_file)
        @error_handle
        def browse(path):
            self.cwd=path
            list_file()
        self.tree.config(browsecmd=browse)
        @error_handle
        def chdir(path):
            browse(path)
            root.event_generate("<<chprojectdir>>",when="tail")
        self.tree.config(command=chdir)
        @error_handle
        def callback_file(e):
            index=self.flst.curselection()
            if not index:return
            fn=self.flst.get(index)
            fp=os.path.join(self.cwd,fn)
            # TODO
        self.flst.bind("<Double-Button-1>",callback_file)
        list_file()
