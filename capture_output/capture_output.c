#include "winpty.h"
WINPTY_API LPCWSTR capture_output(
    LPCWSTR appname /*OPTIONAL*/,
    LPCWSTR cmdline /*OPTIONAL*/,
    LPCWSTR cwd /*OPTIONAL*/,
    LPCWSTR env /*OPTIONAL*/
){
    winpty_config_t *config;
    winpty_t *pty;
    winpty_spawn_config_t *spawn_config;
    BOOL suc;
    if(!(config=winpty_config_new(0,0))) return 0;
    pty=winpty_open(config,0);
    winpty_config_free(config);
    if(!pty) return 0;
    spawn_config=winpty_spawn_config_new(WINPTY_SPAWN_FLAG_AUTO_SHUTDOWN,appname,cmdline,cwd,env,0);
    if(!spawn_config){
        winpty_free(pty);
        return 0;
    }
    suc=winpty_spawn(pty,spawn_config,0,0,0,0);
    winpty_spawn_config_free(spawn_config);
    if(!suc){
        winpty_free(pty);
        return 0;
    }
    return winpty_conout_name(pty);
}
