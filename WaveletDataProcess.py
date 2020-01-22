import pickle
import matplotlib.pyplot as plt
import pywt
import numpy as np
import math
import random
import scipy.signal
# list2=[1,2,1]
list2=[0.1,0.4,0.6,0.8,1,0.8,0.6,0.4,0.1]
#卷积先翻转2 在把2在1上平移
path='D:/工作文件2/1118/数据库/数据库.data'

# f = open(path, 'rb')
# data = pickle.load(f)
# filename=data.filenames[20]

data=[ 1*math.sin(i)+0 for i in np.linspace(0,20,1000)]
datacon=scipy.signal.convolve(data,list2)
print('data',data)
print('datacon',datacon)
plt.plot(datacon)
# data=[ math.sin(i) for i in np.linspace(0,20,1000)]
datanoise=[ i+random.uniform(-0.2,0.2) for i in datacon]
plt.plot(datanoise)
# plt.plot(data)
# plt.plot(datacon)
# plt.plot(datanoise)
# plt.show()

# data=data.filelist[filename].Pro_Data1
w = pywt.Wavelet('db8')  # 选用Daubechies8小波
# maxlev = pywt.dwt_max_level(len(data), w.dec_len)
maxlev = pywt.dwt_max_level(len(datanoise), w.dec_len)
# print("maximum level is " + str(maxlev))

# coeffs = pywt.wavedec(data, 'db8', level=maxlev)
coeffs = pywt.wavedec(datanoise, 'db8', level=maxlev)
# # plt.plot(coeffs[0])
# plt.plot(coeffs[1])
# plt.plot(coeffs[2])
# plt.plot(coeffs[3])
# plt.plot(coeffs[4])
# plt.plot(coeffs[5])
# plt.plot(coeffs[6])
# plt.show()
# print(len(coeffs))

threshold = 3
for i in range(1, len(coeffs)):
    # print(i)
    coeffs[i] = pywt.threshold(coeffs[i], threshold * max(coeffs[i]))  # 将噪声滤波

datarec = pywt.waverec(coeffs, 'db8')  # 将信号进行小波重构

print('datacon',datarec)
mintime = 0
maxtime = mintime + len(datanoise) + 1
# maxtime = mintime + len(datanoise) + 1
plt.plot(datarec)
# datarecdecon=scipy.signal.deconvolve(datarec,list2)
datarecdecon=list(scipy.signal.deconvolve(datarec,list2)[0])
datarecdecon=scipy.signal.wiener(datarec,noise=list2)
# print(datarecdecon)
# print(len(scipy.signal.deconvolve(datarec,list2)))
print('data',datarecdecon)
# plt.plot(datarecdecon)
plt.show()

