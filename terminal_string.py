import re
def delete_escape(st):
    return re.sub("\x1b\\[.*?m|\r","",st)
