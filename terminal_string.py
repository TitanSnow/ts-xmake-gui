import re
class EscapeDeleter:
    def __init__(self):
        self.__escaped=False
    def delete_escape(self,st):
        if len(st)>1:
            return ''.join([self.delete_escape(ch) for ch in st])
        if st=='\x1b':
            self.__escaped=True
        elif self.__escaped and st=='m':
            self.__escaped=False
        elif not self.__escaped and st!='\r':
            return st
        return ''
