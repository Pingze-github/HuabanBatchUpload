# coding=u8
# main.py
# project: HuabanBatchUpload
# author: Pingze-github @ Github

import sys
import os
from lib.batch import batchUpload
from lib.auth import getCookie
from lib.auth import testCookie
from lib.lib import json_parse, json_stringify

# TODO 处理图片来避免因过多采集而上传失败

def main():
    account = "" # 账户名
    password = "" # 密码
    dirpath = "" # 要上传的图片所在目录
    boardName = "" # 要上传到的画板名
    # 优先接受命令行参数
    if len(sys.argv) >= 2:
        account = sys.argv[1]
    if len(sys.argv) >= 3:
        password = sys.argv[2]
    if len(sys.argv) >= 4:
        dirpath = sys.argv[3]
    if len(sys.argv) >= 5:
        boardName = sys.argv[4]
    if not account or not password:
        print(u'未设定账密')
        return
    if not dirpath:
        print(u'未设定图片目录路径')
        return
    if not (os.path.exists(dirpath) and os.path.isdir(dirpath)):
        print(u'设定图片目录路径'+ dirpath + u'无效')
        return
    dirpath = os.path.normpath(dirpath)
    if not boardName:
        print(u'未设定画板名')
        return
        # boardName = dirpath[dirpath.rfind('\\') + 1:]  # 默认取文件夹名
    print(u'你的设置: 账号: {}, 密码: {}, 图片目录路径: {}, 画板名: {}'.format(account, password, dirpath, boardName))
    cookie = None
    cookieJsonPath = './cookie.json'
    if os.path.exists(cookieJsonPath) and os.path.isfile(cookieJsonPath):
        with open(cookieJsonPath, 'r') as f:
            cookieMap = json_parse(f.read())
            if not cookieMap or not cookieMap[account] :
                print(u'未找到缓存Cookie')
            else:
                cookie = cookieMap[account]
                testResult = testCookie(cookie)
                if (testResult):
                    print(u'验证缓存Cookie成功，用户名为 ' + testResult["username"])
                else:
                    print(u'验证缓存Cookie失败')

    if not cookie:
        print(u'使用账密登录...')
        cookie = getCookie(account,password)
        if not cookie:
            return
        print(u'账密登录成功，获取到Cookie:')
        with open(cookieJsonPath, 'w+') as file:
            cookieMap = json_parse(file.read())
            if not cookieMap:
                cookieMap = {}
            cookieMap[account] = cookie
            file.write(json_stringify(cookieMap))
            print(u'缓存Cookie成功')

    batchUpload(cookie, dirpath, boardName)

if __name__ == '__main__':
    main()
