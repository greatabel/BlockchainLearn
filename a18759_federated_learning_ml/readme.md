# 学习材料：

https://pytorch123.com/
PyTorch官方教程

--------------------------------------------------------

# 部署流程：

ubuntu(我是在ubuntu 18.04/ 笔记本用osx上部署）或者其他linux，或者osx等类unix系统
其他系统没有经过充分测试

方案1:如果使用anaconda方案，可以跳过步骤1～4，直接：
安装[Python](https://www.anaconda.com/products/individual)、
[Pytorch](https://pytorch.org/get-started/locally/)环境


方案2:使用python3+pip3部署方案，步骤1～4如下：

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

