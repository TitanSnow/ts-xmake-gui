from unnamed_exception import UnnamedException
from ctypes import CDLL,c_wchar_p
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
    conout=libcapture_output.capture_output(appname,cmdline,cwd,env)
    if conout:
        return str(c_wchar_p(conout).value)
    raise UnnamedException("capture_output error")
