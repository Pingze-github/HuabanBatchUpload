# coding=u8
# main.py
# project: HuabanBatchUpload
# author: Pingze-github @ Github

import sys
import os
from lib.batch import batchUpload
from lib.auth import getCookie
from lib.auth import test

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
        print('invalid account or password!')
        return
    if not dirpath or not (os.path.exists(dirpath) and os.path.isdir(dirpath)):
        print('invalid dirpath!')
        return
    dirpath = os.path.normpath(dirpath)
    if not boardName:
        boardName = dirpath[dirpath.rfind('\\') + 1:]  # 默认取文件夹名
    print('Your options: account: {}, password: {}, dirpath: {}, boardName: {}'.format(account, password, dirpath, boardName))
    cookie = ''
    if os.path.exists('./cookie.bk') and os.path.isfile('./cookie.bk'):
        with open('./cookie.bk', 'r') as f:
            cookie = f.read()
            if (test(cookie)):
                print('Using stored cookie ...')
            else:
                cookie = ''
    if not cookie:
        cookie= getCookie(account,password)
        print('Created new cookie ...')
        with open('./cookie.bk', 'w') as file:
            file.write(cookie)
    batchUpload(cookie, dirpath, boardName)

if __name__ == '__main__':
    main()
