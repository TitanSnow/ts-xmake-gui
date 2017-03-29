import json
import re
def loads(st):
    rg = r'\[("(?:[^"]|\\")*")\] ='
    rst = re.sub(rg, r'\1:', st)
    return json.loads(rst)
