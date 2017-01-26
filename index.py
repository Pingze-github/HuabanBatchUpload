# coding=u8
# index.py
# project: HuabanBatchUpload
# author: Pingze-github @ Github

from lib import *
from upload import upload,setCookies,getUser

import threading
import time

# ****** User Input ******
# You must write your cookies below first

cookies_str = "BDTUJIAID=87ad045ce860ea032fe2ed4f6c07918e; _hmt=1; _f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAABJElEQVRYR%2B1VOxYCIQwMF7KzsvFGXmW9kY2VnQfxCvgCRmfzCD9lnz53myWQAJOZBEfeeyIi7xz%2FyEXzZRPFhYbPc3hHXO6I6TbFixmfEyByeQQSxu6BcAXSkIGMazMjuBcz8pQcq44o0Iuyyc1p38C62kNsOdeSZDOQlLRQ80uOMalDgWCGMfsW2B5%2FATMUyGh2uhgptV9Ly6l5nNOa1%2F6zmjTqkH2aGEk2jY72%2B5k%2BNd9lBfLMh8GIP11iK95vw8uv7RQr4oNxOfbQ%2F7g5Z4meveyt0uKDEIiMLRC4jrG1%2FjkwKxCRE2e5lF30leyXYvQ628MZKV3q64HUFvnPAMkVuSWlEouLSiuV6dp2WtPBrPZ7uO5I18tbXWvEC27t%2BTcv%2Bx0JuJAoUm2L%2FQAAAABJRU5ErkJggg%3D%3D%2CWin32.1366.768.24; uid=12697989; sid=Aj2RCNmAUuqFvrwmNrX2q7T5jnS.nST8HvQ2cIYi98j%2F3%2FOs%2BhtMfmuhk6jxAi2FIM2bl4M; crtg_rta=crtnative3criteo_200x200_Pins%3Bcriteo_200x200_Search%3B; _cnzz_CV1256903590=is-logon%7Clogged-in%7C1485431362647%26urlname%7Cqjo3w1jgyk%7C1485431362648; CNZZDATA1256903590=1211073450-1478946017-%7C1485426021; _ga=GA1.2.257306446.1478949278; __asc=b3660762159da9bc02c2cf196c1; __auc=87f1b88c158583f12a3190a62f8" #cookies

path = "./huaban/test" # dirpath
board_name = "测试" # board name

# def main():
#     files = getDirectFiles(path)
#     setCookies(cookies_str)
#     for file in files:
#         print file
#         upload(file,board_name)
#     print("All uploaded.")

# if __name__ == '__main__':
#     main()

class MThread(threading.Thread):
    '可传递参数、指定运行函数的线程类'
    def __init__(self,target,tname,lock,args):
        super(MThread,self).__init__()
        self.setDaemon(True)
        self.target = target
        self.tname = tname
        self.lock = lock
        self.args = args

    def run(self):
        self.target(self.tname,self.lock,self.args)

def uploadOne(tname,lock,args):
    (file_queue,board_name)=args
    lock.acquire()
    print('[Creeper][%s][%s] Thread Start !' % (time.asctime()[11:19], tname))
    lock.release()
    while True:
        if file_queue.empty() == True:
            break
        file_path = file_queue.get()
        upload(file_path,board_name,lock)
    lock.acquire()
    print('[Creeper][%s][%s] Thread Exit !' % (time.asctime()[11:19], tname))
    lock.release()

setCookies(cookies_str)
getUser()
file_list = getDirectFiles(path)
thread_num = 1
file_queue = list2queue(file_list)
lock = threading.Lock()
thread_list = []
for i in range(thread_num):
    thread = MThread(uploadOne,'thread'+'{:0>2}'.format(i),lock,args=(file_queue,board_name))
    thread_list.append(thread)
    thread.start()
for thread in thread_list:
    thread.join()
