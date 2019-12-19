# coding=utf-8
# lib.py
# project: HuabanBatchUpload
# author: Pingze-github @ Github

import os
import requests
import json
import re
from queue import Queue


def getDirectFiles(path):
    # get direct files in certain dir
    file_list = []
    if os.path.exists(path) and os.path.isdir(path):
        root = ""
        files = []
        for root, dirs, files in os.walk(path):
            root = root
            files = files
            break
        for filename in files:
            ext = os.path.splitext(filename)
            if not ext[1] or not ext[1][1:] in [
                    'jpg', 'png', 'bmp', 'jpeg', 'gif'
            ]:
                print(u'不支持的文件格式 ' + filename + u' 跳过...')
                continue
            file_list.append(root + '/' + filename)
        print(u"发现 {} 张图片等待上传...".format(len(file_list)))
    else:
        print(u"图片目录路径无效")
        exit()
    return file_list


def ssearch(pattern, text):
    # a better regex searcher
    results = re.search(pattern, text)
    i = 0
    result = None
    while True:
        try:
            result = results.group(i)
        except:
            break
        i = i + 1
    return result


def list2queue(alist):
    # turn list to queue
    queue = Queue()
    for ele in alist:
        queue.put(ele)
    return queue


def json_parse(string):
    # a better json parser
    string = re.sub(':undefined', ':"undefined"',
                    string)  #json库不能识别undefined类型
    string = re.sub(':null', ':"null"', string)  #json库不能识别null类型
    try:
        data = json.loads(string)
        return data
    except ValueError as e:
        raise e
        # return None


def json_stringify(obj):
    try:
        string = json.dumps(obj)
        return string
    except ValueError:
        return None


def get(url, params="", cookies="", headers="", timeout=3, max_try=5):
    # GET with timeout & retry
    while (max_try - 1 > 0):
        try:
            res = requests.get(url,
                               params=params,
                               cookies=cookies,
                               headers=headers,
                               timeout=timeout)
            return res
        except:
            max_try = max_try - 1
            print("HTTP/GET failed, Now retry ...")
            continue
    return requests.get(url,
                        params=params,
                        cookies=cookies,
                        headers=headers,
                        timeout=timeout)


def post(url, data="", files="", cookies="", headers="", max_try=5):
    # POST with timeout & retry
    while (max_try - 1 > 0):
        try:
            res = requests.post(url,
                                data=data,
                                files=files,
                                cookies=cookies,
                                headers=headers)
            return res
        except Exception as e:
            print(e)
            max_try = max_try - 1
            print("HTTP/POST failed, Now retry ...")
            continue
    return requests.post(url,
                         data=data,
                         files=files,
                         cookies=cookies,
                         headers=headers)


def getHeaders():
    return {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }


def decode(str):
    # try :
    #     uni = str.decode('utf-8')
    # except:
    #     uni = str.decode('gbk')
    # return uni
    return str