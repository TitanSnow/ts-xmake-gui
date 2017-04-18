import pty
import os
import tk
import re
from threading import Thread,Event
from terminal_string import delete_color
def run_in_async(console,args,callback):
    def insert(st):
        console.insert_queue.append(st)
        console.event_generate("<<insert>>",when="tail")
    console.config(state=tk.NORMAL)
    console.delete(1.0,tk.END)
    console.config(state=tk.DISABLED)
    pid,fd=pty.fork()
    if pid==0:
        #dn=os.open(os.devnull,0)
        #if dn!=0:
            #os.dup2(dn,0)
            #os.close(dn)
        os.execvp(args[0],args)
        exit(127)
    def wait():
        with os.fdopen(fd,"r") as f:
            try:
                while True:
                    st=f.readline()
                    if not st:
                        break
                    st=delete_color(st)
                    insert(st)
                    if re.search('^please input:',st):
                        console.ask_event=Event()
                        console.ask_param=('Input Requested',st)
                        console.event_generate("<<ask>>",when="tail")
                        console.ask_event.wait()
                        os.write(fd,(console.ask_result or '')+'\n')
            except IOError:
                pass
        code=os.waitpid(pid,0)[1]
        insert("Exitcode: %d\n"%code)
        callback()
    Thread(target=wait).start()
    return fd
