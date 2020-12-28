import os
from scipy.optimize import curve_fit
import numpy as np
filenames=[]

import matplotlib.pyplot as plt
import matplotlib; matplotlib.use('TkAgg')

class fun():
    def __init__(self,TimeSpan):
        self.TimeSpan=TimeSpan

    # 双曲积分
    def fun3(self):
        TimeSpan=self.TimeSpan
        def funt(x, s1, s2, s3, s4):
            temp1spot = (1 / (1 + np.asarray(x) / s2)) ** (s3 - 1)
            temp2spot = (1 / (1 + (np.asarray(x) + TimeSpan) / s2)) ** (s3 - 1)
            yfitspot = s1 * s2 * (1 / (s3 - 1)) * (temp1spot - temp2spot) + s4 * TimeSpan
            return yfitspot
        return funt

    # 指数积分
    def fun4(self,x, s1, s2, s3):
        temp1spot = np.exp(-np.asarray(x) / s2)
        temp2spot = np.exp(-(np.asarray(x) + self.TimeSpan) / s2)
        yfitspot = s1 * s2 * (temp1spot - temp2spot) + s3 * self.TimeSpan
        return yfitspot



def getIndexes(y_predict, y_data):
    y_predict = np.array(y_predict)
    y_data = np.array(y_data)
    n = y_data.size
    # SSE为和方差
    SSE = ((y_data - y_predict) ** 2).sum()
    # MSE为均方差
    MSE = SSE / n
    # RMSE为均方根,越接近0，拟合效果越好
    RMSE = np.sqrt(MSE)

    # 求R方，0<=R<=1，越靠近1,拟合效果越好
    u = y_data.mean()
    SST = ((y_data - u) ** 2).sum()
    SSR = SST - SSE
    R_square = SSR / SST
    return [R_square, SSE, MSE, RMSE]

