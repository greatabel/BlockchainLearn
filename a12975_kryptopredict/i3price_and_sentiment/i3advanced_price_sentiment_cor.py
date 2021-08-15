import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy.stats import norm
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model

import pandas
import math
import time
import datetime
import pickle

def sentiment_improve(base, vote):
    M = math.e*base*100
    upper = 50
    down = 30
    a = M + math.log(math.e **vote)
    b = M + math.log(math.e ** 1)

    r = a / b
    print('sentiment_improve a,b=',a, b, 'result=', r)
    return r
    # n = math.log(r)
    # print('n=', n)

# sentiment_improve()
# time.sleep(100)


colnames = ["Date", "Close_Last", "Volume", "Open", "High", "Low"]
data = pandas.read_csv("data/i1btc_price.csv", names=colnames)

dates = data.Date.tolist()[1:]
mydates = []
# print('dates=', dates)
for d in dates:
    fd = datetime.datetime.strptime(d, '%m/%d/%Y').strftime( '%Y-%m-%d')
    mydates.append(fd)
print(len(mydates),'mydates=', mydates)
prices = data.Close_Last.tolist()[1:]
prices = list(map(float, prices))





hot_dict = {}
sentiment_dict = {}
hots = []
sentiments = []
with open("hot.pickle", "rb") as handle:
    hot_dict = pickle.load(handle)



with open("sentiment_dict.pickle", "rb") as handle:
    sentiment_dict = pickle.load(handle)

for key, value in hot_dict.items():
    # print(key, '#',value)
    if key in mydates:
        print('choose:', key, '#',value)
        hots.append(value)

print('\n'*5)
for key, value in sentiment_dict.items():
    if key in mydates:
        print('choose:', key, '#',value)
        sentiments.append(value)

print(hots, '$'*20, sentiments)
print('len(hots)=', len(hots))


newprcies = []
for i in range(0, len(hots)):
    print(i)
    r = sentiment_improve(hots[i], sentiments[i])
    p = prices[i]* r
    newprcies.append(p)

print('price ', '->'*10)
print(prices, "#" * 30)
print(newprcies, '@'*20)
# time.sleep(100)

x = np.arange(0, 31, 1)
print(x)

# y = np.array([4.00, 6.40, 8.00, 8.80, 9.22, 9.50, 9.70, 9.86, 10.00, 10.20, 10.32, 10.42, 10.50, 10.55, 10.58, 10.60])
y = np.array(newprcies)

print(len(x), len(y), "@" * 10)

# z1 = np.polyfit(x, y, 3)#用3次多项式拟合
# p1 = np.poly1d(z1)
# print('- *'*5)
# print(p1) #在屏幕上打印拟合多项式
# print('- *'*5)
# yvals=p1(x)#也可以使用yvals=np.polyval(z1,x)
# plot1=plt.plot(x, y, '*',label='original values')
# plot2=plt.plot(x, yvals, 'r',label='polyfit values')
# plt.xlabel('x axis')
# plt.ylabel('y axis')
# plt.legend(loc=4)#指定legend的位置,读者可以自己help它的用法
# plt.title('polyfitting')
# plt.show()
# # plt.savefig('p1.png')


# ''''' 数据生成 '''
# x = np.arange(0, 1, 0.002)
# y = norm.rvs(0, size=500, scale=0.1)
# y = y + x**2

"""'' 均方误差根 """


def rmse(y_test, y):
    return sp.sqrt(sp.mean((y_test - y) ** 2))


"""'' 与均值相比的优秀程度，介于[0~1]。0表示不如均值。1表示完美预测.这个版本的实现是参考scikit-learn官网文档  """


def R2(y_test, y_true):
    return 1 - ((y_test - y_true) ** 2).sum() / ((y_true - y_true.mean()) ** 2).sum()


def R22(y_test, y_true):
    y_mean = np.array(y_true)
    y_mean[:] = y_mean.mean()
    return 1 - rmse(y_test, y_true) / rmse(y_mean, y_true)


plt.scatter(x, y, s=5)
degree = [1, 2, 3, 100]
y_test = []
y_test = np.array(y_test)


for d in degree:
    clf = Pipeline(
        [
            ("poly", PolynomialFeatures(degree=d)),
            ("linear", LinearRegression(fit_intercept=False)),
        ]
    )
    clf.fit(x[:, np.newaxis], y)
    y_test = clf.predict(x[:, np.newaxis])
    print(" start ->" * 10, d)
    print("coef=> ",clf.named_steps["linear"].coef_)
    print(" end ->" * 10, d)
    print(
        "###rmse=%.2f, R2=%.2f, R22=%.2f, clf.score=%.2f"
        % (
            rmse(y_test, y),
            R2(y_test, y),
            R22(y_test, y),
            clf.score(x[:, np.newaxis], y),
        )
    )

    plt.plot(x, y_test, linewidth=2)
'''
rmse=2307.11, R2=0.76, R22=0.51, clf.score=0.76
rmse=2051.20, R2=0.81, R22=0.56, clf.score=0.81
rmse=1787.04, R2=0.86, R22=0.62, clf.score=0.86
rmse=34886.10, R2=-54.17, R22=-6.43, clf.score=-54.17





'''
plt.grid()
plt.legend(["1", "2", "3", "100"], loc="upper left")
plt.show()
#plt.savefig('i2.png')