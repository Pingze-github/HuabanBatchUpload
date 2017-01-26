# coding=u8
# index.py
# project: HuabanBatchUpload
# author: Pingze-github @ Github

from lib import *
from upload import upload,setCookies

# ****** User Input ******
# You must write your cookies below first

cookies_str = "" #cookies

path = "./huaban/test" # dirpath
board_name = "测试" # board name

def main():
    files = getDirectFiles(path)
    setCookies(cookies_str)
    for file in files:
        print file
        upload(file,board_name)
    print("All uploaded.")

if __name__ == '__main__':
    main()
