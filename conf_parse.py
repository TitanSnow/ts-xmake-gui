import json
def loads(st):
    rst=[]
    non=0
    inq=False
    for ch in st:
        if ch=='"':
            if non<=0:
                inq=not inq;
        elif ch=="\\":
            if inq and non<=0:
                non=2
        rst.append(ch)
        if (ch=="[" or ch=="]") and not inq:
            rst.pop()
        if ch=="=" and not inq:
            rst[-1]=":"
        non-=1
    return json.loads(''.join(rst))
