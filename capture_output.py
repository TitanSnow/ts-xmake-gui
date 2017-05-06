from ctypes import *
assert sizeof(c_wchar)==2
libwinpty=CDLL("winpty.dll")
class WinptyError(Exception):
    pass
def capture_output(appname,cmdline,cwd,env,width,height):
    if appname!=None:
        appname=c_wchar_p(unicode(appname))
    if cmdline!=None:
        cmdline=c_wchar_p(unicode(cmdline))
    if cwd!=None:
        cwd=c_wchar_p(unicode(cwd))
    if env!=None:
        env=c_wchar_p(unicode(env))
    config=c_void_p(libwinpty.winpty_config_new(c_ulonglong(0x2),None))
    if not config:raise WinptyError()
    if width and height:
        libwinpty.winpty_config_set_initial_size(config,c_int(width),c_int(height))
    pty=c_void_p(libwinpty.winpty_open(config,None))
    libwinpty.winpty_config_free(config)
    if not pty:raise WinptyError()
    spawn_config=c_void_p(libwinpty.winpty_spawn_config_new(c_ulonglong(1),appname,cmdline,cwd,env,None))
    if not spawn_config:
        libwinpty.winpty_free(pty)
        raise WinptyError()
    suc=c_int(libwinpty.winpty_spawn(pty,spawn_config,None,None,None,None))
    libwinpty.winpty_spawn_config_free(spawn_config)
    if not suc:
        libwinpty.winpty_free(pty)
        raise WinptyError()
    return pty,str(c_wchar_p(libwinpty.winpty_conin_name(pty)).value),str(c_wchar_p(libwinpty.winpty_conout_name(pty)).value)
