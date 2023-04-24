使用python3+pip3部署方案，步骤1～4如下：

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



5.（可选，非必须, 最好不用跑，要非常之久)
启动1个命令行窗口，在terminal分别按顺序执行下面不同的命令
（头4个可以开4个窗口同时执行，也可以挨个按顺序执行，甚至可以不执行，因为我已经执行过了，缓存了中间结果）



python3 i2main.py -c  utils/conf_cifar.json

python3 i2main.py -c  utils/conf_fashion.json

python3 i2main.py -c  utils/conf_mnist.json (mnist osx 上有些bug)