# 学习材料：

https://www.numpy.org.cn/
NumPy官方的中文文档
http://www.pypandas.cn/
pandas中文文档

# --------------------------------------------------------

# 部署流程：

ubuntu(我是在ubuntu 18.04）或者其他linux，或者osx等类unix系统
其他系统没有经过充分测试

1.
安装python3.6 以上版本

2. 
安装pip3 

3.
（可选，非必须）（创建python3虚拟目录，隔绝不同版本库之间相互影响）
https://docs.python.org/zh-cn/3/tutorial/venv.html


4.
terminal底下进入工程目录下，在requirements.txt同级目录下运行：
pip3 install --upgrade -r requirements.txt


5.
启动3个命令行窗口，在terminal分别输入3个不同的命令：

python3 i0eos_like_app_backend.py

python3 i2bounty_webend.py


6.
浏览器访问：

http://localhost:5000/home

默认账号 greatabel1@126.com ps:abel
自己也可以正常注册

--------------------------------------------------------

# 模块说明：
1. 实现一套类eos的私有链，选举过程中每个EOS代币相当于1票，我们本地机只有1台机器，可以用进程模拟
2. 实现一套悬赏平台（web-based）
3. 通过类eos的区块链api 和 web-based的 api 进行通讯
