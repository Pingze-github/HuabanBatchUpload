# coding=u8
# main.py
# project: HuabanBatchUpload
# author: Pingze-github @ Github

import sys
import os
from lib.batch import batchUpload
from lib.auth import getCookie
from lib.auth import testCookie

# TODO cookie使用json储存。可以保存多个cookie。根据账号读取cookie
# TODO 例外状况测试
# 账号不存在、账密错误、文件包含非图片

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
    if not dirpath or not (os.path.exists(dirpath) and os.path.isdir(dirpath)):
        print(u'未设定图片目录路径或路径无效')
        return
    dirpath = os.path.normpath(dirpath)
    if not boardName:
        print(u'未设定画板名')
        return
        # boardName = dirpath[dirpath.rfind('\\') + 1:]  # 默认取文件夹名
    print(u'你的设置: 账号: {}, 密码: {}, 图片目录路径: {}, 画板名: {}'.format(account, password, dirpath, boardName))
    cookie = ''
    if os.path.exists('./cookie.bk') and os.path.isfile('./cookie.bk'):
        with open('./cookie.bk', 'r') as f:
            cookie = f.read()
            testResult = testCookie(cookie);
            if (testResult):
                print(u'验证缓存Cookie成功，用户名为 ' + testResult["username"])
            else:
                cookie = ''

    if not cookie:
        print(u'缓存Cookie不存在或验证失败，使用账密登录...')
        cookie= getCookie(account,password)
        print(u'账密登录成功，获取到Cookie:')
        print(cookie)
        with open('./cookie.bk', 'w') as file:
            file.write(cookie)
            print(u'缓存Cookie成功')

    batchUpload(cookie, dirpath, boardName)

if __name__ == '__main__':
    main()
