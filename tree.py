import tk
def init(root):
    try:
        tk.DirTree
    except AttributeError:
        return
    menu=tk.Menu(root)
    win=tk.Toplevel(root,menu=menu)
    mn_file=tk.Menu(root)
    mn_file.add_checkbutton(label="Show hidden files")
    mn_file.add_separator()
    mn_file.add_command(label="Close",command=lambda :win.destroy())
    mn_file.add_command(label="Exit",command=lambda :root.quit())
    menu.add_cascade(label="File",menu=mn_file)
    tree=tk.DirTree(win,width=200,height=400)
    tree.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=0)
    flst=tk.Listbox(win,width=0,height=10)
    flst.grid(sticky=tk.W+tk.E+tk.N+tk.S,row=1)
