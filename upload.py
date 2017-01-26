# coding=u8
# upload.py
# project: HuabanBatchUpload
# author: Pingze-github @ Github

import os
from lib import *


# global variable
cookies = {}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
user = ""

def setCookies(cookies_str):
    global cookies
    cookies = {"cookies_are":cookies_str}

def upload(filepath, board_title, pinname=None):
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
    res = requests.post(url, files=files, cookies=cookies, headers=headers) # 上传图片到花瓣服务器
    file_data = json_parse(res.text)
    file_id = file_data["id"]
    user = getUser()
    board_titles = []
    for dic in user["boards"]:
        board_titles.append(dic["title"])
    if board_title in board_titles:
        board_id = user["boards"][board_titles.index(board_title)]["board_id"]
    else:
        print(u'Upload Failed: board name "{}" invalid'.format(board_title))
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
    res = requests.post(url, data=data, cookies=cookies, headers=headers) # 添加图片文件到画板
    if('<i class="error">' in res.text):
        print(u'Upload Failed: "{}" has been cellected for more than 5 times'.format(filename));
    elif json_parse(res.text)!=None:
        data = json_parse(res.text)
        print (u'Upload Success: file "{}" to board "{}"'.format(filename,board_title));
    else:
        print(u'Upload Failed: "{}", for unknown reason'.format(filename));


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
        req_user = req["user"]
        url = url+req_user["urlname"]
        res = get(url, cookies=cookies, headers=headers) # 获取画板页
        user_json = ssearch('app.page\["user"\] = ({.+?});',res.text)
        print ("Successfully load user board page data")
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
