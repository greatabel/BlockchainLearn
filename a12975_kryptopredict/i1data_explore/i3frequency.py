# coding:utf-8
# 绘制转发时间扩散、增长图
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime
import numpy as np

with open("twitter_data/elon_data.csv", "r") as f:
    # with open('twitter_data/pualg_data.csv', 'r') as f:
    rt_time = []
    for line in f:
        time = line.strip().split(",")[-1]
        time = time[1:-1]
        rt_time.append(time)
day = [(str(i)[0:10] + "-" + str(i)[11:13]) for i in rt_time]
day = [datetime.strptime(d, "%Y-%m-%d-%H") for d in day]
day_weibo = datetime.strptime("2020-12-12-16", "%Y-%m-%d-%H")  # 源微博发出时间
hours = [(i - day_weibo).total_seconds() / 3600 for i in day]
values, base = np.histogram(hours, bins=40)
cumulative = np.cumsum(values)
plt.subplot(1, 2, 1)
plt.plot(base[:-1], cumulative, c="blue")
plt.title("Cumulative Diffusion")
plt.ylabel("Number of Retweets")
plt.xlabel("Hours")
plt.subplot(1, 2, 2)
plt.plot(base[:-1], values, c="pink")
plt.title("Hourly Diffusion")
plt.xlabel("Hours")
plt.show()
