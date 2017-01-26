# coding=u8
# lib.py
# project: HuabanBatchUpload
# author: Pingze-github @ Github

import os
import requests
import json
import re
from Queue import Queue

def getDirectFiles(path):
    # get direct files in certain dir
    file_list = []
    if (os.path.exists(path) and os.path.isdir(path)):
        for root, dirs, files in os.walk(path):
            break
        for filename in files:
            file_list.append(root+'/'+filename)
    return file_list

def ssearch(pattern,text):
    # a better regex searcher
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

def list2queue(alist):
    # turn list to queue
    queue = Queue()
    for ele in alist:
        queue.put(ele)
    return queue

def json_parse(string):
    # a better json parser
    string = re.sub('undefined','"undefined"',string) #json库不能识别undefined类型
    string = re.sub('null','"null"',string) #json库不能识别null类型
    try:
        data = json.loads(string)
        return data 
    except ValueError:
        return None

def get(url,params="",cookies="",headers="",timeout=3,max_try=5):
    # GET with timeout & retry
    while(max_try-1>0):
        try:
            res = requests.get(url, params=params, cookies=cookies, headers=headers, timeout=timeout)
            return res
        except:
            max_try = max_try - 1
            print("HTTP/GET failed, Now retry ...")
            continue
    return requests.get(url, params=params, cookies=cookies, headers=headers, timeout=timeout)


def post(url,data="",files="",cookies="",headers="",timeout=3,max_try=5):
    # POST with timeout & retry
    while(max_try-1>0):
        try:
            res = requests.post(url, data=data, files=files, cookies=cookies, headers=headers)
            return res
        except:
            max_try = max_try - 1
            print("HTTP/POST failed, Now retry ...")
            continue
    return requests.post(url, data=data, files=files, cookies=cookies, headers=headers)
    return res
