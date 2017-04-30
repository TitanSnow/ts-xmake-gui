import pty
import os
import tk
from threading import Thread
from tkFont import nametofont
from fcntl import ioctl
from termios import TIOCSWINSZ
from struct import pack
from sys import stdout
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
    pid,fd=pty.fork()
    if pid==0:
        ioctl(stdout.fileno(),TIOCSWINSZ,pack('HHHH',h,w,0,0))
        os.execvp(args[0],args)
        exit(127)
    def wait():
        try:
            while True:
                st=os.read(fd,1)
                if not st:
                    break
                insert(st)
        except OSError as e:
            if e.errno!=5:
                raise
        os.close(fd)
        code=os.waitpid(pid,0)[1]
        insert("Exitcode: %d\n"%code)
        callback()
    Thread(target=wait).start()
    return pid,fd
