import tk
from argsToCommandLine import argsToCommandLine
from capture_output_wrapper import capture_output
from threading import Thread
def run_in_async(console,args,callback):
    def insert(st):
        console.insert_queue.append(st)
        console.event_generate("<<insert>>",when="tail")
    console.config(state=tk.NORMAL)
    console.delete(1.0,tk.END)
    console.config(state=tk.DISABLED)
    conout=capture_output(None,argsToCommandLine(args),None,None)
    def wait():
        f=open(conout,"r")
        try:
            while True:
                st=f.readline()
                if not st:
                    break
                insert(st)
        except IOError:
            pass
        f.close()
        callback()
    Thread(target=wait).start()
