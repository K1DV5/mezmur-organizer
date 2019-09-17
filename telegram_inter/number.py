nums1  = {1: '\u1369'
        , 2: '\u136A'
        , 3: '\u136B'
        , 4: '\u136C'
        , 5: '\u136D'
        , 6: '\u136E'
        , 7: '\u136F'
        , 8: '\u1370'
        , 9: '\u1371'
        , 0: ""}

nums10  = {1: '\u1372'
         , 2: '\u1373'
         , 3: '\u1374'
         , 4: '\u1375'
         , 5: '\u1376'
         , 6: '\u1377'
         , 7: '\u1378'
         , 8: '\u1379'
         , 9: '\u137A'
         , 0: ""}

num00  =   '\u137B'
num0000  = '\u137C'

def geez_num(n):
    n = str(n)
    numlen = len(n)
    if numlen % 2 == 1:
        numlen += 1
        n = "0" + n

    ret = ""
    for i in range(int(numlen/2)):
        current2 = n[i*2:i*2+2]
        ret = ret + nums10[int(current2[0])] + nums1[int(current2[1])] + num00

    #  clip the 00 and the first if it is 1
    startPos = 1 if ret[1] == nums1[1] and len(ret) > 2 else 0
    return ret[startPos:-1]

