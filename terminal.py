import platform
osname=platform.system()
if osname == "Linux":
    from xterm import *
else:
    raise("Not implemented on this system")
