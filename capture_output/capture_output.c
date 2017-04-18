#include "winpty.h"
WINPTY_API void* capture_output(
    LPCWSTR appname /*OPTIONAL*/,
    LPCWSTR cmdline /*OPTIONAL*/,
    LPCWSTR cwd /*OPTIONAL*/,
    LPCWSTR env /*OPTIONAL*/
){
    winpty_config_t *config;
    winpty_t *pty;
    winpty_spawn_config_t *spawn_config;
    BOOL suc;
    if(!(config=winpty_config_new(WINPTY_FLAG_PLAIN_OUTPUT,0))) return 0;
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
    return pty;
}
WINPTY_API LPCWSTR get_conout_name(void* pty){
    return winpty_conout_name((winpty_t*)pty);
}
WINPTY_API LPCWSTR get_conin_name(void* pty){
    return winpty_conin_name((winpty_t*)pty);
}
