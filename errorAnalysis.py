import os
import re
import numpy as np
import xlrd
import xlwt
import xlsxwriter
from scipy.optimize import curve_fit
from datetime import datetime
from xlutils.copy import copy
import matplotlib.pyplot as plt
from scipy.stats import t
import matplotlib; matplotlib.use('TkAgg')
from sympy import symbols, diff
import sympy
from scipy import integrate
TimeSpan=0
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

def fun1(x, s1, s2, s3, s4):
    # return s1 * ((1 + (x / s2)) ** (-s3)) + s4
    return s1 * ((1 + (x / s2)) ** (-s3)) + s4

def fun2(x, s1, s2, s3):
    return s1 * (np.exp(-(x / s2))) + s3

def fun3(x, s1, s2, s3, s4,interval):
    print("TimeSpan:", TimeSpan)
    temp1spot = (1 / (1 + np.asarray(x) / s2)) ** (s3 - 1)
    temp2spot = (1 / (1 + (np.asarray(x) + TimeSpan) / s2)) ** (s3 - 1)
    yfitspot = s1 * s2 * (1 / (s3 - 1)) * (temp1spot - temp2spot) + s4 * TimeSpan
    return yfitspot



def main(fun:list,filepath:str):

    datarow = open(filepath)  # 读取的整个原始文件数据
    # datarowlines = datarow.readlines()  # 读取的整个原始文件的数据，按行分割
    # data = []  # 真正的每行数据数组
    # datax=[]
    # for line in datarowlines:
    #     linenew = line.strip().split("\t")
    #     # print(linenew)
    #     if (linenew != ""):
    #         data.append(int(linenew[1]))
    #         datax.append(float(linenew[0]))

    datarowlines = datarow.readlines()  # 读取的整个原始文件的数据，按行分割
    datapar = []  # 真正的每行数据数组
    for line in datarowlines:
        linenew = line.strip()
        if (linenew != ""):
            datapar.append(linenew)
    Raw_Data1=[]
    Pro_Data1_X=[]
    Pro_mal1=[]
    Excited_Peroid = int(datapar[9].strip(datapar[9].split(": ")[0]).strip(": "))
    Excited_Time = int(datapar[10].strip(datapar[10].split(": ")[0]).strip(": "))
    Acq_Delay_Time = int(datapar[11].strip(datapar[11].split(": ")[0]).strip(": "))
    Gate_Time = int(datapar[12].strip(datapar[12].split(": ")[0]).strip(": "))
    Count_Num_per_gate = int(datapar[13].strip(datapar[13].split(": ")[0]).strip(": "))
    Repeat_Times = int(datapar[14].strip(datapar[14].split(": ")[0]).strip(": "))
    Acq_Gate_Times = int(datapar[15].strip(datapar[15].split(": ")[0]).strip(": "))
    Interval_per_Gate = int(datapar[16].strip(datapar[16].split(": ")[0]).strip(": "))
    datanum = int(Repeat_Times * Count_Num_per_gate)
    Pro_Data1 = np.zeros(Acq_Gate_Times * Count_Num_per_gate).tolist()
    if (datapar[17].strip(datapar[17].split(":")[0]).strip(":") == ""):
        # print("进入")
        Channel_Number = "1"
        for i in range(18, 18 + datanum * Acq_Gate_Times):
            Raw_Data1.append(int(datapar[i]))
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
            Pro_mal1.append(ncpslist)
            Pro_Data1[j * Acq_Gate_Times + i] = ncps * dScale
    Interval = float(Gate_Time / Count_Num_per_gate)

    for i in range(int(Count_Num_per_gate)):
        for j in range(int(Acq_Gate_Times)):
            Pro_Data1_X.append(float(i * Interval + j * Interval_per_Gate * 0.001))
    TimeSpan=Gate_Time
    datax =  Pro_Data1_X
    data = Pro_Data1
    datamax=max(data)
    if 1 in fun:
        # sigmay=data
        # sigmay=[1 for i in range(data)]
        # popt, pcov = curve_fit(fun1, datax, data, maxfev=500000000,sigma=sigmay,absolute_sigma=True, bounds=([0.5* datamax, 0.1, 0.1, 0.1,], [1.5 * datamax, 1000, 10000, 10000]))
        popt, pcov = curve_fit(fun1, datax, data, maxfev=500000000, bounds=([0.5* datamax, 0.1, 0.1, 0.1,], [1.5 * datamax, 1000, 10000, 10000]))
        xfit1 = np.linspace(datax[0],datax[-1],1000)
        yfit1 = fun1(xfit1, popt[0], popt[1], popt[2], popt[3])
        ytempfit1 = fun1(datax, popt[0], popt[1], popt[2], popt[3])
        R21 = getIndexes(ytempfit1, data)
        s1,s2,s3,s4,x = symbols('s1 s2 s3 s4 x', real=True)
        f1 = s1 * ((1 + (x / s2)) ** (-s3)) + s4
        paradata,ailist,bilist,cilist,dilist,Nilist=[],[],[],[],[],[]
        for i in range(len(data)):
            ailist.append(diff(f1, s1).subs({s1:popt[0],s2:popt[1],s3:popt[2],s4:popt[3],x:datax[i]}))
            bilist.append(diff(f1, s2).subs({s1:popt[0],s2:popt[1],s3:popt[2],s4:popt[3],x:datax[i]}))
            cilist.append(diff(f1, s3).subs({s1:popt[0],s2:popt[1],s3:popt[2],s4:popt[3],x:datax[i]}))
            dilist.append(diff(f1, s4).subs({s1:popt[0],s2:popt[1],s3:popt[2],s4:popt[3],x:datax[i]}))
            Nilist.append(fun1(datax[i],popt[0],popt[1],popt[2],popt[3])-data[i])
        paradata.append(ailist)
        paradata.append(bilist)
        paradata.append(cilist)
        paradata.append(dilist)

        m = np.zeros(shape=(len(popt), len(popt)))
        v = np.zeros(shape=(len(popt)))
        for i in range(len(popt)):
            for j in range(len(popt)):
                for k in range(len(data)):
                    m[i,j] += paradata[i][k]*paradata[j][k]

        for i in range(len(popt)):
            for k in range(len(data)):
                v[i] -= Nilist[k]* paradata[i][k]

        m2=np.linalg.inv(m)
        res=np.zeros(len(popt))
        for i in range(len(popt)):
            for j in range(len(popt)):
                res[i]+=m2[i,j]**2*v[j]**2

        # m2=np.linalg.inv(m)
        # res=np.zeros(len(popt))
        # cres=np.zeros(shape=(len(popt),len(data)))
        #


        # for i in range(len(popt)):
        #     for k in range(len(data)):
        #         for j in range(len(popt)):
        #             cres[i,k] += m2[i,j] *paradata[j][k]
        #         res[i] += (cres[i,k]**2)*(Nilist[k]**2)

        # error=np.linalg.solve(m, v)
        pcovdiag=np.sqrt(np.diag(pcov))
        print(pcovdiag)
        print("双曲线 优度："+str(R21[0]))
        for i in range(len(popt)):
            # print(popt[i],error[i],pcov[i])
            # print(str(popt[i])+"±"+str(np.sqrt(res[i]))+"\t±"+str(pcovdiag[i])+" "+str(popt[i]-np.sqrt(res[i]))+"\t"+str(popt[i]+np.sqrt(res[i])))
            # print(str(popt[i])+"±"+str(np.sqrt(res[i]))+"\t±"+str(pcovdiag[i])+"\t"+str(popt[i]-np.sqrt(res[i]))+"\t"+str(popt[i]+np.sqrt(res[i])))
            print(str(popt[i])+"±"+str(np.sqrt(res[i]))+"\t±"+str(popt[i]-np.sqrt(res[i]))+"\t"+str(popt[i]+np.sqrt(res[i])))

        # print(np.sqrt(res[0])/3290)
        # print(np.sqrt(res[1])/5.575)
        # print(np.sqrt(res[2])/1.81)
        # print(np.sqrt(res[3])/1841)
    if 2 in fun:
        # sigmay=data
        sigmay2=[]
        sigmay3=[]
        # for i in range(len(data)):
        #     if (i<10):
        #         sigmay3.append(1)
        #     else:
        #         sigmay3.append(10000000)



        for i in range(len(data)):
            # sigmay3.append(1)
            # sigmay2.append(1/data[i])
            # sigmay3.append(data[i])
            sigmay3.append(np.sqrt(data[i]))
            # sigmay2.append(1)
            sigmay2.append(1/data[i])

        # popt, pcov = curve_fit(fun2, datax, data, maxfev=500000000,
        #                        bounds=([0.5 * datamax, 0.1, 0.1, ], [1.5 * datamax, 1000, 10000]))

        popt, pcov = curve_fit(fun2, datax, data, maxfev=500000000,sigma=sigmay3, absolute_sigma=True,
                               bounds=([0.5 * datamax, 0.1, 0.1, ], [1.5 * datamax, 1000, 10000]))

        # popt, pcov = curve_fit(fun2, datax, data, maxfev=500000000,sigma=sigmay3, absolute_sigma=True,
        #                        bounds=([0.5 * datamax, 0.1, 0.1, ], [1.5 * datamax, 1000, 10000]))

        xfit2 = np.linspace(datax[0],datax[-1],1000)
        yfit2 = fun2(xfit2, popt[0], popt[1], popt[2])




        ytempfit2 = fun2(datax, popt[0], popt[1], popt[2])
        R2 = getIndexes(ytempfit2, data)
        s1, s2, s3, x = symbols('s1 s2 s3 x', real=True)
        f1 = s1 * (sympy.exp(-(x / s2))) + s3
        paradata, ailist, bilist, cilist, Nilist = [], [], [], [], []
        for i in range(len(data)):
            ailist.append(diff(f1, s1).subs({s1: popt[0], s2: popt[1], s3: popt[2], x: datax[i]}))
            bilist.append(diff(f1, s2).subs({s1: popt[0], s2: popt[1], s3: popt[2], x: datax[i]}))
            cilist.append(diff(f1, s3).subs({s1: popt[0], s2: popt[1], s3: popt[2], x: datax[i]}))
            Nilist.append((fun2(datax[i], popt[0], popt[1], popt[2]) - data[i])**2*sigmay2[i])
        paradata.append(ailist)
        paradata.append(bilist)
        paradata.append(cilist)

        m = np.zeros(shape=(3, 3))
        v = np.zeros(shape=(3))
        for i in range(3):
            for j in range(3):
                for k in range(len(data)):
                    m[i, j] += paradata[i][k] * paradata[j][k]*sigmay2[k]

        for i in range(3):
            for k in range(len(data)):
                v[i] = v[i] - Nilist[k] * paradata[i][k]*sigmay2[k]

        m2=np.linalg.inv(m)

        sse = 0
        for tmp in Nilist:
            sse +=tmp
        sse1=sse
        sse=sse/(len(data)-len(popt))


        sse2=0
        for i in range(len(datax)):
            sse2+=(fun2(datax[i], 56420, 4.598, 1992)-data[i])**2*sigmay2[i]
            # sse2+=(fun2(datax[i], 57920, 4.175, 2943)-data[i])**2

        sse22=sse2/(len(data)-len(popt))

        alpha = (1 - 0.95) / 2
        tinv = -t.ppf(alpha, len(data) - len(popt))

        a1=popt[0]-np.sqrt(sse*m2[0,0])*tinv
        b1=popt[1]-np.sqrt(sse*m2[1,1])*tinv
        c1=popt[2]-np.sqrt(sse*m2[2,2])*tinv

        a2=popt[0]+np.sqrt(sse*m2[0,0])*tinv
        b2=popt[1]+np.sqrt(sse*m2[1,1])*tinv
        c2=popt[2]+np.sqrt(sse*m2[2,2])*tinv



        res=np.zeros(len(popt))
        cres=np.zeros(shape=(len(popt),len(data)))

        # for i in range(len(popt)):
        #     for k in range(len(data)):
        #         for j in range(len(popt)):
        #             cres[i,k] += m2[i,j] *paradata[j][k]
        #         res[i] += (cres[i,k]**2)





        # for i in range(len(popt)):
        #     for k in range(len(data)):
        #         for j in range(len(popt)):
        #             cres[i,k] += m2[i,j] *paradata[j][k]
        #         # res[i] += (cres[i,k]**2)*(data[k])
        #         res[i] += (cres[i,k])*(sse/(len(data)-len(popt)))
        #         # res[i] += (cres[i,k])*(Nilist[k])

        for i in range(len(popt)):
            for k in range(len(popt)):
                # res[i] += (cres[i,k]**2)*(data[k])
                res[i] += (m2[i,k])*(sse/(len(data)-len(popt)))

        # for i in range(len(popt)):
        #     for j in range(len(popt)):
        #         res[i]+=m2[i,j]**2*v[j]**2



        # #matlab移植
        # tempparadata = np.array(paradata[0:len(popt)]).T
        # _,R = np.linalg.qr(tempparadata,mode ='reduced')
        # rinv=np.linalg.lstsq(R,np.identity(len(popt)))[0]
        # rinv=rinv**2
        # v=rinv.sum(axis=1)*sse/(len(data)-len(popt))
        # alpha = (1 - 0.95) / 2
        # tinv=-t.ppf(alpha, len(data)-len(popt))
        # db = tinv * np.sqrt(v.T)
        # print(db)



        print("指数 优度："+str(R21[0]))
        for i in range(len(popt)):
            # print(popt[i],error[i],pcov[i])
            # print(str(popt[i])+"±"+str(np.sqrt(res[i]))+"\t±"+str(pcovdiag[i])+" "+str(popt[i]-np.sqrt(res[i]))+"\t"+str(popt[i]+np.sqrt(res[i])))
            print(str(popt[i]))
            # print(str(popt[i])+"±"+str(np.sqrt(res[i]))+"\t±"+str(pcovdiag[i])+"\t"+str(popt[i]-np.sqrt(res[i]))+"\t"+str(popt[i]+np.sqrt(res[i])))
            # print(str(popt[i])+"±"+str(np.sqrt(abs(res[i]))*1.9847)+"\t±"+str(popt[i]-np.sqrt(abs(res[i]))*1.9847)+"\t"+str(popt[i]+np.sqrt(abs(res[i]))*1.9847))
            # print(str(popt[i])+"±"+str(db[i])+"\t±"+str(popt[i]-db[i])+"\t"+str(popt[i]+db[i]))


        #
        # # error = np.linalg.solve(m, v)
        # # pcovdiag = np.sqrt(np.diag(pcov))
        # # print(pcovdiag)
        # print("指数"+str(R2[0]))
        # for i in range(len(popt)):
        #     # print(popt[i],error[i],pcov[i])
        #     print(str(popt[i]) + "±" + str(error[i]))
        #     # print(str(popt[i]) + "±(" + str(error[i]) + ")   (" + str(pcovdiag[i]) + ")")



        # plt.scatter(x,datapar)
        plt.plot(xfit2,yfit2)
        # plt.plot(xfit2,yfit2)
        plt.plot(datax,data)
        print(data[-1])
        plt.show()
    if 3 in fun:
        # sigmay=data
        sigmay2=[]
        sigmay3=[]
        # for i in range(len(data)):
        #     if (i<10):
        #         sigmay3.append(1)
        #     else:
        #         sigmay3.append(10000000)



        for i in range(len(data)):
            sigmay3.append(1)
            # sigmay2.append(1/data[i])
            # sigmay3.append(data[i])
            # sigmay3.append(np.sqrt(data[i]))
            sigmay2.append(1)
            # sigmay2.append(1/data[i])

        # popt, pcov = curve_fit(fun2, datax, data, maxfev=500000000,
        #                        bounds=([0.5 * datamax, 0.1, 0.1, ], [1.5 * datamax, 1000, 10000]))

        popt, pcov = curve_fit(fun3, datax, data, maxfev=500000000,sigma=sigmay3, absolute_sigma=True,
                               bounds=([0.5 * datamax, 0.1, 0.1, ], [1.5 * datamax, 1000, 10000]))

        # popt, pcov = curve_fit(fun2, datax, data, maxfev=500000000,sigma=sigmay3, absolute_sigma=True,
        #                        bounds=([0.5 * datamax, 0.1, 0.1, ], [1.5 * datamax, 1000, 10000]))

        xfit2 = np.linspace(datax[0],datax[-1],1000)
        yfit2 = fun2(xfit2, popt[0], popt[1], popt[2])




        # ytempfit2 = fun2(datax, popt[0], popt[1], popt[2])
        # R2 = getIndexes(ytempfit2, data)
        # s1, s2, s3, x = symbols('s1 s2 s3 x', real=True)
        # f1 = s1 * (sympy.exp(-(x / s2))) + s3
        # paradata, ailist, bilist, cilist, Nilist = [], [], [], [], []
        # for i in range(len(data)):
        #     ailist.append(diff(f1, s1).subs({s1: popt[0], s2: popt[1], s3: popt[2], x: datax[i]}))
        #     bilist.append(diff(f1, s2).subs({s1: popt[0], s2: popt[1], s3: popt[2], x: datax[i]}))
        #     cilist.append(diff(f1, s3).subs({s1: popt[0], s2: popt[1], s3: popt[2], x: datax[i]}))
        #     Nilist.append((fun2(datax[i], popt[0], popt[1], popt[2]) - data[i])**2*sigmay2[i])
        # paradata.append(ailist)
        # paradata.append(bilist)
        # paradata.append(cilist)
        #
        # m = np.zeros(shape=(3, 3))
        # v = np.zeros(shape=(3))
        # for i in range(3):
        #     for j in range(3):
        #         for k in range(len(data)):
        #             m[i, j] += paradata[i][k] * paradata[j][k]*sigmay2[k]
        #
        # for i in range(3):
        #     for k in range(len(data)):
        #         v[i] = v[i] - Nilist[k] * paradata[i][k]*sigmay2[k]
        #
        # m2=np.linalg.inv(m)
        #
        # sse = 0
        # for tmp in Nilist:
        #     sse +=tmp
        # sse1=sse
        # sse=sse/(len(data)-len(popt))
        #
        #
        # sse2=0
        # for i in range(len(datax)):
        #     sse2+=(fun2(datax[i], 56420, 4.598, 1992)-data[i])**2*sigmay2[i]
        #     # sse2+=(fun2(datax[i], 57920, 4.175, 2943)-data[i])**2
        #
        # sse22=sse2/(len(data)-len(popt))
        #
        # alpha = (1 - 0.95) / 2
        # tinv = -t.ppf(alpha, len(data) - len(popt))
        #
        # a1=popt[0]-np.sqrt(sse*m2[0,0])*tinv
        # b1=popt[1]-np.sqrt(sse*m2[1,1])*tinv
        # c1=popt[2]-np.sqrt(sse*m2[2,2])*tinv
        #
        # a2=popt[0]+np.sqrt(sse*m2[0,0])*tinv
        # b2=popt[1]+np.sqrt(sse*m2[1,1])*tinv
        # c2=popt[2]+np.sqrt(sse*m2[2,2])*tinv
        #
        #
        #
        # res=np.zeros(len(popt))
        # cres=np.zeros(shape=(len(popt),len(data)))
        #
        # # for i in range(len(popt)):
        # #     for k in range(len(data)):
        # #         for j in range(len(popt)):
        # #             cres[i,k] += m2[i,j] *paradata[j][k]
        # #         res[i] += (cres[i,k]**2)
        #
        #
        #
        #
        #
        # # for i in range(len(popt)):
        # #     for k in range(len(data)):
        # #         for j in range(len(popt)):
        # #             cres[i,k] += m2[i,j] *paradata[j][k]
        # #         # res[i] += (cres[i,k]**2)*(data[k])
        # #         res[i] += (cres[i,k])*(sse/(len(data)-len(popt)))
        # #         # res[i] += (cres[i,k])*(Nilist[k])
        #
        # for i in range(len(popt)):
        #     for k in range(len(popt)):
        #         # res[i] += (cres[i,k]**2)*(data[k])
        #         res[i] += (m2[i,k])*(sse/(len(data)-len(popt)))
        #
        # # for i in range(len(popt)):
        # #     for j in range(len(popt)):
        # #         res[i]+=m2[i,j]**2*v[j]**2
        #
        #
        #
        # # #matlab移植
        # # tempparadata = np.array(paradata[0:len(popt)]).T
        # # _,R = np.linalg.qr(tempparadata,mode ='reduced')
        # # rinv=np.linalg.lstsq(R,np.identity(len(popt)))[0]
        # # rinv=rinv**2
        # # v=rinv.sum(axis=1)*sse/(len(data)-len(popt))
        # # alpha = (1 - 0.95) / 2
        # # tinv=-t.ppf(alpha, len(data)-len(popt))
        # # db = tinv * np.sqrt(v.T)
        # # print(db)
        #
        #
        #
        # print("指数 优度："+str(R21[0]))
        # for i in range(len(popt)):
        #     # print(popt[i],error[i],pcov[i])
        #     # print(str(popt[i])+"±"+str(np.sqrt(res[i]))+"\t±"+str(pcovdiag[i])+" "+str(popt[i]-np.sqrt(res[i]))+"\t"+str(popt[i]+np.sqrt(res[i])))
        #     print(str(popt[i]))
        #     # print(str(popt[i])+"±"+str(np.sqrt(res[i]))+"\t±"+str(pcovdiag[i])+"\t"+str(popt[i]-np.sqrt(res[i]))+"\t"+str(popt[i]+np.sqrt(res[i])))
        #     # print(str(popt[i])+"±"+str(np.sqrt(abs(res[i]))*1.9847)+"\t±"+str(popt[i]-np.sqrt(abs(res[i]))*1.9847)+"\t"+str(popt[i]+np.sqrt(abs(res[i]))*1.9847))
        #     # print(str(popt[i])+"±"+str(db[i])+"\t±"+str(popt[i]-db[i])+"\t"+str(popt[i]+db[i]))
        #
        #
        # #
        # # # error = np.linalg.solve(m, v)
        # # # pcovdiag = np.sqrt(np.diag(pcov))
        # # # print(pcovdiag)
        # # print("指数"+str(R2[0]))
        # # for i in range(len(popt)):
        # #     # print(popt[i],error[i],pcov[i])
        # #     print(str(popt[i]) + "±" + str(error[i]))
        # #     # print(str(popt[i]) + "±(" + str(error[i]) + ")   (" + str(pcovdiag[i]) + ")")
        #
        #

        # plt.scatter(x,datapar)
        plt.plot(xfit2,yfit2)
        # plt.plot(xfit2,yfit2)
        plt.plot(datax,data)
        print(data[-1])
        plt.show()



if __name__ == '__main__':
    # main(1)
    # main([1,2],"D:/工作文件2/20190924/处理后的原始数据/QCC2019 924 9 938-tq右侧足三里左旁开（24日涂紫药水）-D-处理后.txt")
    # main([1,2],"D:/工作文件2/20190924/QCC2019 924 9 3 4-毛玻璃test1-D.txt")
    # main([1,2],"D:/工作文件2/20190924/QCC2019 924 922 8-tq右侧下巨虚下循经非穴（未涂紫药水）-D.txt")
    main([3],"D:/工作文件2/20190924/QCC2019 924 9 3 1-毛玻璃test1-D.txt")