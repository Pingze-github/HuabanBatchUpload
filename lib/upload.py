# coding=u8
# upload.py
# project: HuabanBatchUpload
# author: Pingze-github @ Github

import os
from lib import *
import time

# global variable
cookies = {}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
user = ""

def setCookies(cookies_str):
    global cookies
    cookies = {"cookies_are":cookies_str}

def printWithLock(string,lock):
    # print with lock control
    if lock!=None and str(type(lock))=="<type 'thread.lock'>":
        lock.acquire()
        print(string)
        lock.release()
    else:
        print(string)

def upload(filepath, board_title, pinname=None, lock=None, tname=None):
    # upload single file
    if (type(board_title)!=unicode):
        board_title = unicode(board_title,"u8")
    filename = os.path.basename(filepath)
    pinname = pinname if pinname else filename
    url = "http://huaban.com/upload/"
    image = open(filepath, 'rb')
    files = {
        'Content-Disposition: form-data; name="title"':''
        ,'Content-Disposition: form-data; name="upload1"; filename="'+filename+'" Content-Type: image/jpeg':image
    }
    res = post(url, files=files, cookies=cookies, headers=headers) # 上传图片到花瓣服务器
    file_data = json_parse(res.text)
    if not file_data:
        printWithLock(u'Upload Failed: upload file "{}" not return "id"'.format(filename), lock)
        printWithLock(u'It returns "{}" '.format(res.text), lock)
        return
    file_id = file_data["id"]
    user = getUser()
    board_titles = []
    for dic in user["boards"]:
        board_titles.append(dic["title"])
    if board_title in board_titles:
        board_id = user["boards"][board_titles.index(board_title)]["board_id"]
    else:
        printWithLock(u'Upload Failed: board name "{}" invalid'.format(board_title),lock)
        return
    data = {
        "board_id":board_id
        ,"text":pinname
        ,"copy":"true"
        ,"file_id":file_id
        ,"via":1
        ,"share_button":0
    }
    url = "http://huaban.com/pins/"
    res = post(url, data=data, cookies=cookies, headers=headers) # 添加图片文件到画板
    if('<i class="error">' in res.text):
        printWithLock(u'Upload Failed: file "{}" has been collected for more than 5 times'.format(filename), lock);
    elif json_parse(res.text)!=None:
        data = json_parse(res.text)
        printWithLock (u'[{}][{}] Upload Success: file "{}" to board "{}"'.format(time.asctime()[11:19],tname,filename,board_title), lock);
    else:
        printWithLock(u'Upload Failed: file "{}", for unknown reason'.format(filename), lock);


def getUser():
    # get user data
    global user
    if type(user)==dict:
        return user
    url = "http://huaban.com/"
    res = get(url, cookies=cookies, headers=headers) # 获取主页
    req_json = ssearch('app\["req"\] = ({.+?});',res.text)
    print ("Successfully load user main page data")
    udata = {}
    if req_json:
        req = json_parse(req_json)
        if req["user"]=="null":
            print ("Cookies invalid, login failed")
            exit()
        req_user = req["user"]
        url = url+req_user["urlname"]
        res = get(url, cookies=cookies, headers=headers) # 获取画板页
        user_json = ssearch('app.page\["user"\] = ({.+?});',res.text)
        print("Successfully load user board page data")
        if user_json:
            user = json_parse(user_json)
            return user
        else:
            return
    else:
        return

def main():
    getUser()
    filepath = './huaban/test/test.jpg'
    board_title = '测试' 
    pinname = '测试图片' 
    upload(filepath,board_title,pinname)

if __name__ == '__main__':
    main()
