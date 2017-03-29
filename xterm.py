import subprocess as sp
def run(cmd):
    sp.Popen(["xterm","-e",cmd]).wait()
def run_keep_window(cmd):
    sp.Popen(["xterm","-e",cmd+";if test $? -eq 0;then echo 'Succeed';else echo 'Fail';fi;cat"]).wait()
try:
    run("echo 'Hello xmake!'|cat")
except:
    print("You might not have xterm")
    raise
