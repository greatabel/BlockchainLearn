import numpy
import matplotlib.pyplot as plt


real = [33139.4, 34504.4, 33461.4]
predict = [32758.78439417,33975.64928439, 34376.95988344]

a_array = numpy.array(real)
b_array = numpy.array(predict)
c_array =  a_array  - b_array
d = [abs(number) for number in c_array]
print('#'*20)
print('gap error with day=', d)
print('#'*20)
dataX = [1,2,3]
dataY = d
plt.plot(dataX,dataY)#plot还有很多参数，可以查API修改，如颜色，虚线等
plt.title("error with days");
plt.xlabel("x");
plt.ylabel("y");
plt.show()
