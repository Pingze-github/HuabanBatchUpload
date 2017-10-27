# coding=u8
# threads.py
# project: HuabanBatchUpload
# author: Pingze-github @ Github

from lib import *
from upload import upload,setCookies,getUser
import threading

total = 0
succeed = 0
failed = 0

class MThread(threading.Thread):
    def __init__(self,target,tname,lock,args):
        super(MThread,self).__init__()
        self.setDaemon(True)
        self.target = target
        self.tname = tname
        self.lock = lock
        self.args = args
    def run(self):
        self.target(self.tname,self.lock,self.args)

# 一个上传线程
def uploadOne(tname,lock,args):
    global succeed, failed
    (file_queue,board_name)=args
    # lock.acquire()
    # print('[%s][%s] Thread start !' % (time.asctime()[11:19], tname))
    # lock.release()
    while True:
        if file_queue.empty() == True:
            break
        file_path = file_queue.get()
        uploadSucceed = upload(file_path,board_name,lock=lock,tname=tname)
        if uploadSucceed:
            succeed = 1 + succeed
        else:
            failed = 1 + failed
        lock.acquire()
        print(u'成功数:{} 失败数:{} 总数:{}'.format(succeed, failed, total))
        lock.release()
    # lock.acquire()
    # print('[%s][%s] Thread exit !' % (time.asctime()[11:19], tname))
    # lock.release()

def batchUpload(cookie,dirpath,board_name):
    global total
    dirpath = unicode(dirpath)
    setCookies(cookie)
    user = getUser()
    board_titles = []
    for dic in user["boards"]:
        board_titles.append(dic["title"])
    if not board_name in board_titles:
        print(u'指定画板 ' + board_name + u' 不存在')
        return
    print(u'正在扫描指定目录 ' + dirpath + u'...')
    file_list = getDirectFiles(dirpath)
    total = len(file_list)
    maxThreadNum = 50
    if len(file_list) > maxThreadNum:
        thread_num = maxThreadNum
    else:
        thread_num = len(file_list)
    print(u'执行线程数: '+ str(thread_num))
    file_queue = list2queue(file_list)
    lock = threading.Lock()
    thread_list = []
    for i in range(thread_num):
        thread = MThread(uploadOne,'{:0>2}'.format(i),lock,args=(file_queue,board_name))
        thread_list.append(thread)
        thread.start()
    for thread in thread_list:
        thread.join()
    print(u'全部图片上传完毕!')
