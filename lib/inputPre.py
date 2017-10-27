# coding=u8

def inputAutoDecode() :
    str = raw_input()
    try :
        uni = str.decode('utf-8')
    except:
        uni = str.decode('gbk')
    return uni

def get(paramList) :
    paramValMap = {}
    for param in paramList:
        print(u'请输入 {} :'.format(param['name']))
        paramValMap[param['key']] = inputAutoDecode()
    return paramValMap