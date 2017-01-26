# coding=u8
# index.py
# project: HuabanBatchUpload
# author: Pingze-github @ Github

from lib.batch import batchUpload
from lib.auth import getCookies

def main():
    account = "******"
    password = "******"
    cookies_str = getCookies(account,password) # get cookies
    dirpath = "./huaban/test" # dirpath
    board_name = "测试" # board name
    batchUpload(cookies_str,dirpath,board_name)

if __name__ == '__main__':
    main()
