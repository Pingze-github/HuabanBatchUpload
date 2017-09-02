# HuabanBatchUpload
花瓣网图片批量上传工具

## 前置库
[requests](https://github.com/kennethreitz/requests/)

## 使用
1. 编辑main.py。将账号/密码/图片文件夹/画板名填入。
5. 运行main.py

## 已实现
+ 上传文件（Python）
+ 添加文件到指定画板
+ 获取用户信息
+ 批量处理
+ 模拟登陆
+ 并发控制

## 待实现
+ GUI
+ 增加保存cookies功能，避免使用者短时间内重复登录造成的bug。

## 从0开始的使用方法

1. 下载Python Release Python 2.7.13，WindowsOS建议选择MSI installer。

2. 使用下载好的文件安装Python。

3. Win+R打开运行，输入cmd回车，打开命令提示符，输入python和pip两个指令，看看是否能正常运行。若不能，百度“Python环境配置”。

4. 在命令提示符中运行 pip install requests。

5. 在Github中下载zip包，并解压。使用任何文本编辑器编辑main文件。

6. 修改account和password值为花瓣网帐号密码；修改board_name值为上传的画板名；修改dirpath为上传图片所在文件夹路径。

7. 打开命令提示符，输入命令 python main.py ，回车运行。这里注意第二个参数应该是main文件的绝对路径或者相对于命令提示符位置的相对路径。
