import subprocess as sp
from unnamed_exception import *
def run(cmd):
    return sp.Popen(["xterm","-e",cmd]).wait()
def run_keep_window(cmd):
    return sp.Popen(["xterm","-hold","-e",cmd+";returncode=$?;if test $returncode -eq 0;then echo 'Succeed';else echo 'Fail';fi;exit $returncode"]).wait()
try:
    if run("echo 'Hello xmake!'")!=0:
        raise UnnamedException()
except:
    print("You might not have xterm")
    raise
