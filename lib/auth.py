# coding=u8
# auth.py
# project: HuabanBatchUpload
# author: Pingze-github @ Github

from lib import *
import os

def getCookie(account,password):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    url = "https://huaban.com/auth/"
    data = {
        "email":account
        ,"password":password
        ,"_ref":"frame"
    }
    import requests
    # 查看有无cacert证书
    verify = './cacert.pem'
    if not os.path.exists(verify) or not os.path.isfile(verify) :
        verify = True
    res = requests.post(url, data = data, headers = headers, verify = verify)
    if u'{"error":["用户不存在"]}' in res.text:
        print(u'登录失败，请检查账密')
        exit()
    if u'登录频率过快' in res.text:
        print(u'登录频率过快，登录被阻断。请在浏览器中登录一次后再尝试')
        exit()
    if 'Set-Cookie' in res.headers:
        cookies = res.headers['Set-Cookie']
    elif 'set-cookie' in res.headers:
        cookies = res.headers['set-cookie']
    else:
        print(u'登录失败，未知原因')
        print(res.text)
        cookies = ''

    return cookies

def testCookie(cookie) :
    url = "http://huaban.com/"
    res = get(url, cookies = {"cookies_are": cookie}, headers = getHeaders()) # 获取主页
    if 'app.page["user_info"]' in res.text :
        username = ssearch('"username":"(.+?)"', res.text)
        return {"username": username}
    else:
        return False

if __name__ == '__main__':
    account = "" 
    password = ""
    getCookie(account,password)
