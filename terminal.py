import tk
from argsToCommandLine import argsToCommandLine
from capture_output import capture_output
import re
from threading import Thread,Event
def run_in_async(console,args,callback):
    def insert(st):
        console.insert_queue.append(st)
        console.event_generate("<<insert>>",when="tail")
    console.config(state=tk.NORMAL)
    console.delete(1.0,tk.END)
    console.config(state=tk.DISABLED)
    pty,conin,conout=capture_output(None,argsToCommandLine(args),None,None)
    fo=open(conin,"w")
    def wait():
        with open(conout,"r") as f:
            try:
                while True:
                    st=f.readline()
                    if not st:
                        break
                    insert(st)
                    if re.search('^please input:',st):
                        console.ask_event=Event()
                        console.ask_param=('Input Requested',st)
                        console.event_generate("<<ask>>",when="tail")
                        console.ask_event.wait()
                        fo.write((console.ask_result or '')+'\n')
                        fo.flush()
            except IOError:
                pass
        callback()
    Thread(target=wait).start()
    return pty,fo
