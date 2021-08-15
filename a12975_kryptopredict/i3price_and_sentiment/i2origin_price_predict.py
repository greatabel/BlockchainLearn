import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy.stats import norm
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model

import pandas


def rmse(y_test, y):
    return sp.sqrt(sp.mean((y_test - y) ** 2))


colnames = ["Date", "Close_Last", "Volume", "Open", "High", "Low"]
data = pandas.read_csv("data/i1btc_price.csv", names=colnames)

dates = data.Date.tolist()[1:]
prices = data.Close_Last.tolist()[1:]
prices = list(map(float, prices))
print(prices, "#" * 30)

x = np.arange(0, 31, 1)
# y = np.array([4.00, 6.40, 8.00, 8.80, 9.22, 9.50, 9.70, 9.86, 10.00, 10.20, 10.32, 10.42, 10.50, 10.55, 10.58, 10.60])
y = np.array(prices)

print(len(x), len(y), "@" * 10)
z1 = np.polyfit(x, y, 2)#用2次多项式拟合
p1 = np.poly1d(z1)
print('- *'*5)
print(p1) #在屏幕上打印拟合多项式
print('- *'*5)
yvals=p1(x)#也可以使用yvals=np.polyval(z1,x)
plot1=plt.plot(x, y, '*',label='original values')
plot2=plt.plot(x, yvals, 'r',label='polyfit values')

myerror = rmse(yvals, y)
print('#'*20, 'myerror=', myerror)
# myerror= 2051.201302791934
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.legend(loc=4)#指定legend的位置,读者可以自己help它的用法
plt.title('polyfitting')

# plt.show()
plt.savefig('p1origin.png')


