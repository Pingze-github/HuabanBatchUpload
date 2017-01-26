# coding=u8
# auth.py
# project: HuabanBatchUpload
# author: Pingze-github @ Github

from lib import *
import requests

def getCookies(account,password):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    url = "https://huaban.com/auth/"
    data = {
        "email":account
        ,"password":password
        ,"_ref":"frame"
    }
    import requests
    res = requests.post(url,data=data,headers=headers,verify=True)
    if u'{"error":["用户不存在"]}' in res.text:
        print('Login in failed, check account/password')
        exit()
    cookies = res.headers['Set-Cookie']
    return cookies

if __name__ == '__main__':
    account = "18200164037" 
    password = ""
    getCookie(account,password)
