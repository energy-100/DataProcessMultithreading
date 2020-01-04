
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from dataread import *
import pickle
class readthread(QThread):
    sinOutpro = pyqtSignal(float)
    sinOuttext = pyqtSignal(str)
    sinOutbool = pyqtSignal(bool)
    # sinOutinlinebool = pyqtSignal(bool)
    # sinOutoutlinebool = pyqtSignal(bool)
    # sinOutinlinetext = pyqtSignal(str)
    # sinOutoutlinetext = pyqtSignal(str)
    sinOutoutEndThread = pyqtSignal(datastruct)
    # sinOutoutpath = pyqtSignal(str)
    # sinOutoutData = pyqtSignal(dataclass)
    def __init__(self,path):
        self.data=""
        self.path=path
        super(readthread,self).__init__()
    def run(self):
        Process= dataProcess(self.sinOutpro, self.sinOuttext, self.sinOutbool)
        print("地址：",self.path,"建立完！")
        print("文件：",Process.data.filelist)
        self.data = Process.readfiles(self.path)
        print("处理完！")
        self.sinOuttext.emit("已读取并转换" + str(len(self.data.filelist)) + "个数据！")
        self.sinOutoutEndThread.emit(self.data)
        print("传送结束！")

class readhistory(QThread):
    sinOuttext = pyqtSignal(str)
    sinOutoutEndThread = pyqtSignal(datastruct)
    def __init__(self,path):
        self.data=""
        self.path = path
        super(readhistory, self).__init__()
    def run(self):
        self.sinOuttext.emit("正在读取历史文件...")
        f = open(self.path, 'rb')
        self.data = pickle.load(f)
        f.close()
        self.sinOuttext.emit("历史文件读取成功！")
        self.sinOutoutEndThread.emit(self.data)

class savehistory(QThread):
    sinOuttext = pyqtSignal(str)
    def __init__(self,path,data):
        self.data=data
        self.path = path
        super(savehistory, self).__init__()
    def run(self):
        print("保存数据")
        # print("self.data.cb1setChecked:",self.data.cb1setChecked)
        # print("self.data.cb2setChecked:",self.data.cb2setChecked)
        self.sinOuttext.emit("正在保存当前状态...")
        filename = self.path + "/" + os.path.basename(self.path) + ".data"
        print(self.data.filelist)
        try:
            with open(filename, "wb") as file:
                pickle.dump(self.data, file, True)
            with open(filename, "rb") as file:
                data1 = pickle.load(file)
            print(data1)
        except Exception as a:
            print(a)
        print("保存缓存")
        filename = os.getcwd() + "/cache/temp.ache"
        filepath = os.getcwd() + "/cache/"
        if (not os.path.exists(filepath)):
            os.makedirs(filepath)
        datapath = self.data.inpath + "/" + os.path.basename(self.data.inpath) + ".data"
        with open(filename, "wb") as file:
            pickle.dump(datapath, file, True)
        self.sinOuttext.emit("当前状态保存成功!")

class fitthread(QThread):
    print("fit in")
    sinOutpro = pyqtSignal(float)
    sinOuttext = pyqtSignal(str)
    sinOutbool = pyqtSignal(bool)
    # sinOutpro = pyqtSignal(float)
    # sinOuttext = pyqtSignal(str)
    # sinOutbool = pyqtSignal(bool)
    # sinOutinlinebool = pyqtSignal(bool)
    # sinOutoutlinebool = pyqtSignal(bool)
    # sinOutinlinetext = pyqtSignal(str)
    # sinOutoutlinetext = pyqtSignal(str)
    # sinOutoutfitEndThread = pyqtSignal(datastruct)
    sinOutoutfitEndThread = pyqtSignal()

    # sinOutoutpath = pyqtSignal(str)
    # sinOutoutData = pyqtSignal(dataclass)
    def __init__(self, data,paras):
        self.data = data
        self.paras=paras
        super(fitthread, self).__init__()

    def run(self):
        print("fit run in")
        Process = dataProcess(self.sinOutpro, self.sinOuttext, self.sinOutbool)
        Process.data=self.data
        for para in self.paras:
            Process.Fitting(para[0], para[1], para[2], para[3], para[4], para[5], para[6],
                              para[7], para[8])
        self.sinOutoutfitEndThread.emit()

class savefilethread(QThread):
    sinOutpro = pyqtSignal(float)
    sinOuttext = pyqtSignal(str)
    sinOutbool = pyqtSignal(bool)
    # sinOutoutfitEndThread = pyqtSignal()
    # sinOutoutpath = pyqtSignal(str)
    # sinOutoutData = pyqtSignal(dataclass)
    def __init__(self, data):
        self.data = data
        super(savefilethread, self).__init__()

    def run(self):
        print("fit run in")
        Process = dataProcess(self.sinOutpro, self.sinOuttext, self.sinOutbool)
        # Process.data=self.data
        Process.writeXls(self.data)
        # self.sinOutoutfitEndThread.emit()

class savesondatathread(QThread):
    sinOutpro = pyqtSignal(float)
    sinOuttext = pyqtSignal(str)
    sinOutbool = pyqtSignal(bool)

    # sinOutoutfitEndThread = pyqtSignal()
    # sinOutoutpath = pyqtSignal(str)
    # sinOutoutData = pyqtSignal(dataclass)
    def __init__(self, data):
        self.data = data
        super(savesondatathread, self).__init__()

    def run(self):
        print("fit run in")
        Process = dataProcess(self.sinOutpro, self.sinOuttext, self.sinOutbool)
        # Process.data = self.data
        Process.writesondataXls(self.data)
        # self.sinOutoutfitEndThread.emit()

class savesingledatathread(QThread):
    sinOutpro = pyqtSignal(float)
    sinOuttext = pyqtSignal(str)
    sinOutbool = pyqtSignal(bool)

    # sinOutoutfitEndThread = pyqtSignal()
    # sinOutoutpath = pyqtSignal(str)
    # sinOutoutData = pyqtSignal(dataclass)
    def __init__(self, data):
        self.data = data
        super(savesingledatathread, self).__init__()

    def run(self):
        print("fit run in")
        Process = dataProcess(self.sinOutpro, self.sinOuttext, self.sinOutbool)
        # Process.data = self.data
        Process.writesinglefiledata(self.data)
        # self.sinOutoutfitEndThread.emit()



