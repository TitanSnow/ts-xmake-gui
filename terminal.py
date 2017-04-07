import pty
import os
import tk
from threading import Thread
def run_in_async(console,args,callback):
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
                console.config(state=tk.NORMAL)
                console.insert(tk.END,st)
                console.config(state=tk.DISABLED)
        except IOError,e:
            pass
        f.close()
        code=os.waitpid(pid,0)[1]
        console.config(state=tk.NORMAL)
        console.insert(tk.END,"Exitcode: %d\n"%code)
        console.config(state=tk.DISABLED)
        callback()
    Thread(target=wait).start()
