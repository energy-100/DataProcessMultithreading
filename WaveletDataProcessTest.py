import pickle
import matplotlib.pyplot as plt
import pywt
import numpy as np
import math
import random
import scipy.signal
from scipy.fftpack import fft,ifft
import numpy.fft as nf
import scipy.io.wavfile as wf
# list2=[1,2,1]
# datarow = open("D:/工作文件2/反卷积数据/校准文档.txt")  # 读取的整个原始文件数据
datarow = open("D:/工作文件2/反卷积数据/校准文档3.txt")  # 读取的整个原始文件数据
# datarow = open("D:/工作文件2/反卷积数据/校准文档4.txt")  # 读取的整个原始文件数据
datarowlines = datarow.readlines()  # 读取的整个原始文件的数据，按行分割
listx=[]
listy=[]
for line in datarowlines:
    linenew = line.strip().split()
    listx.append(int(linenew[0]))
    listy.append(int(linenew[1]))
# listy.append(0)
# listy.append(0)
# listy.append(0)
# listy.append(0)
# listy.append(0)
# listy.append(0)
# listy.append(0)
# listy.append(0)
# listy.append(0)
# listy.append(0)
# listy.append(0)
# listy.append(0)
# listy.append(0)
# listy.append(0)
# list2=[0.1,0.2,0.3,0.4,0.4,0.3,0.2,0.1]
# listy=[1,1,1,1,1,1,1,5,1,1,1,1,1,1]
# listy=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,20,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,]
list2=[0.2,0.4,0.2]
listy=scipy.signal.convolve(listy,list2)
# list2=[0.05,0.05,0.4,0.4,0.05,0.05]
# list2=[0.25,0.5,0.25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# list2=[0.05,0.05,0.4,0.4,0.05,0.05,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
list22=[0.05,0.05,0.4,0.4,0.05,0.05]
# #卷积先翻转2 在把2在1上平移
# path='D:/工作文件2/1118/数据库/数据库.data'
#
# # f = open(path, 'rb')
# # data = pickle.load(f)
# # filename=data.filenames[20]
#
# data=[ 1*math.sin(i)+0 for i in np.linspace(0,20,1000)]
# datacon=scipy.signal.convolve(data,list2)
# print('data',data)
# print('datacon',datacon)
# plt.plot(datacon)
# # data=[ math.sin(i) for i in np.linspace(0,20,1000)]
# datanoise=[ i+random.uniform(-0.2,0.2) for i in datacon]
# plt.plot(datanoise)
# # plt.plot(data)
# # plt.plot(datacon)
# # plt.plot(datanoise)
# # plt.show()
#
# # data=data.filelist[filename].Pro_Data1
# w = pywt.Wavelet('db8')  # 选用Daubechies8小波
# # maxlev = pywt.dwt_max_level(len(data), w.dec_len)
# maxlev = pywt.dwt_max_level(len(listy), w.dec_len)
# # print("maximum level is " + str(maxlev))
#
# # coeffs = pywt.wavedec(data, 'db8', level=maxlev)
# coeffs = pywt.wavedec(listy, 'db8', level=maxlev)
# # # plt.plot(coeffs[0])
# # plt.plot(coeffs[1])
# # plt.plot(coeffs[2])
# # plt.plot(coeffs[3])
# # plt.plot(coeffs[4])
# # plt.plot(coeffs[5])
# # plt.plot(coeffs[6])
# # plt.show()
# # print(len(coeffs))
#
# threshold = 2
# for i in range(1, len(coeffs)):
#     # print(i)
#     coeffs[i] = pywt.threshold(coeffs[i], threshold * max(coeffs[i]))  # 将噪声滤波
#
# datarec = pywt.waverec(coeffs, 'db8')  # 将信号进行小波重构
#
# print('datacon',datarec)
# mintime = 0
# maxtime = mintime + len(datanoise) + 1
# # maxtime = mintime + len(datanoise) + 1
# plt.plot(datarec)
# # datarecdecon=scipy.signal.deconvolve(datarec,list2)
#
#
# plt.show()


# 傅里叶变换
listyfft = fft(listy,len(listy)+len(list2)-1)  # 快速傅里叶变换
listyfftreal = list(listyfft.real)  # 获取实数部分
listyfftimag = list(listyfft.imag)  # 获取虚数部分

list2fft = fft(list2,len(listy)+len(list2)-1)  # 快速傅里叶变换
list2fftreal = list(list2fft.real)  # 获取实数部分
list2fftimag = list(list2fft.imag)  # 获取虚数部分

# for i in range(len(list2)-1):
#     listyfftreal.append(0)
#
#
# for i in range(len(listy)-1):
#     list2fftreal.append(0)

# finalllisty=listyfft./list2fft
finalllisty=[]
# print(listyfftreal)
# print(list2fftreal)
for i in range(len(list2fft)):
    finalllisty.append(listyfft[i]/list2fft[i])

ifft = np.fft.ifft(finalllisty)
plt.plot(ifft.real)
plt.plot(listy)
# plt.plot(np.real(ifft))
# yf = abs(fft(y))  # 取绝对值
# yf1 = abs(fft(y)) / len(x)  # 归一化处理
# yf2 = yf1[range(int(len(x) / 2))]  # 由于对称性，只取一半区间
#
# xf = np.arange(len(y))  # 频率
# xf1 = xf
# xf2 = xf[range(int(len(x) / 2))]  # 取一半区间


# cov=scipy.signal.convolve(listy,list2)
# datarecdecon=list(scipy.signal.deconvolve(listy,list2)[0])
# datarecdecon=list(scipy.signal.deconvolve(listy[0:10],list2)[0])
# datarecdecon=list(scipy.signal.deconvolve(cov,list22)[0])
# datarecdecon=list(scipy.signal.deconvolve(datarec,list2)[0])
# datarecdeconerror=list(scipy.signal.deconvolve(datarec,list2)[1])
# datarecdecon=[datarecdecon[i]-datarecdeconerror[i] for i in range(len(datarecdecon))]
# datarecdecon=scipy.signal.wiener(datarec,noise=list2)
# print(datarecdecon)
# print(len(scipy.signal.deconvolve(datarec,list2)))
# print('data',datarecdecon)
# print('y',listy)
# print('datarecdecon',datarecdecon)
# plt.plot(datarecdecon)
# plt.plot(listy)
# plt.plot(listy[0:10])
# plt.plot(datarecdecon)

# plt.plot(datarecdecon)
# plt.plot(datarecdecon[0:30])
plt.show()

