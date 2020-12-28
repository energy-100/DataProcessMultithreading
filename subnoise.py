import os
import pandas as pd
import numpy as np
import os
from datetime import datetime
class dataclass():
    def __init__(self):
        self.filename=""
        self.Project = ""
        self.Name = ""
        self.part = ""
        self.Operator = ""
        self.Desc = ""
        self.Excited_Peroid = 0
        self.Excited_Time = 0
        self.Acq_Delay_Time = 0
        self.Gate_Time = 0
        self.Count_Num_per_gate = 0
        self.Repeat_Times = 0
        self.Acq_Gate_Times = 0
        self.Interval_per_Gate = 0
        self.datanum = 0
        self.Raw_Data1=[]
        
class main():
    def __init__(self,folderpath:str,noisefilepath:str):
        self.folderpath=folderpath
        self.outfolderpath = folderpath+"/REMOVE_NOISE/"
        self.noisefilepath=noisefilepath
        self.filenames=[]
        self.noisedata=dataclass()
        self.datalist=[]
        self.errfilelist=[]
    def process(self):
        files = os.listdir(self.folderpath)
        for f in files:
            if (os.path.isdir(self.folderpath + '/' + f)):
                # 排除隐藏文件夹。因为隐藏文件夹过多
                if (f[0] == '.'):
                    pass
                else:
                    pass
            if (os.path.isfile(self.folderpath + '/' + f)):
                # 添加文件
                if (os.path.splitext(f)[1] == ".txt"):
                    self.filenames.append(f)
        # #检查噪声文件
        # if "error"==self.filenames.pop(self.noisefilename,"error"):
        #     print("噪声文件不在数据目录下，请检查噪声文件名！")
        #     return

        #读取噪声文件
        datarow = open(self.noisefilepath)
        datarowlines = datarow.readlines()  # 读取的整个原始文件的数据，按行分割
        datapar = []  # 真正的每行数据数组
        for line in datarowlines:
            linenew = line.strip()
            if (linenew != ""):
                datapar.append(linenew)

        self.noisedata.Project = datapar[2].strip(datapar[2].split(": ")[0]).strip(": ")
        self.noisedata.Name = datapar[3].strip(datapar[3].split(": ")[0]).strip(": ")
        self.noisedata.part = datapar[4].strip(datapar[4].split(": ")[0]).strip(": ")
        self.noisedata.Operator = datapar[5].strip(datapar[5].split(": ")[0]).strip(": ")
        self.noisedata.Desc = datapar[6].strip(datapar[6].split(": ")[0]).strip(": ")
        self.noisedata.Excited_Peroid = int(datapar[9].strip(datapar[9].split(": ")[0]).strip(": "))
        self.noisedata.Excited_Time = int(datapar[10].strip(datapar[10].split(": ")[0]).strip(": "))
        self.noisedata.Acq_Delay_Time = int(datapar[11].strip(datapar[11].split(": ")[0]).strip(": "))
        self.noisedata.Gate_Time = int(datapar[12].strip(datapar[12].split(": ")[0]).strip(": "))
        self.noisedata.Count_Num_per_gate = int(datapar[13].strip(datapar[13].split(": ")[0]).strip(": "))
        self.noisedata.Repeat_Times = int(datapar[14].strip(datapar[14].split(": ")[0]).strip(": "))
        self.noisedata.Acq_Gate_Times = int(datapar[15].strip(datapar[15].split(": ")[0]).strip(": "))
        self.noisedata.Interval_per_Gate = int(datapar[16].strip(datapar[16].split(": ")[0]).strip(": "))
        self.noisedata.datanum = int(self.noisedata.Repeat_Times * self.noisedata.Count_Num_per_gate)  # 每门数据量（包含重复测量数据）
        # 保存原始数据
        if (datapar[17].strip(datapar[17].split(":")[0]).strip(":") == ""):
            # print("进入")
            self.noisedata.Channel_Number = "1"
            for i in range(18, 18 + self.noisedata.datanum * self.noisedata.Acq_Gate_Times):
                self.noisedata.Raw_Data1.append(float(datapar[i]))
            # if (data.Channel_Number == 2):
            #     for i in range(18 + datanum + 1,
            #                    18 + datanum * data.Acq_Gate_Times + 1 + datanum * data.Acq_Gate_Times):
            #         data.Raw_Data2.append(int(datapar[i]))
        else:
            self.noisedata.Channel_Number = int(datapar[17].strip(datapar[17].split(": ")[0]).strip(": "))
            for i in range(19, 19 + self.noisedata.datanum * self.noisedata.Acq_Gate_Times):
                self.noisedata.Raw_Data1.append(float(datapar[i]))
                
                
        #读取数据文件
        p=1    
        for f in self.filenames:
            tmpdata=dataclass()
            datarow = open(self.folderpath + '/' + f)  # 读取的整个原始文件数据
            datarowlines = datarow.readlines()  # 读取的整个原始文件的数据，按行分割
            datapar = []  # 真正的每行数据数组
            for line in datarowlines:
                linenew = line.strip()
                if (linenew != ""):
                    datapar.append(linenew)
            tmpdata.filename=os.path.splitext(f)[0]
            tmpdata.Project = datapar[2].strip(datapar[2].split(": ")[0]).strip(": ")
            tmpdata.Name = datapar[3].strip(datapar[3].split(": ")[0]).strip(": ")
            tmpdata.part = datapar[4].strip(datapar[4].split(": ")[0]).strip(": ")
            tmpdata.Operator = datapar[5].strip(datapar[5].split(": ")[0]).strip(": ")
            tmpdata.Desc = datapar[6].strip(datapar[6].split(": ")[0]).strip(": ")
            tmpdata.Excited_Peroid = int(datapar[9].strip(datapar[9].split(": ")[0]).strip(": "))
            tmpdata.Excited_Time = int(datapar[10].strip(datapar[10].split(": ")[0]).strip(": "))
            tmpdata.Acq_Delay_Time = int(datapar[11].strip(datapar[11].split(": ")[0]).strip(": "))
            tmpdata.Gate_Time = int(datapar[12].strip(datapar[12].split(": ")[0]).strip(": "))
            tmpdata.Count_Num_per_gate = int(datapar[13].strip(datapar[13].split(": ")[0]).strip(": "))
            tmpdata.Repeat_Times = int(datapar[14].strip(datapar[14].split(": ")[0]).strip(": "))
            tmpdata.Acq_Gate_Times = int(datapar[15].strip(datapar[15].split(": ")[0]).strip(": "))
            tmpdata.Interval_per_Gate = int(datapar[16].strip(datapar[16].split(": ")[0]).strip(": "))
            tmpdata.datanum = int(tmpdata.Repeat_Times * tmpdata.Count_Num_per_gate)  # 每门数据量（包含重复测量数据）
            tmpdata.Pro_Data1 = np.zeros(tmpdata.Acq_Gate_Times * tmpdata.Count_Num_per_gate).tolist()  # 不重复情况下所有数据数量（门数*每门测量次数）
            tmpdata.Pro_mal1 = np.zeros(tmpdata.Acq_Gate_Times * tmpdata.Count_Num_per_gate).tolist()  # 不重复情况下所有数据数量（门数*每门测量次数）
            # 保存原始数据
            if (datapar[17].strip(datapar[17].split(":")[0]).strip(":") == ""):
                # print("进入")
                tmpdata.Channel_Number = "1"
                for i in range(18, 18 + tmpdata.datanum * tmpdata.Acq_Gate_Times):
                    tmpdata.Raw_Data1.append(float(datapar[i]))
                # if (data.Channel_Number == 2):
                #     for i in range(18 + datanum + 1,
                #                    18 + datanum * data.Acq_Gate_Times + 1 + datanum * data.Acq_Gate_Times):
                #         data.Raw_Data2.append(int(datapar[i]))
            else:
                tmpdata.Channel_Number = int(datapar[17].strip(datapar[17].split(": ")[0]).strip(": "))
                for i in range(19, 19 + tmpdata.datanum * tmpdata.Acq_Gate_Times):
                    tmpdata.Raw_Data1.append(float(datapar[i]))
            if(tmpdata.Excited_Peroid ==self.noisedata.Excited_Peroid
                    and tmpdata.Excited_Time ==self.noisedata.Excited_Time
                    and tmpdata.Acq_Delay_Time ==self.noisedata.Acq_Delay_Time
                    and tmpdata.Gate_Time ==self.noisedata.Gate_Time
                    and tmpdata.Count_Num_per_gate ==self.noisedata.Count_Num_per_gate
                    and tmpdata.Repeat_Times ==self.noisedata.Repeat_Times
                    and tmpdata.Acq_Gate_Times==self.noisedata.Acq_Gate_Times
                    and tmpdata.Interval_per_Gate==self.noisedata.Interval_per_Gate
                    and tmpdata.Channel_Number==self.noisedata.Channel_Number):
                self.datalist.append(tmpdata)
            else:
                self.errfilelist.append(tmpdata)


        print("目录下和噪声文件相同结构的数据文件有"+str(len(self.datalist))+"个")

        if not os.path.exists(self.outfolderpath):
            os.makedirs(self.outfolderpath)

        #写入新文件
        p=1
        for i in range(len(self.datalist)):
            with open(self.outfolderpath + self.datalist[i].filename + "_RemoveNoise.txt", "w") as file:  # ”w"代表着每次运行都覆盖内容
                file.write("Project Info:" + "\n\n")
                file.write("    ACQ Time: " + datetime.now().strftime('%Y-%m-%d  %H:%M:%S.%f .') + "\n\n")
                file.write("    Project: " + str(self.datalist[i].Project) + "\n\n")
                file.write("    Name: " + str(self.datalist[i].Name) + "\n\n")
                file.write("    Part: " + str(self.datalist[i].part) + "\n\n")
                file.write("    Operator:  " + str(self.datalist[i].Operator) + "\n\n")
                file.write("    Desc.:  " + str(self.datalist[i].Desc) + "\n\n")
                file.write("    Sample Data Acquired." + "\n\n\n\n")
                file.write("ACQ Parameters:" + "\n\n")
                file.write("    Excited Peroid(ms): " + str(self.datalist[i].Excited_Peroid) + "\n\n")
                file.write("    Excited Time(ms): " + str(self.datalist[i].Excited_Time) + "\n\n")
                file.write("    Acq Delay Time(us): " + str(self.datalist[i].Acq_Delay_Time) + "\n\n")
                file.write("    Gate Time(ms): " + str(self.datalist[i].Gate_Time) + "\n\n")
                file.write("    Count Num per gate: " + str(self.datalist[i].Count_Num_per_gate) + "\n\n")
                file.write("    Repeat Times: " + str(self.datalist[i].Repeat_Times) + "\n\n")
                file.write("    Acq Gate Times: " + str(self.datalist[i].Acq_Gate_Times) + "\n\n")
                file.write("    Interval per Gate(us): " + str(self.datalist[i].Interval_per_Gate) + "\n\n")
                file.write("    Channel Number: " + str(self.datalist[i].Channel_Number) + "\n\n\n\n")
                file.write("Data:\n\n")
                for j in range(len(self.datalist[i].Raw_Data1)):
                    file.write("    " + str(float(self.datalist[i].Raw_Data1[j])-float(self.noisedata.Raw_Data1[j])) + "\n\n")
            print(self.datalist[i].filename+" 已完成("+str(i+1)+"/"+str(len(self.datalist))+")")




        if len(self.errfilelist)!=0:
            print("以下文件和噪声文件结构不同：" + str(len(self.errfilelist)) + "个,")
            for errfile in self.errfilelist:
                print(errfile.filename)


