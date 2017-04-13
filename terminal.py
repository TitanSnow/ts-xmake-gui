import subprocess as sp
import os
def run_out_sync(args):
    sp.Popen([os.getenv("COMSPEC") or "cmd","/K"]+args).wait()
