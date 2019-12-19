# coding=u8
# upload.py
# project: HuabanBatchUpload
# author: Pingze-github @ Github

import time
from .lib import *
from .recreateImg import recreate
# global variable
cookies = {}
headers = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}
user = ""


def setCookies(cookies_str):
    global cookies
    cookies = {"cookies_are": cookies_str}


def printWithLock(string, lock):
    # print with lock control
    if lock != None and str(type(lock)) == "<type 'thread.lock'>":
        lock.acquire()
        print(string)
        lock.release()
    else:
        print(string)


def upload(filepath, board_title, pinname=None, lock=None, tname=None):
    # upload single file
    board_title = board_title
    filename = os.path.basename(filepath)
    pinname = pinname if pinname else filename

    url = "https://huaban.com/upload/"
    image = open(os.path.abspath(filepath), 'rb')
    files = [
        # 此处空置tuple的首个属性（原本为文件名，中文文件名报错）
        ('file', ('', image, 'image/png'))
    ]
    res = post(url, files=files, cookies=cookies, headers=headers)
    file_data = json_parse(res.text)
    if file_data.get('err') == 500:
        printWithLock(
            u'[{}] 上传失败: "{}" 未知原因'.format(time.asctime()[11:19], filename),
            lock)
        printWithLock(u'服务器返回:' + res.text, lock)
        return False
    if not file_data:
        printWithLock(
            u'[{}] 上传失败: "{}" 上传请求未返回id'.format(time.asctime()[11:19],
                                                filename), lock)
        printWithLock(u'返回了 "{}" '.format(res.text), lock)
        return False
    file_id = file_data["id"]
    user = getUser()
    board_titles = []
    for dic in user["boards"]:
        board_titles.append(dic["title"])
    if board_title in board_titles:
        board_id = user["boards"][board_titles.index(board_title)]["board_id"]
    else:
        printWithLock(
            u'[{}] 上传失败: 画板名 "{}" 不存在，请先建立画板'.format(time.asctime()[11:19],
                                                     board_title), lock)
        return False
    data = {
        "board_id": board_id,
        "text": pinname,
        "copy": "true",
        "file_id": file_id,
        "via": 1,
        "share_button": 0
    }
    url = "https://huaban.com/pins/"
    res = post(url, data=data, cookies=cookies, headers=headers)  # 添加图片文件到画板
    if ('<i class="error">' in res.text):
        printWithLock(
            u'[{}] 上传失败: 图片 "{}" 已经被采集超过5次，准备处理图片后重试...'.format(
                time.asctime()[11:19], filename), lock)
        recreate(filepath)
        return upload(filepath, board_title, pinname, lock, tname)
    elif json_parse(res.text) != None:
        printWithLock(
            u'[{}] 上传成功: 图片 "{}" 到画板 "{}"'.format(time.asctime()[11:19],
                                                  filename, board_title), lock)
        return True
    else:
        printWithLock(
            u'[{}] 上传失败: 图片 "{}", 原因不明'.format(time.asctime()[11:19],
                                               filename), lock)
        return False


def getUser():
    # get user data
    global user
    if type(user) == dict:
        return user
    url = "http://huaban.com/"
    res = get(url, cookies=cookies, headers=headers)  # 获取主页
    req_json = ssearch('app\["req"\] = ({.+?});', res.text)

    if req_json:
        print(u"成功读取用户主页信息")
        req = json_parse(req_json)
        if req["user"] == "null":
            print(u"未成功获取用户主页信息")
            exit(1)
        req_user = req["user"]
        url = url + req_user["urlname"]
        # 获取画板页
        res = get(url, cookies=cookies, headers=headers)
        user_json = ssearch('app.page\["user"\] = ({.+?});', res.text)
        if user_json:
            print(u"成功读取用户画板信息")

            d = json.loads(user_json)

            with open("user_json.txt", "w", encoding="utf-8") as f:
                f.write(user_json)
            user = json.loads(user_json)
            print(u'解析成功')

            return user
        else:
            print(u"未能成功读取用户画板信息")
            exit(1)
    else:
        print(u"未能成功读取用户画板信息")
        exit(1)


def main():
    getUser()
    filepath = './huaban/test/test.jpg'
    board_title = '测试'
    pinname = '测试图片'
    upload(filepath, board_title, pinname)


if __name__ == '__main__':
    main()