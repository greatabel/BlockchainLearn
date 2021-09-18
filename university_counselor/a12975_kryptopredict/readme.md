检测部分推荐部署ubuntu或者其他linux，或者osx等类unix系统
其他系统没有经过充分测试

###############

总体而言：
i0SGScrapy 是所有的twitter/quora下载爬虫、轮询的工程
i1data_explore 是进行网络分析和数据探索的工程
i2sentiment_analysis 主要是进行情感分析模型训练和测试的工程
docs 是文档和报告

###############

1.
安装python3.6 以上版本

1.1
在osx上安装
brew link libpng
（否则requirements.txt中的dlib安装会有问题）

在ubuntu也是提前安装dlib:
https://www.jianshu.com/p/44469d7d86b3

2. 
安装pip3 

3.
（可选，非必须）（创建python3虚拟目录，隔绝不同版本库之间相互影响）
https://docs.python.org/zh-cn/3/tutorial/venv.html


4.
terminal底下进入工程目录下，在requirements.txt同级目录下运行：
pip3 install --upgrade -r requirements.txt


5.
启动不同terminal（命令行）
cd 进入  i0SGScrapy
运行：python3 quora_main.py

cd 进入 i0SGScrapy/twitter_scrapy
运行： python3 i0my_tw_downloader.py

在命令行下，（进入虚拟环境， 如果设置过虚拟环境）
cd 进入 i2sentiment_analysis
运行：jupyter notebook i2deep-learning-for-sentiment-analysis.ipynb



6.
另外开一个命令行，进入i2sentiment_analysis/i3sentiment_predict_web
进入虚拟环境
执行：app.py

可以访问情感模型的web调用模式访问：
http://127.0.0.1:5000/home

