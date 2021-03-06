import os
import re
import numpy as np
import xlrd
import xlwt
import xlsxwriter
from scipy.optimize import curve_fit
from datetime import datetime
from xlutils.copy import copy
from sympy import symbols, diff
from scipy.stats import t
from scipy import integrate
import math
import copy
import sympy

class cutclass():
    def __init__(self):
        self.weightfit=False
        self.filename = ""
        self.funtype = ""
        self.para = []
        self.para_error = []
        self.fitx = []
        self.fity = []
        self.xfit=[]    #原始散点x坐标
        self.yfit=[]    #原始散点y坐标
        self.method = ""
        self.cutstartnum1 = 0
        self.cutendnum1 = 0
        self.cutstartnumspot1 = 0
        self.cutendnumspot1 = 0
        self.R2 = 0
        self.Max = 0
        self.Min = 0

class dataclass():
    def __init__(self, parent=None):
        self.filepath = ""
        self.outpath = ""
        self.filename = ""
        self.Max = 0
        self.Min = 0
        self.paras = dict()
        self.paras["双曲线拟合"] = []
        self.paras["指数拟合"] = []
        self.paras["双曲线积分拟合"] = []
        self.paras["指数积分拟合"] = []
        self.Interval = 0  # 每个点的间隔

        self.ACQ_Time = ""
        self.ACQ_TimeMinuteCount = ""
        self.Project = ""
        self.Name = ""
        self.Part = ""
        self.Operator = ""
        self.Desc = ""
        self.Excited_Peroid = ""
        self.Excited_Time = ""
        self.Acq_Delay_Time = ""
        self.Gate_Time = ""
        self.Count_Num_per_gate = ""
        self.Repeat_Times = ""  # 重复次数
        self.Acq_Gate_Times = ""
        self.Interval_per_Gate = ""
        self.Channel_Number = ""
        # ----------data1--------------
        # 原始数据
        self.Raw_Data1 = []

        # 预处理后的数据
        self.Pro_mal1 = []  # 每个数据点的子数据矩阵
        self.mal1MES=[]
        self.Pro_Data1_X = []
        self.Pro_Data1_variety_X = []
        self.Pro_Data1 = []
        # 裁剪数据
        self.cutstartnum1 = 0
        self.cutendnum1 = 0  # 最后一个数据点的序号
        self.Cut_Data1_X = []
        self.Cut_Data1 = []
        self.Cut_Data1fit_X = []
        self.Cut_Data1fit = []
        # ----------data2--------------
        # 原始数据
        self.Raw_Data2 = []

        # 预处理后的数据
        self.Pro_mal2 = []
        self.Pro_Data2_X = []
        self.Pro_Data2 = []
        # 裁剪数据
        self.cutstartnum2 = 0
        self.cutendnum2 = 0
        self.Cut_Data2_X = []
        self.Cut_Data2 = []
        self.Cut_Data2fit_X = []
        self.Cut_Data2fity = []

