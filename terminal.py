import pty
import os
import tk
from threading import Thread
def run_in_async(console,args,callback):
    def insert(st):
        console.insert_queue.append(st)
        console.event_generate("<<insert>>",when="tail")
    console.config(state=tk.NORMAL)
    console.delete(1.0,tk.END)
    console.config(state=tk.DISABLED)
    pid,fd=pty.fork()
    if pid==0:
        os.execvp(args[0],args)
        exit(127)
    def wait():
        with os.fdopen(fd,"r") as f:
            try:
                while True:
                    st=f.readline()
                    if not st:
                        break
                    insert(st)
            except IOError:
                pass
        code=os.waitpid(pid,0)[1]
        insert("Exitcode: %d\n"%code)
        callback()
    Thread(target=wait).start()
    return pid,fd
