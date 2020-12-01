import os
import re
import numpy as np
import xlrd
import xlwt
import xlsxwriter
from scipy.optimize import curve_fit
from datetime import datetime
from xlutils.copy import copy
#
# datarow = open(filepath + '/' + f)  # 读取的整个原始文件数据
# datarowlines = datarow.readlines()  # 读取的整个原始文件的数据，按行分割
# datapar = []  # 真正的每行数据数组
# for line in datarowlines:
#     linenew = line.strip()
#     if (linenew != ""):
#         datapar.append(linenew)
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
import pickle
f = open("D:/工作文件2/DLData400/DLData400.data", 'rb')
data = pickle.load(f)
print(data.outpath)
f.close()
data.outpath="D:/工作文件2/DLData400/预处理后的数据"
with open("D:/工作文件2/DLData400/DLData400.data", "wb") as file:
    pickle.dump(data, file, True)