# class dataread():
#     def __init__(self,sinOutpro, sinOuttext,sinOutbool):
#         self.sinOutpro = sinOutpro
#         self.sinOuttext = sinOuttext
#         self.sinOutbool = sinOutbool
#         self.filelist = dict()
#         self.maxCol = 0
#         self.filenames = []
#         self.dirList = []
#         self.filepath = ""
#
#     def readfiles(self, filepath):  # 存入数据
#         print("readfile in")
#         self.sinOutbool.emit(True)
#         self.sinOuttext.emit("正在进行数据转换...")
#         self.sinOutpro.emit(0)
#         print("readfile in")
#         try:
#             files = os.listdir(filepath)
#         except Exception as a:
#             print(a)
#         print(files)
#         # 排除隐藏文件和文件夹
#         for f in files:
#             if (os.path.isdir(filepath + '/' + f)):
#                 # 排除隐藏文件夹。因为隐藏文件夹过多
#                 if (f[0] == '.'):
#                     pass
#                 else:
#                     # 添加非隐藏文件夹
#                     self.dirList.append(f)
#             if (os.path.isfile(filepath + '/' + f)):
#                 # 添加文件
#                 if (os.path.splitext(f)[1] == ".txt"):
#                     self.filenames.append(f)
#         p = 1
#         # print(self.filenames)
#
#         for f in self.filenames:
#             self.sinOuttext.emit("正在转换 " + str(p) + "/" + str(len(self.filenames)) + " " + f)
#             data = dataclass()
#             data.filepath = filepath
#             datarow = open(filepath + '/' + f)  # 读取的整个原始文件数据
#             datarowlines = datarow.readlines()  # 读取的整个原始文件的数据，按行分割
#             datapar = []  # 真正的每行数据数组
#             for line in datarowlines:
#                 linenew = line.strip()
#                 if (linenew != ""):
#                     datapar.append(linenew)
#             # print(datapar)
#             # self.ACQ_Time=re.search("(\d{4}-\d{1,2}-\d{1,2}\s*\d{1,2}:\d{1,2}:\d{1,2}:\s*\d{1,3})",datapar[1])
#             temptime = re.search("\d{4}-\s*\d{1,2}-\s*\d{1,2}\s*\d{1,2}:\s*\d{1,2}:\s*\d{1,2}.\s*\d{1,3}\s*.",
#                                  datapar[1]).group(0)
#             # print(temptime)
#             # strtemp=temptime[5].split('.')
#             # temptime[5]=strtemp[0]
#             # temptime.append(strtemp[1])
#             timelist = re.split('[- :.]\s*', temptime)
#             # print(timelist)
#
#             timestr = timelist[0] + "-" + timelist[1] + "-" + timelist[2] + "  " + timelist[3] + ":" + timelist[
#                 4] + ":" + timelist[5] + "." + timelist[6]
#             data.ACQ_Time = datetime.strptime(timestr, '%Y-%m-%d  %H:%M:%S.%f')
#             data.Project = datapar[2].strip(datapar[2].split(": ")[0]).strip(": ")
#             data.Name = datapar[3].strip(datapar[3].split(": ")[0]).strip(": ")
#             data.part = datapar[4].strip(datapar[4].split(": ")[0]).strip(": ")
#             data.Operator = datapar[5].strip(datapar[5].split(": ")[0]).strip(": ")
#             data.Desc = datapar[6].strip(datapar[6].split(": ")[0]).strip(": ")
#             data.Excited_Peroid = int(datapar[9].strip(datapar[9].split(": ")[0]).strip(": "))
#             data.Excited_Time = int(datapar[10].strip(datapar[10].split(": ")[0]).strip(": "))
#             data.Acq_Delay_Time = int(datapar[11].strip(datapar[11].split(": ")[0]).strip(": "))
#             data.Gate_Time = int(datapar[12].strip(datapar[12].split(": ")[0]).strip(": "))
#             data.Count_Num_per_gate = int(datapar[13].strip(datapar[13].split(": ")[0]).strip(": "))
#             data.Repeat_Times = int(datapar[14].strip(datapar[14].split(": ")[0]).strip(": "))
#             data.Acq_Gate_Times = int(datapar[15].strip(datapar[15].split(": ")[0]).strip(": "))
#             data.Interval_per_Gate = int(datapar[16].strip(datapar[16].split(": ")[0]).strip(": "))
#             datanum = int(data.Repeat_Times * data.Count_Num_per_gate)
#             data.Pro_Data1 = np.zeros(data.Acq_Gate_Times * data.Count_Num_per_gate).tolist()
#             print("okkk")
#             print(datapar[17])
#             print(datapar[17].strip(datapar[17].split(":")[0]).strip(":"))
#             if (datapar[17].strip(datapar[17].split(":")[0]).strip(":") == ""):
#                 print("进入")
#                 data.Channel_Number = "1"
#                 for i in range(18, 18 + datanum * data.Acq_Gate_Times):
#                     data.Raw_Data1.append(int(datapar[i]))
#                 # if (data.Channel_Number == 2):
#                 #     for i in range(18 + datanum + 1,
#                 #                    18 + datanum * data.Acq_Gate_Times + 1 + datanum * data.Acq_Gate_Times):
#                 #         data.Raw_Data2.append(int(datapar[i]))
#             else:
#                 data.Channel_Number = int(datapar[17].strip(datapar[17].split(": ")[0]).strip(": "))
#                 for i in range(19, 19 + datanum * data.Acq_Gate_Times):
#                     data.Raw_Data1.append(int(datapar[i]))
#                 # if (data.Channel_Number == 2):
#                 #     for i in range(19 + datanum + 1,
#                 #                    19 + datanum * data.Acq_Gate_Times + 1 + datanum * data.Acq_Gate_Times):
#                 #         data.Raw_Data2.append(int(datapar[i]))
#             # print(data.ACQ_Time)
#             # 计算时间，以分钟为单位
#             # minutecount=0
#             # timelist=re.split('[- :]\s*',data.ACQ_Time)
#             # data1 =timelist[0] + "-" + timelist[1] + "-" + timelist[2] + " " + timelist[3] + ":" + timelist[4] + ":" + timelist[5]
#             #
#             # year=(float(timelist[0])-2019)*364*24*60
#             # mouth=(float(timelist[1])-1)*30.5*24*60
#             # day=  (float(timelist[2])-1)*24*
#             # print(data)
#
#             # datanum = int(data.Repeat_Times * data.Count_Num_per_gate)
#             # datanum=int(data.Repeat_Times*data.Count_Num_per_gate*data.Acq_Gate_Times)
#             # print("datanum",datanum)
#             # print(datanum/data.Repeat_Times,data.Acq_Gate_Times*data.Count_Num_per_gate)
#             # print()
#             # data.Pro_Data1 = np.zeros(data.Acq_Gate_Times * data.Count_Num_per_gate).tolist()
#             # [0 for i in range(data.Acq_Gate_Times*data.Count_Num_per_gate)]
#             # print(data.Gate_Time)
#             # print("len(data.Raw_Data1)",len(data.Pro_Data1))
#             # print("data.Count_Num_per_gate*data.Gate_Time",data.Count_Num_per_gate*data.Gate_Time)
#             #
#             # for i in range(19, 19 + datanum * data.Acq_Gate_Times):
#             #     data.Raw_Data1.append(int(datapar[i]))
#             # if (data.Channel_Number == "2"):
#             #     for i in range(19 + datanum + 1,
#             #                    19 + datanum * data.Acq_Gate_Times + 1 + datanum * data.Acq_Gate_Times):
#             #         data.Raw_Data2.append(int(datapar[i]))
#             # print(len(data.Raw_Data1))
#             # print(len(data.Raw_Data2))
#
#             dScale = data.Count_Num_per_gate * 1000 / (data.Gate_Time * data.Repeat_Times)
#             for i in range(int(data.Acq_Gate_Times)):
#                 for j in range(int(data.Count_Num_per_gate)):
#                     ncps = 0
#                     ncpslist = []
#                     for k in range(int(data.Repeat_Times)):
#                         ncps += data.Raw_Data1[k * data.Count_Num_per_gate + j + i * datanum]
#                         ncpslist.append(data.Raw_Data1[k * data.Count_Num_per_gate + j + i * datanum])
#                     data.Pro_mal1.append(ncpslist)
#                     data.Pro_Data1[j * data.Acq_Gate_Times + i] = ncps * dScale
#             # data.Interval=float((data.Gate_Time)/len(data.Pro_Data1))*data.Count_Num_per_gate*0.001
#             data.Interval = float(data.Gate_Time / data.Count_Num_per_gate)
#             # print(data.Pro_Data1)
#
#             # print("data.Interval",data.Interval)
#
#             # for i in range(len(data.Pro_Data1)):
#             #     data.Pro_Data1_X.append(round(i*data.Interval,5))
#             #
#
#             for i in range(int(data.Count_Num_per_gate)):
#                 for j in range(int(data.Acq_Gate_Times)):
#                     data.Pro_Data1_X.append(float(i * data.Interval + j * data.Interval_per_Gate * 0.001))
#             # print(data.Interval)
#             # print(data.Pro_Data1_X)
#
#             # print(data.Pro_Data1)
#             data.Max = np.max(data.Pro_Data1)
#             data.Min = np.min(data.Pro_Data1)
#             if(data.Max==0):
#                 self.data.filenames.remove(f)
#                 continue
#             data.cutendnum1 = len(data.Pro_Data1) - 1
#             # 复制原始数据到Cut
#             data.Cut_Data1 = copy.deepcopy(data.Pro_Data1)
#             data.Cut_Data1_X = copy.deepcopy(data.Pro_Data1_X)
#             if (len(data.Cut_Data1) > self.maxCol):
#                 self.maxCol = len(data.Cut_Data1)
#             # print("data.Cut_Data1",data.Cut_Data1)
#             self.filelist[f] = data
#
#             # print(self.filelist[f].Pro_Data1)
#             self.sinOutpro.emit(p / len(self.filenames) * 100)
#
#             p += 1
#             self.sinOuttext.emit("完成！")
#         self.sinOutbool.emit(False)
#         self.sinOuttext.emit("数据转换成功！")
#
#     def writeXls(self, outpath):
#         self.sinOutbool.emit(True)
#         self.sinOutpro.emit(0)
#         text = ""
#         workbook = ""
#         if (not (os.path.exists(outpath + "/预处理后的数据.xlsx"))):
#             if (not os.path.exists(outpath)):
#                 os.makedirs(outpath)
#                 # os.mknod(outpath+"/预处理后的数据.xls")
#                 # print("422")
#             workbook = xlsxwriter.Workbook(outpath + "/预处理后的数据.xlsx")
#             # workbookson = xlsxwriter.Workbook(outpath + "/数据子矩阵.xlsx")
#
#             # workbook.save(outpath + "/预处理后的数据.xls")  # 保存工作簿
#             # print("424")
#             text = "数据保存成功！(首次保存，已创建目录及文件)"
#             # self.sinOuttext.emit("数据保存成功！(首次保存，已创建目录及文件)")
#
#         else:
#             try:
#                 os.remove(outpath + "/预处理后的数据.xlsx")
#             except Exception as a:
#                 self.sinOuttext.emit("保存失败！(文件被占用，请关闭关闭文件后重试)")
#                 text = "保存失败！(文件被占用，请关闭关闭文件后重试)"
#                 self.sinOutbool.emit(False)
#                 return
#                 # print(a)
#             else:
#                 workbook = xlsxwriter.Workbook(outpath + "/预处理后的数据.xlsx")
#                 # workbookson = xlsxwriter.Workbook(outpath + "/数据子矩阵.xlsx")
#                 text = "数据保存成功！(数据文件存在，已覆盖原数据文件)"
#                 # workbook.save(outpath + "/预处理后的数据.xls")  # 保存工作簿
#                 # print("xls格式表格写入数据成功！")
#                 # self.sinOuttext.emit("数据保存成功！(数据文件存在，已覆盖原数据文件)")
#         # print(self.filelist)
#         self.sinOuttext.emit("正在保存...")
#         # workbook = xlsxwriter.Workbook()  #表
#         bold1 = workbook.add_format({'fg_color': '#FFC1C1'})
#         bold12 = workbook.add_format({'fg_color': '#CD9B9B'})
#         bold2 = workbook.add_format({'fg_color': '#9AFF9A'})
#         bold22 = workbook.add_format({'fg_color': '#7CCD7C'})
#         bold3 = workbook.add_format({'fg_color': 'blue'})
#         bold4 = workbook.add_format({'fg_color': 'yellow'})
#
#         sheetpars = workbook.add_worksheet("参数数据")  # 参数数据表
#         Prodata = workbook.add_worksheet("预处理后的数据")  # 预处理后的数据表
#         cutdata1 = workbook.add_worksheet("(双曲线)裁剪后的数据")  # 预处理后的数据表
#         cutdata2 = workbook.add_worksheet("(指数)裁剪后的数据")  # 预处理后的数据表
#         inf = workbook.add_worksheet("文件信息")  # 预处理后的数据表
#         # datamat = workbook.add_worksheet("子数据矩阵")  # 子数据矩阵表
#
#         filenamelen = self.countlen(list(self.filelist.keys()))
#         Prodata.write(0, 0, "文件名")
#         cutdata1.write(0, 0, "文件名")
#         cutdata2.write(0, 0, "文件名")
#         # for i in range(len(self.filelist.)):
#         #     Prodata.write(0, i+1, str(i+1))
#         #     cutdata.write(0, i+1, str(i+1))
#         sheetpars.write(0, 0, "文件名")
#         sheetpars.write(0, 1, "Max(原始)")
#         sheetpars.write(0, 2, "Min(原始)")
#         sheetpars.write(0, 3, "ACQ_Time")
#         sheetpars.write(0, 4, "(双曲线)前截点")
#         sheetpars.write(0, 5, "(双曲线)后截点")
#         sheetpars.write(0, 6, "(双曲线)I_0")
#         sheetpars.write(0, 7, "(双曲线)τ")
#         sheetpars.write(0, 8, "(双曲线)Γ")
#         sheetpars.write(0, 9, "(双曲线)D")
#         sheetpars.write(0, 10, "(双曲线)τ/Γ")
#         sheetpars.write(0, 11, "(双曲线)R_square")
#         sheetpars.write(0, 12, "(双曲线)SSE")
#         sheetpars.write(0, 13, "(双曲线)MSE")
#         sheetpars.write(0, 14, "(双曲线)RMSE")
#         sheetpars.write(0, 15, "(指数)前截点")
#         sheetpars.write(0, 16, "(指数)后截点")
#         sheetpars.write(0, 17, "(指数)I_0")
#         sheetpars.write(0, 18, "(指数)τ")
#         sheetpars.write(0, 19, "(指数)D")
#         sheetpars.write(0, 20, "(指数)R_square")
#         sheetpars.write(0, 21, "(指数)SSE")
#         sheetpars.write(0, 22, "(指数)MSE")
#         sheetpars.write(0, 23, "(指数)RMSE")
#         sheetpars.write(0, 24, "(双曲线积分)I_0")
#         sheetpars.write(0, 25, "(双曲线积分)τ")
#         sheetpars.write(0, 26, "(双曲线积分)Γ")
#         sheetpars.write(0, 27, "(双曲线)D")
#         sheetpars.write(0, 28, "(指数积分)I_0")
#         sheetpars.write(0, 29, "(指数积分)τ")
#         sheetpars.write(0, 30, "(指数)D")
#         try:
#             print(self.colnum_string(0))
#             sheetpars.set_column(self.colnum_string(0), filenamelen)
#             sheetpars.set_column(self.colnum_string(3), 28)
#         except Exception as a:
#             print(a)
#         for i in range(4, 30):
#             sheetpars.set_column(self.colnum_string(i), self.countlen("(双曲线积分)I_0"))
#
#         i = 1
#         for key, value in self.filelist.items():
#             sheetpars.write(i, 0, key)  # 像表格中写入数据（对应的行和列）
#             sheetpars.write_number(i, 1, value.Max)  # 像表格中写入数据（对应的行和列）
#             sheetpars.write_number(i, 2, value.Min)  # 像表格中写入数据（对应的行和列）
#             sheetpars.write(i, 3, str(value.ACQ_Time.strftime('%Y-%m-%d  %H:%M:%S.%f')))  # 像表格中写入数据（对应的行和列）
#             # sheetpars.write_datetime(i, 3, value.ACQ_Time.strftime('%Y-%m-%d  %H:%M:%S.%f'))  # 像表格中写入数据（对应的行和列）
#
#             if (value.paras["双曲线拟合"] != []):
#                 sheetpars.write_number(i, 4, value.paras["双曲线拟合"][-1].cutstartnumspot1)
#                 sheetpars.write_number(i, 5, value.paras["双曲线拟合"][-1].cutendnumspot1)
#                 j = 6
#                 for para in value.paras["双曲线拟合"][-1].para:
#                     print(para)
#                     print("拟合1")
#                     if (para != ""):
#                         para = round(para, 3)
#                     sheetpars.write_number(i, j, para, bold1)
#                     j += 1
#                 sheetpars.write_number(i, j,
#                                        round(value.paras["双曲线拟合"][-1].para[1] / value.paras["双曲线拟合"][-1].para[2], 5),
#                                        bold1)
#                 j += 1
#                 for r in value.paras["双曲线拟合"][-1].R2:
#                     if (r != ""):
#                         r = round(r, 5)
#                     sheetpars.write_number(i, j, r, bold12)
#                     j += 1
#             else:
#                 # for r in range(4,12):
#                 #     sheetpars.write(i, j, "", bold1)
#                 j += 8
#             if (value.paras["指数拟合"] != []):
#                 sheetpars.write_number(i, j, value.paras["指数拟合"][-1].cutstartnumspot1)
#                 sheetpars.write_number(i, j, value.paras["指数拟合"][-1].cutendnumspot1)
#                 j += 2
#                 for para in value.paras["指数拟合"][-1].para:
#                     print(para)
#                     print("拟合2")
#                     if (para != ""):
#                         para = round(para, 3)
#                     sheetpars.write_number(i, j, para, bold2)
#                     j += 1
#                 for t in value.paras["指数拟合"][-1].R2:
#                     if (t != ""):
#                         t = round(t, 5)
#                         print(t)
#                     sheetpars.write_number(i, j, t, bold22)
#                     j += 1
#
#             else:
#
#                 j += 7
#             print("okk")
#             if (value.paras["双曲线积分拟合"] != []):
#                 for para in value.paras["双曲线积分拟合"][-1].para:
#                     if (para != ""):
#                         para = round(para, 3)
#                     sheetpars.write_number(i, j, para, bold3)
#                     print(para)
#                     print("拟合3")
#                     j += 1
#             else:
#                 j += 8
#             if (value.paras["指数积分拟合"] != []):
#                 for para in value.paras["指数积分拟合"]:
#                     if (para != ""):
#                         para = round(para, 3)
#                     sheetpars.write_number(i, j, para, bold4)
#                     print(para)
#                     print("拟合4")
#                     j += 1
#             else:
#                 j += 7
#
#             # 保存预处理后的数据
#             Prodata.write(i, 0, key)
#             Prodata.set_column(self.colnum_string(0), filenamelen)
#             z = 1
#             for spot in value.Pro_Data1:
#                 Prodata.write_number(i, z, spot)
#                 z += 1
#
#             # 保存预剪切后的数据
#             if (value.paras["双曲线拟合"] != []):
#                 cutdata1.write(i, 0, key)
#                 cutdata1.set_column(self.colnum_string(0), filenamelen)
#                 z = 1
#                 print(value.cutstartnum1)
#                 print(value.cutendnum1 + 1)
#                 cutdata1.write_number(i, z, value.paras["双曲线拟合"][-1].cutstartnumspot1)
#                 cutdata1.write_number(i, z + 1, value.paras["双曲线拟合"][-1].cutendnumspot1)
#                 z += 2
#                 for spot in value.Pro_Data1[
#                             value.paras["双曲线拟合"][-1].cutstartnum1:value.paras["双曲线拟合"][-1].cutendnum1 + 1]:
#                     cutdata1.write_number(i, z, spot)
#
#                     z += 1
#             if (value.paras["指数拟合"] != []):
#                 cutdata2.write(i, 0, key)
#                 cutdata2.set_column(self.colnum_string(0), filenamelen)
#                 z = 1
#                 print(value.cutstartnum1)
#                 print(value.cutendnum1 + 1)
#                 cutdata2.write_number(i, z, value.paras["指数拟合"][-1].cutstartnumspot1)
#                 cutdata2.write_number(i, z + 1, value.paras["指数拟合"][-1].cutendnumspot1)
#                 z += 2
#                 for spot in value.Pro_Data1[
#                             value.paras["指数拟合"][-1].cutstartnum1:value.paras["指数拟合"][-1].cutendnum1 + 1]:
#                     cutdata2.write_number(i, z, spot)
#
#                     z += 1
#             self.sinOutpro.emit(i / len(self.filelist) * 80)
#             i += 1
#         print("round2")
#         # 文件信息
#         inf.write(0, 0, "文件名")
#         inf.write(0, 1, "ACQ_Time")
#         inf.write(0, 2, "Project")
#         inf.write(0, 3, "Name")
#         inf.write(0, 4, "Part")
#         inf.write(0, 5, "Operator")
#         inf.write(0, 6, "Desc")
#         inf.write(0, 7, "Excited_Peroid(ms)")
#         inf.write(0, 8, "Excited_Time(ms)")
#         inf.write(0, 9, "Acq_Delay_Time(ms)")
#         inf.write(0, 10, "Gate_Time(ms)")
#         inf.write(0, 11, "Count_Num_per_gate")
#         inf.write(0, 12, "Repeat_Times")
#         inf.write(0, 13, "Acq_Gate_Times")
#         inf.write(0, 14, "Interval_per_Gate(ms)")
#         inf.write(0, 15, "Channel_Number")
#         print(type(inf))
#
#         inf.set_column(self.colnum_string(0), self.countlen(list(self.filelist.keys())))
#         inf.set_column(self.colnum_string(1), 28)
#         inf.set_column(self.colnum_string(2), self.countlen("Project"))
#         inf.set_column(self.colnum_string(3), self.countlen("Name  "))
#         inf.set_column(self.colnum_string(4), self.countlen("Part  "))
#         inf.set_column(self.colnum_string(5), self.countlen("Operator"))
#         inf.set_column(self.colnum_string(6), self.countlen("Desc "))
#         inf.set_column(self.colnum_string(7), self.countlen("Excited_Peroid(ms)"))
#         inf.set_column(self.colnum_string(8), self.countlen("Excited_Time(ms)"))
#         inf.set_column(self.colnum_string(9), self.countlen("Acq_Delay_Time(ms)"))
#         inf.set_column(self.colnum_string(10), self.countlen("Gate_Time(ms)"))
#         inf.set_column(self.colnum_string(11), self.countlen("Count_Num_per_gate"))
#         inf.set_column(self.colnum_string(12), self.countlen("Repeat_Times"))
#         inf.set_column(self.colnum_string(13), self.countlen("Acq_Gate_Times"))
#         inf.set_column(self.colnum_string(14), self.countlen("Interval_per_Gate(ms)"))
#         inf.set_column(self.colnum_string(15), self.countlen("Channel_Number"))
#
#         # for i in range(0,16):
#         # inf.col(i).width=256*(len(inf.cell(0,i).value.encode('utf-8').encode()))
#         # print(len(inf.cell(0,i).value.encode('utf-8').encode()))
#
#         i = 1
#
#         for key, value in self.filelist.items():
#             inf.write(i, 0, str(key))
#             # inf.write_datetime(i, 1,value.ACQ_Time)
#             inf.write(i, 1, str(value.ACQ_Time.strftime('%Y-%m-%d  %H:%M:%S.%f')))
#             inf.write(i, 2, str(value.Project))
#             inf.write(i, 3, str(value.Name))
#             inf.write(i, 4, str(value.Part))
#             inf.write(i, 5, str(value.Operator))
#             inf.write(i, 6, str(value.Desc))
#             inf.write_number(i, 7, round(value.Excited_Peroid, 2))
#             inf.write_number(i, 8, round(value.Excited_Time, 2))
#             inf.write_number(i, 9, round(value.Acq_Delay_Time, 2))
#             inf.write_number(i, 10, round(value.Gate_Time, 2))
#             inf.write_number(i, 11, round(value.Count_Num_per_gate, 2))
#             inf.write_number(i, 12, round(value.Repeat_Times, 2))
#             inf.write_number(i, 13, round(value.Acq_Gate_Times, 2))
#             inf.write_number(i, 14, round(value.Interval_per_Gate, 2))
#             inf.write_number(i, 15, round(value.Channel_Number, 2))
#             self.sinOutpro.emit(i / len(self.filelist) * 20 + 80)
#             i += 1
#         workbook.close()
#         # 生成子矩阵文件夹
#
#         # if iswrite==True:
#         #     if (not os.path.exists(outpath+"/数据子矩阵")):
#         #         os.makedirs(outpath+"/数据子矩阵")
#         #     for filename, file in self.filelist.items():
#         #         Worktemp=xlsxwriter.Workbook(outpath + "/数据子矩阵/"+filename+".xlsx")
#         #         sheet=Worktemp.add_worksheet("数据子矩阵")
#         #         for i in range(len(file.Pro_Data1)):
#         #             sheet.write(0,i,str(file.Pro_Data1[i]))
#         #             for j in range(len(file.Pro_mal1[0])):
#         #                 sheet.write(j+1, i, str(file.Pro_mal1[i][j]))
#         #         Worktemp.close()
#
#         # 数据子矩阵
#         # 写入一个文件（文件名不能超过31个char）
#         # try:
#         #     for filename, file in self.filelist.items():
#         #         sheet=workbookson.add_worksheet(filename)
#         #         for i in range(len(file.Pro_Data1)):
#         #             sheet.write(0,i,str(file.Pro_Data1[i]))
#         #             for j in range(file.Pro_mal1[0]):
#         #                 sheet.write(j+1, i, str(file.Pro_mal1[i][j]))
#         #     workbookson.close()
#         # except Exception as a:
#         #     print(a)
#         self.sinOutbool.emit(False)
#         self.sinOuttext.emit(text)
#
#         # print(outpath)
#         # print(not (os.path.exists(outpath)))
#         # print(os.path.exists(outpath))
#         # if( not (os.path.exists(outpath+ "/预处理后的数据.xls"))):
#         #     if( not os.path.exists(outpath)):
#         #         os.makedirs(outpath)
#         #     # os.mknod(outpath+"/预处理后的数据.xls")
#         #     print("422")
#         #     try:
#         #         workbook.save(outpath + "/预处理后的数据.xls")  # 保存工作簿
#         #     print("424")
#         #     self.sinOuttext.emit("数据保存成功！(首次保存，已创建目录及文件)")
#         # else:
#         #     try:
#         #         os.remove(outpath+"/预处理后的数据.xls")
#         #     except Exception as a:
#         #         self.sinOuttext.emit("保存失败！(文件被占用，请关闭关闭文件后重试)")
#         #         print(a)
#         #     else:
#         #         workbook.save(outpath+"/预处理后的数据.xls")  # 保存工作簿
#         #         print("xls格式表格写入数据成功！")
#         #         self.sinOuttext.emit("数据保存成功！(数据文件存在，已覆盖原数据文件)")
#
#     def writesondataXls(self, outpath):
#         exist = True
#         if (not os.path.exists(outpath + "/数据子矩阵/")):
#             os.makedirs(outpath + "/数据子矩阵")
#             exist = False
#         self.sinOutbool.emit(True)
#
#         p = 1
#         for filename, file in self.filelist.items():
#             self.sinOuttext.emit(
#                 "正在保存数据子矩阵 " + str(p) + "/" + str(len(self.filelist)) + " " + os.path.splitext(filename)[0])
#             self.sinOutpro.emit(p / len(self.filelist) * 100)
#             # try:
#             #     os.remove(outpath + "/数据子矩阵/"+os.path.splitext(filename)[0]+".xlsx")
#             # except Exception as a:
#             #     return
#             Worktemp = xlsxwriter.Workbook(outpath + "/数据子矩阵/" + os.path.splitext(filename)[0] + ".xlsx")
#             sheet = Worktemp.add_worksheet("数据子矩阵")
#             for i in range(len(file.Pro_Data1)):
#                 sheet.write_number(0, i, file.Pro_Data1[i])
#                 for j in range(len(file.Pro_mal1[0])):
#                     sheet.write_number(j + 1, i, file.Pro_mal1[i][j])
#             Worktemp.close()
#             p += 1
#         if (exist == False):
#             self.sinOuttext.emit("首次保存，已将子矩阵文件保存到数据目录下的‘数据子矩阵文件夹’！")
#         else:
#             self.sinOuttext.emit("数据子矩阵数据更新成功！")
#         self.sinOutbool.emit(False)
#
#     def writesinglefiledata(self, outpath):
#         exist = True
#         if (not os.path.exists(outpath + "/单文件裁剪后拟合数据/")):
#             os.makedirs(outpath + "/单文件裁剪后拟合数据/")
#             exist = False
#         self.sinOutbool.emit(True)
#         p = 1
#         errlist = []
#         for filename, file in self.filelist.items():
#             self.sinOuttext.emit(
#                 "正在保存单文件裁剪数据 " + str(p) + "/" + str(len(self.filelist)) + " " + os.path.splitext(filename)[0])
#             self.sinOutpro.emit(p / len(self.filelist) * 100)
#             # try:
#             #     os.remove(outpath + "/单文件裁剪后拟合数据/" + os.path.splitext(filename)[0] + ".xlsx")
#             # except Exception :
#             #     errlist.append(os.path.splitext(filename))
#             #     p+=1
#             #     continue
#             Worktemp = xlsxwriter.Workbook(outpath + "/单文件裁剪后拟合数据/" + os.path.splitext(filename)[0] + ".xlsx")
#             sheet1 = Worktemp.add_worksheet("双曲线拟合")
#             sheet2 = Worktemp.add_worksheet("指数拟合")
#             sheet3 = Worktemp.add_worksheet("双曲线裁剪后拟合")
#             sheet4 = Worktemp.add_worksheet("指数裁剪后拟合")
#
#             # 写sheet1
#             sheet1.write(0, 0, "文件名")
#             sheet1.write(0, 1, "前截点数")
#             sheet1.write(0, 2, "后截点数")
#             sheet1.write(0, 3, "I_0")
#             sheet1.write(0, 4, "τ")
#             sheet1.write(0, 5, "Γ")
#             sheet1.write(0, 6, "D")
#             sheet1.write(0, 7, "R_square")
#             sheet1.write(0, 8, "SSE")
#             sheet1.write(0, 9, "MME")
#             sheet1.write(0, 10, "RMSE")
#             for i in range(len(file.paras["双曲线拟合"])):
#                 sheet1.write(i + 1, 0, filename)
#                 sheet1.write_number(i + 1, 1, file.paras["双曲线拟合"][i].cutstartnumspot1)
#                 sheet1.write_number(i + 1, 2, file.paras["双曲线拟合"][i].cutendnumspot1)
#                 sheet1.write_number(i + 1, 3, round(file.paras["双曲线拟合"][i].para[0], 5))
#                 sheet1.write_number(i + 1, 4, round(file.paras["双曲线拟合"][i].para[1], 2))
#                 sheet1.write_number(i + 1, 5, round(file.paras["双曲线拟合"][i].para[2], 2))
#                 sheet1.write_number(i + 1, 6, round(file.paras["双曲线拟合"][i].para[3], 2))
#                 sheet1.write_number(i + 1, 7, round(file.paras["双曲线拟合"][i].R2[0], 8))
#                 sheet1.write_number(i + 1, 8, round(file.paras["双曲线拟合"][i].R2[1], 8))
#                 sheet1.write_number(i + 1, 9, round(file.paras["双曲线拟合"][i].R2[2], 8))
#                 sheet1.write_number(i + 1, 10, round(file.paras["双曲线拟合"][i].R2[3], 8))
#                 i += 1
#             # 写sheet2
#             sheet2.write(0, 0, "文件名")
#             sheet2.write(0, 1, "前截点数")
#             sheet2.write(0, 2, "后截点数")
#             sheet2.write(0, 3, "I_0")
#             sheet2.write(0, 4, "τ")
#             sheet2.write(0, 5, "D")
#             sheet2.write(0, 6, "R_square")
#             sheet2.write(0, 7, "SSE")
#             sheet2.write(0, 8, "MME")
#             sheet2.write(0, 9, "RMSE")
#             for i in range(len(file.paras["指数拟合"])):
#                 sheet2.write(i + 1, 0, filename)
#                 sheet2.write_number(i + 1, 1, file.paras["指数拟合"][i].cutstartnumspot1)
#                 sheet2.write_number(i + 1, 2, file.paras["指数拟合"][i].cutendnumspot1)
#                 sheet2.write_number(i + 1, 3, round(file.paras["指数拟合"][i].para[0], 2))
#                 sheet2.write_number(i + 1, 4, round(file.paras["指数拟合"][i].para[1], 2))
#                 sheet2.write_number(i + 1, 5, round(file.paras["指数拟合"][i].para[2], 2))
#                 sheet2.write_number(i + 1, 6, round(file.paras["指数拟合"][i].R2[0], 2))
#                 sheet2.write_number(i + 1, 7, round(file.paras["指数拟合"][i].R2[1], 2))
#                 sheet2.write_number(i + 1, 8, round(file.paras["指数拟合"][i].R2[2], 2))
#                 sheet2.write_number(i + 1, 9, round(file.paras["指数拟合"][i].R2[3], 2))
#                 i += 1
#             # 写sheet3
#             sheet3.write(0, 0, "前截点数")
#             sheet3.write(0, 1, "后截点数")
#             for i in range(len(file.paras["双曲线拟合"])):
#                 sheet3.write_number(i + 1, 0, file.paras["双曲线拟合"][i].cutstartnumspot1)
#                 sheet3.write_number(i + 1, 1, file.paras["双曲线拟合"][i].cutendnumspot1)
#                 data = file.Pro_Data1[file.paras["双曲线拟合"][i].cutstartnum1:file.paras["双曲线拟合"][i].cutendnum1]
#                 for j in range(len(data)):
#                     sheet3.write_number(i + 1, j + 2, data[j])
#                     j += 1
#                 i += 1
#
#             # 写sheet4
#             sheet4.write(0, 0, "前截点数")
#             sheet4.write(0, 1, "后截点数")
#             for i in range(len(file.paras["指数拟合"])):
#                 sheet4.write_number(i + 1, 0, file.paras["指数拟合"][i].cutstartnumspot1)
#                 sheet4.write_number(i + 1, 1, file.paras["指数拟合"][i].cutendnumspot1)
#                 data = file.Pro_Data1[file.paras["双曲线拟合"][i].cutstartnum1:file.paras["指数拟合"][i].cutendnum1]
#                 for j in range(len(data)):
#                     sheet4.write_number(i + 1, j + 2, data[j])
#                     j += 1
#                 i += 1
#             Worktemp.close()
#             p += 1
#         if (exist == False):
#             self.sinOuttext.emit("首次保存，已将单数据裁剪文件保存到数据目录下的‘单文件裁剪后拟合数据’！")
#         else:
#             if errlist == []:
#                 self.sinOuttext.emit("单文件裁剪后拟合数据更新成功！")
#             else:
#                 name = ""
#                 for temp in errlist:
#                     name += temp
#                 self.sinOuttext.emit(name + "保存失败(文件被占用)，其余文件保存成功")
#         self.sinOutbool.emit(False)
#
#     def Fitting(self,sinOuttext,sinOutpro, funtype, method, startnum, endnum, filename, b1low, b1top, b2low, b2top):
#         self.sinOuttext=sinOuttext
#         self.sinOupro=sinOutpro
#         print(b1low, b1top, b2low, b2top)
#         b1low = [float(i) for i in b1low]
#         b1top = [float(i) for i in b1top]
#         b2low = [float(i) for i in b2low]
#         b2top = [float(i) for i in b2top]
#
#         # b1low=[0.8,0.1,0,0]
#         # b1top=[1.2,1000,1000,10000]
#         # b2low=[0.8,0.1,0]
#         # b2top=[1.2, 1000, 10000]
#         param_bounds1 = ([0, 1, 0, 0], [9999999999, 100, 100, 10000])
#         param_bounds2 = ([0, 1, 0], [999999999, 9999999999, 9999999999])
#         param_bounds3 = ([0, 0, 0, 0], [np.inf, np.inf, np.inf, np.inf])
#         param_bounds4 = ([0, 0, 0], [np.inf, np.inf, np.inf])
#
#         def getIndexes(y_predict, y_data):
#             y_predict = np.array(y_predict)
#             y_data = np.array(y_data)
#             n = y_data.size
#             # SSE为和方差
#             SSE = ((y_data - y_predict) ** 2).sum()
#             # MSE为均方差
#             MSE = SSE / n
#             # RMSE为均方根,越接近0，拟合效果越好
#             RMSE = np.sqrt(MSE)
#
#             # 求R方，0<=R<=1，越靠近1,拟合效果越好
#             u = y_data.mean()
#             SST = ((y_data - u) ** 2).sum()
#             SSR = SST - SSE
#             R_square = SSR / SST
#             return [R_square, SSE, MSE, RMSE]
#
#         def fun1(x, s1, s2, s3, s4):
#             # return s1 * ((1 + (x / s2)) ** (-s3)) + s4
#             return s1 * ((1 + (x / s2)) ** (-s3)) + s4
#
#         def fun2(x, s1, s2, s3):
#             return s1 * (np.exp(-(x / s2))) + s3
#
#         def fun3(x, s1, s2, s3, s4):
#             temp1spot = (1 / (1 + np.asarray(x) / s2)) ** (s3 - 1)
#             temp2spot = (1 / (1 + (np.asarray(x) + TimeSpan) / s2)) ** (s3 - 1)
#             yfitspot = s1 * s2 * (1 / (s3 - 1)) * (temp1spot - temp2spot) + s4 * TimeSpan
#
#         def fun4(x, s1, s2, s3):
#             temp1spot = np.exp(-np.asarray(x) / s2)
#             temp2spot = np.exp(-(np.asarray(x) + TimeSpan) / s2)
#             yfitspot = s1 * s2 * (temp1spot - temp2spot) + s3 * TimeSpan
#
#         self.sinOutbool.emit(True)
#         self.sinOutpro.emit(0)
#         fitfilelist=dict()
#         if (filename == ""):
#             fitfilelist=self.filelist
#         else:
#             fitfilelist[filename] = self.filelist[filename]
#
#         p = 1
#         for key, value in self.filelist.items():
#             if startnum >= len(value.Pro_Data1) - 2:
#                 startnum = len(value.Pro_Data1) - 2
#             if endnum >= len(value.Pro_Data1) - 2:
#                 endnum = len(value.Pro_Data1) - 2
#             starttruenum = startnum
#             endtruenum = len(value.Pro_Data1) - endnum - 1
#             x = value.Pro_Data1_X[starttruenum:endtruenum + 1]
#             y = value.Pro_Data1[starttruenum:endtruenum + 1]
#             Max = np.max(value.Pro_Data1[starttruenum:endtruenum + 1])
#             Min = np.min(value.Pro_Data1[starttruenum:endtruenum + 1])
#             # print("x:",x)
#             # print("y:",y)
#             # value.Cut_Data1fit_X = np.linspace(value.Pro_Data1_X[starttruenum],value.Pro_Data1_X[endtruenum], 1000).tolist()
#             xfit = np.linspace(value.Pro_Data1_X[starttruenum], value.Pro_Data1_X[endtruenum], 1000).tolist()
#             if (funtype == 1):
#                 self.sinOuttext.emit("正在进行双曲线拟合 " + str(p) + "/" + str(len(self.filenames)) + " " + key)
#                 try:
#                     # print("双曲")
#                     # print(b1low[0]*Max,b1low[1],b1low[2],b1low[3])
#                     # print(b1top[0]*Max,b1top[1],b1top[2],b1top[3])
#                     popt, pcov = curve_fit(fun1, x, y, maxfev=500000000, bounds=(
#                     [b1low[0] * Max, b1low[1], b1low[2], b1low[3]], [b1top[0] * Max, b1top[1], b1top[2], b1top[3]]),
#                                            method=method)
#                     yfit = fun1(xfit, popt[0], popt[1], popt[2], popt[3])
#                     ytempfit = fun1(x, popt[0], popt[1], popt[2], popt[3])
#                     R2 = getIndexes(ytempfit, y)
#                 except Exception as a:
#                     print(a)
#
#                 isexist = 0
#                 # print(value.paras["双曲线拟合"])
#                 if (value.paras["双曲线拟合"] != []):
#                     for i in range(len(value.paras["双曲线拟合"])):
#                         if ((value.paras["双曲线拟合"][i].cutstartnum1 == starttruenum) and (
#                                 value.paras["双曲线拟合"][i].cutendnum1 == endtruenum)):
#                             value.paras["双曲线拟合"][i].para = popt
#                             value.paras["双曲线拟合"][i].method = method
#                             value.paras["双曲线拟合"][i].fity = yfit
#                             value.paras["双曲线拟合"][i].fitx = xfit
#                             value.paras["双曲线拟合"][i].R2 = R2
#                             isexist = 1
#                             break
#                 if (isexist == 0):
#                     cutdata = cutclass()
#                     cutdata.cutstartnum1 = starttruenum
#                     cutdata.cutendnum1 = endtruenum
#                     cutdata.cutstartnumspot1 = startnum
#                     cutdata.cutendnumspot1 = endnum
#                     cutdata.funtype = funtype
#                     cutdata.method = method
#                     cutdata.fitx = xfit
#                     cutdata.fity = yfit
#                     cutdata.para = popt
#                     cutdata.R2 = R2
#                     cutdata.Max = Max
#                     cutdata.Min = Min
#                     value.paras["双曲线拟合"].append(cutdata)
#
#                 # value.Cut_Data1fit = fun1(value.Cut_Data1fit_X, popt[0], popt[1], popt[2], popt[3])
#             elif (funtype == 2):
#                 # print(key)
#                 self.sinOuttext.emit("正在进行指数拟合 " + str(p) + "/" + str(len(self.filenames)) + " " + key)
#                 #
#                 # print(x)
#                 # print(y)
#                 try:
#                     # print("指数")
#                     # print(b2low[0]*Max,b2low[1],b2low[2])
#                     # print(b2top[0]*Max,b2top[1],b2top[2])
#                     popt, pcov = curve_fit(fun2, x, y, maxfev=50000000, bounds=(
#                     [b2low[0] * Max, b2low[1], b2low[2]], [b2top[0] * Max, b2top[1], b2top[2]]), method=method)
#                     yfit = fun2(xfit, popt[0], popt[1], popt[2])
#                     ytempfit = fun2(x, popt[0], popt[1], popt[2])
#                     R2 = getIndexes(ytempfit, y)
#                 except Exception as a:
#                     print(a)
#                 isexist = 0
#                 if (value.paras["双曲线拟合"] != []):
#                     for i in range(len(value.paras["指数拟合"])):
#                         if ((value.paras["指数拟合"][i].cutstartnum1 == starttruenum) and (
#                                 value.paras["指数拟合"][i].cutendnum1 == endtruenum)):
#                             value.paras["指数拟合"][i].para = popt
#                             value.paras["指数拟合"][i].method = method
#                             value.paras["指数拟合"][i].fity = yfit
#                             value.paras["指数拟合"][i].fitx = xfit
#                             value.paras["指数拟合"][i].R2 = R2
#
#                             isexist = 1
#                             break
#                 if (isexist == 0):
#                     cutdata = cutclass()
#                     cutdata.cutstartnum1 = starttruenum
#                     cutdata.cutendnum1 = endtruenum
#                     cutdata.cutstartnumspot1 = startnum
#                     cutdata.cutendnumspot1 = endnum
#                     cutdata.funtype = funtype
#                     cutdata.method = method
#                     cutdata.fitx = xfit
#                     cutdata.fity = yfit
#                     cutdata.para = popt
#                     cutdata.R2 = R2
#                     cutdata.Max = np.max(value.Pro_Data1[starttruenum:endtruenum + 1])
#                     cutdata.Min = np.min(value.Pro_Data1[starttruenum:endtruenum + 1])
#                     value.paras["指数拟合"].append(cutdata)
#
#                 # value.Cut_Data1fit = fun2(value.Cut_Data1fit_X, popt[0], popt[1], popt[2])
#             elif (funtype == 3):
#                 self.sinOuttext.emit("正在进行双曲线积分拟合 " + str(p) + "/" + str(len(self.filenames)))
#                 popt, pcov = curve_fit(fun3, x, y, maxfev=500000, bounds=param_bounds3, method=method)
#                 value.paras["双曲线积分拟合"] = popt
#                 value.Cut_Data1fit = fun3(value.Cut_Data1fit_X, popt[0], popt[1], popt[2], popt[3])
#             elif (funtype == 4):
#                 self.sinOuttext.emit("正在进行指数积分拟合 " + str(p) + "/" + str(len(self.filenames)))
#                 popt, pcov = curve_fit(fun4, x, y, maxfev=500000, bounds=param_bounds4, method=method)
#                 value.paras["指数积分拟合"] = popt
#                 value.Cut_Data1fit = fun4(value.Cut_Data1fit_X, popt[0], popt[1], popt[2])
#
#             # print(value.Cut_Data1fit)
#             # self.sinOuttext.emit("正在拟合"+str(p)+"/"+str(len(self.filelist))+"  "+key)
#             # print("正在拟合",str(p))
#             self.sinOutpro.emit(p / len(self.filenames) * 100)
#             p = p + 1
#
#
#         # if (filename == ""):
#         #     fitfilelist=self.filelist
#         #     p = 1
#         #     for key, value in self.filelist.items():
#         #         if startnum >= len(value.Pro_Data1) - 2:
#         #             startnum = len(value.Pro_Data1) - 2
#         #         if endnum >= len(value.Pro_Data1) - 2:
#         #             endnum = len(value.Pro_Data1) - 2
#         #         starttruenum = startnum
#         #         endtruenum = len(value.Pro_Data1) - endnum - 1
#         #         x = value.Pro_Data1_X[starttruenum:endtruenum + 1]
#         #         y = value.Pro_Data1[starttruenum:endtruenum + 1]
#         #         Max = np.max(value.Pro_Data1[starttruenum:endtruenum + 1])
#         #         Min = np.min(value.Pro_Data1[starttruenum:endtruenum + 1])
#         #         # print("x:",x)
#         #         # print("y:",y)
#         #         # value.Cut_Data1fit_X = np.linspace(value.Pro_Data1_X[starttruenum],value.Pro_Data1_X[endtruenum], 1000).tolist()
#         #         xfit = np.linspace(value.Pro_Data1_X[starttruenum], value.Pro_Data1_X[endtruenum], 1000).tolist()
#         #         if (funtype == 1):
#         #             self.sinOuttext.emit("正在进行双曲线拟合 " + str(p) + "/" + str(len(self.filenames)) + " " + key)
#         #             try:
#         #                 # print("双曲")
#         #                 # print(b1low[0]*Max,b1low[1],b1low[2],b1low[3])
#         #                 # print(b1top[0]*Max,b1top[1],b1top[2],b1top[3])
#         #                 popt, pcov = curve_fit(fun1, x, y, maxfev=500000000, bounds=(
#         #                 [b1low[0] * Max, b1low[1], b1low[2], b1low[3]], [b1top[0] * Max, b1top[1], b1top[2], b1top[3]]),
#         #                                        method=method)
#         #                 yfit = fun1(xfit, popt[0], popt[1], popt[2], popt[3])
#         #                 ytempfit = fun1(x, popt[0], popt[1], popt[2], popt[3])
#         #                 R2 = getIndexes(ytempfit, y)
#         #             except Exception as a:
#         #                 print(a)
#         #
#         #             isexist = 0
#         #             # print(value.paras["双曲线拟合"])
#         #             if (value.paras["双曲线拟合"] != []):
#         #                 for i in range(len(value.paras["双曲线拟合"])):
#         #                     if ((value.paras["双曲线拟合"][i].cutstartnum1 == starttruenum) and (
#         #                             value.paras["双曲线拟合"][i].cutendnum1 == endtruenum)):
#         #                         value.paras["双曲线拟合"][i].para = popt
#         #                         value.paras["双曲线拟合"][i].method = method
#         #                         value.paras["双曲线拟合"][i].fity = yfit
#         #                         value.paras["双曲线拟合"][i].fitx = xfit
#         #                         value.paras["双曲线拟合"][i].R2 = R2
#         #                         isexist = 1
#         #                         break
#         #             if (isexist == 0):
#         #                 cutdata = cutclass()
#         #                 cutdata.cutstartnum1 = starttruenum
#         #                 cutdata.cutendnum1 = endtruenum
#         #                 cutdata.cutstartnumspot1 = startnum
#         #                 cutdata.cutendnumspot1 = endnum
#         #                 cutdata.funtype = funtype
#         #                 cutdata.method = method
#         #                 cutdata.fitx = xfit
#         #                 cutdata.fity = yfit
#         #                 cutdata.para = popt
#         #                 cutdata.R2 = R2
#         #                 cutdata.Max = Max
#         #                 cutdata.Min = Min
#         #                 value.paras["双曲线拟合"].append(cutdata)
#         #
#         #             # value.Cut_Data1fit = fun1(value.Cut_Data1fit_X, popt[0], popt[1], popt[2], popt[3])
#         #         elif (funtype == 2):
#         #             # print(key)
#         #             self.sinOuttext.emit("正在进行指数拟合 " + str(p) + "/" + str(len(self.filenames)) + " " + key)
#         #             #
#         #             # print(x)
#         #             # print(y)
#         #             try:
#         #                 # print("指数")
#         #                 # print(b2low[0]*Max,b2low[1],b2low[2])
#         #                 # print(b2top[0]*Max,b2top[1],b2top[2])
#         #                 popt, pcov = curve_fit(fun2, x, y, maxfev=50000000, bounds=(
#         #                 [b2low[0] * Max, b2low[1], b2low[2]], [b2top[0] * Max, b2top[1], b2top[2]]), method=method)
#         #                 yfit = fun2(xfit, popt[0], popt[1], popt[2])
#         #                 ytempfit = fun2(x, popt[0], popt[1], popt[2])
#         #                 R2 = getIndexes(ytempfit, y)
#         #             except Exception as a:
#         #                 print(a)
#         #             isexist = 0
#         #             if (value.paras["双曲线拟合"] != []):
#         #                 for i in range(len(value.paras["指数拟合"])):
#         #                     if ((value.paras["指数拟合"][i].cutstartnum1 == starttruenum) and (
#         #                             value.paras["指数拟合"][i].cutendnum1 == endtruenum)):
#         #                         value.paras["指数拟合"][i].para = popt
#         #                         value.paras["指数拟合"][i].method = method
#         #                         value.paras["指数拟合"][i].fity = yfit
#         #                         value.paras["指数拟合"][i].fitx = xfit
#         #                         value.paras["指数拟合"][i].R2 = R2
#         #
#         #                         isexist = 1
#         #                         break
#         #             if (isexist == 0):
#         #                 cutdata = cutclass()
#         #                 cutdata.cutstartnum1 = starttruenum
#         #                 cutdata.cutendnum1 = endtruenum
#         #                 cutdata.cutstartnumspot1 = startnum
#         #                 cutdata.cutendnumspot1 = endnum
#         #                 cutdata.funtype = funtype
#         #                 cutdata.method = method
#         #                 cutdata.fitx = xfit
#         #                 cutdata.fity = yfit
#         #                 cutdata.para = popt
#         #                 cutdata.R2 = R2
#         #                 cutdata.Max = np.max(value.Pro_Data1[starttruenum:endtruenum + 1])
#         #                 cutdata.Min = np.min(value.Pro_Data1[starttruenum:endtruenum + 1])
#         #                 value.paras["指数拟合"].append(cutdata)
#         #
#         #             # value.Cut_Data1fit = fun2(value.Cut_Data1fit_X, popt[0], popt[1], popt[2])
#         #         elif (funtype == 3):
#         #             self.sinOuttext.emit("正在进行双曲线积分拟合 " + str(p) + "/" + str(len(self.filenames)))
#         #             popt, pcov = curve_fit(fun3, x, y, maxfev=500000, bounds=param_bounds3, method=method)
#         #             value.paras["双曲线积分拟合"] = popt
#         #             value.Cut_Data1fit = fun3(value.Cut_Data1fit_X, popt[0], popt[1], popt[2], popt[3])
#         #         elif (funtype == 4):
#         #             self.sinOuttext.emit("正在进行指数积分拟合 " + str(p) + "/" + str(len(self.filenames)))
#         #             popt, pcov = curve_fit(fun4, x, y, maxfev=500000, bounds=param_bounds4, method=method)
#         #             value.paras["指数积分拟合"] = popt
#         #             value.Cut_Data1fit = fun4(value.Cut_Data1fit_X, popt[0], popt[1], popt[2])
#         #
#         #         # print(value.Cut_Data1fit)
#         #         # self.sinOuttext.emit("正在拟合"+str(p)+"/"+str(len(self.filelist))+"  "+key)
#         #         # print("正在拟合",str(p))
#         #         self.sinOutpro.emit(p / len(self.filenames) * 100)
#         #         p = p + 1
#         # else:
#         #
#         #     try:
#         #         value = self.filelist[filename]
#         #     except Exception as a:
#         #         print(a)
#         #     if startnum >= len(value.Pro_Data1) - 2:
#         #         startnum = len(value.Pro_Data1) - 2
#         #     if endnum >= len(value.Pro_Data1) - 2:
#         #         endnum = len(value.Pro_Data1) - 2
#         #     starttruenum = startnum
#         #     endtruenum = len(value.Pro_Data1) - endnum - 1
#         #     Max = np.max(value.Pro_Data1[starttruenum:endtruenum + 1])
#         #     Min = np.min(value.Pro_Data1[starttruenum:endtruenum + 1])
#         #     TimeSpan = value.Gate_Time
#         #     x = value.Pro_Data1_X[starttruenum:endtruenum + 1]
#         #     y = value.Pro_Data1[starttruenum:endtruenum + 1]
#         #     xfit = np.linspace(value.Pro_Data1_X[starttruenum], value.Pro_Data1_X[endtruenum], 1000).tolist()
#         #     try:
#         #         if (funtype == 1):
#         #             # print("双曲")
#         #             # print(b1low[0]*Max,b1low[1],b1low[2],b1low[3])
#         #             # print(b1top[0]*Max,b1top[1],b1top[2],b1top[3])
#         #             popt, pcov = curve_fit(fun1, x, y, maxfev=500000, bounds=(
#         #             [b1low[0] * Max, b1low[1], b1low[2], b1low[3]], [b1top[0] * Max, b1top[1], b1top[2], b1top[3]]))
#         #             yfit = fun1(xfit, popt[0], popt[1], popt[2], popt[3])
#         #             ytempfit = fun1(x, popt[0], popt[1], popt[2], popt[3])
#         #             R2 = getIndexes(ytempfit, y)
#         #             isexist = 0
#         #             # print(value.paras["双曲线拟合"])
#         #             if (value.paras["双曲线拟合"] != []):
#         #                 for i in range(len(value.paras["双曲线拟合"])):
#         #                     if ((value.paras["双曲线拟合"][i].cutstartnum1 == starttruenum) and (
#         #                             value.paras["双曲线拟合"][i].cutendnum1 == endtruenum)):
#         #                         value.paras["双曲线拟合"][i].para = popt
#         #                         value.paras["双曲线拟合"][i].method = method
#         #                         value.paras["双曲线拟合"][i].fity = yfit
#         #                         value.paras["双曲线拟合"][i].fitx = xfit
#         #                         value.paras["双曲线拟合"][i].R2 = R2
#         #                         isexist = 1
#         #                         break
#         #             if (isexist == 0):
#         #                 cutdata = cutclass()
#         #                 cutdata.cutstartnum1 = starttruenum
#         #                 cutdata.cutendnum1 = endtruenum
#         #                 cutdata.cutstartnumspot1 = startnum
#         #                 cutdata.cutendnumspot1 = endnum
#         #                 cutdata.funtype = funtype
#         #                 cutdata.method = method
#         #                 cutdata.fitx = xfit
#         #                 cutdata.fity = yfit
#         #                 cutdata.para = popt
#         #                 cutdata.R2 = R2
#         #                 cutdata.Max = Max
#         #                 cutdata.Min = Min
#         #                 value.paras["双曲线拟合"].append(cutdata)
#         #
#         #
#         #         elif (funtype == 2):
#         #             # print(value)
#         #             # print(x)
#         #             # print(y)
#         #             # print("指数")
#         #             # print(b2low[0] * Max, b2low[1], b2low[2])
#         #             # print(b2top[0] * Max, b2top[1], b2top[2])
#         #             popt, pcov = curve_fit(fun2, x, y, maxfev=500000, bounds=(
#         #             [b2low[0] * Max, b2low[1], b2low[2]], [b2top[0] * Max, b2top[1], b2top[2]]))
#         #             yfit = fun2(xfit, popt[0], popt[1], popt[2])
#         #             ytempfit = fun2(x, popt[0], popt[1], popt[2])
#         #             R2 = getIndexes(ytempfit, y)
#         #             isexist = 0
#         #             # print(value.paras["指数拟合"])
#         #             if (value.paras["指数拟合"] != []):
#         #                 for i in range(len(value.paras["指数拟合"])):
#         #                     if ((value.paras["指数拟合"][i].cutstartnum1 == starttruenum) and (
#         #                             value.paras["指数拟合"][i].cutendnum1 == endtruenum)):
#         #                         value.paras["指数拟合"][i].para = popt
#         #                         value.paras["指数拟合"][i].method = method
#         #                         value.paras["指数拟合"][i].fity = yfit
#         #                         value.paras["指数拟合"][i].fitx = xfit
#         #                         value.paras["指数拟合"][i].R2 = R2
#         #                         isexist = 1
#         #                         break
#         #             if (isexist == 0):
#         #                 cutdata = cutclass()
#         #                 cutdata.cutstartnum1 = starttruenum
#         #                 cutdata.cutendnum1 = endtruenum
#         #                 cutdata.cutstartnumspot1 = startnum
#         #                 cutdata.cutendnumspot1 = endnum
#         #                 cutdata.funtype = funtype
#         #                 cutdata.method = method
#         #                 cutdata.fitx = xfit
#         #                 cutdata.fity = yfit
#         #                 cutdata.para = popt
#         #                 cutdata.R2 = R2
#         #                 cutdata.Max = Max
#         #                 cutdata.Min = Min
#         #                 value.paras["指数拟合"].append(cutdata)
#         #
#         #         elif (funtype == 3):
#         #             popt, pcov = curve_fit(fun3, x, y, maxfev=500000, bounds=param_bounds3)
#         #             value.paras["双曲线积分拟合"] = popt
#         #             value.Cut_Data1fit = fun3(value.Cut_Data1fit_X, popt[0], popt[1], popt[2], popt[3])
#         #         elif (funtype == 4):
#         #             popt, pcov = curve_fit(fun4, x, y, maxfev=500000, bounds=param_bounds4)
#         #             value.paras["指数积分拟合"] = popt
#         #             value.Cut_Data1fit = fun4(value.Cut_Data1fit_X, popt[0], popt[1], popt[2])
#         #
#         #     except Exception as a:
#         #         print(a)
#         self.sinOutpro.emit(100)
#         self.sinOutbool.emit(False)
#         self.sinOuttext.emit(filename + "文件数据拟合成功！")
#
#     def cutdata(self, numstart, numend, filename):
#
#         # 单文件
#         print(filename)
#         if (filename != "批量裁剪"):
#             index = filename.find("]")
#             title = filename[(index + 1):]
#             print(title)
#             self.filelist[title].cutstartnum1 = numstart
#             self.filelist[title].cutendnum1 = len(self.filelist[title].Pro_Data1) - numend - 1
#             # print("numstart",self.filelist[title].cutstartnum1)
#             # print("numend",self.filelist[title].cutendnum1)
#             self.sinOuttext.emit(
#                 "已经移除 " + filename + " 文件的前" + str(numstart) + "后" + str(numend) + "个数据点,并更新数据的区间内最值")
#             self.countparas(title)
#
#
#         # 批处理
#         else:
#             # self.filelist[filename].cutstartnum1=numstart
#             # self.filelist[filename].cutendnum1=len(self.filelist[filename].Pro_Data1)-numend-1
#             p = 1
#             for key, value in self.filelist.items():
#                 value.cutstartnum1 = numstart
#                 value.cutendnum1 = len(self.filelist[key].Pro_Data1) - numend - 1
#                 # for i in range(numstart):
#                 #     value.Cut_Data1_X.pop(0)
#                 #     value.Cut_Data1.pop(0)
#                 p += 1
#
#                 # value.Max = np.max(value.Cut_Data1)
#                 # value.Min = np.min(value.Cut_Data1)
#                 self.countparas(key)
#             self.sinOuttext.emit("已经移除所有文件的前" + str(numstart) + "后" + str(numend) + "个数据点,并更新数据的区间内最值")
#
#     def countparas(self, filename):
#         numstart = self.filelist[filename].cutstartnum1
#         numend = self.filelist[filename].cutendnum1
#         self.filelist[filename].Max = np.max(self.filelist[filename].Pro_Data1[numstart:numend + 1])
#         self.filelist[filename].Min = np.min(self.filelist[filename].Pro_Data1[numstart:numend + 1])
#
#     def countlen(self, x):
#         if type(x) == list:
#             max = 0
#             for str in x:
#                 if (len(str.encode()) > max):
#                     max = len(str.encode())
#             return max + 1
#         else:
#             return len(x.encode()) + 1
#
#     def colnum_string(self, n):
#         div = n + 1
#         string = ""
#         while div > 0:
#             module = (div - 1) % 26
#             string = chr(65 + module) + string
#             div = int((div - module) / 26)
#         return string + ":" + string

