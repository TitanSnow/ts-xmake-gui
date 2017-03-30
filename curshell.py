import os
def run(cmd):
    if os.system(cmd)==0:
        print("Succeed")
    else:
        print("Fail")
def run_keep_window(cmd):
    return run(cmd)
