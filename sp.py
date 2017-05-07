from capture_output import capture_output
from argsToCommandLine import argsToCommandLine
def check_output(args):
    with open(capture_output(None,argsToCommandLine(args),None,None,None,None)[2],"r") as f:
        return f.read()
