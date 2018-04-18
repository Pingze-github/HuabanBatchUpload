# coding=u8

def inputAutoDecode() :
    str = input()
    return str

def get(paramList) :
    paramValMap = {}
    for param in paramList:
        print(u'请输入 {} :'.format(param['name']))
        paramValMap[param['key']] = inputAutoDecode()
    return paramValMap