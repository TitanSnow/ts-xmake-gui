import tk
from argsToCommandLine import argsToCommandLine
from capture_output import capture_output
import re
from threading import Thread
from tkFont import nametofont
def run_in_async(console,args,callback):
    def insert(st):
        console.insert_queue.append(st)
        console.event_generate("<<insert>>",when="tail")
    console.config(state=tk.NORMAL)
    console.delete(1.0,tk.END)
    console.config(state=tk.DISABLED)
    w=console.winfo_width()
    w//=nametofont(console['font']).measure('0')
    h=console.winfo_height()
    h//=nametofont(console['font']).metrics()['linespace']
    pty,conin,conout=capture_output(None,argsToCommandLine(args),None,None,w,h)
    fo=open(conin,"w",0)
    def wait():
        with open(conout,"r",0) as f:
            try:
                while True:
                    st=f.read(1)
                    if not st:
                        break
                    insert(st)
            except IOError:
                pass
        callback()
    Thread(target=wait).start()
    return pty,fo
