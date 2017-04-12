from unnamed_exception import *
try:
    from xterm import *
except (UnnamedException,OSError):
    from curshell import *