class mainMean():
    def __init__(self, folderpath: str, noisefilepath: str):
        self.folderpath = folderpath
        self.outfolderpath = folderpath + "/REMOVE_NOISE/"
        self.noisefilepath = noisefilepath
        self.filenames = []
        self.noisedata = dataclass()
        self.datalist = []
        self.errfilelist = []

    def process(self):
        files = os.listdir(self.folderpath)
        for f in files:
            if (os.path.isdir(self.folderpath + '/' + f)):
                # 排除隐藏文件夹。因为隐藏文件夹过多
                if (f[0] == '.'):
                    pass
                else:
                    pass
            if (os.path.isfile(self.folderpath + '/' + f)):
                # 添加文件
                if (os.path.splitext(f)[1] == ".txt"):
                    self.filenames.append(f)
        # #检查噪声文件
        # if "error"==self.filenames.pop(self.noisefilename,"error"):
        #     print("噪声文件不在数据目录下，请检查噪声文件名！")
        #     return

        # 读取噪声文件
        datarow = open(self.noisefilepath)
        datarowlines = datarow.readlines()  # 读取的整个原始文件的数据，按行分割
        datapar = []  # 真正的每行数据数组
        for line in datarowlines:
            linenew = line.strip()
            if (linenew != ""):
                datapar.append(linenew)

        self.noisedata.Project = datapar[2].strip(datapar[2].split(": ")[0]).strip(": ")
        self.noisedata.Name = datapar[3].strip(datapar[3].split(": ")[0]).strip(": ")
        self.noisedata.part = datapar[4].strip(datapar[4].split(": ")[0]).strip(": ")
        self.noisedata.Operator = datapar[5].strip(datapar[5].split(": ")[0]).strip(": ")
        self.noisedata.Desc = datapar[6].strip(datapar[6].split(": ")[0]).strip(": ")
        self.noisedata.Excited_Peroid = int(datapar[9].strip(datapar[9].split(": ")[0]).strip(": "))
        self.noisedata.Excited_Time = int(datapar[10].strip(datapar[10].split(": ")[0]).strip(": "))
        self.noisedata.Acq_Delay_Time = int(datapar[11].strip(datapar[11].split(": ")[0]).strip(": "))
        self.noisedata.Gate_Time = int(datapar[12].strip(datapar[12].split(": ")[0]).strip(": "))
        self.noisedata.Count_Num_per_gate = int(datapar[13].strip(datapar[13].split(": ")[0]).strip(": "))
        self.noisedata.Repeat_Times = int(datapar[14].strip(datapar[14].split(": ")[0]).strip(": "))
        self.noisedata.Acq_Gate_Times = int(datapar[15].strip(datapar[15].split(": ")[0]).strip(": "))
        self.noisedata.Interval_per_Gate = int(datapar[16].strip(datapar[16].split(": ")[0]).strip(": "))
        self.noisedata.datanum = int(self.noisedata.Repeat_Times * self.noisedata.Count_Num_per_gate)  # 每门数据量（包含重复测量数据）

        # 保存原始数据
        if (datapar[17].strip(datapar[17].split(":")[0]).strip(":") == ""):
            # print("进入")
            self.noisedata.Channel_Number = "1"
            for i in range(18, 18 + self.noisedata.datanum * self.noisedata.Acq_Gate_Times):
                self.noisedata.Raw_Data1.append(float(datapar[i]))
            # if (data.Channel_Number == 2):
            #     for i in range(18 + datanum + 1,
            #                    18 + datanum * data.Acq_Gate_Times + 1 + datanum * data.Acq_Gate_Times):
            #         data.Raw_Data2.append(int(datapar[i]))
        else:
            self.noisedata.Channel_Number = int(datapar[17].strip(datapar[17].split(": ")[0]).strip(": "))
            for i in range(19, 19 + self.noisedata.datanum * self.noisedata.Acq_Gate_Times):
                self.noisedata.Raw_Data1.append(float(datapar[i]))

        #保留原始数据顺序的噪声数据
        noiseRawOrderData=[]
        # noiseRawOrderData=[-1 for i in range(self.noisedata.Acq_Gate_Times*self.noisedata.Count_Num_per_gate)]
        for i in range(self.noisedata.Acq_Gate_Times):
            for j in range(self.noisedata.Count_Num_per_gate):
                RepeatDataList=[]
                for k in range(self.noisedata.Repeat_Times):
                    # print(i*(self.noisedata.Count_Num_per_gate*self.noisedata.Repeat_Times)+j+k*self.noisedata.Count_Num_per_gate)
                    RepeatDataList.append(self.noisedata.Raw_Data1[i*(self.noisedata.Count_Num_per_gate*self.noisedata.Repeat_Times)+j+k*self.noisedata.Count_Num_per_gate])
                noiseRawOrderData.append(np.mean(RepeatDataList))

        # 读取数据文件
        p = 1
        for f in self.filenames:
            tmpdata = dataclass()
            datarow = open(self.folderpath + '/' + f)  # 读取的整个原始文件数据
            datarowlines = datarow.readlines()  # 读取的整个原始文件的数据，按行分割
            datapar = []  # 真正的每行数据数组
            for line in datarowlines:
                linenew = line.strip()
                if (linenew != ""):
                    datapar.append(linenew)
            tmpdata.filename = os.path.splitext(f)[0]
            tmpdata.Project = datapar[2].strip(datapar[2].split(": ")[0]).strip(": ")
            tmpdata.Name = datapar[3].strip(datapar[3].split(": ")[0]).strip(": ")
            tmpdata.part = datapar[4].strip(datapar[4].split(": ")[0]).strip(": ")
            tmpdata.Operator = datapar[5].strip(datapar[5].split(": ")[0]).strip(": ")
            tmpdata.Desc = datapar[6].strip(datapar[6].split(": ")[0]).strip(": ")
            tmpdata.Excited_Peroid = int(datapar[9].strip(datapar[9].split(": ")[0]).strip(": "))
            tmpdata.Excited_Time = int(datapar[10].strip(datapar[10].split(": ")[0]).strip(": "))
            tmpdata.Acq_Delay_Time = int(datapar[11].strip(datapar[11].split(": ")[0]).strip(": "))
            tmpdata.Gate_Time = int(datapar[12].strip(datapar[12].split(": ")[0]).strip(": "))
            tmpdata.Count_Num_per_gate = int(datapar[13].strip(datapar[13].split(": ")[0]).strip(": "))
            tmpdata.Repeat_Times = int(datapar[14].strip(datapar[14].split(": ")[0]).strip(": "))
            tmpdata.Acq_Gate_Times = int(datapar[15].strip(datapar[15].split(": ")[0]).strip(": "))
            tmpdata.Interval_per_Gate = int(datapar[16].strip(datapar[16].split(": ")[0]).strip(": "))
            tmpdata.datanum = int(tmpdata.Repeat_Times * tmpdata.Count_Num_per_gate)  # 每门数据量（包含重复测量数据）
            tmpdata.Pro_Data1 = np.zeros(
                tmpdata.Acq_Gate_Times * tmpdata.Count_Num_per_gate).tolist()  # 不重复情况下所有数据数量（门数*每门测量次数）
            tmpdata.Pro_mal1 = np.zeros(
                tmpdata.Acq_Gate_Times * tmpdata.Count_Num_per_gate).tolist()  # 不重复情况下所有数据数量（门数*每门测量次数）
            # 保存原始数据
            if (datapar[17].strip(datapar[17].split(":")[0]).strip(":") == ""):
                # print("进入")
                tmpdata.Channel_Number = "1"
                for i in range(18, 18 + tmpdata.datanum * tmpdata.Acq_Gate_Times):
                    tmpdata.Raw_Data1.append(float(datapar[i]))
                # if (data.Channel_Number == 2):
                #     for i in range(18 + datanum + 1,
                #                    18 + datanum * data.Acq_Gate_Times + 1 + datanum * data.Acq_Gate_Times):
                #         data.Raw_Data2.append(int(datapar[i]))
            else:
                tmpdata.Channel_Number = int(datapar[17].strip(datapar[17].split(": ")[0]).strip(": "))
                for i in range(19, 19 + tmpdata.datanum * tmpdata.Acq_Gate_Times):
                    tmpdata.Raw_Data1.append(float(datapar[i]))
            if (tmpdata.Excited_Peroid == self.noisedata.Excited_Peroid
                    and tmpdata.Excited_Time == self.noisedata.Excited_Time
                    and tmpdata.Acq_Delay_Time == self.noisedata.Acq_Delay_Time
                    and tmpdata.Gate_Time == self.noisedata.Gate_Time
                    and tmpdata.Count_Num_per_gate == self.noisedata.Count_Num_per_gate
                    and tmpdata.Acq_Gate_Times == self.noisedata.Acq_Gate_Times
                    and tmpdata.Interval_per_Gate == self.noisedata.Interval_per_Gate
                    and tmpdata.Channel_Number == self.noisedata.Channel_Number):
                self.datalist.append(tmpdata)
            else:
                self.errfilelist.append(tmpdata)

        print("目录下和噪声文件相同结构的数据文件有" + str(len(self.datalist)) + "个")

        if not os.path.exists(self.outfolderpath):
            os.makedirs(self.outfolderpath)

        # 写入新文件
        p = 1
        for i in range(len(self.datalist)):
            with open(self.outfolderpath + self.datalist[i].filename + "_RemoveNoise.txt",
                      "w") as file:  # ”w"代表着每次运行都覆盖内容
                file.write("Project Info:" + "\n\n")
                file.write("    ACQ Time: " + datetime.now().strftime('%Y-%m-%d  %H:%M:%S.%f .') + "\n\n")
                file.write("    Project: " + str(self.datalist[i].Project) + "\n\n")
                file.write("    Name: " + str(self.datalist[i].Name) + "\n\n")
                file.write("    Part: " + str(self.datalist[i].part) + "\n\n")
                file.write("    Operator:  " + str(self.datalist[i].Operator) + "\n\n")
                file.write("    Desc.:  " + str(self.datalist[i].Desc) + "\n\n")
                file.write("    Sample Data Acquired." + "\n\n\n\n")
                file.write("ACQ Parameters:" + "\n\n")
                file.write("    Excited Peroid(ms): " + str(self.datalist[i].Excited_Peroid) + "\n\n")
                file.write("    Excited Time(ms): " + str(self.datalist[i].Excited_Time) + "\n\n")
                file.write("    Acq Delay Time(us): " + str(self.datalist[i].Acq_Delay_Time) + "\n\n")
                file.write("    Gate Time(ms): " + str(self.datalist[i].Gate_Time) + "\n\n")
                file.write("    Count Num per gate: " + str(self.datalist[i].Count_Num_per_gate) + "\n\n")
                file.write("    Repeat Times: " + str(self.datalist[i].Repeat_Times) + "\n\n")
                file.write("    Acq Gate Times: " + str(self.datalist[i].Acq_Gate_Times) + "\n\n")
                file.write("    Interval per Gate(us): " + str(self.datalist[i].Interval_per_Gate) + "\n\n")
                file.write("    Channel Number: " + str(self.datalist[i].Channel_Number) + "\n\n\n\n")
                file.write("Data:\n\n")

                for ii in range(self.datalist[i].Acq_Gate_Times):
                    for j in range(self.datalist[i].Count_Num_per_gate):
                        for k in range(self.datalist[i].Repeat_Times):
                            # print(ii * self.noisedata.Count_Num_per_gate * self.noisedata.Repeat_Times + j + k * self.noisedata.Count_Num_per_gate,self.noisedata.Count_Num_per_gate*ii+j)
                            self.datalist[i].Raw_Data1[ii * self.datalist[i].Count_Num_per_gate * self.datalist[i].Repeat_Times + j + k * self.datalist[i].Count_Num_per_gate] -=noiseRawOrderData[self.noisedata.Count_Num_per_gate*ii+j]
                for j in range(len(self.datalist[i].Raw_Data1)):
                    file.write("    " + str(float(self.datalist[i].Raw_Data1[j])) + "\n\n")
            print(self.datalist[i].filename + " 已完成(" + str(i + 1) + "/" + str(len(self.datalist)) + ")")

        if len(self.errfilelist) != 0:
            print("以下文件和噪声文件结构不同：" + str(len(self.errfilelist)) + "个,")
            for errfile in self.errfilelist:
                print(errfile.filename)

if __name__ == '__main__':
    while(True) :
        print("请输入数据目录路径\n")
        datafolderpath = input()
        print("请输入噪声文件路径\n")
        noisefilepathpath = input()
        #
        # datafolderpath="D:/工作文件2/光子数据/不同浓度/0"
        # noisefilepathpath="D:/工作文件2/光子数据/不同浓度/PBS/QCC201911 51618 5-1105-yeast-PBS'-M7-D.txt"
        a = mainMean(datafolderpath,noisefilepathpath)
        a.process()
        print("完成，任意键继续进行数据处理，结束请关闭")
        input()
