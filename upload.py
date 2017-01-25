# coding=u8

# upload.py

import os
import requests
import json
import re
from cprint import cprint

cookies_str = "BDTUJIAID=87ad045ce860ea032fe2ed4f6c07918e; _hmt=1; _f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAABJElEQVRYR%2B1VOxYCIQwMF7KzsvFGXmW9kY2VnQfxCvgCRmfzCD9lnz53myWQAJOZBEfeeyIi7xz%2FyEXzZRPFhYbPc3hHXO6I6TbFixmfEyByeQQSxu6BcAXSkIGMazMjuBcz8pQcq44o0Iuyyc1p38C62kNsOdeSZDOQlLRQ80uOMalDgWCGMfsW2B5%2FATMUyGh2uhgptV9Ly6l5nNOa1%2F6zmjTqkH2aGEk2jY72%2B5k%2BNd9lBfLMh8GIP11iK95vw8uv7RQr4oNxOfbQ%2F7g5Z4meveyt0uKDEIiMLRC4jrG1%2FjkwKxCRE2e5lF30leyXYvQ628MZKV3q64HUFvnPAMkVuSWlEouLSiuV6dp2WtPBrPZ7uO5I18tbXWvEC27t%2BTcv%2Bx0JuJAoUm2L%2FQAAAABJRU5ErkJggg%3D%3D%2CWin32.1366.768.24; _tp-257aedc912c3569e1ea1e387539a138d8c2333f56a9f=1; referer=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D9sTbjXCRqNe9PEamSJT5k0l5eO-XyAuqMZUe7_MQqQbOVsh6WczJKIOoqH4p3u6d%26wd%3D%26eqid%3Dfa85c76b000823620000000358874b07; _ga=GA1.2.257306446.1478949278; __asc=2bf46e9b159d071fcf9e3df4c33; __auc=87f1b88c158583f12a3190a62f8; crtg_rta=crtnative3criteo_200x200_Pins%3Bcriteo_200x200_Search%3B; _cnzz_CV1256903590=is-logon%7Clogged-in%7C1485261673896%26urlname%7Cqjo3w1jgyk%7C1485261673896; CNZZDATA1256903590=1211073450-1478946017-%7C1485258621; uid=12697989; sid=Aj2RCNmAUuqFvrwmNrX2q7T5jnS.nST8HvQ2cIYi98j%2F3%2FOs%2BhtMfmuhk6jxAi2FIM2bl4M"
cookies = {
    "cookies_are":cookies_str
}

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

# 全局变量
user = "" # 用户信息

def upload(filepath, board_title, pinname):
    # 上传单个文件
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
    file_data = json.loads(res.text)
    file_id = file_data["id"]
    user = getUser()
    board_titles = []
    for dic in user["boards"]:
        board_titles.append(dic["title"])
    cprint (board_titles)
    if board_title in board_titles:
        board_id = user["boards"][board_titles.index(board_title)]["board_id"]
    else:
        print("上传失败：画板名不存在")
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
    print (res.text)

def ssearch(pattern,text):
    results = re.search(pattern,text)
    i = 0
    result = None
    while True:
        try:
            result = results.group(i)
        except:
            break
        i=i+1
    return result

def json_parse(string):
    string = re.sub('undefined','"undefined"',string) #json库不能识别undefined类型
    data = json.loads(string)
    return data 

def getUser():
    # 获取用户信息
    global user
    if type(user)==dict:
        return user
    url = "http://huaban.com/"
    res = requests.get(url, cookies=cookies, headers=headers) # 获取主页
    req_json = ssearch('app\["req"\] = ({.+?});',res.text)
    udata = {}
    if req_json:
        req = json_parse(req_json)
        req_user = req["user"]
        url = url+req_user["urlname"]
        res = requests.get(url, cookies=cookies, headers=headers) # 获取画板页
        user_json = ssearch('app.page\["user"\] = ({.+?});',res.text)
        if user_json:
            user = json_parse(user_json)
            return user
        else:
            return
    else:
        return

def main():
    filepath = './huaban/test/test.jpg'
    board_title = '测试' 
    pinname = '测试图片' 
    upload(filepath,board_title,pinname)

if __name__ == '__main__':
    main()
