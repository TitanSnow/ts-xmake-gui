import subprocess as sp
def run(cmd):
    sp.Popen(["xterm","-e",cmd])
def run_keep_window(cmd):
    return run(cmd+";cat")
try:
    run("echo 'Hello xmake!'|cat")
except:
    print("You might not have xterm")
    raise
