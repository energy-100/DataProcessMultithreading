
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

def getfile():
    conn = MongoClient('47.105.38.117', 27017)
    db2 = conn.userfiledata  # 选定数据库，设定数据库名称为file
    fs = GridFS(db2, collection='datas')  # 连接GridFS集合，名称为pdf
    for cursor in fs.find():
        filename = cursor.文件名
        content = cursor.read()
        if(not (os.path.exists('C:/Users/ENERGY/Desktop/用户数据/' +cursor.来源+'/'))):
            os.mkdir('C:/Users/ENERGY/Desktop/用户数据/' +cursor.来源+'/')
            if(os.path.exists(not('C:/Users/ENERGY/Desktop/用户数据/' +cursor.来源+'/'+ filename))):
                with open('C:/Users/ENERGY/Desktop/用户数据/' +cursor.来源+'/'+ filename, 'wb') as f:
                    f.write(content)
def getimage():
    conn = MongoClient('47.105.38.117', 27017)
    db = conn.userimagedata  # 选定数据库，设定数据库名称为file
    fs = GridFS(db, collection='images')  # 连接GridFS集合，名称为pdf
    for cursor in fs.find():
        filename = cursor.文件名

        content = cursor.read()
        if(not (os.path.exists('F:/用户图片/' +cursor.来源+'/'))):
            os.mkdir('F:/用户图片/' +cursor.来源+'/')
        if(os.path.exists(not('F:/用户图片/' +cursor.来源+'/'+ filename))):
            with open('F:/用户图片/' +cursor.来源+'/'+ filename, 'wb') as f:
                print('filename',filename)
                f.write(content)

    covdat2image('F:/用户图片/' +cursor.来源+'/')

def covdat2image(path):
    files=os.listdir(path)
    file=[]
    for f in files:
        if (os.path.isfile(path + '/' + f)):
            # 添加文件
            file.append(f)

    if (not os.path.exists(path + '/jpgfile/')):
        os.mkdir(path + '/jpgfile/')
    for i in range(len(file)):
        dat_read = open(path+'/'+file[i], "rb")
        path+file[i]
        out = path + '/jpgfile/'+str(i) + '.jpg'
        png_write = open(out, "wb")
        for now in dat_read:
            for nowByte in now:
                # print('nowByte',nowByte)
                # print(type(key))
                # print(key)
                newByte = nowByte ^ 0x05
                # newByte = nowByte ^ int(str(key),2)
                png_write.write(bytes([newByte]))
        png_write.close()

# getimage()
covdat2image('F:\用户图片\ENERGY-DESKTOP-B8B3U7T')