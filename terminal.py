import pty
import os
import tk
from threading import Thread
from terminal_string import delete_color
def run_in_async(console,args,callback):
    def insert(st):
        console.config(state=tk.NORMAL)
        console.insert(tk.END,delete_color(st))
        console.see(tk.END)
        console.config(state=tk.DISABLED)
    console.config(state=tk.NORMAL)
    console.delete(1.0,tk.END)
    console.config(state=tk.DISABLED)
    pid,fd=pty.fork()
    if pid==0:
        dn=os.open(os.devnull,0)
        if dn!=0:
            os.dup2(dn,0)
            os.close(dn)
        os.execvp(args[0],args)
        exit(127)
    def wait():
        f=os.fdopen(fd,"r")
        try:
            while True:
                st=f.readline()
                if not st:
                    break
                insert(st)
        except IOError,e:
            pass
        f.close()
        code=os.waitpid(pid,0)[1]
        insert("Exitcode: %d\n"%code)
        callback()
    Thread(target=wait).start()
