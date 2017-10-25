# HuabanBatchUpload
花瓣网图片批量上传工具

#### 由于花瓣网登录改用https加密，已经不能直接用账密登录！如果要用，请改写cookie！

-----------------------------------------------------------

## 前置库
[requests](https://github.com/kennethreitz/requests/)

## 使用
0. 安装python，并 ```pip install requests``` 安装必备库。
1. 命令行执行 ```python main.py 账号 密码 图片文件目录 画板名```。
* 画板可以不填，默认取图片目录名

## 已实现
+ 上传文件（Python）
+ 添加文件到指定画板
+ 获取用户信息
+ 批量处理
+ 模拟登陆
+ 并发控制
+ 特殊字符路径支持

## 有的同学不会装python

1. 去Python官网下载Python2.xxxx。

2. 安装Python。

3. Win+R打开运行，输入cmd回车，打开命令提示符，输入python和pip两个指令，看看是否能正常运行。若不能，百度“Python环境配置”。

4. 在命令提示符中运行 pip install requests。