def plot(filepath):  # 存入数据
    datarow = open(filepath)  # 读取的整个原始文件数据
    datarowlines = datarow.readlines()  # 读取的整个原始文件的数据，按行分割
    datapar = []  # 真正的每行数据数组
    for line in datarowlines:
        linenew = line.strip()
        if (linenew != ""):
            datapar.append(linenew)
    # # print(datapar)
    # # self.ACQ_Time=re.search("(\d{4}-\d{1,2}-\d{1,2}\s*\d{1,2}:\d{1,2}:\d{1,2}:\s*\d{1,3})",datapar[1])
    # temptime = re.search("\d{4}-\s*\d{1,2}-\s*\d{1,2}\s*\d{1,2}:\s*\d{1,2}:\s*\d{1,2}.\s*\d{1,3}\s*.",
    #                      datapar[1]).group(0)
    # # print(temptime)
    # # strtemp=temptime[5].split('.')
    # # temptime[5]=strtemp[0]
    # # temptime.append(strtemp[1])
    # timelist = re.split('[- :.]\s*', temptime)
    # # print(timelist)
    #
    # timestr = timelist[0] + "-" + timelist[1] + "-" + timelist[2] + "  " + timelist[3] + ":" + timelist[
    #     4] + ":" + timelist[5] + "." + timelist[6]
    # data.ACQ_Time = datetime.strptime(timestr, '%Y-%m-%d  %H:%M:%S.%f')
    # data.Project = datapar[2].strip(datapar[2].split(": ")[0]).strip(": ")
    # data.Name = datapar[3].strip(datapar[3].split(": ")[0]).strip(": ")
    # data.part = datapar[4].strip(datapar[4].split(": ")[0]).strip(": ")
    # data.Operator = datapar[5].strip(datapar[5].split(": ")[0]).strip(": ")
    # data.Desc = datapar[6].strip(datapar[6].split(": ")[0]).strip(": ")
    # data.Excited_Peroid = int(datapar[9].strip(datapar[9].split(": ")[0]).strip(": "))
    # data.Excited_Time = int(datapar[10].strip(datapar[10].split(": ")[0]).strip(": "))
    # data.Acq_Delay_Time = int(datapar[11].strip(datapar[11].split(": ")[0]).strip(": "))
    Gate_Time = int(datapar[12].strip(datapar[12].split(": ")[0]).strip(": "))
    Count_Num_per_gate = int(datapar[13].strip(datapar[13].split(": ")[0]).strip(": "))
    Repeat_Times = int(datapar[14].strip(datapar[14].split(": ")[0]).strip(": "))
    Acq_Gate_Times = int(datapar[15].strip(datapar[15].split(": ")[0]).strip(": "))
    Interval_per_Gate = int(datapar[16].strip(datapar[16].split(": ")[0]).strip(": "))
    datanum = int(Repeat_Times * Count_Num_per_gate)
    Pro_Data1 = np.zeros(Acq_Gate_Times * Count_Num_per_gate).tolist()
    Raw_Data1 = []
    if (datapar[17].strip(datapar[17].split(":")[0]).strip(":") == ""):
        Channel_Number = "1"
        for i in range(18, 18 + datanum * Acq_Gate_Times):
            Raw_Data1.append(int(datapar[i]))
        # if (data.Channel_Number == 2):
        #     for i in range(18 + datanum + 1,
        #                    18 + datanum * data.Acq_Gate_Times + 1 + datanum * data.Acq_Gate_Times):
        #         data.Raw_Data2.append(int(datapar[i]))
    else:
        Channel_Number = int(datapar[17].strip(datapar[17].split(": ")[0]).strip(": "))
        for i in range(19, 19 + datanum * Acq_Gate_Times):
            Raw_Data1.append(int(datapar[i]))

    dScale = Count_Num_per_gate * 1000 / (Gate_Time * Repeat_Times)
    for i in range(int(Acq_Gate_Times)):
        for j in range(int(Count_Num_per_gate)):
            ncps = 0
            ncpslist = []
            for k in range(int(Repeat_Times)):
                ncps += Raw_Data1[k * Count_Num_per_gate + j + i * datanum]
                ncpslist.append(Raw_Data1[k * Count_Num_per_gate + j + i * datanum])
            # Pro_mal1.append(ncpslist)
            Pro_Data1[j * Acq_Gate_Times + i] = ncps * dScale
    # data.Interval=float((data.Gate_Time)/len(data.Pro_Data1))*data.Count_Num_per_gate*0.001
    Interval = float(Gate_Time / Count_Num_per_gate)

    Pro_Data1_X=[]
    for i in range(int(Count_Num_per_gate)):
        for j in range(int(Acq_Gate_Times)):
            Pro_Data1_X.append(float(i * Interval + j * Interval_per_Gate * 0.001))
    funtemp=fun(Gate_Time)
    Max = np.max(Pro_Data1)
    Min = np.min(Pro_Data1)
    print("最值：",Max,Min)
    Pro_Data1MulitInteral=[x*Interval for x in Pro_Data1]
    Max = np.max(Pro_Data1)
    Min = np.min(Pro_Data1)

    xfit = np.linspace(Pro_Data1_X[0], Pro_Data1_X[-1], 1000).tolist()
    print(Gate_Time)
    def fun3(x, s1, s2, s3, s4):
        temp1spot = (1 / (1 + np.asarray(x) / s2)) ** (s3 - 1)
        temp2spot = (1 / (1 + (np.asarray(x) + Interval) / s2)) ** (s3 - 1)
        yfitspot = s1 * s2 * (1 / (s3 - 1)) * (temp1spot - temp2spot) + s4 * Interval
        return yfitspot

    def fun1(x, s1, s2, s3, s4):
        return s1 * ((1 + (x / s2)) ** (-s3)) + s4


    popt, pcov = curve_fit(fun3, Pro_Data1_X, Pro_Data1MulitInteral, maxfev=50000000, bounds=([0.1 * Min, 0.1, 0.1, 0.1],[10*Max, 1000, 1000, 1000]))
    yfit = fun1(xfit, popt[0], popt[1], popt[2], popt[3])
    ytempfit = fun1(Pro_Data1_X, popt[0], popt[1], popt[2], popt[3])
    R2 = getIndexes(ytempfit, Pro_Data1)
    print(R2)
    print(popt)
    print()
    plt.scatter(Pro_Data1_X,Pro_Data1,s=3,c="red")
    plt.plot(xfit,yfit)
    plt.xlabel('input number')
    plt.ylabel('ouput number')
    plt.title('测试某些函数')
    plt.legend()
    plt.show()
    plt.show()

plot("D:/工作文件2/QCC2019 422 95229-手指发光-D.txt")