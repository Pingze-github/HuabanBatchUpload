# HuabanBatchUpload
花瓣网图片批量上传工具

## 功能说明
这是一个用于向花瓣网批量上传图片的程序。
+ 多线程并发，可以快速上传大量文件
+ 自动传输错误重试
+ 自动图片处理，避免因“图片已经采集超过5次”而上传失败

## 获取windows可执行版方法
[github-release](https://github.com/Pingze-github/HuabanBatchUpload/releases)

## 使用方法 1
在命令行中执行：`main.exe "账号" "密码" "画板名" "图片目录绝对路径"`

## 使用方法 2
双击打开 main.exe，按提示操作

## 开发
使用Python3.6

## 更新
+ 2018.4.18
更改Python版本为Python3
修复中文名文件上传失败问题
更改打包方法

