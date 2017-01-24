# coding=u8

# upload.py

import os
import requests


filepath = './huaban/test/A1.jpg'
filename = os.path.basename(filepath)
url = "http://huaban.com/upload/"
cookies = "BDTUJIAID=87ad045ce860ea032fe2ed4f6c07918e; _hmt=1; _f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAABJElEQVRYR%2B1VOxYCIQwMF7KzsvFGXmW9kY2VnQfxCvgCRmfzCD9lnz53myWQAJOZBEfeeyIi7xz%2FyEXzZRPFhYbPc3hHXO6I6TbFixmfEyByeQQSxu6BcAXSkIGMazMjuBcz8pQcq44o0Iuyyc1p38C62kNsOdeSZDOQlLRQ80uOMalDgWCGMfsW2B5%2FATMUyGh2uhgptV9Ly6l5nNOa1%2F6zmjTqkH2aGEk2jY72%2B5k%2BNd9lBfLMh8GIP11iK95vw8uv7RQr4oNxOfbQ%2F7g5Z4meveyt0uKDEIiMLRC4jrG1%2FjkwKxCRE2e5lF30leyXYvQ628MZKV3q64HUFvnPAMkVuSWlEouLSiuV6dp2WtPBrPZ7uO5I18tbXWvEC27t%2BTcv%2Bx0JuJAoUm2L%2FQAAAABJRU5ErkJggg%3D%3D%2CWin32.1366.768.24; _tp-257aedc912c3569e1ea1e387539a138d8c2333f56a9f=1; referer=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D9sTbjXCRqNe9PEamSJT5k0l5eO-XyAuqMZUe7_MQqQbOVsh6WczJKIOoqH4p3u6d%26wd%3D%26eqid%3Dfa85c76b000823620000000358874b07; _ga=GA1.2.257306446.1478949278; __asc=2bf46e9b159d071fcf9e3df4c33; __auc=87f1b88c158583f12a3190a62f8; crtg_rta=crtnative3criteo_200x200_Pins%3Bcriteo_200x200_Search%3B; _cnzz_CV1256903590=is-logon%7Clogged-in%7C1485261673896%26urlname%7Cqjo3w1jgyk%7C1485261673896; CNZZDATA1256903590=1211073450-1478946017-%7C1485258621; uid=12697989; sid=Aj2RCNmAUuqFvrwmNrX2q7T5jnS.nST8HvQ2cIYi98j%2F3%2FOs%2BhtMfmuhk6jxAi2FIM2bl4M"
image = open(filepath, 'rb')
cookies = {
    "cookies_are":cookies
}
data = {
    'Content-Disposition: form-data; name="title"':''
    ,'Content-Disposition: form-data; name="upload1"; filename="'+filename+'" Content-Type: image/jpeg':image
}

r = requests.post(url, files=data, cookies=cookies)

print (r.text)