class datastruct():
    def __init__(self):
        self.filelist = dict()
        self.Table2selectrow=-1
        self.Table2verticalScrollindex=0
        self.maxCol = 0
        self.filenames = []
        self.dirList = []
        self.filepath = ""
        self.inpath = ""
        self.outpath = ""
        self.imagen1Name = ''
        self.imagen2Name = ''
        self.imagen3Name = ''
        self.imagen4Name = ''
        self.Table2V = ""
        self.Table2H = ""
        self.showcut = 0
        self.featurex = 0
        self.fitweightindex=0
        self.cb1setChecked="True"
        self.cb2setChecked="True"
        self.cb3setChecked="True"
        self.cb4setChecked="True"


        self.fitComboBoxtext=""
        self.cutComboBoxstarttext=""
        self.cutComboBoxendtext=""
        self.b1low = [0.8, 0.1, 0, 0]
        self.b1top = [1.2, 1000, 1000, 1000000]
        self.b2low = [0.8, 0.1, 0]
        self.b2top = [1.2, 1000, 1000000]
        self.currentimage1=""
        self.currentimage2=""
        self.currentimage3=""
        self.currentimage4=""
        self.currentimage5=""


class dataProcess():
    def __init__(self,sinOutpro, sinOuttext,sinOutbool):
        self.data=datastruct()
        # print("init")
        # for f in self.data.filelist:
        #     print(f)
        self.sinOutpro = sinOutpro
        self.sinOuttext = sinOuttext
        self.sinOutbool = sinOutbool

    def readfiles(self, filepath):  # 存入数据
        print("readfile in")
        self.sinOutbool.emit(True)
        self.sinOuttext.emit("正在进行数据转换...")
        self.sinOutpro.emit(0)
        self.data.inpath=filepath
        print("readfile in")
        files = os.listdir(filepath)
        print(files)
        # 排除隐藏文件和文件夹
        for f in files:
            if (os.path.isdir(filepath + '/' + f)):
                # 排除隐藏文件夹。因为隐藏文件夹过多
                if (f[0] == '.'):
                    pass
                else:
                    # 添加非隐藏文件夹
                    self.data.dirList.append(f)
            if (os.path.isfile(filepath + '/' + f)):
                # 添加文件
                if (os.path.splitext(f)[1] == ".txt"):
                    self.data.filenames.append(f)
        p = 1
        # print(self.filenames)
        # print("打印文件")
        # for f in self.data.filenames:
        #     print(f)
        for f in self.data.filenames:
            self.sinOuttext.emit("正在转换 " + str(p) + "/" + str(len(self.data.filenames)) + " " + f)
            data = dataclass()
            data.filepath = filepath
            datarow = open(filepath + '/' + f)  # 读取的整个原始文件数据
            datarowlines = datarow.readlines()  # 读取的整个原始文件的数据，按行分割
            datapar = []  # 真正的每行数据数组
            for line in datarowlines:
                linenew = line.strip()
                if (linenew != ""):
                    datapar.append(linenew)
            # print(datapar)
            # self.ACQ_Time=re.search("(\d{4}-\d{1,2}-\d{1,2}\s*\d{1,2}:\d{1,2}:\d{1,2}:\s*\d{1,3})",datapar[1])
            temptime = re.search("\d{4}-\s*\d{1,2}-\s*\d{1,2}\s*\d{1,2}:\s*\d{1,2}:\s*\d{1,2}.\s*\d{1,3}\s*.",
                                 datapar[1]).group(0)
            # print(temptime)
            # strtemp=temptime[5].split('.')
            # temptime[5]=strtemp[0]
            # temptime.append(strtemp[1])
            timelist = re.split('[- :.]\s*', temptime)
            # print(timelist)

            timestr = timelist[0] + "-" + timelist[1] + "-" + timelist[2] + "  " + timelist[3] + ":" + timelist[
                4] + ":" + timelist[5] + "." + timelist[6]
            data.ACQ_Time = datetime.strptime(timestr, '%Y-%m-%d  %H:%M:%S.%f')
            data.Project = datapar[2].strip(datapar[2].split(": ")[0]).strip(": ")
            data.Name = datapar[3].strip(datapar[3].split(": ")[0]).strip(": ")
            data.part = datapar[4].strip(datapar[4].split(": ")[0]).strip(": ")
            data.Operator = datapar[5].strip(datapar[5].split(": ")[0]).strip(": ")
            data.Desc = datapar[6].strip(datapar[6].split(": ")[0]).strip(": ")
            data.Excited_Peroid = int(datapar[9].strip(datapar[9].split(": ")[0]).strip(": "))
            data.Excited_Time = int(datapar[10].strip(datapar[10].split(": ")[0]).strip(": "))
            data.Acq_Delay_Time = int(datapar[11].strip(datapar[11].split(": ")[0]).strip(": "))
            data.Gate_Time = int(datapar[12].strip(datapar[12].split(": ")[0]).strip(": "))
            data.Count_Num_per_gate = int(datapar[13].strip(datapar[13].split(": ")[0]).strip(": "))
            data.Repeat_Times = int(datapar[14].strip(datapar[14].split(": ")[0]).strip(": "))
            data.Acq_Gate_Times = int(datapar[15].strip(datapar[15].split(": ")[0]).strip(": "))
            data.Interval_per_Gate = int(datapar[16].strip(datapar[16].split(": ")[0]).strip(": "))
            datanum = int(data.Repeat_Times * data.Count_Num_per_gate) #每门数据量（包含重复测量数据）
            data.Pro_Data1 = np.zeros(data.Acq_Gate_Times * data.Count_Num_per_gate).tolist()#不重复情况下所有数据数量（门数*每门测量次数）
            data.Pro_mal1=[[] for i in range(data.Acq_Gate_Times * data.Count_Num_per_gate)]#不重复情况下所有数据数量（门数*每门测量次数）
            # print("okkk")
            # print(datapar[17])
            # print(datapar[17].strip(datapar[17].split(":")[0]).strip(":"))

            #保存原始数据
            if (datapar[17].strip(datapar[17].split(":")[0]).strip(":") == ""):
                # print("进入")
                data.Channel_Number = "1"
                for i in range(18, 18 + datanum * data.Acq_Gate_Times):
                    data.Raw_Data1.append(float(datapar[i]))
                # if (data.Channel_Number == 2):
                #     for i in range(18 + datanum + 1,
                #                    18 + datanum * data.Acq_Gate_Times + 1 + datanum * data.Acq_Gate_Times):
                #         data.Raw_Data2.append(int(datapar[i]))
            else:
                data.Channel_Number = int(datapar[17].strip(datapar[17].split(": ")[0]).strip(": "))
                for i in range(19, 19 + datanum * data.Acq_Gate_Times):
                    data.Raw_Data1.append(float(datapar[i]))
                # if (data.Channel_Number == 2):
                #     for i in range(19 + datanum + 1,
                #                    19 + datanum * data.Acq_Gate_Times + 1 + datanum * data.Acq_Gate_Times):
                #         data.Raw_Data2.append(int(datapar[i]))
            # print(data.ACQ_Time)
            # 计算时间，以分钟为单位
            # minutecount=0
            # timelist=re.split('[- :]\s*',data.ACQ_Time)
            # data1 =timelist[0] + "-" + timelist[1] + "-" + timelist[2] + " " + timelist[3] + ":" + timelist[4] + ":" + timelist[5]
            #
            # year=(float(timelist[0])-2019)*364*24*60
            # mouth=(float(timelist[1])-1)*30.5*24*60
            # day=  (float(timelist[2])-1)*24*
            # print(data)

            # datanum = int(data.Repeat_Times * data.Count_Num_per_gate)
            # datanum=int(data.Repeat_Times*data.Count_Num_per_gate*data.Acq_Gate_Times)
            # print("datanum",datanum)
            # print(datanum/data.Repeat_Times,data.Acq_Gate_Times*data.Count_Num_per_gate)
            # print()
            # data.Pro_Data1 = np.zeros(data.Acq_Gate_Times * data.Count_Num_per_gate).tolist()
            # [0 for i in range(data.Acq_Gate_Times*data.Count_Num_per_gate)]
            # print(data.Gate_Time)
            # print("len(data.Raw_Data1)",len(data.Pro_Data1))
            # print("data.Count_Num_per_gate*data.Gate_Time",data.Count_Num_per_gate*data.Gate_Time)
            #
            # for i in range(19, 19 + datanum * data.Acq_Gate_Times):
            #     data.Raw_Data1.append(int(datapar[i]))
            # if (data.Channel_Number == "2"):
            #     for i in range(19 + datanum + 1,
            #                    19 + datanum * data.Acq_Gate_Times + 1 + datanum * data.Acq_Gate_Times):
            #         data.Raw_Data2.append(int(datapar[i]))
            # print(len(data.Raw_Data1))
            # print(len(data.Raw_Data2))

            #
            dScale = data.Count_Num_per_gate * 1000 / (data.Gate_Time * data.Repeat_Times)
            for i in range(int(data.Acq_Gate_Times)):
                for j in range(int(data.Count_Num_per_gate)):
                    ncps = 0
                    ncpslist = []
                    for k in range(int(data.Repeat_Times)):
                        ncps += data.Raw_Data1[k * data.Count_Num_per_gate + j + i * datanum]   #每秒光子数（50次测量均值）
                        ncpslist.append(data.Raw_Data1[k * data.Count_Num_per_gate + j + i * datanum])
                    data.Pro_mal1[j * data.Acq_Gate_Times + i]=ncpslist
                    data.Pro_Data1[j * data.Acq_Gate_Times + i] = ncps * dScale
            # data.Interval=float((data.Gate_Time)/len(data.Pro_Data1))*data.Count_Num_per_gate*0.001
            data.Interval = float(data.Gate_Time / data.Count_Num_per_gate)
            data.mal1MES=[np.std(tmplist,ddof=1) for tmplist in data.Pro_mal1]
            # print(data.Pro_Data1)

            # print("data.Interval",data.Interval)

            # for i in range(len(data.Pro_Data1)):
            #     data.Pro_Data1_X.append(round(i*data.Interval,5))
            #

            for i in range(int(data.Count_Num_per_gate)):
                for j in range(int(data.Acq_Gate_Times)):
                    data.Pro_Data1_X.append(float(i * data.Interval + j * data.Interval_per_Gate * 0.001))
            # print(data.Interval)
            # print(data.Pro_Data1_X)

            # print(data.Pro_Data1)
            data.Max = np.max(data.Pro_Data1)
            data.Min = np.min(data.Pro_Data1)
            if(data.Max==0):
                self.data.filenames.remove(f)
                continue
            data.cutendnum1 = len(data.Pro_Data1) - 1
            # 复制原始数据到Cut
            data.Cut_Data1 = copy.deepcopy(data.Pro_Data1)
            data.Cut_Data1_X = copy.deepcopy(data.Pro_Data1_X)
            data.Pro_Data1_variety_X = copy.deepcopy(data.Pro_Data1_X)
            if (len(data.Cut_Data1) > self.data.maxCol):
                self.data.maxCol = len(data.Cut_Data1)
            # print("data.Cut_Data1",data.Cut_Data1)
            self.data.filelist[f] = data

            # print(self.filelist[f].Pro_Data1)
            self.sinOutpro.emit(p / len(self.data.filenames) * 100)

            p += 1
            self.sinOuttext.emit("完成！")
        self.sinOutbool.emit(False)
        self.sinOuttext.emit("数据转换成功！")
        return self.data

    def readsinglefile(self,filepath,filename):
        self.sinOuttext.emit("正在读取文件...")

        data = dataclass()
        data.filepath = filepath
        datarow = open(filepath + '/' + filename)  # 读取的整个原始文件数据
        datarowlines = datarow.readlines()  # 读取的整个原始文件的数据，按行分割
        datapar = []  # 真正的每行数据数组
        for line in datarowlines:
            linenew = line.strip()
            if (linenew != ""):
                datapar.append(linenew)

        temptime = re.search("\d{4}-\s*\d{1,2}-\s*\d{1,2}\s*\d{1,2}:\s*\d{1,2}:\s*\d{1,2}.\s*\d{1,3}\s*.",
                             datapar[1]).group(0)

        timelist = re.split('[- :.]\s*', temptime)

        timestr = timelist[0] + "-" + timelist[1] + "-" + timelist[2] + "  " + timelist[3] + ":" + timelist[
            4] + ":" + timelist[5] + "." + timelist[6]
        data.ACQ_Time = datetime.strptime(timestr, '%Y-%m-%d  %H:%M:%S.%f')
        data.Project = datapar[2].strip(datapar[2].split(": ")[0]).strip(": ")
        data.Name = datapar[3].strip(datapar[3].split(": ")[0]).strip(": ")
        data.part = datapar[4].strip(datapar[4].split(": ")[0]).strip(": ")
        data.Operator = datapar[5].strip(datapar[5].split(": ")[0]).strip(": ")
        data.Desc = datapar[6].strip(datapar[6].split(": ")[0]).strip(": ")
        data.Excited_Peroid = int(datapar[9].strip(datapar[9].split(": ")[0]).strip(": "))
        data.Excited_Time = int(datapar[10].strip(datapar[10].split(": ")[0]).strip(": "))
        data.Acq_Delay_Time = int(datapar[11].strip(datapar[11].split(": ")[0]).strip(": "))
        data.Gate_Time = int(datapar[12].strip(datapar[12].split(": ")[0]).strip(": "))
        data.Count_Num_per_gate = int(datapar[13].strip(datapar[13].split(": ")[0]).strip(": "))
        data.Repeat_Times = int(datapar[14].strip(datapar[14].split(": ")[0]).strip(": "))
        data.Acq_Gate_Times = int(datapar[15].strip(datapar[15].split(": ")[0]).strip(": "))
        data.Interval_per_Gate = int(datapar[16].strip(datapar[16].split(": ")[0]).strip(": "))
        datanum = int(data.Repeat_Times * data.Count_Num_per_gate)  # 每门数据量（包含重复测量数据）
        data.Pro_Data1 = np.zeros(data.Acq_Gate_Times * data.Count_Num_per_gate).tolist()  # 不重复情况下所有数据数量（门数*每门测量次数）
        data.Pro_mal1 = np.zeros(data.Acq_Gate_Times * data.Count_Num_per_gate).tolist()  # 不重复情况下所有数据数量（门数*每门测量次数）


        # 保存原始数据
        if (datapar[17].strip(datapar[17].split(":")[0]).strip(":") == ""):
            # print("进入")
            data.Channel_Number = "1"
            for i in range(18, 18 + datanum * data.Acq_Gate_Times):
                data.Raw_Data1.append(float(datapar[i]))

        else:
            data.Channel_Number = int(datapar[17].strip(datapar[17].split(": ")[0]).strip(": "))
            for i in range(19, 19 + datanum * data.Acq_Gate_Times):
                data.Raw_Data1.append(float(datapar[i]))

        dScale = data.Count_Num_per_gate * 1000 / (data.Gate_Time * data.Repeat_Times)
        for i in range(int(data.Acq_Gate_Times)):
            for j in range(int(data.Count_Num_per_gate)):
                ncps = 0
                ncpslist = []
                for k in range(int(data.Repeat_Times)):
                    ncps += data.Raw_Data1[k * data.Count_Num_per_gate + j + i * datanum]  # 每秒光子数（50次测量均值）
                    ncpslist.append(data.Raw_Data1[k * data.Count_Num_per_gate + j + i * datanum])
                data.Pro_mal1[j * data.Acq_Gate_Times + i] = ncpslist
                data.Pro_Data1[j * data.Acq_Gate_Times + i] = ncps * dScale
        # data.Interval=float((data.Gate_Time)/len(data.Pro_Data1))*data.Count_Num_per_gate*0.001
        data.Interval = float(data.Gate_Time / data.Count_Num_per_gate)
        data.mal1MES = [np.std(tmplist, ddof=1) for tmplist in data.Pro_mal1]
        # print(data.Pro_Data1)

        # print("data.Interval",data.Interval)

        # for i in range(len(data.Pro_Data1)):
        #     data.Pro_Data1_X.append(round(i*data.Interval,5))
        #

        for i in range(int(data.Count_Num_per_gate)):
            for j in range(int(data.Acq_Gate_Times)):
                data.Pro_Data1_X.append(float(i * data.Interval + j * data.Interval_per_Gate * 0.001))
        # print(data.Interval)
        # print(data.Pro_Data1_X)

        # print(data.Pro_Data1)
        data.Max = np.max(data.Pro_Data1)
        data.Min = np.min(data.Pro_Data1)
        if (data.Max == 0):
            self.sinOuttext.emit("数据最大值=0 读取失败！")
            return
        data.cutendnum1 = len(data.Pro_Data1) - 1
        # 复制原始数据到Cut
        data.Cut_Data1 = copy.deepcopy(data.Pro_Data1)
        data.Cut_Data1_X = copy.deepcopy(data.Pro_Data1_X)
        data.Pro_Data1_variety_X = copy.deepcopy(data.Pro_Data1_X)
        if (len(data.Cut_Data1) > self.data.maxCol):
            self.data.maxCol = len(data.Cut_Data1)
        # print("data.Cut_Data1",data.Cut_Data1)
        self.data.filenames.append(filename)
        self.data.filelist[filename] = data
        self.sinOuttext.emit("文件读取成功！")

    def getMeanData(self):
        # newdata = dataclass()
        self.sinOuttext.emit("正在计算...")
        print(os.path.split(self.data.inpath)[1] + "-整体均值数据")
        if 'error'!=self.data.filelist.pop(os.path.split(self.data.inpath)[1] + "-整体均值数据",'error'):
            self.data.filenames.remove(os.path.split(self.data.inpath)[1] + "-整体均值数据")
        if(len(self.data.filelist)==0):
            self.sinOuttext.emit("数据总数为0，无法计算！")
            return
        for i in range(len(self.data.filenames)):
            if(len(self.data.filelist[self.data.filenames[i]].Pro_Data1)!=len(self.data.filelist[self.data.filenames[i]].Pro_Data1)):
                self.sinOuttext.emit("数据格式不统一，无法计算！")
                return

        standarddata = self.data.filelist[self.data.filenames[0]]
        datagroup=[[] for i in range(len(standarddata.Pro_Data1))]

        for key,data in self.data.filelist.items():
            for i in range(standarddata.Acq_Gate_Times):
                startindex=i*standarddata.Repeat_Times*standarddata.Count_Num_per_gate
                endindex=(i+1)*standarddata.Repeat_Times*standarddata.Count_Num_per_gate
                datagroup[i].extend(data.Raw_Data1[startindex:endindex])
        txtdata=[]
        for data in datagroup:
            txtdata.extend(data)

        new_filename=os.path.split(self.data.inpath)[1]+"-整体均值数据"
        #生成txt文件
        try:
            with open(self.data.inpath+"/"+new_filename+".txt", "w") as file:  # ”w"代表着每次运行都覆盖内容
                file.write("Project Info:" + "\n\n")
                file.write("    ACQ Time: " +datetime.now().strftime('%Y-%m-%d  %H:%M:%S.%f .')+ "\n\n")
                file.write("    Project: " + new_filename+"\n\n")
                file.write("    Name: " + str(standarddata.Name)+"\n\n")
                file.write("    Part: " + str(standarddata.part)+"\n\n")
                file.write("    Operator:  " +str(standarddata.Operator)+ "\n\n")
                file.write("    Desc.:  " +str(standarddata.Desc)+ "\n\n")
                file.write("    Sample Data Acquired."+"\n\n\n\n")
                file.write("ACQ Parameters:" + "\n\n")
                file.write("    Excited Peroid(ms): " +str(standarddata.Excited_Peroid)+ "\n\n")
                file.write("    Excited Time(ms): " +str(standarddata.Excited_Time)+ "\n\n")
                file.write("    Acq Delay Time(us): " +str(standarddata.Acq_Delay_Time)+ "\n\n")
                file.write("    Gate Time(ms): " +str(standarddata.Gate_Time)+ "\n\n")
                file.write("    Count Num per gate: " +str(standarddata.Count_Num_per_gate)+ "\n\n")
                file.write("    Repeat Times: " +str(standarddata.Repeat_Times*len(self.data.filelist))+ "\n\n")
                file.write("    Acq Gate Times: " +str(standarddata.Acq_Gate_Times)+ "\n\n")
                file.write("    Interval per Gate(us): " +str(standarddata.Interval_per_Gate)+ "\n\n")
                file.write("    Channel Number: " +str(standarddata.Channel_Number)+ "\n\n\n\n")
                file.write("Data:\n\n")
                for i in range(len(txtdata)):
                    file.write("    "+str(int(txtdata[i]))+"\n\n")
        except Exception as e:
            self.sinOuttext.emit("均值文件导出失败！(文件被占用，请关闭关闭文件后重试)")







        # #生成结构
        # newdata=copy.deepcopy(self.data.filelist[self.data.filenames[0]])
        # newdata.Repeat_Times=self.data.filelist[self.data.filenames[0]].Repeat_Times*len(self.data.filelist)
        # newdata.mal1MES=[None] * len(self.data.filelist[self.data.filenames[0]].Pro_Data1)
        # newdata.Pro_mal1=[None] * len(self.data.filelist[self.data.filenames[0]].Pro_Data1)
        # for i in range(len(self.data.filelist[self.data.filenames[0]].Pro_Data1)): #数据点数
        #     Pro_Data1_tmp = []
        #     for j in range(len(self.data.filenames)):
        #         Pro_Data1_tmp.extend(self.data.filelist[self.data.filenames[j]].Pro_mal1[i])
        #         print(i)
        #     newdata.ACQ_Time=datetime.now()
        #     newdata.Pro_Data1[i]=np.mean(Pro_Data1_tmp)*newdata.Count_Num_per_gate * 1000 / (newdata.Gate_Time)
        #     newdata.mal1MES[i] = np.std(Pro_Data1_tmp, ddof=1)
        #     newdata.Pro_mal1[i]=Pro_Data1_tmp
        #     # data.Pro_Data1[i]=np.mean([self.data.filelist[self.data.filenames[j]].Pro_Data1[i] for j in range(len(self.data.filenames))])
        # newdata.Max = np.max(newdata.Pro_Data1)
        # newdata.Min = np.min(newdata.Pro_Data1)
        # newdata.Cut_Data1 = copy.deepcopy(newdata.Pro_Data1)
        # newdata.Cut_Data1_X = copy.deepcopy(newdata.Pro_Data1_X)
        # newdata.Pro_Data1_variety_X = copy.deepcopy(newdata.Pro_Data1_X)
        # self.data.filenames.append(os.path.split(self.data.inpath)[1]+"-整体均值数据")
        # self.data.filelist[os.path.split(self.data.inpath)[1]+"-整体均值数据"] = newdata
        self.readsinglefile(self.data.inpath,new_filename+".txt")

        self.sinOuttext.emit("整体均值数据计算成功！即将进行拟合操作...")

    def Fitting(self,funtype, method, startnum, endnum, filename, b1low, b1top, b2low, b2top,fitweightindex):

        # self.sinOuttext=sinOuttext
        # self.sinOupro=sinOutpro
        print(b1low, b1top, b2low, b2top)
        b1low = [float(i) for i in b1low]
        b1top = [float(i) for i in b1top]
        b2low = [float(i) for i in b2low]
        b2top = [float(i) for i in b2top]

        # b1low=[0.8,0.1,0,0]
        # b1top=[1.2,1000,1000,10000]
        # b2low=[0.8,0.1,0]
        # b2top=[1.2, 1000, 10000]
        param_bounds1 = ([0, 1, 0, 0], [9999999999, 100, 100, 10000])
        param_bounds2 = ([0, 1, 0], [999999999, 9999999999, 9999999999])
        param_bounds3 = ([0, 0, 0, 0], [np.inf, np.inf, np.inf, np.inf])
        param_bounds4 = ([0, 0, 0], [np.inf, np.inf, np.inf])
        Interval=0

        def count_error(funtype,datax,data,ytempfit,popt,sigma=[]):
            # if sigma==[]:
            #     sigma=np.ones(shape=(len(data)))
            if funtype==1:
                # return[1,1,1,1]
                # weight = 1 / data
                s1, s2, s3, s4, x = symbols('s1 s2 s3 s4 x', real=True)
                f1 = (s1 * ((1 + (x / s2)) ** (-s3)) + s4)
                paradata, ailist, bilist, cilist, dilist, Nilist = [],[],[],[],[],[]
                for i in range(len(data)):
                    ailist.append(diff(f1, s1).subs({s1: popt[0], s2: popt[1], s3: popt[2], s4: popt[3], x: datax[i]}))
                    bilist.append(diff(f1, s2).subs({s1: popt[0], s2: popt[1], s3: popt[2], s4: popt[3], x: datax[i]}))
                    cilist.append(diff(f1, s3).subs({s1: popt[0], s2: popt[1], s3: popt[2], s4: popt[3], x: datax[i]}))
                    dilist.append(diff(f1, s4).subs({s1: popt[0], s2: popt[1], s3: popt[2], s4: popt[3], x: datax[i]}))
                    Nilist.append((fun1(datax[i], popt[0], popt[1], popt[2], popt[3]) - data[i])**2*sigma[i])
                paradata.append(ailist)
                paradata.append(bilist)
                paradata.append(cilist)
                paradata.append(dilist)

                m = np.zeros(shape=(len(popt), len(popt)))
                # v = np.zeros(shape=(len(popt)))
                for i in range(len(popt)):
                    for j in range(len(popt)):
                        for k in range(len(data)):
                            m[i, j] += paradata[i][k] * paradata[j][k] * sigma[k]

                m2 = np.linalg.inv(m)

                alpha = (1 - 0.95) / 2
                tinv = -t.ppf(alpha, len(data) - len(popt))
                res = []

                sse = 0
                for tmp in Nilist:
                    sse += tmp
                sse = sse / (len(data) - len(popt))

                for i in range(len(popt)):
                    res.append(np.sqrt(sse * m2[i, i]) * tinv)

            elif funtype==2:
                # return [1, 1, 1]
                s1, s2, s3, x = symbols('s1 s2 s3 x', real=True)
                f1 = (s1 * (sympy.exp(-(x / s2))) + s3)
                paradata, ailist, bilist, cilist, Nilist = [], [], [], [], []
                for i in range(len(data)):
                    ailist.append(diff(f1, s1).subs({s1: popt[0], s2: popt[1], s3: popt[2], x: datax[i]}))
                    bilist.append(diff(f1, s2).subs({s1: popt[0], s2: popt[1], s3: popt[2], x: datax[i]}))
                    cilist.append(diff(f1, s3).subs({s1: popt[0], s2: popt[1], s3: popt[2], x: datax[i]}))
                    Nilist.append((fun2(datax[i], popt[0], popt[1], popt[2]) - data[i])**2*sigma[i])
                paradata.append(ailist)
                paradata.append(bilist)
                paradata.append(cilist)

                m = np.zeros(shape=(len(popt), len(popt)))
                # v = np.zeros(shape=(len(popt)))
                for i in range(len(popt)):
                    for j in range(len(popt)):
                        for k in range(len(data)):
                            m[i, j] += paradata[i][k] * paradata[j][k]*sigma[k]

                m2 = np.linalg.inv(m)

                alpha = (1 - 0.95) / 2
                tinv = -t.ppf(alpha, len(data) - len(popt))
                res = []

                sse=0
                for tmp in Nilist:
                    sse += tmp
                sse=sse/(len(data) - len(popt))

                for i in range(len(popt)):
                    res.append(np.sqrt(sse * m2[i, i]) * tinv)


            elif funtype==3:
                # return [1, 1, 1, 1]
                s1, s2, s3, s4, x = symbols('s1 s2 s3 s4 x', real=True)
                temp1spot = (1 / (1 + x / s2)) ** (s3 - 1)
                temp2spot = (1 / (1 + (x + Interval) / s2)) ** (s3 - 1)
                f1 = (s1 * s2 * (1 / (s3 - 1)) * (temp1spot - temp2spot) + s4 * Interval)/(Interval)

                paradata, ailist, bilist, cilist, dilist, Nilist = [], [], [], [], [], []
                for i in range(len(data)):
                    ailist.append(
                        diff(f1, s1).subs({s1: popt[0], s2: popt[1], s3: popt[2], s4: popt[3], x: datax[i]}))
                    bilist.append(
                        diff(f1, s2).subs({s1: popt[0], s2: popt[1], s3: popt[2], s4: popt[3], x: datax[i]}))
                    cilist.append(
                        diff(f1, s3).subs({s1: popt[0], s2: popt[1], s3: popt[2], s4: popt[3], x: datax[i]}))
                    dilist.append(
                        diff(f1, s4).subs({s1: popt[0], s2: popt[1], s3: popt[2], s4: popt[3], x: datax[i]}))
                    Nilist.append((fun3(datax[i], popt[0], popt[1], popt[2], popt[3]) - data[i]) ** 2 * sigma[i])
                paradata.append(ailist)
                paradata.append(bilist)
                paradata.append(cilist)
                paradata.append(dilist)

                m = np.zeros(shape=(len(popt), len(popt)))
                # v = np.zeros(shape=(len(popt)))
                for i in range(len(popt)):
                    for j in range(len(popt)):
                        for k in range(len(data)):
                            m[i, j] += paradata[i][k] * paradata[j][k] * sigma[k]

                m2 = np.linalg.inv(m)

                alpha = (1 - 0.95) / 2
                tinv = -t.ppf(alpha, len(data) - len(popt))
                res = []

                sse = 0
                for tmp in Nilist:
                    sse += tmp
                sse = sse / (len(data) - len(popt))

                for i in range(len(popt)):
                    res.append(np.sqrt(sse * m2[i, i]) * tinv)

            elif funtype==4:
                # return [1, 1, 1]
                s1, s2, s3, x = symbols('s1 s2 s3 x', real=True)
                temp1spot = sympy.exp(-x / s2)
                temp2spot = sympy.exp(-(x + Interval) / s2)
                f1 = (s1 * s2 * (temp1spot - temp2spot) + s3 * Interval)/(Interval)
                paradata, ailist, bilist, cilist, Nilist = [], [], [], [], []
                for i in range(len(data)):
                    ailist.append(diff(f1, s1).subs({s1: popt[0], s2: popt[1], s3: popt[2], x: datax[i]}))
                    bilist.append(diff(f1, s2).subs({s1: popt[0], s2: popt[1], s3: popt[2], x: datax[i]}))
                    cilist.append(diff(f1, s3).subs({s1: popt[0], s2: popt[1], s3: popt[2], x: datax[i]}))
                    Nilist.append((fun4(datax[i], popt[0], popt[1], popt[2]) - data[i]) ** 2 * sigma[i])
                paradata.append(ailist)
                paradata.append(bilist)
                paradata.append(cilist)

                m = np.zeros(shape=(len(popt), len(popt)))
                # v = np.zeros(shape=(len(popt)))
                for i in range(len(popt)):
                    for j in range(len(popt)):
                        for k in range(len(data)):
                            m[i, j] += paradata[i][k] * paradata[j][k] * sigma[k]

                m2 = np.linalg.inv(m)

                alpha = (1 - 0.95) / 2
                tinv = -t.ppf(alpha, len(data) - len(popt))
                res = []

                sse = 0
                for tmp in Nilist:
                    sse += tmp
                sse = sse / (len(data) - len(popt))

                for i in range(len(popt)):
                    res.append(np.sqrt(sse * m2[i, i]) * tinv)

            print("res", res)
            return res



        # def count_error2(funtype, datax, data, ytempfit, popt, sigma=[]):
        #         # if sigma==[]:
        #         #     sigma=np.ones(shape=(len(data)))
        #     if funtype == 1:
        #         # weight = 1 / data
        #         s1, s2, s3, s4, x = symbols('s1 s2 s3 s4 x', real=True)
        #         f1 = s1 * ((1 + (x / s2)) ** (-s3)) + s4
        #         paradata, ailist, bilist, cilist, dilist, Nilist = [], [], [], [], [], []
        #         for i in range(len(data)):
        #             ailist.append(
        #                 diff(f1, s1).subs({s1: popt[0], s2: popt[1], s3: popt[2], s4: popt[3], x: datax[i]}))
        #             bilist.append(
        #                 diff(f1, s2).subs({s1: popt[0], s2: popt[1], s3: popt[2], s4: popt[3], x: datax[i]}))
        #             cilist.append(
        #                 diff(f1, s3).subs({s1: popt[0], s2: popt[1], s3: popt[2], s4: popt[3], x: datax[i]}))
        #             dilist.append(
        #                 diff(f1, s4).subs({s1: popt[0], s2: popt[1], s3: popt[2], s4: popt[3], x: datax[i]}))
        #             Nilist.append((fun1(datax[i], popt[0], popt[1], popt[2], popt[3]) - data[i]) ** 2 * sigma[i])
        #         paradata.append(ailist)
        #         paradata.append(bilist)
        #         paradata.append(cilist)
        #         paradata.append(dilist)
        #
        #         print("sigma:", sigma)
        #         print(ailist, bilist, cilist)
        #         m = np.zeros(shape=(len(popt), len(popt)))
        #         v = np.zeros(shape=(len(popt)))
        #         for i in range(len(popt)):
        #             for j in range(len(popt)):
        #                 for k in range(len(data)):
        #                     # m[i, j] += paradata[i][k] * paradata[j][k]
        #                     m[i, j] += paradata[i][k] * paradata[j][k] / sigma[k]
        #
        #         m2 = np.linalg.inv(m)
        #
        #         sse = 0
        #         for tmp in Nilist:
        #             sse += tmp
        #
        #         alpha = (1 - 0.95) / 2
        #         tinv = -t.ppf(alpha, len(data) - len(popt))
        #         res = []
        #
        #         for i in range(len(popt)):
        #             res.append(np.sqrt(sse * m2[i, i]) * tinv)
        #     elif funtype == 2:
        #         s1, s2, s3, x = symbols('s1 s2 s3 x', real=True)
        #         f1 = s1 * (sympy.exp(-(x / s2))) + s3
        #         paradata, ailist, bilist, cilist, Nilist = [], [], [], [], []
        #         for i in range(len(data)):
        #             ailist.append(diff(f1, s1).subs({s1: popt[0], s2: popt[1], s3: popt[2], x: datax[i]}))
        #             bilist.append(diff(f1, s2).subs({s1: popt[0], s2: popt[1], s3: popt[2], x: datax[i]}))
        #             cilist.append(diff(f1, s3).subs({s1: popt[0], s2: popt[1], s3: popt[2], x: datax[i]}))
        #             Nilist.append((fun2(datax[i], popt[0], popt[1], popt[2]) - data[i]) ** 2 * sigma[i])
        #         paradata.append(ailist)
        #         paradata.append(bilist)
        #         paradata.append(cilist)
        #
        #         m = np.zeros(shape=(len(popt), len(popt)))
        #         v = np.zeros(shape=(len(popt)))
        #         for i in range(len(popt)):
        #             for j in range(len(popt)):
        #                 for k in range(len(data)):
        #                     m[i, j] += paradata[i][k] * paradata[j][k] / sigma[k]
        #
        #         m2 = np.linalg.inv(m)
        #
        #         alpha = (1 - 0.95) / 2
        #         tinv = -t.ppf(alpha, len(data) - len(popt))
        #         res = []
        #
        #         sse = 0
        #         for tmp in Nilist:
        #             sse += tmp
        #         sse = sse / (len(data) - len(popt))
        #
        #         for i in range(len(popt)):
        #             res.append(np.sqrt(sse * m2[i, i]) * tinv)
        #     elif funtype == 3:
        #         return[1,1,1,1]
        #     elif funtype == 4:
        #         return [1, 1, 1]
        #     print("res", res)
        #     return res



        def getIndexes(y_predict, y_data,sigmaerror,dfe):
            y_predict = np.array(y_predict)
            y_data = np.array(y_data)
            sigmaerror = np.array(sigmaerror)
            n = y_data.size

            ybar = sum(y_data* sigmaerror) / sum(sigmaerror)
            sst = sum(sigmaerror*(y_data- ybar)**2)

            ssetmp1=(y_predict - y_data)
            ssetmp2=(y_predict - y_data)**2
            ssetmp3=((y_predict - y_data)**2)* sigmaerror
            ssetmp4=sum( ((y_predict - y_data)**2)* sigmaerror)

            sse=sum( ((y_predict - y_data)**2)* sigmaerror)
            # sse=sum( ((y_predict - y_data)**2)* sigmaerror)/dfe
            rsquare = 1 - sse / sst
            adjrsquare = 1 - (1 - rsquare) * (y_data.size - 1) / dfe
            mse = sse / dfe
            rmse = math.sqrt(mse)
            return [rsquare, sse, mse, rmse]

            # for tmp in Nilist:
            #         sse += tmp
            #     sse = sse / (len(data) - len(popt))
            # # SSE为和方差
            # SSE = (((y_data - y_predict)*sigmaerror) ** 2).sum()
            # # MSE为均方差
            # MSE = SSE / n
            # # RMSE为均方根,越接近0，拟合效果越好
            # RMSE = np.sqrt(MSE)
            #
            # # 求R方，0<=R<=1，越靠近1,拟合效果越好
            # u = y_data.mean()
            # SST = ((y_data - u) ** 2).sum()
            # SSR = SST - SSE
            # R_square = SSR / SST
            # return [R_square, SSE, MSE, RMSE]


        def count_variety_X(ytempfit,Interval,funtype,popt):
            if funtype==3:
                x=[]
                for y in ytempfit:
                    x.append(y)


        def fun1(x, s1, s2, s3, s4):
            # return s1 * ((1 + (x / s2)) ** (-s3)) + s4
            return (s1 * ((1 + (x / s2)) ** (-s3)) + s4)
            # return (s1 * ((1 + (x / s2)) ** (-s3)) + s4)/(Interval*0.0001)

        def fun2(x, s1, s2, s3):
            return (s1 * (np.exp(-(x / s2))) + s3)
            # return (s1 * (np.exp(-(x / s2))) + s3)/(Interval*0.0001)

        def fun3(x, s1, s2, s3, s4):
            # print("Interval:",Interval)
            temp1spot = (1 / (1 + np.asarray(x) / s2)) ** (s3 - 1)
            temp2spot = (1 / (1 + (np.asarray(x) + Interval) / s2)) ** (s3 - 1)
            # tmp1=temp1spot - temp2spot
            # tmp2=s1 * s2 * (1 / (s3 - 1)) * (temp1spot - temp2spot)
            # tmp3=(s1 * s2 * (1 / (s3 - 1)) * (temp1spot - temp2spot) + s4 * Interval)
            # tmp4=(s1 * s2 * (1 / (s3 - 1)) * (temp1spot - temp2spot) + s4 * Interval) / Interval
            # yfitspot = (s1 * s2 * (1 / (s3 - 1)) * (temp1spot - temp2spot) + s4 * Interval) / Interval


            yfitspot = (s1 * s2 * (1 / (s3 - 1)) * (temp1spot - temp2spot) + s4 * Interval)/Interval
            # yfitspot = (s1 * s2 * (1 / (s3 - 1)) * (temp1spot - temp2spot) + s4 * Interval)*(Interval)
            return yfitspot
            # v, err = integrate.quad(fun1, x, x+Interval, args=(s1, s2, s3, s4))
            # # return yfitspot
            # print(v)
            # return v

        def fun4(x, s1, s2, s3):
            temp1spot = np.exp(-np.asarray(x) / s2)
            temp2spot = np.exp(-(np.asarray(x) + Interval) / s2)
            yfitspot = (s1 * s2 * (temp1spot - temp2spot) + s3 * Interval)/Interval
            # yfitspot = (s1 * s2 * (temp1spot - temp2spot) + s3 * Interval)*(Interval)
            return yfitspot

        self.sinOutbool.emit(True)
        self.sinOutpro.emit(0)
        if (filename == ""):

            p = 1
            for key, value in self.data.filelist.items():
                if startnum >= len(value.Pro_Data1) - 2:
                    startnum = len(value.Pro_Data1) - 2
                if endnum >= len(value.Pro_Data1) - 2:
                    endnum = len(value.Pro_Data1) - 2
                starttruenum = startnum
                endtruenum = len(value.Pro_Data1) - endnum - 1
                x = value.Pro_Data1_X[starttruenum:endtruenum + 1]
                y = value.Pro_Data1[starttruenum:endtruenum + 1]
                if fitweightindex==0:
                    sigmafit = np.ones(shape=(len(y)))
                    sigmaerror = np.ones(shape=(len(y)))
                elif fitweightindex==1:
                    sigmafit=[np.sqrt(1/999999999999) if tmp==0 else np.sqrt(tmp) for tmp in y]
                    sigmaerror=[999999999999 if tmp==0 else 1/tmp for tmp in y]
                else:
                    sigmafit=[np.sqrt(1/999999999999) if tmp==0 else np.sqrt(tmp)  for tmp in value.mal1MES[starttruenum:endtruenum + 1]]
                    sigmaerror=[999999999999 if tmp==0 else 1/tmp for tmp in value.mal1MES[starttruenum:endtruenum + 1]]
                Max = np.max(value.Pro_Data1[starttruenum:endtruenum + 1])
                Min = np.min(value.Pro_Data1[starttruenum:endtruenum + 1])
                Interval = value.Interval
                # print("value.Pro_Data1",value.Pro_Data1)
                # print("x:",x)
                # print("y:",y)
                # value.Cut_Data1fit_X = np.linspace(value.Pro_Data1_X[starttruenum],value.Pro_Data1_X[endtruenum], 1000).tolist()
                xfit = np.linspace(value.Pro_Data1_X[starttruenum], value.Pro_Data1_X[endtruenum], 1000).tolist()
                if (funtype == 1):
                    self.sinOuttext.emit("正在进行双曲线拟合 " + str(p) + "/" + str(len(self.data.filenames)) + " " + key)
                    try:
                        # print("双曲")
                        # print(b1low[0]*Max,b1low[1],b1low[2],b1low[3])
                        # print(b1top[0]*Max,b1top[1],b1top[2],b1top[3])
                        # print("Max", Max)
                        # popt, pcov = curve_fit(fun1, x, y,maxfev=500000000000, bounds=([b1low[0] * Max, b1low[1], b1low[2], b1low[3]], [b1top[0] * Max, b1top[1], b1top[2], b1top[3]]))
                        popt, pcov = curve_fit(fun1, x, y,sigma=sigmafit,absolute_sigma=True, maxfev=500000000, bounds=([b1low[0] * Max, b1low[1], b1low[2], b1low[3]], [b1top[0] * Max, b1top[1], b1top[2], b1top[3]]),method=method)
                        # print(y)
                        # print(sigmay)
                    except Exception as a:
                        print(a)
                        popt=[1,1,1,1]
                    yfit = [fun1(tmp, popt[0], popt[1], popt[2], popt[3]) for tmp in xfit]
                    ytempfit = [fun1(tmp, popt[0], popt[1], popt[2], popt[3]) for tmp in x]
                    R2 = getIndexes(ytempfit, y,sigmaerror,(len(y) - len(popt)))
                    isexist = 0
                    # print(value.paras["双曲线拟合"])
                    if (value.paras["双曲线拟合"] != []):
                        for i in range(len(value.paras["双曲线拟合"])):
                            if ((value.paras["双曲线拟合"][i].cutstartnum1 == starttruenum) and (
                                    value.paras["双曲线拟合"][i].cutendnum1 == endtruenum))and(value.paras["双曲线拟合"][i].fitweightindex==fitweightindex):
                                tmpvalue = value.paras["双曲线拟合"].pop(i)
                                tmpvalue.para = popt
                                tmpvalue.para_error = count_error(funtype,x,y,ytempfit,popt,sigmaerror)
                                tmpvalue.method = method
                                tmpvalue.yfit = ytempfit
                                tmpvalue.fity = yfit
                                tmpvalue.fitx = xfit
                                tmpvalue.R2 = R2
                                value.paras["双曲线拟合"].append(tmpvalue)
                                isexist = 1
                                break
                    if (isexist == 0):
                        cutdata = cutclass()
                        cutdata.cutstartnum1 = starttruenum
                        cutdata.cutendnum1 = endtruenum
                        cutdata.cutstartnumspot1 = startnum
                        cutdata.cutendnumspot1 = endnum
                        cutdata.funtype = funtype
                        cutdata.method = method
                        cutdata.fitx = xfit
                        cutdata.fity = yfit
                        cutdata.yfit = ytempfit
                        cutdata.para = popt
                        cutdata.para_error=count_error(funtype,x,y,ytempfit,popt,sigmaerror)
                        cutdata.R2 = R2
                        cutdata.Max = Max
                        cutdata.Min = Min
                        cutdata.fitweightindex = fitweightindex
                        value.paras["双曲线拟合"].append(cutdata)

                    # value.Cut_Data1fit = fun1(value.Cut_Data1fit_X, popt[0], popt[1], popt[2], popt[3])
                elif (funtype == 2):
                    # print(key)
                    self.sinOuttext.emit("正在进行指数拟合 " + str(p) + "/" + str(len(self.data.filenames)) + " " + key)
                    #
                    # print(x)
                    # print(y)
                    try:
                        # print("指数")
                        # print(b2low[0]*Max,b2low[1],b2low[2])
                        # print(b2top[0]*Max,b2top[1],b2top[2])
                        popt, pcov = curve_fit(fun2, x, y,sigma=sigmafit,absolute_sigma=True, maxfev=50000000, bounds=(
                        [b2low[0] * Max, b2low[1], b2low[2]], [b2top[0] * Max, b2top[1], b2top[2]]), method=method)
                        # print("Max",Max)

                    except Exception as a:
                        print(a)
                        popt = [1, 1, 1]

                    yfit = [fun2(tmp, popt[0], popt[1], popt[2]) for tmp in xfit]
                    ytempfit = [fun2(tmp, popt[0], popt[1], popt[2]) for tmp in x]
                    R2 = getIndexes(ytempfit, y,sigmaerror,(len(y) - len(popt)))
                    isexist = 0
                    if (value.paras["指数拟合"] != []):
                        for i in range(len(value.paras["指数拟合"])):
                            if ((value.paras["指数拟合"][i].cutstartnum1 == starttruenum) and (
                                    value.paras["指数拟合"][i].cutendnum1 == endtruenum)and(value.paras["指数拟合"][i].fitweightindex==fitweightindex)):
                                tmpvalue = value.paras["指数拟合"].pop(i)
                                tmpvalue.para = popt
                                tmpvalue.para_error = count_error(funtype,x,y,ytempfit,popt,sigmaerror)
                                tmpvalue.method = method
                                tmpvalue.yfit = ytempfit
                                tmpvalue.fity = yfit
                                tmpvalue.fitx = xfit
                                tmpvalue.R2 = R2
                                value.paras["指数拟合"].append(tmpvalue)

                                isexist = 1
                                break
                    if (isexist == 0):
                        cutdata = cutclass()
                        cutdata.cutstartnum1 = starttruenum
                        cutdata.cutendnum1 = endtruenum
                        cutdata.cutstartnumspot1 = startnum
                        cutdata.cutendnumspot1 = endnum
                        cutdata.funtype = funtype
                        cutdata.method = method
                        cutdata.fitx = xfit
                        cutdata.fity = yfit
                        cutdata.yfit = ytempfit
                        cutdata.para = popt
                        cutdata.para_error = count_error(funtype,x,y,ytempfit,popt,sigmaerror)
                        cutdata.R2 = R2
                        cutdata.Max = np.max(value.Pro_Data1[starttruenum:endtruenum + 1])
                        cutdata.Min = np.min(value.Pro_Data1[starttruenum:endtruenum + 1])
                        cutdata.fitweightindex = fitweightindex
                        value.paras["指数拟合"].append(cutdata)

                    # value.Cut_Data1fit = fun2(value.Cut_Data1fit_X, popt[0], popt[1], popt[2])
                elif (funtype == 3):
                    self.sinOuttext.emit("正在进行双曲线积分拟合 " + str(p) + "/" + str(len(self.data.filenames)))
                    try:
                        # print("指数")
                        # print(b1low[0] * Max, b1low[1], b1low[2], b1low[3],b1top[0] * Max*10, b1top[1]*10, b1top[2]*10, b1top[3]*10)
                        # print(b2top[0]*Max,b2top[1],b2top[2])
                        popt, pcov = curve_fit(fun3, x, y,sigma=sigmafit,absolute_sigma=True,maxfev=500000000, bounds=([b1low[0] * Max, b1low[1], b1low[2], b1low[3]], [b1top[0] * Max, b1top[1], b1top[2], b1top[3]]),method=method)
                        # popt, pcov = curve_fit(fun3, x, y,sigma=sigmafit,absolute_sigma=True,maxfev=500000000, bounds=([b1low[0] * Max/Interval, b1low[1], b1low[2], b1low[3]], [b1top[0] * Max/Interval, b1top[1], b1top[2], b1top[3]]),method=method)
                        # print("Max",Max)

                    except Exception as a:
                        print(a)
                        popt = [1, 1, 1, 1]
                    yfit = [fun3(tmp, popt[0], popt[1], popt[2], popt[3]) for tmp in xfit]
                    ytempfit = [fun3(tmp, popt[0], popt[1], popt[2], popt[3]) for tmp in x]
                    R2 = getIndexes(ytempfit, y,sigmaerror,(len(y) - len(popt)))
                    isexist = 0
                    if (value.paras["双曲线积分拟合"] != []):
                        for i in range(len(value.paras["双曲线积分拟合"])):
                            if ((value.paras["双曲线积分拟合"][i].cutstartnum1 == starttruenum) and (
                                    value.paras["双曲线积分拟合"][i].cutendnum1 == endtruenum) and (
                                    value.paras["双曲线积分拟合"][i].fitweightindex == fitweightindex)):
                                tmpvalue = value.paras["双曲线积分拟合"].pop(i)
                                tmpvalue.para = popt
                                tmpvalue.para_error = count_error(funtype, x, y, ytempfit, popt, sigmaerror)
                                tmpvalue.method = method
                                tmpvalue.yfit = ytempfit
                                tmpvalue.xfit = x
                                # tmpvalue.xfit = count_variety_X(ytempfit,Interval,funtype,popt)
                                tmpvalue.fity = yfit
                                tmpvalue.fitx = xfit
                                tmpvalue.R2 = R2
                                value.paras["双曲线积分拟合"].append(tmpvalue)

                                isexist = 1
                                break
                    if (isexist == 0):
                        cutdata = cutclass()
                        cutdata.cutstartnum1 = starttruenum
                        cutdata.cutendnum1 = endtruenum
                        cutdata.cutstartnumspot1 = startnum
                        cutdata.cutendnumspot1 = endnum
                        cutdata.funtype = funtype
                        cutdata.method = method
                        cutdata.fitx = xfit
                        cutdata.fity = yfit
                        cutdata.yfit = ytempfit
                        cutdata.xfit = x
                        # cutdata.xfit = count_variety_X(ytempfit,Interval,funtype,popt)
                        cutdata.para = popt
                        cutdata.para_error = count_error(funtype, x, y, ytempfit, popt, sigmaerror)
                        cutdata.R2 = R2
                        cutdata.Max = np.max(value.Pro_Data1[starttruenum:endtruenum + 1])
                        cutdata.Min = np.min(value.Pro_Data1[starttruenum:endtruenum + 1])
                        cutdata.fitweightindex = fitweightindex
                        value.paras["双曲线积分拟合"].append(cutdata)
                elif (funtype == 4):
                    self.sinOuttext.emit("正在进行指数积分拟合 " + str(p) + "/" + str(len(self.data.filenames)))
                    try:
                        # print("指数")
                        # print(b2top[0]*Max,b2top[1],b2top[2])
                        # popt, pcov = curve_fit(fun4, x, y, sigma=sigmafit, absolute_sigma=True, maxfev=500000000,
                        #                        bounds=(
                        #                        [b1low[0] * Max /Interval, b1low[1] * 0.1, b1low[2] * 0.1],
                        #                        [b1top[0] * Max /Interval, b1top[1] *10, b1top[2] *10]),
                        #                        method=method)

                        popt, pcov = curve_fit(fun4, x, y, sigma=sigmafit, absolute_sigma=True, maxfev=500000000,
                                               bounds=(
                                               [b2low[0] * Max, b2low[1] , b2low[2] ],
                                               [b2top[0] * Max, b2top[1] , b2top[2] ]),
                                               method=method)
                        # print("Max",Max)

                    except Exception as a:
                        print(a)
                        popt = [1, 1, 1]
                    yfit = [fun4(tmp, popt[0], popt[1], popt[2]) for tmp in xfit]
                    ytempfit = [fun4(tmp, popt[0], popt[1], popt[2]) for tmp in x]
                    R2 = getIndexes(ytempfit, y,sigmaerror,(len(y) - len(popt)))
                    isexist = 0
                    if (value.paras["指数积分拟合"] != []):
                        for i in range(len(value.paras["指数积分拟合"])):
                            if ((value.paras["指数积分拟合"][i].cutstartnum1 == starttruenum) and (
                                    value.paras["指数积分拟合"][i].cutendnum1 == endtruenum) and (
                                    value.paras["指数积分拟合"][i].fitweightindex == fitweightindex)):
                                tmpvalue = value.paras["指数积分拟合"].pop(i)
                                tmpvalue.para = popt
                                tmpvalue.para_error = count_error(funtype, x, y, ytempfit, popt, sigmaerror)
                                tmpvalue.method = method
                                tmpvalue.yfit = ytempfit
                                tmpvalue.xfit = x
                                # tmpvalue.xfit = count_variety_X(ytempfit,Interval,funtype,popt)
                                tmpvalue.fity = yfit
                                tmpvalue.fitx = xfit
                                tmpvalue.R2 = R2
                                value.paras["指数积分拟合"].append(tmpvalue)

                                isexist = 1
                                break
                    if (isexist == 0):
                        cutdata = cutclass()
                        cutdata.cutstartnum1 = starttruenum
                        cutdata.cutendnum1 = endtruenum
                        cutdata.cutstartnumspot1 = startnum
                        cutdata.cutendnumspot1 = endnum
                        cutdata.funtype = funtype
                        cutdata.method = method
                        cutdata.fitx = xfit
                        cutdata.fity = yfit
                        cutdata.yfit = ytempfit
                        cutdata.xfit = x
                        # cutdata.xfit = count_variety_X(ytempfit,Interval,funtype,popt)
                        cutdata.para = popt
                        cutdata.para_error = count_error(funtype, x, y, ytempfit, popt, sigmaerror)
                        cutdata.R2 = R2
                        cutdata.Max = np.max(value.Pro_Data1[starttruenum:endtruenum + 1])
                        cutdata.Min = np.min(value.Pro_Data1[starttruenum:endtruenum + 1])
                        cutdata.fitweightindex = fitweightindex
                        value.paras["指数积分拟合"].append(cutdata)

                # print(value.Cut_Data1fit)
                # self.sinOuttext.emit("正在拟合"+str(p)+"/"+str(len(self.filelist))+"  "+key)
                # print("正在拟合",str(p))
                self.sinOutpro.emit(p / len(self.data.filenames) * 100)
                p = p + 1
        else:
            try:
                value = self.data.filelist[filename]
            except Exception as a:
                print(a)
            if startnum >= len(value.Pro_Data1) - 2:
                startnum = len(value.Pro_Data1) - 2
            if endnum >= len(value.Pro_Data1) - 2:
                endnum = len(value.Pro_Data1) - 2
            starttruenum = startnum
            endtruenum = len(value.Pro_Data1) - endnum - 1
            Max = np.max(value.Pro_Data1[starttruenum:endtruenum + 1])
            Min = np.min(value.Pro_Data1[starttruenum:endtruenum + 1])
            Interval = value.Interval
            x = value.Pro_Data1_X[starttruenum:endtruenum + 1]
            y = value.Pro_Data1[starttruenum:endtruenum + 1]

            if fitweightindex == 0:
                sigmafit = np.ones(shape=(len(y)))
                sigmaerror = np.ones(shape=(len(y)))
            elif fitweightindex == 1:
                sigmafit = [np.sqrt(1 / 999999999999) if tmp == 0 else np.sqrt(tmp) for tmp in y]
                sigmaerror = [999999999999 if tmp == 0 else 1 / tmp for tmp in y]
            else:
                sigmafit = [np.sqrt(1 / 999999999999) if tmp == 0 else np.sqrt(tmp) for tmp in
                            value.mal1MES[starttruenum:endtruenum + 1]]
                sigmaerror = [999999999999 if tmp == 0 else 1 / tmp for tmp in
                              value.mal1MES[starttruenum:endtruenum + 1]]

            xfit = np.linspace(value.Pro_Data1_X[starttruenum], value.Pro_Data1_X[endtruenum], 1000).tolist()
            try:
                if (funtype == 1):
                    # print("双曲")
                    # print(b1low[0]*Max,b1low[1],b1low[2],b1low[3])
                    # print(b1top[0]*Max,b1top[1],b1top[2],b1top[3])
                    self.sinOuttext.emit("正在进行双曲线拟合")
                    try:
                        popt, pcov = curve_fit(fun1, x, y,sigma=sigmafit,absolute_sigma=True, maxfev=500000, bounds=(
                        [b1low[0] * Max, b1low[1], b1low[2], b1low[3]], [b1top[0] * Max, b1top[1], b1top[2], b1top[3]]))
                    except Exception as a:
                        print(a)
                        popt = [1, 1, 1, 1]

                    yfit = [fun1(tmp, popt[0], popt[1], popt[2], popt[3]) for tmp in xfit]
                    ytempfit = [fun1(tmp, popt[0], popt[1], popt[2], popt[3]) for tmp in x]
                    R2 = getIndexes(ytempfit, y,sigmaerror,(len(y) - len(popt)))
                    isexist = 0
                    # print(value.paras["双曲线拟合"])
                    if (value.paras["双曲线拟合"] != []):
                        for i in range(len(value.paras["双曲线拟合"])):
                            if ((value.paras["双曲线拟合"][i].cutstartnum1 == starttruenum) and (
                                    value.paras["双曲线拟合"][i].cutendnum1 == endtruenum)and(value.paras["双曲线拟合"][i].fitweightindex==fitweightindex)):
                                tmpvalue = value.paras["双曲线拟合"].pop(i)
                                tmpvalue.para = popt
                                tmpvalue.para_error = count_error(funtype,x,y,ytempfit,popt,sigmaerror)
                                tmpvalue.method = method
                                tmpvalue.yfit = ytempfit
                                tmpvalue.fity = yfit
                                tmpvalue.fitx = xfit
                                tmpvalue.R2 = R2
                                value.paras["双曲线拟合"].append(tmpvalue)
                                isexist = 1
                                break
                    if (isexist == 0):
                        cutdata = cutclass()
                        cutdata.cutstartnum1 = starttruenum
                        cutdata.cutendnum1 = endtruenum
                        cutdata.cutstartnumspot1 = startnum
                        cutdata.cutendnumspot1 = endnum
                        cutdata.funtype = funtype
                        cutdata.method = method
                        cutdata.fitx = xfit
                        cutdata.fity = yfit
                        cutdata.yfit = ytempfit
                        cutdata.para = popt
                        cutdata.para_error = count_error(funtype,x,y,ytempfit,popt,sigmaerror)
                        cutdata.R2 = R2
                        cutdata.Max = Max
                        cutdata.Min = Min
                        cutdata.fitweightindex = fitweightindex
                        value.paras["双曲线拟合"].append(cutdata)


                elif (funtype == 2):
                    # print(value)
                    # print(x)
                    # print(y)
                    # print("指数")
                    # print(b2low[0] * Max, b2low[1], b2low[2])
                    # print(b2top[0] * Max, b2top[1], b2top[2])
                    self.sinOuttext.emit("正在进行指数拟合")
                    try:
                        popt, pcov = curve_fit(fun2, x, y,sigma=sigmafit,absolute_sigma=True, maxfev=500000, bounds=(
                        [b2low[0] * Max, b2low[1], b2low[2]], [b2top[0] * Max, b2top[1], b2top[2]]))
                    except Exception as a:
                        print(a)
                        popt = [1, 1, 1]

                    yfit = [fun2(tmp, popt[0], popt[1], popt[2]) for tmp in xfit]
                    ytempfit = [fun2(tmp, popt[0], popt[1], popt[2]) for tmp in x]
                    R2 = getIndexes(ytempfit, y,sigmaerror,(len(y) - len(popt)))
                    isexist = 0
                    # print(value.paras["指数拟合"])
                    if (value.paras["指数拟合"] != []):
                        for i in range(len(value.paras["指数拟合"])):
                            if ((value.paras["指数拟合"][i].cutstartnum1 == starttruenum) and (
                                    value.paras["指数拟合"][i].cutendnum1 == endtruenum)and(value.paras["指数拟合"][i].fitweightindex==fitweightindex)):
                                tmpvalue = value.paras["指数拟合"].pop(i)
                                tmpvalue.para = popt
                                tmpvalue.para_error = count_error(funtype,x,y,ytempfit,popt,sigmaerror)
                                tmpvalue.method = method
                                tmpvalue.yfit = ytempfit
                                tmpvalue.fity = yfit
                                tmpvalue.fitx = xfit
                                tmpvalue.R2 = R2
                                value.paras["指数拟合"].append(tmpvalue)
                                isexist = 1
                                break
                    if (isexist == 0):
                        cutdata = cutclass()
                        cutdata.cutstartnum1 = starttruenum
                        cutdata.cutendnum1 = endtruenum
                        cutdata.cutstartnumspot1 = startnum
                        cutdata.cutendnumspot1 = endnum
                        cutdata.funtype = funtype
                        cutdata.method = method
                        cutdata.fitx = xfit
                        cutdata.fity = yfit
                        cutdata.yfit = ytempfit
                        cutdata.para = popt
                        cutdata.para_error = count_error(funtype,x,y,ytempfit,popt,sigmaerror)
                        cutdata.R2 = R2
                        cutdata.Max = Max
                        cutdata.Min = Min
                        cutdata.fitweightindex = fitweightindex
                        value.paras["指数拟合"].append(cutdata)

                elif (funtype == 3):
                    # popt, pcov = curve_fit(fun3, x, y, maxfev=500000, bounds=param_bounds3)
                    # value.paras["双曲线积分拟合"] = popt
                    # value.Cut_Data1fit = fun3(value.Cut_Data1fit_X, popt[0], popt[1], popt[2], popt[3])
                    self.sinOuttext.emit("正在进行双曲线积分拟合")
                    try:
                        # print("指数")
                        # print(b1low[0] * Max, b1low[1], b1low[2], b1low[3],b1top[0] * Max*10, b1top[1]*10, b1top[2]*10, b1top[3]*10)
                        # print(b2top[0]*Max,b2top[1],b2top[2])
                        popt, pcov = curve_fit(fun3, x, y,sigma=sigmafit,absolute_sigma=True,maxfev=500000000, bounds=([b1low[0] * Max, b1low[1], b1low[2], b1low[3]], [b1top[0] * Max, b1top[1], b1top[2], b1top[3]]),method=method)
                        # popt, pcov = curve_fit(fun3, x, y,sigma=sigmafit,absolute_sigma=True,maxfev=500000000, bounds=([b1low[0] * Max/Interval, b1low[1], b1low[2], b1low[3]], [b1top[0] * Max/Interval, b1top[1], b1top[2], b1top[3]]),method=method)
                        # print("Max",Max)

                    except Exception as a:
                        print(a)
                        popt = [1, 1, 1, 1]
                    yfit = [fun3(tmp, popt[0], popt[1], popt[2], popt[3]) for tmp in xfit]
                    ytempfit = [fun3(tmp, popt[0], popt[1], popt[2], popt[3]) for tmp in x]
                    R2 = getIndexes(ytempfit, y,sigmaerror,(len(y) - len(popt)))
                    isexist = 0
                    if (value.paras["双曲线积分拟合"] != []):
                        for i in range(len(value.paras["双曲线积分拟合"])):
                            if ((value.paras["双曲线积分拟合"][i].cutstartnum1 == starttruenum) and (
                                    value.paras["双曲线积分拟合"][i].cutendnum1 == endtruenum) and (
                                    value.paras["双曲线积分拟合"][i].fitweightindex == fitweightindex)):
                                tmpvalue = value.paras["双曲线积分拟合"].pop(i)
                                tmpvalue.para = popt
                                tmpvalue.para_error = count_error(funtype, x, y, ytempfit, popt, sigmaerror)
                                tmpvalue.method = method
                                tmpvalue.yfit = ytempfit
                                tmpvalue.xfit = x
                                # tmpvalue.xfit = count_variety_X(ytempfit,Interval,funtype,popt)
                                tmpvalue.fity = yfit
                                tmpvalue.fitx = xfit
                                tmpvalue.R2 = R2
                                value.paras["双曲线积分拟合"].append(tmpvalue)

                                isexist = 1
                                break
                    if (isexist == 0):
                        cutdata = cutclass()
                        cutdata.cutstartnum1 = starttruenum
                        cutdata.cutendnum1 = endtruenum
                        cutdata.cutstartnumspot1 = startnum
                        cutdata.cutendnumspot1 = endnum
                        cutdata.funtype = funtype
                        cutdata.method = method
                        cutdata.fitx = xfit
                        cutdata.fity = yfit
                        cutdata.yfit = ytempfit
                        cutdata.xfit = x
                        # cutdata.xfit = count_variety_X(ytempfit,Interval,funtype,popt)
                        cutdata.para = popt
                        cutdata.para_error = count_error(funtype, x, y, ytempfit, popt, sigmaerror)
                        cutdata.R2 = R2
                        cutdata.Max = np.max(value.Pro_Data1[starttruenum:endtruenum + 1])
                        cutdata.Min = np.min(value.Pro_Data1[starttruenum:endtruenum + 1])
                        cutdata.fitweightindex = fitweightindex
                        value.paras["双曲线积分拟合"].append(cutdata)

                elif (funtype == 4):
                    # popt, pcov = curve_fit(fun4, x, y, maxfev=500000, bounds=param_bounds4)
                    #                     # value.paras["指数积分拟合"] = popt
                    #                     # value.Cut_Data1fit = fun4(value.Cut_Data1fit_X, popt[0], popt[1], popt[2])
                    self.sinOuttext.emit("正在进行指数积分拟合")
                    try:
                        # print("指数")
                        # print(b2top[0]*Max,b2top[1],b2top[2])
                        # popt, pcov = curve_fit(fun4, x, y, sigma=sigmafit, absolute_sigma=True, maxfev=500000000,
                        #                        bounds=(
                        #                        [b1low[0] * Max /Interval, b1low[1] * 0.1, b1low[2] * 0.1],
                        #                        [b1top[0] * Max /Interval, b1top[1] *10, b1top[2] *10]),
                        #                        method=method)

                        popt, pcov = curve_fit(fun4, x, y, sigma=sigmafit, absolute_sigma=True, maxfev=500000000,
                                               bounds=(
                                                   [b2low[0] * Max, b2low[1], b2low[2]],
                                                   [b2top[0] * Max, b2top[1], b2top[2]]),
                                               method=method)
                        # print("Max",Max)

                    except Exception as a:
                        print(a)
                        popt = [1, 1, 1]
                    yfit = [fun4(tmp, popt[0], popt[1], popt[2]) for tmp in xfit]
                    ytempfit = [fun4(tmp, popt[0], popt[1], popt[2]) for tmp in x]
                    R2 = getIndexes(ytempfit, y, sigmaerror,(len(y) - len(popt)))
                    isexist = 0
                    if (value.paras["指数积分拟合"] != []):
                        for i in range(len(value.paras["指数积分拟合"])):
                            if ((value.paras["指数积分拟合"][i].cutstartnum1 == starttruenum) and (
                                    value.paras["指数积分拟合"][i].cutendnum1 == endtruenum) and (
                                    value.paras["指数积分拟合"][i].fitweightindex == fitweightindex)):
                                tmpvalue = value.paras["指数积分拟合"].pop(i)
                                tmpvalue.para = popt
                                tmpvalue.para_error = count_error(funtype, x, y, ytempfit, popt, sigmaerror)
                                tmpvalue.method = method
                                tmpvalue.yfit = ytempfit
                                tmpvalue.xfit = x
                                # tmpvalue.xfit = count_variety_X(ytempfit,Interval,funtype,popt)
                                tmpvalue.fity = yfit
                                tmpvalue.fitx = xfit
                                tmpvalue.R2 = R2
                                value.paras["指数积分拟合"].append(tmpvalue)

                                isexist = 1
                                break
                    if (isexist == 0):
                        cutdata = cutclass()
                        cutdata.cutstartnum1 = starttruenum
                        cutdata.cutendnum1 = endtruenum
                        cutdata.cutstartnumspot1 = startnum
                        cutdata.cutendnumspot1 = endnum
                        cutdata.funtype = funtype
                        cutdata.method = method
                        cutdata.fitx = xfit
                        cutdata.fity = yfit
                        cutdata.yfit = ytempfit
                        cutdata.xfit = x
                        # cutdata.xfit = count_variety_X(ytempfit,Interval,funtype,popt)
                        cutdata.para = popt
                        cutdata.para_error = count_error(funtype, x, y, ytempfit, popt, sigmaerror)
                        cutdata.R2 = R2
                        cutdata.Max = np.max(value.Pro_Data1[starttruenum:endtruenum + 1])
                        cutdata.Min = np.min(value.Pro_Data1[starttruenum:endtruenum + 1])
                        cutdata.fitweightindex = fitweightindex
                        value.paras["指数积分拟合"].append(cutdata)



            except Exception as a:
                print(a)



        self.sinOutpro.emit(100)
        self.sinOutbool.emit(False)
        self.sinOuttext.emit(filename + "文件数据拟合成功！")

    def writeXls(self,data):
        self.sinOutbool.emit(True)
        self.sinOutpro.emit(0)
        self.data=data
        text = ""
        workbook = ""
        if (not (os.path.exists(self.data.outpath+"/"+os.path.basename(self.data.inpath)+".xlsx"))):
            if (not os.path.exists(self.data.outpath)):
                os.makedirs(self.data.outpath)
                # os.mknod(outpath+"/预处理后的数据.xls")
                # print("422")
            workbook = xlsxwriter.Workbook(self.data.outpath+"/"+os.path.basename(self.data.inpath)+".xlsx")
            # workbookson = xlsxwriter.Workbook(outpath + "/数据子矩阵.xlsx")

            # workbook.save(outpath + "/预处理后的数据.xls")  # 保存工作簿
            # print("424")
            text = "数据保存成功！(首次保存，已创建目录及文件)"
            # self.sinOuttext.emit("数据保存成功！(首次保存，已创建目录及文件)")

        else:
            try:
                os.remove(self.data.outpath +"/"+os.path.basename(self.data.inpath)+".xlsx")
            except Exception as a:
                self.sinOuttext.emit("保存失败！(文件被占用，请关闭关闭文件后重试)")
                text = "保存失败！(文件被占用，请关闭关闭文件后重试)"
                self.sinOutbool.emit(False)
                return
                # print(a)
            else:
                workbook = xlsxwriter.Workbook(self.data.outpath +"/"+os.path.basename(self.data.inpath)+".xlsx")
                # workbookson = xlsxwriter.Workbook(outpath + "/数据子矩阵.xlsx")
                text = "数据保存成功！(数据文件存在，已覆盖原数据文件)"
                # workbook.save(outpath + "/预处理后的数据.xls")  # 保存工作簿
                # print("xls格式表格写入数据成功！")
                # self.sinOuttext.emit("数据保存成功！(数据文件存在，已覆盖原数据文件)")
        # print(self.filelist)
        self.sinOuttext.emit("正在保存...")
        # workbook = xlsxwriter.Workbook()  #表
        bold1 = workbook.add_format({'fg_color': '#FFC1C1'})
        bold12 = workbook.add_format({'fg_color': '#CD9B9B'})
        bold2 = workbook.add_format({'fg_color': '#9AFF9A'})
        bold22 = workbook.add_format({'fg_color': '#7CCD7C'})
        bold3 = workbook.add_format({'fg_color': 'blue'})
        bold4 = workbook.add_format({'fg_color': 'yellow'})

        sheetpars = workbook.add_worksheet("参数数据")  # 参数数据表
        sheetpars2 = workbook.add_worksheet("参数数据（含置信区间）")  # 参数数据表
        Prodata = workbook.add_worksheet("原始数据")  # 预处理后的数据表
        xdata = workbook.add_worksheet("原始x轴数据")  # 预处理后的数据表

        cutdata1 = workbook.add_worksheet("(双曲线)裁剪后的数据")  # 预处理后的数据表
        cutxdata1 = workbook.add_worksheet("(双曲线)裁剪x轴数据")  # 预处理后的数据表
        cutdata1fit = workbook.add_worksheet("(双曲线)裁剪后拟合数据")  # 预处理后的数据表

        cutdata2 = workbook.add_worksheet("(指数)裁剪后的数据")  # 预处理后的数据表
        cutxdata2 = workbook.add_worksheet("(指数)裁剪x轴数据")  # 预处理后的数据表
        cutdata2fit = workbook.add_worksheet("(指数)裁剪后拟合数据")  # 预处理后的数据表

        cutdata3 = workbook.add_worksheet("(双曲线积分)裁剪后的数据")  # 预处理后的数据表
        cutxdata3 = workbook.add_worksheet("(双曲线积分)裁剪x轴数据")  # 预处理后的数据表
        cutdata3fit = workbook.add_worksheet("(双曲线积分)裁剪后拟合数据")  # 预处理后的数据表

        cutdata4 = workbook.add_worksheet("(指数积分)裁剪后的数据")  # 预处理后的数据表
        cutxdata4 = workbook.add_worksheet("(指数积分)裁剪x轴数据")  # 预处理后的数据表
        cutdata4fit = workbook.add_worksheet("(指数积分)裁剪后拟合数据")  # 预处理后的数据表

        inf = workbook.add_worksheet("文件信息")  # 预处理后的数据表
        # datamat = workbook.add_worksheet("子数据矩阵")  # 子数据矩阵表

        filenamelen = self.countlen(list(self.data.filelist.keys()))
        Prodata.write(0, 0, "文件名")
        xdata.write(0, 0, "文件名")
        cutdata1.write(0, 0, "文件名")
        cutdata1.write(0, 1, "前截点数")
        cutdata1.write(0, 2, "后截点数")

        cutdata2.write(0, 0, "文件名")
        cutdata2.write(0, 1, "前截点数")
        cutdata2.write(0, 2, "后截点数")

        cutxdata1.write(0, 0, "文件名")
        cutxdata1.write(0, 1, "前截点数")
        cutxdata1.write(0, 2, "后截点数")

        cutxdata2.write(0, 0, "文件名")
        cutxdata2.write(0, 1, "前截点数")
        cutxdata2.write(0, 2, "后截点数")

        cutxdata3.write(0, 0, "文件名")
        cutxdata3.write(0, 1, "前截点数")
        cutxdata3.write(0, 2, "后截点数")

        cutxdata4.write(0, 0, "文件名")
        cutxdata4.write(0, 1, "前截点数")
        cutxdata4.write(0, 2, "后截点数")

        # for i in range(len(self.filelist.)):
        #     Prodata.write(0, i+1, str(i+1))
        #     cutdata.write(0, i+1, str(i+1))
        sheetpars.write(0, 0, "文件名")
        sheetpars.write(0, 1, "Max(原始)")
        sheetpars.write(0, 2, "Min(原始)")
        sheetpars.write(0, 3, "ACQ_Time")
        sheetpars.write(0, 4, "(双曲线)前截点")
        sheetpars.write(0, 5, "(双曲线)后截点")
        sheetpars.write(0, 6, "(双曲线)I_0")
        sheetpars.write(0, 7, "(双曲线)τ")
        sheetpars.write(0, 8, "(双曲线)Γ")
        sheetpars.write(0, 9, "(双曲线)D")
        sheetpars.write(0, 10, "(双曲线)τ/Γ")
        sheetpars.write(0, 11, "(双曲线)R_square")
        sheetpars.write(0, 12, "(双曲线)SSE")
        sheetpars.write(0, 13, "(双曲线)MSE")
        sheetpars.write(0, 14, "(双曲线)RMSE")
        sheetpars.write(0, 15, "(指数)前截点")
        sheetpars.write(0, 16, "(指数)后截点")
        sheetpars.write(0, 17, "(指数)I_0")
        sheetpars.write(0, 18, "(指数)τ")
        sheetpars.write(0, 19, "(指数)D")
        sheetpars.write(0, 20, "(指数)R_square")
        sheetpars.write(0, 21, "(指数)SSE")
        sheetpars.write(0, 22, "(指数)MSE")
        sheetpars.write(0, 23, "(指数)RMSE")
        sheetpars.write(0, 24, "(双曲积分)前截点")
        sheetpars.write(0, 25, "(双曲积分)后截点")
        sheetpars.write(0, 26, "(双曲线积分)I_0")
        sheetpars.write(0, 27, "(双曲线积分)τ")
        sheetpars.write(0, 28, "(双曲线积分)Γ")
        sheetpars.write(0, 29, "(双曲线)D")
        sheetpars.write(0, 30, "(双曲线)τ/Γ")
        sheetpars.write(0, 31, "(双曲线)R_square")
        sheetpars.write(0, 32, "(双曲线)SSE")
        sheetpars.write(0, 33, "(双曲线)MSE")
        sheetpars.write(0, 34, "(双曲线)RMSE")
        sheetpars.write(0, 35, "(指数积分)前截点")
        sheetpars.write(0, 36, "(指数积分)后截点")
        sheetpars.write(0, 37, "(指数积分)I_0")
        sheetpars.write(0, 38, "(指数积分)τ")
        sheetpars.write(0, 39, "(指数)D")
        sheetpars.write(0, 40, "(指数)R_square")
        sheetpars.write(0, 41, "(指数)SSE")
        sheetpars.write(0, 42, "(指数)MSE")
        sheetpars.write(0, 43, "(指数)RMSE")
        
        sheetpars2.write(0, 0, "文件名")
        sheetpars2.write(0, 1, "Max(原始)")
        sheetpars2.write(0, 2, "Min(原始)")
        sheetpars2.write(0, 3, "ACQ_Time")
        sheetpars2.write(0, 4, "(双曲线)前截点")
        sheetpars2.write(0, 5, "(双曲线)后截点")
        sheetpars2.write(0, 6, "(双曲线)I_0")
        sheetpars2.write(0, 7, "(双曲线)τ")
        sheetpars2.write(0, 8, "(双曲线)Γ")
        sheetpars2.write(0, 9, "(双曲线)D")
        sheetpars2.write(0, 10, "(双曲线)τ/Γ")
        sheetpars2.write(0, 11, "(双曲线)R_square")
        sheetpars2.write(0, 12, "(双曲线)SSE")
        sheetpars2.write(0, 13, "(双曲线)MSE")
        sheetpars2.write(0, 14, "(双曲线)RMSE")
        sheetpars2.write(0, 15, "(指数)前截点")
        sheetpars2.write(0, 16, "(指数)后截点")
        sheetpars2.write(0, 17, "(指数)I_0")
        sheetpars2.write(0, 18, "(指数)τ")
        sheetpars2.write(0, 19, "(指数)D")
        sheetpars2.write(0, 20, "(指数)R_square")
        sheetpars2.write(0, 21, "(指数)SSE")
        sheetpars2.write(0, 22, "(指数)MSE")
        sheetpars2.write(0, 23, "(指数)RMSE")
        sheetpars2.write(0, 24, "(双曲积分)前截点")
        sheetpars2.write(0, 25, "(双曲积分)后截点")
        sheetpars2.write(0, 26, "(双曲线积分)I_0")
        sheetpars2.write(0, 27, "(双曲线积分)τ")
        sheetpars2.write(0, 28, "(双曲线积分)Γ")
        sheetpars2.write(0, 29, "(双曲线)D")
        sheetpars2.write(0, 30, "(双曲线)τ/Γ")
        sheetpars2.write(0, 31, "(双曲线)R_square")
        sheetpars2.write(0, 32, "(双曲线)SSE")
        sheetpars2.write(0, 33, "(双曲线)MSE")
        sheetpars2.write(0, 34, "(双曲线)RMSE")
        sheetpars2.write(0, 35, "(指数积分)前截点")
        sheetpars2.write(0, 36, "(指数积分)后截点")
        sheetpars2.write(0, 37, "(指数积分)I_0")
        sheetpars2.write(0, 38, "(指数积分)τ")
        sheetpars2.write(0, 39, "(指数)D")
        sheetpars2.write(0, 40, "(指数)R_square")
        sheetpars2.write(0, 41, "(指数)SSE")
        sheetpars2.write(0, 42, "(指数)MSE")
        sheetpars2.write(0, 43, "(指数)RMSE")
        
        

        try:
            # print(self.colnum_string(0))
            sheetpars.set_column(self.colnum_string(0), filenamelen)
            sheetpars.set_column(self.colnum_string(3), 28)
            sheetpars2.set_column(self.colnum_string(0), filenamelen)
            sheetpars2.set_column(self.colnum_string(3), 28)
        except Exception as a:
            print(a)
        for i in range(4, 44):
            sheetpars.set_column(self.colnum_string(i), self.countlen("(双曲线积分)I_0"))
            sheetpars2.set_column(self.colnum_string(i), self.countlen("(双曲线积分)I_0"))


        i = 1
        for key, value in self.data.filelist.items():
            sheetpars.write(i, 0, key)  # 像表格中写入数据（对应的行和列）
            sheetpars.write_number(i, 1, value.Max)  # 像表格中写入数据（对应的行和列）
            sheetpars.write_number(i, 2, value.Min)  # 像表格中写入数据（对应的行和列）
            sheetpars.write(i, 3, str(value.ACQ_Time.strftime('%Y-%m-%d  %H:%M:%S.%f')))  # 像表格中写入数据（对应的行和列）

            sheetpars2.write(i, 0, key)  # 像表格中写入数据（对应的行和列）
            sheetpars2.write_number(i, 1, value.Max)  # 像表格中写入数据（对应的行和列）
            sheetpars2.write_number(i, 2, value.Min)  # 像表格中写入数据（对应的行和列）
            sheetpars2.write(i, 3, str(value.ACQ_Time.strftime('%Y-%m-%d  %H:%M:%S.%f')))  # 像表格中写入数据（对应的行和列）
            # sheetpars.write_datetime(i, 3, value.ACQ_Time.strftime('%Y-%m-%d  %H:%M:%S.%f'))  # 像表格中写入数据（对应的行和列）

            if (value.paras["双曲线拟合"] != []):
                sheetpars.write_number(i, 4, value.paras["双曲线拟合"][-1].cutstartnumspot1)
                sheetpars.write_number(i, 5, value.paras["双曲线拟合"][-1].cutendnumspot1)
                sheetpars2.write_number(i, 4, value.paras["双曲线拟合"][-1].cutstartnumspot1)
                sheetpars2.write_number(i, 5, value.paras["双曲线拟合"][-1].cutendnumspot1)

                j = 6
                for ii in range(len(value.paras["双曲线拟合"][-1].para)):
                    para=value.paras["双曲线拟合"][-1].para[ii]
                    para_error=value.paras["双曲线拟合"][-1].para_error[ii]
                    # print(para)
                    # print("拟合1")
                    if (para != ""):
                        para = round(para, 5)
                    if (para_error != ""):
                        para_error = round(para_error, 5)

                    sheetpars.write_number(i, j, para, bold1)
                    sheetpars2.write(i, j, str(para)+"±"+str(para_error), bold1)
                    j += 1
                sheetpars.write_number(i, j,
                                       round(value.paras["双曲线拟合"][-1].para[1] / value.paras["双曲线拟合"][-1].para[2], 5),
                                       bold1)
                sheetpars2.write_number(i, j,
                                       round(value.paras["双曲线拟合"][-1].para[1] / value.paras["双曲线拟合"][-1].para[2], 5),
                                       bold1)
                j += 1
                for r in value.paras["双曲线拟合"][-1].R2:
                    if (r != ""):
                        r = round(r, 5)
                    sheetpars.write_number(i, j, r, bold12)
                    sheetpars2.write_number(i, j, r, bold12)
                    j += 1
            else:
                # for r in range(4,12):
                #     sheetpars.write(i, j, "", bold1)
                j = 15
            if (value.paras["指数拟合"] != []):
                sheetpars.write_number(i, j, value.paras["指数拟合"][-1].cutstartnumspot1)
                sheetpars.write_number(i, j+1, value.paras["指数拟合"][-1].cutendnumspot1)

                sheetpars2.write_number(i, j, value.paras["指数拟合"][-1].cutstartnumspot1)
                sheetpars2.write_number(i, j+1, value.paras["指数拟合"][-1].cutendnumspot1)

                j += 2
                for ii in range(len(value.paras["指数拟合"][-1].para)):
                    para=value.paras["指数拟合"][-1].para[ii]
                    para_error=value.paras["指数拟合"][-1].para_error[ii]
                    # print(para)
                    # print("拟合2")
                    if (para != ""):
                        para = round(para, 5)
                    if (para_error != ""):
                        para_error = round(para_error, 5)
                    sheetpars.write_number(i, j, para, bold2)
                    sheetpars2.write(i, j, str(para)+"±"+str(para_error), bold2)
                    j += 1
                for t in value.paras["指数拟合"][-1].R2:
                    if (t != ""):
                        t = round(t, 5)
                        # print(t)
                    sheetpars.write_number(i, j, t, bold22)
                    sheetpars2.write_number(i, j, t, bold22)
                    j += 1
            else:
                j =24
            # print("okk")
            if (value.paras["双曲线积分拟合"] != []):
                # for para in value.paras["双曲线积分拟合"][-1].para:
                #     if (para != ""):
                #         para = round(para, 3)
                #     sheetpars.write_number(i, j, para, bold3)
                #     sheetpars2.write_number(i, j, para, bold3)
                #     # print(para)
                #     # print("拟合3")
                #     j += 1

                sheetpars.write_number(i, j, value.paras["双曲线积分拟合"][-1].cutstartnumspot1)
                sheetpars.write_number(i, j+1, value.paras["双曲线积分拟合"][-1].cutendnumspot1)
                sheetpars2.write_number(i, j, value.paras["双曲线积分拟合"][-1].cutstartnumspot1)
                sheetpars2.write_number(i, j+1, value.paras["双曲线积分拟合"][-1].cutendnumspot1)

                j += 2
                for ii in range(len(value.paras["双曲线积分拟合"][-1].para)):
                    para = value.paras["双曲线积分拟合"][-1].para[ii]
                    para_error = value.paras["双曲线积分拟合"][-1].para_error[ii]
                    # print(para)
                    # print("拟合1")
                    if (para != ""):
                        para = round(para, 5)
                    if (para_error != ""):
                        para_error = round(para_error, 5)

                    sheetpars.write_number(i, j, para, bold1)
                    sheetpars2.write(i, j, str(para) + "±" + str(para_error), bold1)
                    j += 1
                sheetpars.write_number(i, j,
                                       round(value.paras["双曲线积分拟合"][-1].para[1] / value.paras["双曲线积分拟合"][-1].para[2], 5),
                                       bold1)
                sheetpars2.write_number(i, j,
                                        round(value.paras["双曲线积分拟合"][-1].para[1] / value.paras["双曲线积分拟合"][-1].para[2], 5),
                                        bold1)
                j += 1
                for r in value.paras["双曲线积分拟合"][-1].R2:
                    if (r != ""):
                        r = round(r, 5)
                    sheetpars.write_number(i, j, r, bold12)
                    sheetpars2.write_number(i, j, r, bold12)
                    j += 1
            else:
                j +=35
            if (value.paras["指数积分拟合"] != []):
                # for para in value.paras["指数积分拟合"][-1].para:
                #     if (para != ""):
                #         para = round(para, 3)
                #     sheetpars.write_number(i, j, para, bold4)
                #     sheetpars2.write_number(i, j, para, bold4)
                #     # print(para)
                #     # print("拟合4")
                #     j += 1

                sheetpars.write_number(i, j, value.paras["指数积分拟合"][-1].cutstartnumspot1)
                sheetpars.write_number(i, j + 1, value.paras["指数积分拟合"][-1].cutendnumspot1)

                sheetpars2.write_number(i, j, value.paras["指数积分拟合"][-1].cutstartnumspot1)
                sheetpars2.write_number(i, j + 1, value.paras["指数积分拟合"][-1].cutendnumspot1)

                j += 2
                for ii in range(len(value.paras["指数积分拟合"][-1].para)):
                    para = value.paras["指数积分拟合"][-1].para[ii]
                    para_error = value.paras["指数积分拟合"][-1].para_error[ii]
                    # print(para)
                    # print("拟合2")
                    if (para != ""):
                        para = round(para, 5)
                    if (para_error != ""):
                        para_error = round(para_error, 5)
                    sheetpars.write_number(i, j, para, bold2)
                    sheetpars2.write(i, j, str(para) + "±" + str(para_error), bold2)
                    j += 1
                for t in value.paras["指数积分拟合"][-1].R2:
                    if (t != ""):
                        t = round(t, 5)
                        # print(t)
                    sheetpars.write_number(i, j, t, bold22)
                    sheetpars2.write_number(i, j, t, bold22)
                    j += 1

            else:
                j = 44

            # 保存原始数据
            Prodata.write(i, 0, key)
            Prodata.set_column(self.colnum_string(0), filenamelen)
            z = 1
            for spot in value.Pro_Data1:
                Prodata.write_number(i, z, spot)
                z += 1

            # 保存剪切后的数据
            if (value.paras["双曲线拟合"] != []):
                cutdata1.write(i, 0, key)
                cutdata1.set_column(self.colnum_string(0), filenamelen)
                z = 1
                # print(value.cutstartnum1)
                # print(value.cutendnum1 + 1)
                cutdata1.write_number(i, z, value.paras["双曲线拟合"][-1].cutstartnumspot1)
                cutdata1.write_number(i, z + 1, value.paras["双曲线拟合"][-1].cutendnumspot1)
                z += 2
                for spot in value.Pro_Data1[
                            value.paras["双曲线拟合"][-1].cutstartnum1:value.paras["双曲线拟合"][-1].cutendnum1 + 1]:
                    cutdata1.write_number(i, z, spot)

                    z += 1
            if (value.paras["指数拟合"] != []):
                cutdata2.write(i, 0, key)
                cutdata2.set_column(self.colnum_string(0), filenamelen)
                z = 1
                # print(value.cutstartnum1)
                # print(value.cutendnum1 + 1)
                cutdata2.write_number(i, z, value.paras["指数拟合"][-1].cutstartnumspot1)
                cutdata2.write_number(i, z + 1, value.paras["指数拟合"][-1].cutendnumspot1)
                z += 2
                for spot in value.Pro_Data1[
                            value.paras["指数拟合"][-1].cutstartnum1:value.paras["指数拟合"][-1].cutendnum1 + 1]:
                    cutdata2.write_number(i, z, spot)

                    z += 1
            if (value.paras["双曲线积分拟合"] != []):
                cutdata3.write(i, 0, key)
                cutdata3.set_column(self.colnum_string(0), filenamelen)
                z = 1
                # print(value.cutstartnum1)
                # print(value.cutendnum1 + 1)
                cutdata3.write_number(i, z, value.paras["双曲线积分拟合"][-1].cutstartnumspot1)
                cutdata3.write_number(i, z + 1, value.paras["双曲线积分拟合"][-1].cutendnumspot1)
                z += 2
                for spot in value.Pro_Data1[
                            value.paras["双曲线积分拟合"][-1].cutstartnum1:value.paras["双曲线积分拟合"][-1].cutendnum1 + 1]:
                    cutdata3.write_number(i, z, spot)

                    z += 1
            if (value.paras["指数积分拟合"] != []):
                cutdata4.write(i, 0, key)
                cutdata4.set_column(self.colnum_string(0), filenamelen)
                z = 1
                # print(value.cutstartnum1)
                # print(value.cutendnum1 + 1)
                cutdata4.write_number(i, z, value.paras["指数积分拟合"][-1].cutstartnumspot1)
                cutdata4.write_number(i, z + 1, value.paras["指数积分拟合"][-1].cutendnumspot1)
                z += 2
                for spot in value.Pro_Data1[
                            value.paras["指数积分拟合"][-1].cutstartnum1:value.paras["指数积分拟合"][-1].cutendnum1 + 1]:
                    cutdata4.write_number(i, z, spot)

                    z += 1

            self.sinOutpro.emit(i / len(self.data.filelist) * 80)


            #原始x轴数据
            xdata.write(i, 0, key)
            xdata.set_column(self.colnum_string(0), filenamelen)
            z = 1
            for spot in value.Pro_Data1_X:
                xdata.write_number(i, z, spot)
                z += 1

            # 双曲线裁剪后x轴数据
            if (value.paras["双曲线拟合"] != []):
                cutxdata1.write(i, 0, key)
                cutxdata1.set_column(self.colnum_string(0), filenamelen)

                cutdata1fit.write(i, 0, key)
                cutdata1fit.set_column(self.colnum_string(0), filenamelen)

                cutxdata1.write_number(i, 1, value.paras["双曲线拟合"][-1].cutstartnumspot1)
                cutxdata1.write_number(i, 2, value.paras["双曲线拟合"][-1].cutendnumspot1)

                cutdata1fit.write_number(i, 1, value.paras["双曲线拟合"][-1].cutstartnumspot1)
                cutdata1fit.write_number(i, 2, value.paras["双曲线拟合"][-1].cutendnumspot1)

                z =3
                for spot in value.paras["双曲线拟合"][-1].yfit:
                    cutdata1fit.write_number(i, z, spot)
                    z += 1


                z =3
                for spot in value.Pro_Data1_X[
                            value.paras["双曲线拟合"][-1].cutstartnum1:value.paras["双曲线拟合"][-1].cutendnum1 + 1]:
                    cutxdata1.write_number(i, z, spot)
                    z += 1

            # 指数裁剪后x轴数据
            if (value.paras["指数拟合"] != []):
                cutxdata2.write(i, 0, key)
                cutxdata2.set_column(self.colnum_string(0), filenamelen)

                cutdata2fit.write(i, 0, key)
                cutdata2fit.set_column(self.colnum_string(0), filenamelen)

                cutxdata2.write_number(i, 1, value.paras["指数拟合"][-1].cutstartnumspot1)
                cutxdata2.write_number(i, 2, value.paras["指数拟合"][-1].cutendnumspot1)

                cutdata2fit.write_number(i, 1, value.paras["指数拟合"][-1].cutstartnumspot1)
                cutdata2fit.write_number(i, 2, value.paras["指数拟合"][-1].cutendnumspot1)

                z =3
                for spot in value.paras["指数拟合"][-1].yfit:
                    cutdata2fit.write_number(i, z, spot)
                    z += 1

                z =3
                for spot in value.Pro_Data1_X[
                            value.paras["指数拟合"][-1].cutstartnum1:value.paras["指数拟合"][-1].cutendnum1 + 1]:
                    cutxdata2.write_number(i, z, spot)
                    z += 1

            # 双曲线积分裁剪后x轴数据
            if (value.paras["双曲线积分拟合"] != []):
                cutxdata3.write(i, 0, key)
                cutxdata3.set_column(self.colnum_string(0), filenamelen)

                cutdata3fit.write(i, 0, key)
                cutdata3fit.set_column(self.colnum_string(0), filenamelen)

                cutxdata3.write_number(i, 1, value.paras["双曲线积分拟合"][-1].cutstartnumspot1)
                cutxdata3.write_number(i, 2, value.paras["双曲线积分拟合"][-1].cutendnumspot1)

                cutdata3fit.write_number(i, 1, value.paras["双曲线积分拟合"][-1].cutstartnumspot1)
                cutdata3fit.write_number(i, 2, value.paras["双曲线积分拟合"][-1].cutendnumspot1)

                z =3
                for spot in value.paras["双曲线积分拟合"][-1].yfit:
                    cutdata3fit.write_number(i, z, spot)
                    z += 1


                z =3
                for spot in value.Pro_Data1_X[
                            value.paras["双曲线积分拟合"][-1].cutstartnum1:value.paras["双曲线积分拟合"][-1].cutendnum1 + 1]:
                    cutxdata3.write_number(i, z, spot)
                    z += 1

            # 指数积分裁剪后x轴数据
            if (value.paras["指数积分拟合"] != []):
                cutxdata4.write(i, 0, key)
                cutxdata4.set_column(self.colnum_string(0), filenamelen)

                cutdata4fit.write(i, 0, key)
                cutdata4fit.set_column(self.colnum_string(0), filenamelen)

                cutxdata4.write_number(i, 1, value.paras["指数积分拟合"][-1].cutstartnumspot1)
                cutxdata4.write_number(i, 2, value.paras["指数积分拟合"][-1].cutendnumspot1)

                cutdata4fit.write_number(i, 1, value.paras["指数积分拟合"][-1].cutstartnumspot1)
                cutdata4fit.write_number(i, 2, value.paras["指数积分拟合"][-1].cutendnumspot1)

                z =3
                for spot in value.paras["指数积分拟合"][-1].yfit:
                    cutdata4fit.write_number(i, z, spot)
                    z += 1

                z =3
                for spot in value.Pro_Data1_X[
                            value.paras["指数积分拟合"][-1].cutstartnum1:value.paras["指数积分拟合"][-1].cutendnum1 + 1]:
                    cutxdata4.write_number(i, z, spot)
                    z += 1
            i += 1




        print("round2")
        # 文件信息
        inf.write(0, 0, "文件名")
        inf.write(0, 1, "ACQ_Time")
        inf.write(0, 2, "Project")
        inf.write(0, 3, "Name")
        inf.write(0, 4, "Part")
        inf.write(0, 5, "Operator")
        inf.write(0, 6, "Desc")
        inf.write(0, 7, "Excited_Peroid(ms)")
        inf.write(0, 8, "Excited_Time(ms)")
        inf.write(0, 9, "Acq_Delay_Time(ms)")
        inf.write(0, 10, "Gate_Time(ms)")
        inf.write(0, 11, "Count_Num_per_gate")
        inf.write(0, 12, "Repeat_Times")
        inf.write(0, 13, "Acq_Gate_Times")
        inf.write(0, 14, "Interval_per_Gate(ms)")
        inf.write(0, 15, "Channel_Number")
        # print(type(inf))

        inf.set_column(self.colnum_string(0), self.countlen(list(self.data.filelist.keys())))
        inf.set_column(self.colnum_string(1), 28)
        inf.set_column(self.colnum_string(2), self.countlen("Project"))
        inf.set_column(self.colnum_string(3), self.countlen("Name  "))
        inf.set_column(self.colnum_string(4), self.countlen("Part  "))
        inf.set_column(self.colnum_string(5), self.countlen("Operator"))
        inf.set_column(self.colnum_string(6), self.countlen("Desc "))
        inf.set_column(self.colnum_string(7), self.countlen("Excited_Peroid(ms)"))
        inf.set_column(self.colnum_string(8), self.countlen("Excited_Time(ms)"))
        inf.set_column(self.colnum_string(9), self.countlen("Acq_Delay_Time(ms)"))
        inf.set_column(self.colnum_string(10), self.countlen("Gate_Time(ms)"))
        inf.set_column(self.colnum_string(11), self.countlen("Count_Num_per_gate"))
        inf.set_column(self.colnum_string(12), self.countlen("Repeat_Times"))
        inf.set_column(self.colnum_string(13), self.countlen("Acq_Gate_Times"))
        inf.set_column(self.colnum_string(14), self.countlen("Interval_per_Gate(ms)"))
        inf.set_column(self.colnum_string(15), self.countlen("Channel_Number"))

        # for i in range(0,16):
        # inf.col(i).width=256*(len(inf.cell(0,i).value.encode('utf-8').encode()))
        # print(len(inf.cell(0,i).value.encode('utf-8').encode()))

        i = 1

        for key, value in self.data.filelist.items():
            inf.write(i, 0, str(key))
            # inf.write_datetime(i, 1,value.ACQ_Time)
            inf.write(i, 1, str(value.ACQ_Time.strftime('%Y-%m-%d  %H:%M:%S.%f')))
            inf.write(i, 2, str(value.Project))
            inf.write(i, 3, str(value.Name))
            inf.write(i, 4, str(value.Part))
            inf.write(i, 5, str(value.Operator))
            inf.write(i, 6, str(value.Desc))
            inf.write_number(i, 7, round(value.Excited_Peroid, 2))
            inf.write_number(i, 8, round(value.Excited_Time, 2))
            inf.write_number(i, 9, round(value.Acq_Delay_Time, 2))
            inf.write_number(i, 10, round(value.Gate_Time, 2))
            inf.write_number(i, 11, round(value.Count_Num_per_gate, 2))
            inf.write_number(i, 12, round(value.Repeat_Times, 2))
            inf.write_number(i, 13, round(value.Acq_Gate_Times, 2))
            inf.write_number(i, 14, round(value.Interval_per_Gate, 2))
            inf.write_number(i, 15, round(value.Channel_Number, 2))
            self.sinOutpro.emit(i / len(self.data.filelist) * 20 + 80)
            i += 1
        workbook.close()
        # 生成子矩阵文件夹

        # if iswrite==True:
        #     if (not os.path.exists(outpath+"/数据子矩阵")):
        #         os.makedirs(outpath+"/数据子矩阵")
        #     for filename, file in self.filelist.items():
        #         Worktemp=xlsxwriter.Workbook(outpath + "/数据子矩阵/"+filename+".xlsx")
        #         sheet=Worktemp.add_worksheet("数据子矩阵")
        #         for i in range(len(file.Pro_Data1)):
        #             sheet.write(0,i,str(file.Pro_Data1[i]))
        #             for j in range(len(file.Pro_mal1[0])):
        #                 sheet.write(j+1, i, str(file.Pro_mal1[i][j]))
        #         Worktemp.close()

        # 数据子矩阵
        # 写入一个文件（文件名不能超过31个char）
        # try:
        #     for filename, file in self.filelist.items():
        #         sheet=workbookson.add_worksheet(filename)
        #         for i in range(len(file.Pro_Data1)):
        #             sheet.write(0,i,str(file.Pro_Data1[i]))
        #             for j in range(file.Pro_mal1[0]):
        #                 sheet.write(j+1, i, str(file.Pro_mal1[i][j]))
        #     workbookson.close()
        # except Exception as a:
        #     print(a)
        self.sinOutbool.emit(False)
        self.sinOuttext.emit(text)

        # print(outpath)
        # print(not (os.path.exists(outpath)))
        # print(os.path.exists(outpath))
        # if( not (os.path.exists(outpath+ "/预处理后的数据.xls"))):
        #     if( not os.path.exists(outpath)):
        #         os.makedirs(outpath)
        #     # os.mknod(outpath+"/预处理后的数据.xls")
        #     print("422")
        #     try:
        #         workbook.save(outpath + "/预处理后的数据.xls")  # 保存工作簿
        #     print("424")
        #     self.sinOuttext.emit("数据保存成功！(首次保存，已创建目录及文件)")
        # else:
        #     try:
        #         os.remove(outpath+"/预处理后的数据.xls")
        #     except Exception as a:
        #         self.sinOuttext.emit("保存失败！(文件被占用，请关闭关闭文件后重试)")
        #         print(a)
        #     else:
        #         workbook.save(outpath+"/预处理后的数据.xls")  # 保存工作簿
        #         print("xls格式表格写入数据成功！")
        #         self.sinOuttext.emit("数据保存成功！(数据文件存在，已覆盖原数据文件)")

    def writesondataXls(self,data):
        self.data=data
        exist = True
        if (not os.path.exists(self.data.outpath + "/数据子矩阵/")):
            os.makedirs(self.data.outpath + "/数据子矩阵")
            exist = False
        self.sinOutbool.emit(True)

        p = 1
        for filename, file in self.data.filelist.items():
            self.sinOuttext.emit(
                "正在保存数据子矩阵 " + str(p) + "/" + str(len(self.data.filelist)) + " " + os.path.splitext(filename)[0])
            self.sinOutpro.emit(p / len(self.data.filelist) * 100)
            # try:
            #     os.remove(self.data.outpath + "/数据子矩阵/"+os.path.splitext(filename)[0]+".xlsx")
            # except Exception as a:
            #     return
            Worktemp = xlsxwriter.Workbook(self.data.outpath + "/数据子矩阵/" + os.path.splitext(filename)[0] + ".xlsx")
            sheet = Worktemp.add_worksheet("数据子矩阵")
            for i in range(len(file.Pro_Data1)):
                sheet.write_number(0, i, file.Pro_Data1[i])
                for j in range(len(file.Pro_mal1[0])):
                    sheet.write_number(j + 1, i, file.Pro_mal1[i][j])
            Worktemp.close()
            p += 1
        if (exist == False):
            self.sinOuttext.emit("首次保存，已将子矩阵文件保存到数据目录下的‘数据子矩阵文件夹’！")
        else:
            self.sinOuttext.emit("数据子矩阵数据更新成功！")
        self.sinOutbool.emit(False)

    def writesondatatxt(self,data):
        self.data=data
        exist = True
        if (not os.path.exists(self.data.outpath + "/处理后的txt文件/")):
            os.makedirs(self.data.outpath + "/处理后的txt文件")
            exist = False
        self.sinOutbool.emit(True)
        p=1
        for filename, file in self.data.filelist.items():
            self.sinOuttext.emit(
                "正在保存预处理后TXT文件 " + str(p) + "/" + str(len(self.data.filelist)) + " " + os.path.splitext(filename)[0])
            self.sinOutpro.emit(p / len(self.data.filelist) * 100)
            with open(self.data.outpath + "/处理后的txt文件/"+os.path.splitext(filename)[0]+'.txt', 'w') as f:
                for i in range(len(file.Pro_Data1)):
                    f.write(str(round(file.Pro_Data1_X[i],4))+"\t"+str(file.Pro_Data1[i]) +'\n' )
            p+=1
        if (exist == False):
            self.sinOuttext.emit("首次保存，已将处理后的txt文件保存到数据目录下的‘处理后的txt文件’！")
        else:
            self.sinOuttext.emit("处理后的txt文件更新成功！")
        self.sinOutbool.emit(False)

    def writesinglefiledata(self, datatemp):
        self.data=datatemp
        exist = True
        if (not os.path.exists(self.data.outpath + "/单文件裁剪后拟合数据/")):
            os.makedirs(self.data.outpath + "/单文件裁剪后拟合数据/")
            exist = False
        self.sinOutbool.emit(True)
        p = 1
        errlist = []
        for filename, file in self.data.filelist.items():
            self.sinOuttext.emit(
                "正在保存单文件裁剪数据 " + str(p) + "/" + str(len(self.data.filelist)) + " " + os.path.splitext(filename)[0])
            self.sinOutpro.emit(p / len(self.data.filelist) * 100)
            # try:
            #     os.remove(self.data.outpath + "/单文件裁剪后拟合数据/" + os.path.splitext(filename)[0] + ".xlsx")
            # except Exception :
            #     errlist.append(os.path.splitext(filename))
            #     p+=1
            #     continue
            Worktemp = xlsxwriter.Workbook(self.data.outpath + "/单文件裁剪后拟合数据/" + os.path.splitext(filename)[0] + ".xlsx")
            sheet1 = Worktemp.add_worksheet("双曲线拟合")
            sheet2 = Worktemp.add_worksheet("指数拟合")
            sheet3 = Worktemp.add_worksheet("双曲线裁剪后拟合")
            sheet4 = Worktemp.add_worksheet("指数裁剪后拟合")

            # 写sheet1
            sheet1.write(0, 0, "文件名")
            sheet1.write(0, 1, "前截点数")
            sheet1.write(0, 2, "后截点数")
            sheet1.write(0, 3, "I_0")
            sheet1.write(0, 4, "τ")
            sheet1.write(0, 5, "Γ")
            sheet1.write(0, 6, "D")
            sheet1.write(0, 7, "R_square")
            sheet1.write(0, 8, "SSE")
            sheet1.write(0, 9, "MME")
            sheet1.write(0, 10, "RMSE")
            for i in range(len(file.paras["双曲线拟合"])):
                sheet1.write(i + 1, 0, filename)
                sheet1.write_number(i + 1, 1, file.paras["双曲线拟合"][i].cutstartnumspot1)
                sheet1.write_number(i + 1, 2, file.paras["双曲线拟合"][i].cutendnumspot1)
                sheet1.write_number(i + 1, 3, round(file.paras["双曲线拟合"][i].para[0], 5))
                sheet1.write_number(i + 1, 4, round(file.paras["双曲线拟合"][i].para[1], 2))
                sheet1.write_number(i + 1, 5, round(file.paras["双曲线拟合"][i].para[2], 2))
                sheet1.write_number(i + 1, 6, round(file.paras["双曲线拟合"][i].para[3], 2))
                sheet1.write_number(i + 1, 7, round(file.paras["双曲线拟合"][i].R2[0], 8))
                sheet1.write_number(i + 1, 8, round(file.paras["双曲线拟合"][i].R2[1], 8))
                sheet1.write_number(i + 1, 9, round(file.paras["双曲线拟合"][i].R2[2], 8))
                sheet1.write_number(i + 1, 10, round(file.paras["双曲线拟合"][i].R2[3], 8))
                i += 1
            # 写sheet2
            sheet2.write(0, 0, "文件名")
            sheet2.write(0, 1, "前截点数")
            sheet2.write(0, 2, "后截点数")
            sheet2.write(0, 3, "I_0")
            sheet2.write(0, 4, "τ")
            sheet2.write(0, 5, "D")
            sheet2.write(0, 6, "R_square")
            sheet2.write(0, 7, "SSE")
            sheet2.write(0, 8, "MME")
            sheet2.write(0, 9, "RMSE")
            for i in range(len(file.paras["指数拟合"])):
                sheet2.write(i + 1, 0, filename)
                sheet2.write_number(i + 1, 1, file.paras["指数拟合"][i].cutstartnumspot1)
                sheet2.write_number(i + 1, 2, file.paras["指数拟合"][i].cutendnumspot1)
                sheet2.write_number(i + 1, 3, round(file.paras["指数拟合"][i].para[0], 2))
                sheet2.write_number(i + 1, 4, round(file.paras["指数拟合"][i].para[1], 2))
                sheet2.write_number(i + 1, 5, round(file.paras["指数拟合"][i].para[2], 2))
                sheet2.write_number(i + 1, 6, round(file.paras["指数拟合"][i].R2[0], 2))
                sheet2.write_number(i + 1, 7, round(file.paras["指数拟合"][i].R2[1], 2))
                sheet2.write_number(i + 1, 8, round(file.paras["指数拟合"][i].R2[2], 2))
                sheet2.write_number(i + 1, 9, round(file.paras["指数拟合"][i].R2[3], 2))
                i += 1
            # 写sheet3
            sheet3.write(0, 0, "前截点数")
            sheet3.write(0, 1, "后截点数")
            for i in range(len(file.paras["双曲线拟合"])):
                sheet3.write_number(i + 1, 0, file.paras["双曲线拟合"][i].cutstartnumspot1)
                sheet3.write_number(i + 1, 1, file.paras["双曲线拟合"][i].cutendnumspot1)
                data = file.Pro_Data1[file.paras["双曲线拟合"][i].cutstartnum1:file.paras["双曲线拟合"][i].cutendnum1]
                for j in range(len(data)):
                    sheet3.write_number(i + 1, j + 2, data[j])
                    j += 1
                i += 1

            # 写sheet4
            sheet4.write(0, 0, "前截点数")
            sheet4.write(0, 1, "后截点数")
            for i in range(len(file.paras["指数拟合"])):
                sheet4.write_number(i + 1, 0, file.paras["指数拟合"][i].cutstartnumspot1)
                sheet4.write_number(i + 1, 1, file.paras["指数拟合"][i].cutendnumspot1)
                data = file.Pro_Data1[file.paras["双曲线拟合"][i].cutstartnum1:file.paras["指数拟合"][i].cutendnum1]
                for j in range(len(data)):
                    sheet4.write_number(i + 1, j + 2, data[j])
                    j += 1
                i += 1
            Worktemp.close()
            p += 1
        if (exist == False):
            self.sinOuttext.emit("首次保存，已将单数据裁剪文件保存到数据目录下的‘单文件裁剪后拟合数据’！")
        else:
            if errlist == []:
                self.sinOuttext.emit("单文件裁剪后拟合数据更新成功！")
            else:
                name = ""
                for temp in errlist:
                    name += temp
                self.sinOuttext.emit(name + "保存失败(文件被占用)，其余文件保存成功")
        self.sinOutbool.emit(False)

    def cutdata(self, numstart, numend, filename):

        # 单文件
        # print(filename)
        if (filename != "批量裁剪"):
            index = filename.find("]")
            title = filename[(index + 1):]
            # print(title)
            self.data.filelist[title].cutstartnum1 = numstart
            self.data.filelist[title].cutendnum1 = len(self.data.filelist[title].Pro_Data1) - numend - 1
            # print("numstart",self.filelist[title].cutstartnum1)
            # print("numend",self.filelist[title].cutendnum1)
            self.sinOuttext.emit(
                "已经移除 " + filename + " 文件的前" + str(numstart) + "后" + str(numend) + "个数据点,并更新数据的区间内最值")
            self.countparas(title)


        # 批处理
        else:
            # self.filelist[filename].cutstartnum1=numstart
            # self.filelist[filename].cutendnum1=len(self.filelist[filename].Pro_Data1)-numend-1
            p = 1
            for key, value in self.data.filelist.items():
                value.cutstartnum1 = numstart
                value.cutendnum1 = len(self.data.filelist[key].Pro_Data1) - numend - 1
                # for i in range(numstart):
                #     value.Cut_Data1_X.pop(0)
                #     value.Cut_Data1.pop(0)
                p += 1

                # value.Max = np.max(value.Cut_Data1)
                # value.Min = np.min(value.Cut_Data1)
                self.countparas(key)
            self.sinOuttext.emit("已经移除所有文件的前" + str(numstart) + "后" + str(numend) + "个数据点,并更新数据的区间内最值")

    def countparas(self, filename):
        numstart = self.data.filelist[filename].cutstartnum1
        numend = self.data.filelist[filename].cutendnum1
        self.data.filelist[filename].Max = np.max(self.data.filelist[filename].Pro_Data1[numstart:numend + 1])
        self.data.filelist[filename].Min = np.min(self.data.filelist[filename].Pro_Data1[numstart:numend + 1])

    def countlen(self, x):
        if type(x) == list:
            max = 0
            for str in x:
                if (len(str.encode()) > max):
                    max = len(str.encode())
            return max + 1
        else:
            return len(x.encode()) + 1

    def colnum_string(self, n):
        div = n + 1
        string = ""
        while div > 0:
            module = (div - 1) % 26
            string = chr(65 + module) + string
            div = int((div - module) / 26)
        return string + ":" + string
# if __name__ == '__main__':
#     a = dataread()
#     a.readfiles("C:/Users/ENERGY/Desktop/工作文件/test")
#     a.writeXls("C:/Users/ENERGY/Desktop/工作文件/test")





