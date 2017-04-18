from unnamed_exception import UnnamedException
from ctypes import CDLL,c_wchar_p,c_wchar,c_void_p,sizeof
assert sizeof(c_wchar)==2
libcapture_output=CDLL("capture_output")
def capture_output(appname,cmdline,cwd,env):
    if appname!=None:
        appname=c_wchar_p(unicode(appname))
    if cmdline!=None:
        cmdline=c_wchar_p(unicode(cmdline))
    if cwd!=None:
        cwd=c_wchar_p(unicode(cwd))
    if env!=None:
        env=c_wchar_p(unicode(env))
    pty=c_void_p(libcapture_output.capture_output(appname,cmdline,cwd,env))
    if pty:
        return pty,str(c_wchar_p(libcapture_output.get_conin_name(pty)).value),str(c_wchar_p(libcapture_output.get_conout_name(pty)).value)
    raise UnnamedException("capture_output error")
