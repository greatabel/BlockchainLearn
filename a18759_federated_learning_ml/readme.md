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



5.（可选，非必须）
启动1个命令行窗口，在terminal分别按顺序执行下面不同的命令
（头4个可以开4个窗口同时执行，也可以挨个按顺序执行，甚至可以不执行，因为我已经执行过了，缓存了中间结果）
python3 i2main.py -c  utils/conf_centralized1_1.json

python3 i2main.py -c  utils/conf_centralized1_2.json

python3 i2main.py -c  utils/conf_centralized1_3.json

python3 i2main.py -c  utils/conf_f5.json

6.
python3 i3experiment_drawing.py

