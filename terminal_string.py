import re
COLOR_TABLE={
    "30":{"foreground":"#000000"},
    "31":{"foreground":"#CD0000"},
    "32":{"foreground":"#00CD00"},
    "33":{"foreground":"#CDCD00"},
    "34":{"foreground":"#0000EE"},
    "35":{"foreground":"#CD00CD"},
    "36":{"foreground":"#00CDCD"},
    "37":{"foreground":"#E5E5E5"},
    "39":{},#foreground reset

    "40":{"background":"#000000"},
    "41":{"background":"#CD0000"},
    "42":{"background":"#00CD00"},
    "43":{"background":"#CDCD00"},
    "44":{"background":"#0000EE"},
    "45":{"background":"#CD00CD"},
    "46":{"background":"#00CDCD"},
    "47":{"background":"#E5E5E5"},
    "49":{},#background reset
}
class EscapeDeleter:
    def __init__(self,text=None):
        self.__escaped=False
        self.__tag=[]
        self.__escapes=[]
        if text:
            for key,val in COLOR_TABLE.items():
                text.tag_config(key,**val)
    def delete_escape(self,st):
        if len(st)>1:
            return ''.join([self.delete_escape(ch) for ch in st])
        if st=='\x1b':
            self.__escaped=True
        elif self.__escaped and not re.search(r'^(?:\d|;|\[|)$',st):
            self.__escaped=False
            ess=''.join(self.__escapes)
            self.__escapes=[]
            rst=re.search(r'^\x1b\[(\d+)(?:;(\d+))?$',ess)
            if rst and st=='m':
                for tag in [int(x or '0') for x in rst.groups() if x!=None]:
                    if tag==0:
                        self.__tag=[]
                    elif str(tag) in COLOR_TABLE:
                        self.__tag=[x for x in self.__tag if x[0]!=str(tag)[0]]+[str(tag)]
        elif not self.__escaped and st!='\r':
            return st
        if self.__escaped:
            self.__escapes.append(st)
        return ''
    def get_tag(self):
        return tuple(self.__tag) or None
