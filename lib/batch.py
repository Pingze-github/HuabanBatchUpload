# coding=u8
# threads.py
# project: HuabanBatchUpload
# author: Pingze-github @ Github

from lib import *
from upload import upload,setCookies,getUser
import threading
import time

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
    print('[%s][%s] Thread start !' % (time.asctime()[11:19], tname))
    lock.release()
    while True:
        if file_queue.empty() == True:
            break
        file_path = file_queue.get()
        upload(file_path,board_name,lock=lock,tname=tname)
    lock.acquire()
    print('[%s][%s] Thread exit !' % (time.asctime()[11:19], tname))
    lock.release()

def batchUpload(cookie,dirpath,board_name):
    dirpath = unicode(dirpath)
    file_list = getDirectFiles(dirpath)
    setCookies(cookie)
    getUser()
    if len(file_list) > 10:
        thread_num = 10
    else:
        thread_num = len(file_list)
    file_queue = list2queue(file_list)
    lock = threading.Lock()
    thread_list = []
    for i in range(thread_num):
        thread = MThread(uploadOne,'{:0>2}'.format(i),lock,args=(file_queue,board_name))
        thread_list.append(thread)
        thread.start()
    for thread in thread_list:
        thread.join()
    print('All files uploaded !')
