import re
def delete_color(st):
    return re.sub("\x1b\\[.*?m|\r","",st)
